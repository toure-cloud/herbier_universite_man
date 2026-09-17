# api/views.py
import random
import string
import hashlib
import time
from datetime import timedelta
import pyotp
import qrcode
import base64
import secrets
from io import BytesIO
from django.conf import settings
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from .authentication import BearerTokenAuthentication, verify_token
from .audit import log_action, record_login_attempt, check_login_rate_limit
from .models import (
    SuperAdmin, OTPCode, UserToken, AuditLog,
    LoginAttempt, UserKnownIP, Notification,
    Plante, Equipe, Slide, Projet, Activite,
    Partenaire, Temoignage, Publication, FAQ,
    Statistique, Methodologie,
)
from .serializers import (
    SuperAdminSerializer, SuperAdminCreateSerializer, AuditLogSerializer,
    PlanteSerializer, EquipeSerializer, SlideSerializer,
    ProjetSerializer, ActiviteSerializer, TemoignageSerializer,
    PublicationSerializer, FAQSerializer, StatistiqueSerializer,
    MethodologieSerializer, PartenaireSerializer,
)
from .permissions import IsSuperIT, IsAdminOrSuperIT
from .audit import (
    log_action,
    record_login_attempt,
    check_login_rate_limit,
    get_client_ip,
    detect_login_anomalies,
)


# ============================================================
# HELPERS
# ============================================================

def generate_token(user):
    UserToken.objects.filter(user=user, is_active=True).update(is_active=False)
    raw = f"{user.email}:{int(time.time())}:{random.randint(1000, 9999)}"
    token = hashlib.sha256(raw.encode()).hexdigest()
    UserToken.objects.create(
        user=user,
        token=token,
        expires_at=timezone.now() + timedelta(days=7),
    )
    return token


def generate_otp():
    return ''.join(random.choices(string.digits, k=6))


def _do_login(request, expected_role, endpoint_label):
    email = (request.data.get('email') or '').strip().lower()
    password = request.data.get('password') or ''

    if not email or not password:
        return Response(
            {'success': False, 'error': 'Email et mot de passe requis'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # ---------- RATE LIMITING ----------
    blocked, reason = check_login_rate_limit(request, email)
    if blocked:
        record_login_attempt(request, email, False, 'rate_limited')
        log_action(request, 'LOGIN_FAILED', details={
            'email': email,
            'endpoint': endpoint_label,
            'reason': 'rate_limited',
        })
        return Response(
            {'success': False, 'error': reason},
            status=status.HTTP_429_TOO_MANY_REQUESTS,
        )

    # ---------- RECHERCHE UTILISATEUR ----------
    try:
        user = SuperAdmin.objects.get(email=email)
    except SuperAdmin.DoesNotExist:
        record_login_attempt(request, email, False, 'not_found')
        log_action(request, 'LOGIN_FAILED', details={
            'email': email,
            'endpoint': endpoint_label,
            'reason': 'not_found',
        })
        return Response(
            {'success': False, 'error': 'Identifiants incorrects'},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    # ---------- VÉRIFICATION DU RÔLE ----------
    if user.role != expected_role:
        record_login_attempt(request, email, False, 'wrong_role')
        log_action(request, 'LOGIN_FAILED', model_name='SuperAdmin', obj=user, details={
            'email': email,
            'endpoint': endpoint_label,
            'reason': 'wrong_role',
            'expected': expected_role,
            'actual': user.role,
        })
        return Response(
            {'success': False, 'error': 'Identifiants incorrects'},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    # ---------- VÉRIFICATION DU MOT DE PASSE ----------
    if not user.check_password(password):
        record_login_attempt(request, email, False, 'bad_password')
        log_action(request, 'LOGIN_FAILED', model_name='SuperAdmin', obj=user, details={
            'email': email,
            'endpoint': endpoint_label,
            'reason': 'bad_password',
        })
        return Response(
            {'success': False, 'error': 'Identifiants incorrects'},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    # ---------- VÉRIFICATION DU COMPTE ACTIF ----------
    if not user.is_active:
        record_login_attempt(request, email, False, 'inactive')
        log_action(request, 'LOGIN_FAILED', model_name='SuperAdmin', obj=user, details={
            'email': email,
            'endpoint': endpoint_label,
            'reason': 'inactive',
        })
        return Response(
            {'success': False, 'error': 'Compte désactivé. Contactez le SuperIT.'},
            status=status.HTTP_403_FORBIDDEN,
        )

    # ---------- DÉTECTION D'ANOMALIES ----------
    ip = get_client_ip(request)
    now = timezone.now()
    hour = now.hour
    anomaly = {}

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

    if anomaly:
        log_action(request, 'LOGIN', model_name='SuperAdmin', obj=user, details={
            'role': user.role,
            'endpoint': endpoint_label,
            'anomaly': anomaly,
        })

    # ---------- TENTATIVE RÉUSSIE ----------
    record_login_attempt(request, email, True, 'success')

    # ---------- GÉNÉRATION OTP ----------
    code = generate_otp()
    OTPCode.objects.filter(user=user, is_used=False).delete()
    OTPCode.objects.create(
        user=user,
        code=code,
        type='email',
        expires_at=timezone.now() + timedelta(minutes=10),
    )

    print(f"\n🔐 CODE OTP [{endpoint_label}] pour {email} : {code}\n")

    return Response({
        'success': True,
        'message': 'Code envoyé',
        'email': user.email,
        'requires_2fa': True,
        'test_code': code if settings.DEBUG else None,
    })


# ============================================================
# AUTHENTIFICATION
# ============================================================

@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
@csrf_exempt
def it_login(request):
    """Login SuperIT (rôle = it_admin)."""
    return _do_login(request, expected_role='it_admin', endpoint_label='SuperIT')


@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
@csrf_exempt
def admin_login(request):
    """Login Admin lambda (rôle = admin)."""
    return _do_login(request, expected_role='admin', endpoint_label='Admin')


@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
@csrf_exempt
def verify_2fa(request):
    """
    Vérifie le code :
    - Si TOTP est activé → vérifie via pyotp
    - Sinon → vérifie l'OTP par email
    """
    email = (request.data.get('email') or '').strip().lower()
    code = (request.data.get('code') or '').strip()

    if not email or not code:
        return Response(
            {'success': False, 'error': 'Email et code requis'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        user = SuperAdmin.objects.get(email=email)
    except SuperAdmin.DoesNotExist:
        return Response(
            {'success': False, 'error': 'Utilisateur introuvable'},
            status=status.HTTP_404_NOT_FOUND,
        )

    # ---------- CAS 1 : TOTP ----------
    if user.totp_enabled and user.totp_secret:
        totp = pyotp.TOTP(user.totp_secret)
        code_upper = code.upper()

        if totp.verify(code, valid_window=1):
            user.totp_last_used = timezone.now()
            user.save(update_fields=['totp_last_used'])
            return _issue_token(request, user, method='totp')

        if code_upper in user.totp_backup_codes:
            user.totp_backup_codes.remove(code_upper)
            user.save(update_fields=['totp_backup_codes'])
            log_action(request, 'LOGIN', model_name='SuperAdmin', obj=user, details={
                'method': 'backup_code',
            })
            return _issue_token(request, user, method='backup_code')

        log_action(request, 'LOGIN_FAILED', model_name='SuperAdmin', obj=user, details={
            'reason': 'bad_totp',
        })
        return Response(
            {'success': False, 'error': 'Code TOTP invalide'},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    # ---------- CAS 2 : OTP par email ----------
    otp = OTPCode.objects.filter(user=user, code=code, is_used=False).first()
    if not otp or not otp.is_valid():
        log_action(request, 'LOGIN_FAILED', model_name='SuperAdmin', obj=user, details={
            'reason': 'bad_otp',
        })
        return Response(
            {'success': False, 'error': 'Code invalide ou expiré'},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    otp.is_used = True
    otp.save(update_fields=['is_used'])

    return _issue_token(request, user, method='email_otp')


def _issue_token(request, user, method='unknown'):
    """Génère un token et retourne la réponse."""
    user.is_active = True
    user.last_login = timezone.now()
    user.save(update_fields=['is_active', 'last_login'])

    token = generate_token(user)

    log_action(request, 'LOGIN', model_name='SuperAdmin', obj=user, details={
        'role': user.role,
        'method': method,
    })

    return Response({
        'success': True,
        'access': token,
        'refresh': token,
        'user': SuperAdminSerializer(user).data,
    })


@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
@csrf_exempt
def resend_code(request):
    email = (request.data.get('email') or '').strip().lower()
    try:
        user = SuperAdmin.objects.get(email=email)
    except SuperAdmin.DoesNotExist:
        return Response({'success': False, 'error': 'Utilisateur non trouvé'}, status=404)

    code = generate_otp()
    OTPCode.objects.filter(user=user, is_used=False).delete()
    OTPCode.objects.create(
        user=user, code=code, type='email',
        expires_at=timezone.now() + timedelta(minutes=10),
    )
    print(f"\n🔄 NOUVEAU CODE pour {email} : {code}\n")

    return Response({
        'success': True,
        'message': 'Code renvoyé',
        'test_code': code if settings.DEBUG else None,
    })


@api_view(['POST'])
@authentication_classes([BearerTokenAuthentication])
@permission_classes([IsAuthenticated])
def logout_view(request):
    header = request.headers.get('Authorization')
    if header and header.startswith('Bearer '):
        token = header.split(' ', 1)[1]
        ut = UserToken.objects.filter(token=token, is_active=True).first()
        if ut:
            log_action(request, 'LOGOUT', model_name='SuperAdmin', obj=ut.user)
            ut.is_active = False
            ut.save()
    return Response({'success': True})


@api_view(['GET'])
@authentication_classes([BearerTokenAuthentication])
@permission_classes([IsAuthenticated])
def me_view(request):
    user = request.user
    return Response({
        'user': SuperAdminSerializer(user).data,
        'permissions': {
            'can_manage_users': user.role == 'it_admin',
            'can_view_audit': user.role == 'it_admin',
            'can_crud_content': user.role in ('admin', 'it_admin'),
            'can_sync': user.role == 'it_admin',
            'dashboard_type': 'superit' if user.role == 'it_admin' else 'admin',
        },
    })


@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
@csrf_exempt
def forgot_password(request):
    email = (request.data.get('email') or '').strip().lower()
    if not email:
        return Response({'error': 'Email requis'}, status=400)

    try:
        user = SuperAdmin.objects.get(email=email)
        code = generate_otp()
        OTPCode.objects.filter(user=user, is_used=False).delete()
        OTPCode.objects.create(
            user=user, code=code, type='email',
            expires_at=timezone.now() + timedelta(minutes=15),
        )
        print(f"\n🔑 RÉINITIALISATION MOT DE PASSE - Code: {code}\n")
        return Response({
            'success': True,
            'message': 'Code envoyé',
            'test_code': code if settings.DEBUG else None,
        })
    except SuperAdmin.DoesNotExist:
        return Response({'error': 'Email non trouvé'}, status=404)


@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
@csrf_exempt
def reset_password(request):
    email = (request.data.get('email') or '').strip().lower()
    code = (request.data.get('code') or '').strip()
    new_password = request.data.get('new_password')
    new_password2 = request.data.get('new_password2')

    if not email or not code or not new_password:
        return Response({'error': 'Email, code et mot de passe requis'}, status=400)

    if new_password != new_password2:
        return Response({'error': 'Les mots de passe ne correspondent pas'}, status=400)

    if len(new_password) < 8:
        return Response({'error': 'Le mot de passe doit contenir au moins 8 caractères'}, status=400)

    try:
        user = SuperAdmin.objects.get(email=email)
        otp = OTPCode.objects.filter(user=user, code=code, is_used=False).first()

        if not otp or not otp.is_valid():
            return Response({'error': 'Code invalide ou expiré'}, status=401)

        otp.is_used = True
        otp.save()

        user.set_password(new_password)
        user.save()

        return Response({'success': True, 'message': 'Mot de passe réinitialisé avec succès'})
    except SuperAdmin.DoesNotExist:
        return Response({'error': 'Email non trouvé'}, status=404)


# ============================================================
# GESTION DES UTILISATEURS (SuperIT uniquement)
# ============================================================

@api_view(['GET'])
@authentication_classes([BearerTokenAuthentication])
@permission_classes([IsAuthenticated, IsSuperIT])
def list_users(request):
    users = SuperAdmin.objects.all().order_by('-date_joined')
    return Response(SuperAdminSerializer(users, many=True).data)


@api_view(['POST'])
@authentication_classes([BearerTokenAuthentication])
@permission_classes([IsAuthenticated, IsSuperIT])
def create_user(request):
    serializer = SuperAdminCreateSerializer(data=request.data)
    if serializer.is_valid():
        new_user = serializer.save()
        if not new_user.role or new_user.role not in ('admin', 'it_admin'):
            new_user.role = 'admin'
            new_user.save()

        log_action(request, 'CREATE', model_name='SuperAdmin', obj=new_user, details={
            'role': new_user.role,
        })
        return Response({
            'success': True,
            'user': SuperAdminSerializer(new_user).data,
        }, status=201)
    return Response({'errors': serializer.errors}, status=400)


@api_view(['PATCH'])
@authentication_classes([BearerTokenAuthentication])
@permission_classes([IsAuthenticated, IsSuperIT])
def update_user(request, user_id):
    try:
        target = SuperAdmin.objects.get(id=user_id)
    except SuperAdmin.DoesNotExist:
        return Response({'error': 'Utilisateur non trouvé'}, status=404)

    if target.id == request.user.id:
        return Response({'error': 'Modifiez votre profil via /me/'}, status=400)

    allowed = ['nom', 'telephone', 'role', 'is_active']
    changes = {}
    for key in allowed:
        if key in request.data:
            new_val = request.data[key]
            old_val = getattr(target, key)
            if new_val != old_val:
                setattr(target, key, new_val)
                changes[key] = {'old': str(old_val), 'new': str(new_val)}
    target.save()

    log_action(request, 'UPDATE', model_name='SuperAdmin', obj=target, details={
        'changes': changes,
    })
    return Response({'success': True, 'user': SuperAdminSerializer(target).data})


@api_view(['DELETE'])
@authentication_classes([BearerTokenAuthentication])
@permission_classes([IsAuthenticated, IsSuperIT])
def delete_user(request, user_id):
    if int(user_id) == request.user.id:
        return Response({'error': 'Impossible de se supprimer'}, status=400)

    try:
        target = SuperAdmin.objects.get(id=user_id)
    except SuperAdmin.DoesNotExist:
        return Response({'error': 'Utilisateur non trouvé'}, status=404)

    log_action(request, 'DELETE', model_name='SuperAdmin', obj=target, details={
        'email': target.email,
    })
    target.delete()
    return Response({'success': True})


# ============================================================
# AUDIT (SuperIT uniquement)
# ============================================================

@api_view(['GET'])
@authentication_classes([BearerTokenAuthentication])
@permission_classes([IsAuthenticated, IsSuperIT])
def list_audit_logs(request):
    qs = AuditLog.objects.select_related('user').all()

    action = request.query_params.get('action')
    if action:
        qs = qs.filter(action=action)

    user_id = request.query_params.get('user_id')
    if user_id:
        qs = qs.filter(user_id=user_id)

    date_from = request.query_params.get('date_from')
    if date_from:
        qs = qs.filter(created_at__gte=date_from)

    try:
        limit = int(request.query_params.get('limit', 100))
    except (ValueError, TypeError):
        limit = 100

    qs = qs[:limit]
    return Response(AuditLogSerializer(qs, many=True).data)


# ============================================================
# STATS — adaptées au rôle
# ============================================================

@api_view(['GET'])
@authentication_classes([BearerTokenAuthentication])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    """
    Renvoie des statistiques différentes selon le rôle :
    - it_admin : vue système complète (utilisateurs, équipe, partenaires)
    - admin    : vue contenu uniquement (ni équipe, ni partenaires, ni admins)
    """
    user = request.user

    if user.role == 'it_admin':
        return Response({
            'scope': 'it',
            'total_plantes': Plante.objects.filter(actif=True).count(),
            'total_projets': Projet.objects.count(),
            'total_activites': Activite.objects.filter(actif=True).count(),
            'total_publications': Publication.objects.filter(actif=True).count(),
            'total_partenaires': Partenaire.objects.filter(actif=True).count(),
            'total_equipe': Equipe.objects.filter(actif=True).count(),
            'total_users': SuperAdmin.objects.count(),
            'active_users': SuperAdmin.objects.filter(is_active=True).count(),
        })

    # Admin lambda : PAS d'équipe, PAS de partenaires, PAS d'utilisateurs
    return Response({
        'scope': 'admin',
        'total_plantes': Plante.objects.filter(actif=True).count(),
        'total_projets': Projet.objects.count(),
        'total_activites': Activite.objects.filter(actif=True).count(),
        'total_publications': Publication.objects.filter(actif=True).count(),
    })


# ============================================================
# VIEWSETS avec audit automatique
# ============================================================

class AuditedModelViewSet(viewsets.ModelViewSet):
    authentication_classes = [BearerTokenAuthentication]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_permissions(self):
        if self.request.method in ('GET', 'HEAD', 'OPTIONS'):
            return [AllowAny()]
        return [IsAuthenticated(), IsAdminOrSuperIT()]

    def perform_create(self, serializer):
        instance = serializer.save()
        log_action(self.request, 'CREATE',
                   model_name=self.queryset.model.__name__, obj=instance)

    def perform_update(self, serializer):
        instance = serializer.save()
        log_action(self.request, 'UPDATE',
                   model_name=self.queryset.model.__name__, obj=instance)

    def perform_destroy(self, instance):
        log_action(self.request, 'DELETE',
                   model_name=self.queryset.model.__name__, obj=instance)
        instance.delete()


# ----- CONTENU : Admin + SuperIT -----

class PlanteViewSet(AuditedModelViewSet):
    queryset = Plante.objects.all()
    serializer_class = PlanteSerializer


class ProjetViewSet(AuditedModelViewSet):
    queryset = Projet.objects.all()
    serializer_class = ProjetSerializer


class ActiviteViewSet(AuditedModelViewSet):
    queryset = Activite.objects.all()
    serializer_class = ActiviteSerializer


class PublicationViewSet(AuditedModelViewSet):
    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer


class SlideViewSet(AuditedModelViewSet):
    queryset = Slide.objects.all()
    serializer_class = SlideSerializer


class TemoignageViewSet(AuditedModelViewSet):
    queryset = Temoignage.objects.all()
    serializer_class = TemoignageSerializer


class FAQViewSet(AuditedModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer


class StatistiqueViewSet(AuditedModelViewSet):
    queryset = Statistique.objects.all()
    serializer_class = StatistiqueSerializer


class MethodologieViewSet(AuditedModelViewSet):
    queryset = Methodologie.objects.all()
    serializer_class = MethodologieSerializer


# ----- CONTENU : écriture SuperIT uniquement -----

class EquipeViewSet(AuditedModelViewSet):
    """Équipe — lecture publique, écriture réservée au SuperIT."""
    queryset = Equipe.objects.all()
    serializer_class = EquipeSerializer

    def get_permissions(self):
        if self.request.method in ('GET', 'HEAD', 'OPTIONS'):
            return [AllowAny()]
        return [IsAuthenticated(), IsSuperIT()]


class PartenaireViewSet(AuditedModelViewSet):
    """Partenaires — lecture publique, écriture réservée au SuperIT."""
    queryset = Partenaire.objects.all()
    serializer_class = PartenaireSerializer

    def get_permissions(self):
        if self.request.method in ('GET', 'HEAD', 'OPTIONS'):
            return [AllowAny()]
        return [IsAuthenticated(), IsSuperIT()]


# ============================================================
# SYNC (SuperIT uniquement)
# ============================================================

@api_view(['POST'])
@authentication_classes([BearerTokenAuthentication])
@permission_classes([IsAuthenticated, IsSuperIT])
def sync_all(request):
    log_action(request, 'SYNC', details={'scope': 'all'})
    return Response({'status': 'success', 'message': 'Synchronisation lancée'})


# ============================================================
# HEALTH, ROOT, MEDIA
# ============================================================

@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def health_check(request):
    return Response({'status': 'healthy'})


@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def api_root(request):
    return Response({
        'status': 'ok',
        'message': 'Admin API Herbier',
        'endpoints': {
            'auth': {
                'it_login': '/api/it/login/',
                'admin_login': '/api/admin/login/',
                'verify_2fa': '/api/verify-2fa/',
                'resend_code': '/api/resend-code/',
                'logout': '/api/logout/',
                'me': '/api/me/',
            },
            'users': '/api/users/',
            'audit': '/api/audit/logs/',
            'stats': '/api/stats/',
            'content': {
                'plantes': '/api/plantes/',
                'projets': '/api/projets/',
                'activites': '/api/activites/',
                'publications': '/api/publications/',
                'equipe': '/api/equipe/',
                'partenaires': '/api/partenaires/',
                'temoignages': '/api/temoignages/',
            },
        },
    })


@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def test_media(request):
    import os
    media_root = settings.MEDIA_ROOT
    exists = os.path.exists(media_root)
    return Response({
        'media_root': media_root,
        'exists': exists,
        'base_url': getattr(settings, 'BASE_URL', 'http://localhost:8001'),
    })


def serve_media(request, path):
    import os
    from django.http import HttpResponse, Http404
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if not os.path.exists(file_path):
        raise Http404("Fichier non trouvé")
    with open(file_path, 'rb') as f:
        return HttpResponse(f.read(), content_type='image/png')


# ============================================================
# CREATE SUPERADMIN (RÉTROCOMPATIBILITÉ)
# ============================================================

@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
@csrf_exempt
def create_superadmin(request):
    serializer = SuperAdminCreateSerializer(data=request.data)
    if serializer.is_valid():
        try:
            user = serializer.save()
            code = generate_otp()
            OTPCode.objects.create(
                user=user, code=code, type='email',
                expires_at=timezone.now() + timedelta(minutes=10),
            )
            print(f"\n🔐 NOUVEAU COMPTE - Code OTP: {code}\n")
            return Response({
                'success': True,
                'message': 'Compte créé',
                'email': user.email,
                'test_code': code if settings.DEBUG else None,
            }, status=201)
        except Exception as e:
            return Response({'success': False, 'errors': {'general': str(e)}}, status=400)
    return Response({'success': False, 'errors': serializer.errors}, status=400)


# ============================================================
# MES ACTIVITÉS (Admin voit ses propres actions)
# ============================================================

@api_view(['GET'])
@authentication_classes([BearerTokenAuthentication])
@permission_classes([IsAuthenticated])
def my_activity(request):
    """
    Retourne les actions de l'utilisateur connecté UNIQUEMENT.
    Confidentialité : un Admin ne voit que ses propres actions.
    """
    limit = min(int(request.query_params.get('limit', 20)), 100)

    qs = AuditLog.objects.filter(user=request.user).order_by('-created_at')[:limit]

    data = []
    for log in qs:
        item = {
            'id': log.id,
            'action': log.action,
            'action_label': log.get_action_display(),
            'model_name': log.model_name,
            'object_repr': log.object_repr,
            'created_at': log.created_at.isoformat(),
        }
        if request.user.role == 'it_admin':
            item['ip_address'] = log.ip_address
            item['user_agent'] = log.user_agent
        data.append(item)

    return Response(data)


# ============================================================
# 2FA TOTP — Setup & Vérification
# ============================================================

@api_view(['POST'])
@authentication_classes([BearerTokenAuthentication])
@permission_classes([IsAuthenticated])
def totp_setup(request):
    user = request.user

    if user.totp_enabled:
        return Response(
            {'error': 'TOTP déjà activé. Désactivez-le d\'abord.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    secret = pyotp.random_base32()
    user.totp_secret = secret
    user.save(update_fields=['totp_secret'])

    totp_uri = pyotp.totp.TOTP(secret).provisioning_uri(
        name=user.email,
        issuer_name='Herbier Admin'
    )

    qr = qrcode.QRCode(version=1, box_size=10, border=2)
    qr.add_data(totp_uri)
    qr.make(fit=True)

    img = qr.make_image(fill_color='black', back_color='white')
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    qr_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    log_action(request, 'UPDATE', model_name='SuperAdmin', obj=user, details={
        'action': 'totp_setup',
    })

    return Response({
        'success': True,
        'secret': secret,
        'qr_code': qr_base64,
        'uri': totp_uri,
        'message': 'Scannez le QR code avec Google Authenticator',
    })


@api_view(['POST'])
@authentication_classes([BearerTokenAuthentication])
@permission_classes([IsAuthenticated])
def totp_verify_setup(request):
    user = request.user
    code = (request.data.get('code') or '').strip()

    if not user.totp_secret:
        return Response(
            {'error': 'Aucun setup TOTP en cours'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    totp = pyotp.TOTP(user.totp_secret)

    if not totp.verify(code, valid_window=1):
        return Response(
            {'error': 'Code invalide'},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    user.totp_enabled = True
    user.requires_2fa = True

    backup_codes = [secrets.token_hex(4).upper() for _ in range(8)]
    user.totp_backup_codes = backup_codes
    user.save(update_fields=['totp_enabled', 'requires_2fa', 'totp_backup_codes'])

    log_action(request, 'UPDATE', model_name='SuperAdmin', obj=user, details={
        'action': 'totp_activated',
    })

    return Response({
        'success': True,
        'message': '2FA TOTP activée',
        'backup_codes': backup_codes,
    })


@api_view(['POST'])
@authentication_classes([BearerTokenAuthentication])
@permission_classes([IsAuthenticated])
def totp_disable(request):
    user = request.user
    password = request.data.get('password') or ''

    if not user.check_password(password):
        return Response(
            {'error': 'Mot de passe incorrect'},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    user.totp_enabled = False
    user.totp_secret = None
    user.totp_backup_codes = []
    user.save(update_fields=['totp_enabled', 'totp_secret', 'totp_backup_codes'])

    log_action(request, 'UPDATE', model_name='SuperAdmin', obj=user, details={
        'action': 'totp_disabled',
    })

    return Response({'success': True, 'message': '2FA TOTP désactivée'})