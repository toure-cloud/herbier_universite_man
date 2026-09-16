# api/audit.py
from .models import AuditLog


def get_client_ip(request):
    xff = request.META.get('HTTP_X_FORWARDED_FOR')
    if xff:
        return xff.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


def log_action(request, action, model_name=None, obj=None, details=None):
    """
    Enregistre une action dans l'historique d'audit.
    - action : 'CREATE', 'UPDATE', 'DELETE', 'LOGIN', 'LOGOUT', 'SYNC'...
    - model_name : nom du modèle (ex: 'Plante')
    - obj : instance Django (pour object_id et object_repr)
    - details : dict de détails supplémentaires
    """
    user = getattr(request, 'user', None)
    if not user or not getattr(user, 'is_authenticated', False):
        user = None

    object_id = str(obj.pk) if obj and hasattr(obj, 'pk') else None
    object_repr = str(obj)[:255] if obj else None

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