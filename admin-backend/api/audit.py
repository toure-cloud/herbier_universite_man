# api/audit.py
from django.utils import timezone
from datetime import timedelta

from .models import AuditLog, LoginAttempt, UserKnownIP


# ============================================================
# HELPERS
# ============================================================

def get_client_ip(request):
    """Récupère l'IP du client (gère les proxies)."""
    xff = request.META.get('HTTP_X_FORWARDED_FOR')
    if xff:
        return xff.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


# ============================================================
# AUDIT — Log des actions
# ============================================================

def log_action(request, action, model_name=None, obj=None, details=None):
    """
    Enregistre une action dans l'historique d'audit.
    - action : 'CREATE', 'UPDATE', 'DELETE', 'LOGIN', 'LOGOUT', 'LOGIN_FAILED', 'SYNC', 'EXPORT'
    - model_name : nom du modèle (ex: 'Plante')
    - obj : instance Django (pour object_id et object_repr)
    - details : dict de détails supplémentaires
    """
    user = getattr(request, 'user', None)
    if not user or not getattr(user, 'is_authenticated', False):
        user = None

    object_id = str(obj.pk) if obj and hasattr(obj, 'pk') else None
    object_repr = str(obj)[:255] if obj else None

    try:
        AuditLog.objects.create(
            user=user,
            action=action,
            model_name=model_name,
            object_id=object_id,
            object_repr=object_repr,
            details=details or {},
            ip_address=get_client_ip(request),
            user_agent=(request.META.get('HTTP_USER_AGENT') or '')[:500],
        )
    except Exception as e:
        # Ne jamais bloquer une action pour un problème de log
        print(f"⚠️ Erreur log_action: {e}")


# ============================================================
# ✅ RATE LIMITING — Suivi des tentatives de connexion
# ============================================================

def record_login_attempt(request, email, success, reason=''):
    """Enregistre une tentative de connexion."""
    try:
        LoginAttempt.objects.create(
            email=(email or '').lower(),
            ip_address=get_client_ip(request) or '0.0.0.0',
            user_agent=(request.META.get('HTTP_USER_AGENT') or '')[:500],
            success=success,
            reason=reason,
        )
    except Exception as e:
        # Ne jamais bloquer une action pour un problème de log
        print(f"⚠️ Erreur record_login_attempt: {e}")


def check_login_rate_limit(request, email):
    """
    Vérifie si l'utilisateur a dépassé le quota de tentatives.
    Retourne (blocked: bool, reason: str | None).
    """
    ip = get_client_ip(request)
    now = timezone.now()

    # ✅ 5 tentatives échouées par email en 15 min → blocage 15 min
    recent_email_fails = LoginAttempt.objects.filter(
        email=(email or '').lower(),
        success=False,
        created_at__gte=now - timedelta(minutes=15),
    ).count()

    if recent_email_fails >= 5:
        return True, (
            f"Trop de tentatives pour cet email ({recent_email_fails}/5). "
            f"Réessayez dans 15 minutes."
        )

    # ✅ 10 tentatives échouées par IP en 15 min → blocage 15 min
    recent_ip_fails = LoginAttempt.objects.filter(
        ip_address=ip,
        success=False,
        created_at__gte=now - timedelta(minutes=15),
    ).count()

    if recent_ip_fails >= 10:
        return True, (
            f"Trop de tentatives depuis votre IP ({recent_ip_fails}/10). "
            f"Réessayez dans 15 minutes."
        )

    return False, None


# ============================================================
# ✅ DÉTECTION D'ANOMALIES
# ============================================================

def detect_login_anomalies(request, user):
    """
    Détecte les anomalies à la connexion :
    - Nouvelle IP inconnue
    - Heure inhabituelle (2h-5h du matin)

    Retourne un dict avec les anomalies détectées (vide si rien).
    """
    from .models import Notification

    ip = get_client_ip(request)
    now = timezone.now()
    hour = now.hour
    anomaly = {}

    # 1. Nouvelle IP ?
    known_ip = UserKnownIP.objects.filter(user=user, ip_address=ip).first()

    if not known_ip:
        anomaly['new_ip'] = True
        anomaly['ip'] = ip

        UserKnownIP.objects.create(user=user, ip_address=ip)

        Notification.objects.create(
            user=user,
            type='SECURITY',
            title='Nouvelle connexion détectée',
            message=f'Connexion depuis une nouvelle adresse IP : {ip}',
            details={'ip': ip, 'hour': hour},
        )
    else:
        known_ip.login_count += 1
        known_ip.save(update_fields=['login_count', 'last_seen'])

    # 2. Heure inhabituelle ? (2h - 5h du matin)
    if 2 <= hour <= 5:
        anomaly['unusual_hour'] = True
        anomaly['hour'] = hour

        Notification.objects.create(
            user=user,
            type='SECURITY',
            title='Connexion à une heure inhabituelle',
            message=f'Connexion à {hour}h du matin.',
            details={'hour': hour, 'ip': ip},
        )

    return anomaly
