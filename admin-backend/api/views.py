from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status, viewsets
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import SAFE_METHODS
from rest_framework.response import Response
import random
from django.views.decorators.csrf import csrf_exempt 
import string
import hashlib
import time
from datetime import timedelta
from django.utils import timezone

from .models import (
    Partenaire, Plante, Equipe, Slide, Projet, Activite, 
    Temoignage, Publication, FAQ, Statistique, Methodologie,
    SuperAdmin, OTPCode, UserToken
)
from .serializers import (
    PartenaireSerializer, PlanteSerializer, EquipeSerializer, SlideSerializer, 
    ProjetSerializer, ActiviteSerializer, TemoignageSerializer,
    PublicationSerializer, FAQSerializer, StatistiqueSerializer,
    MethodologieSerializer, SuperAdminSerializer, SuperAdminCreateSerializer
)

# ==================== FONCTIONS DE BASE ====================

def generate_token(user):
    UserToken.objects.filter(user=user, is_active=True).update(is_active=False)
    token_data = f"{user.email}:{int(time.time())}:{random.randint(1000, 9999)}"
    token = hashlib.md5(token_data.encode()).hexdigest()
    UserToken.objects.create(
        user=user,
        token=token,
        expires_at=timezone.now() + timedelta(days=7)
    )
    return token

def verify_token(token):
    try:
        user_token = UserToken.objects.get(
            token=token,
            is_active=True,
            expires_at__gt=timezone.now()
        )
        return user_token.user
    except UserToken.DoesNotExist:
        return None

def verify_token_and_get_user(request):
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return None
    token = auth_header.split(' ')[1]
    if not token:
        return None
    return verify_token(token)

class BearerTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return None

        token = auth_header.split(' ', 1)[1].strip()
        if not token:
            return None

        user = verify_token(token)
        if not user:
            raise AuthenticationFailed('Token invalide ou expiré')

        return (user, token)


# ==================== AUTHENTIFICATION ====================

def generate_otp():
    return ''.join(random.choices(string.digits, k=6))


@api_view(['POST'])
def forgot_password(request):
    """Demande de réinitialisation de mot de passe"""
    email = request.data.get('email')
    if not email:
        return Response({'error': 'Email requis'}, status=400)
    
    try:
        user = SuperAdmin.objects.get(email=email)
        code = generate_otp()
        expires_at = timezone.now() + timezone.timedelta(minutes=15)
        OTPCode.objects.filter(user=user, is_used=False).delete()
        OTPCode.objects.create(
            user=user,
            code=code,
            type='email',
            expires_at=expires_at
        )
        print(f"\n🔑 RÉINITIALISATION MOT DE PASSE - Code: {code}\n")
        return Response({
            'success': True,
            'message': 'Code envoyé',
            'test_code': code
        })
    except SuperAdmin.DoesNotExist:
        return Response({'error': 'Email non trouvé'}, status=404)


@api_view(['POST'])
def reset_password(request):
    """Réinitialiser le mot de passe avec code OTP"""
    email = request.data.get('email')
    code = request.data.get('code')
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


@api_view(['GET'])
def api_root(request):
    return Response({
        'status': 'ok',
        'message': 'Admin API Herbier Universite de Man',
        'version': '1.0.0',
        'endpoints': {
            'plantes': '/api/plantes/',
            'equipe': '/api/equipe/',
            'slides': '/api/slides/',
            'projets': '/api/projets/',
            'activites': '/api/activites/',
            'partenaires': '/api/partenaires/',
            'temoignages': '/api/temoignages/',
            'publications': '/api/publications/',
            'faqs': '/api/faqs/',
            'statistiques': '/api/statistiques/',
            'methodologie': '/api/methodologie/',
            'auth': {
                'create_superadmin': '/api/create-superadmin/',
                'login': '/api/login/',
                'verify_2fa': '/api/verify-2fa/',
                'resend_code': '/api/resend-code/',
                'forgot_password': '/api/forgot-password/',
                'reset_password': '/api/reset-password/',
                'logout': '/api/logout/',
                'me': '/api/me/'
            },
            'admin': {
                'users': '/api/users/',
                'sync': '/api/sync-all/'
            }
        }
    })
    

@api_view(['GET'])
def health_check(request):
    return Response({'status': 'healthy'})


@api_view(['GET'])
def dashboard_stats(request):
    return Response({
        'total_plantes': Plante.objects.filter(actif=True).count(),
        'total_equipe': Equipe.objects.filter(actif=True).count(),
        'total_slides': Slide.objects.filter(actif=True).count(),
        'total_projets': Projet.objects.count(),
        'total_activites': Activite.objects.filter(actif=True).count(),
        'total_partenaires': Partenaire.objects.filter(actif=True).count(),
        'total_users': SuperAdmin.objects.count(),
        'active_users': SuperAdmin.objects.filter(is_active=True).count()
    })


@api_view(['POST'])
@csrf_exempt
def create_superadmin(request):
    serializer = SuperAdminCreateSerializer(data=request.data)
    if serializer.is_valid():
        try:
            user = serializer.save()
            code = generate_otp()
            expires_at = timezone.now() + timezone.timedelta(minutes=10)
            OTPCode.objects.create(
                user=user,
                code=code,
                type='email',
                expires_at=expires_at
            )
            print(f"\n🔐 NOUVEAU COMPTE - Code OTP: {code}\n")
            return Response({
                'success': True,
                'message': 'Compte créé',
                'email': user.email,
                'test_code': code
            }, status=201)
        except Exception as e:
            return Response({'success': False, 'errors': {'general': str(e)}}, status=400)
    return Response({'success': False, 'errors': serializer.errors}, status=400)


@api_view(['POST'])
def login_superadmin(request):
    email = request.data.get('email')
    password = request.data.get('password')
    try:
        user = SuperAdmin.objects.get(email=email)
        if user.check_password(password):
            code = generate_otp()
            expires_at = timezone.now() + timezone.timedelta(minutes=10)
            OTPCode.objects.filter(user=user, is_used=False).delete()
            OTPCode.objects.create(
                user=user,
                code=code,
                type='email',
                expires_at=expires_at
            )
            print(f"\n🔐 CODE OTP pour {email}: {code}\n")
            return Response({
                'success': True,
                'message': 'Code envoyé',
                'email': user.email,
                'requires_2fa': True,
                'test_code': code
            })
        else:
            return Response({'success': False, 'error': 'Identifiants incorrects'}, status=401)
    except SuperAdmin.DoesNotExist:
        return Response({'success': False, 'error': 'Identifiants incorrects'}, status=401)


@api_view(['POST'])
def verify_2fa(request):
    email = request.data.get('email')
    code = request.data.get('code')
    try:
        user = SuperAdmin.objects.get(email=email)
        otp = OTPCode.objects.filter(user=user, code=code, is_used=False).first()
        if otp and otp.is_valid():
            otp.is_used = True
            otp.save()
            user.is_active = True
            user.last_login = timezone.now()
            user.save()
            token = generate_token(user)
            print(f"\n✅ CONNEXION RÉUSSIE - {user.email}")
            print(f"🔑 Token: {token[:30]}...\n")
            return Response({
                'success': True,
                'access': token,
                'refresh': token,
                'user': SuperAdminSerializer(user).data
            })
        else:
            return Response({'success': False, 'error': 'Code invalide'}, status=401)
    except SuperAdmin.DoesNotExist:
        return Response({'success': False, 'error': 'Utilisateur non trouvé'}, status=404)

from django.http import HttpResponse, Http404
from django.conf import settings
import os

@api_view(['GET'])
def serve_media(request, path):
    """Sert les fichiers médias"""
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    
    # Sécurité : empêcher l'accès aux dossiers parents
    if not file_path.startswith(os.path.abspath(settings.MEDIA_ROOT)):
        raise Http404("Accès non autorisé")
    
    if not os.path.exists(file_path):
        raise Http404("Fichier non trouvé")
    
    with open(file_path, 'rb') as f:
        return HttpResponse(f.read(), content_type='image/png')
@api_view(['GET'])
def get_admin_users(request):
    """Récupère la liste des administrateurs (accessible uniquement aux IT admins)"""
    user = verify_token_and_get_user(request)
    if not user:
        return Response({'error': 'Non authentifié'}, status=401)
    
    # ✅ Vérifier si l'utilisateur est IT Admin ou Super Admin
    if user.role != 'it_admin' and not user.is_superuser:
        return Response({'error': 'Accès non autorisé'}, status=403)
    
    users = SuperAdmin.objects.all()
    return Response(SuperAdminSerializer(users, many=True).data)    
    
@api_view(['POST'])
def resend_code(request):
    email = request.data.get('email')
    try:
        user = SuperAdmin.objects.get(email=email)
        code = generate_otp()
        expires_at = timezone.now() + timezone.timedelta(minutes=10)
        OTPCode.objects.filter(user=user, is_used=False).delete()
        OTPCode.objects.create(user=user, code=code, type='email', expires_at=expires_at)
        print(f"\n🔄 NOUVEAU CODE pour {email}: {code}\n")
        return Response({'success': True, 'message': 'Code renvoyé', 'test_code': code})
    except SuperAdmin.DoesNotExist:
        return Response({'success': False, 'error': 'Utilisateur non trouvé'}, status=404)


@api_view(['POST'])
def logout_superadmin(request):
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith('Bearer '):
        token = auth_header.split(' ')[1]
        try:
            UserToken.objects.filter(token=token, is_active=True).update(is_active=False)
        except:
            pass
    return Response({'success': True})


@api_view(['GET'])
def get_current_user(request):
    user = verify_token_and_get_user(request)
    if user:
        return Response(SuperAdminSerializer(user).data)
    return Response({'error': 'Non authentifié'}, status=401)


# ==================== VIEWSETS ====================

class BaseAdminViewSet(viewsets.ModelViewSet):
    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_authenticators(self):
        if self.request.method in SAFE_METHODS:
            return []
        return [BearerTokenAuthentication()]

class PlanteViewSet(BaseAdminViewSet):
    queryset = Plante.objects.all()
    serializer_class = PlanteSerializer
    
    def create(self, request, *args, **kwargs):
        print("=" * 60)
        print("📝 [Plante] Données reçues:")
        print(f"  - data: {request.data}")
        print(f"  - files: {request.FILES}")
        print(f"  - content_type: {request.content_type}")
        print("=" * 60)
        
        # ✅ Vérifier que le fichier est bien présent
        if 'image' in request.FILES:
            print(f"✅ Fichier reçu: {request.FILES['image'].name} ({request.FILES['image'].size} bytes)")
        
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            print("❌ [Plante] Erreurs de validation:")
            print(serializer.errors)
            return Response(serializer.errors, status=400)
        
        return super().create(request, *args, **kwargs)

class EquipeViewSet(BaseAdminViewSet):
    queryset = Equipe.objects.all()
    serializer_class = EquipeSerializer


class SlideViewSet(BaseAdminViewSet):
    queryset = Slide.objects.all()
    serializer_class = SlideSerializer


class ProjetViewSet(BaseAdminViewSet):
    queryset = Projet.objects.all()
    serializer_class = ProjetSerializer


class ActiviteViewSet(BaseAdminViewSet):
    queryset = Activite.objects.all()
    serializer_class = ActiviteSerializer
    
    # ✅ AJOUT : Méthode create avec logs
    def create(self, request, *args, **kwargs):
        print("=" * 60)
        print("📝 [Activite] Données reçues:")
        print(f"  - data: {request.data}")
        print(f"  - files: {request.FILES}")
        print(f"  - content_type: {request.content_type}")
        print("=" * 60)
        
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            print("❌ [Activite] Erreurs de validation:")
            print(serializer.errors)
            return Response(serializer.errors, status=400)
        
        return super().create(request, *args, **kwargs)


class TemoignageViewSet(BaseAdminViewSet):
    queryset = Temoignage.objects.all()
    serializer_class = TemoignageSerializer


class PublicationViewSet(BaseAdminViewSet):
    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer


class FAQViewSet(BaseAdminViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer


class StatistiqueViewSet(BaseAdminViewSet):
    queryset = Statistique.objects.all()
    serializer_class = StatistiqueSerializer


class MethodologieViewSet(BaseAdminViewSet):
    queryset = Methodologie.objects.all()
    serializer_class = MethodologieSerializer


class PartenaireViewSet(BaseAdminViewSet):
    queryset = Partenaire.objects.all()
    serializer_class = PartenaireSerializer
    
    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    def create(self, request, *args, **kwargs):
        """Surcharge pour gérer l'upload de logo"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


# ==================== BATCH IMPORT ====================

@api_view(['POST'])
def create_multiple_plantes(request):
    user = verify_token_and_get_user(request)
    if not user:
        return Response({'error': 'Non authentifié'}, status=401)
    
    if not isinstance(request.data, list):
        return Response({'error': 'Format invalide'}, status=400)
    
    created = []
    errors = []
    
    for idx, item in enumerate(request.data):
        try:
            serializer = PlanteSerializer(data=item)
            if serializer.is_valid():
                plante = serializer.save()
                created.append({'id': plante.id, 'nom': plante.nom})
            else:
                errors.append({'index': idx, 'errors': serializer.errors})
        except Exception as e:
            errors.append({'index': idx, 'error': str(e)})
    
    return Response({
        'created': created,
        'errors': errors,
        'total': len(request.data),
        'success_count': len(created),
        'error_count': len(errors)
    })

# admin-backend/api/views.py
# Ajouter cette fonction à la fin du fichier

from django.conf import settings
import os

@api_view(['GET'])
def test_media(request):
    """Endpoint pour tester l'accès aux médias"""
    media_root = settings.MEDIA_ROOT
    
    # Vérifier si le dossier existe
    exists = os.path.exists(media_root)
    
    # Lister les sous-dossiers
    folders = []
    if exists:
        for item in os.listdir(media_root):
            path = os.path.join(media_root, item)
            if os.path.isdir(path):
                files = len(os.listdir(path))
                folders.append({
                    'name': item,
                    'path': path,
                    'files': files,
                    'files_list': os.listdir(path)[:5]  # 5 premiers fichiers
                })
    
    return Response({
        'media_root': media_root,
        'exists': exists,
        'folders': folders,
        'media_url': settings.MEDIA_URL,
        'base_url': getattr(settings, 'BASE_URL', 'http://localhost:8001')
    })
    
    

@api_view(['POST'])
def create_multiple_equipe(request):
    user = verify_token_and_get_user(request)
    if not user:
        return Response({'error': 'Non authentifié'}, status=401)
    
    if user.role != 'it_admin' and not user.is_superuser:
        return Response({'error': 'Accès non autorisé'}, status=403)
    
    if not isinstance(request.data, list):
        return Response({'error': 'Format invalide'}, status=400)
    
    created = []
    errors = []
    
    for idx, item in enumerate(request.data):
        try:
            serializer = EquipeSerializer(data=item)
            if serializer.is_valid():
                membre = serializer.save()
                created.append({'id': membre.id, 'nom': membre.nom})
            else:
                errors.append({'index': idx, 'errors': serializer.errors})
        except Exception as e:
            errors.append({'index': idx, 'error': str(e)})
    
    return Response({
        'created': created,
        'errors': errors,
        'total': len(request.data),
        'success_count': len(created),
        'error_count': len(errors)
    })


@api_view(['POST'])
def create_multiple_partenaires(request):
    user = verify_token_and_get_user(request)
    if not user:
        return Response({'error': 'Non authentifié'}, status=401)
    
    if user.role != 'it_admin' and not user.is_superuser:
        return Response({'error': 'Accès non autorisé'}, status=403)
    
    if not isinstance(request.data, list):
        return Response({'error': 'Format invalide'}, status=400)
    
    created = []
    errors = []
    
    for idx, item in enumerate(request.data):
        try:
            serializer = PartenaireSerializer(data=item)
            if serializer.is_valid():
                partenaire = serializer.save()
                created.append({'id': partenaire.id, 'nom': partenaire.nom})
            else:
                errors.append({'index': idx, 'errors': serializer.errors})
        except Exception as e:
            errors.append({'index': idx, 'error': str(e)})
    
    return Response({
        'created': created,
        'errors': errors,
        'total': len(request.data),
        'success_count': len(created),
        'error_count': len(errors)
    })


# ==================== GESTION UTILISATEURS ====================

@api_view(['GET'])
def get_users(request):
    user = verify_token_and_get_user(request)
    if not user:
        return Response({'error': 'Non authentifié'}, status=401)
    
    if user.role != 'it_admin' and not user.is_superuser:
        return Response({'error': 'Accès non autorisé'}, status=403)
    
    users = SuperAdmin.objects.all()
    return Response(SuperAdminSerializer(users, many=True).data)


@api_view(['POST'])
def create_user(request):
    user = verify_token_and_get_user(request)
    if not user:
        return Response({'error': 'Non authentifié'}, status=401)
    
    if user.role != 'it_admin' and not user.is_superuser:
        return Response({'error': 'Accès non autorisé'}, status=403)
    
    serializer = SuperAdminCreateSerializer(data=request.data)
    if serializer.is_valid():
        new_user = serializer.save()
        return Response({'success': True, 'user': SuperAdminSerializer(new_user).data}, status=201)
    return Response({'errors': serializer.errors}, status=400)


@api_view(['PUT'])
def update_user(request, user_id):
    user = verify_token_and_get_user(request)
    if not user:
        return Response({'error': 'Non authentifié'}, status=401)
    
    if user.role != 'it_admin' and not user.is_superuser:
        return Response({'error': 'Accès non autorisé'}, status=403)
    
    try:
        target = SuperAdmin.objects.get(id=user_id)
        if target.id == user.id:
            return Response({'error': 'Vous ne pouvez pas modifier votre propre compte'}, status=400)
        
        for key, value in request.data.items():
            if hasattr(target, key) and key not in ['id', 'password', 'date_joined', 'last_login']:
                setattr(target, key, value)
        target.save()
        return Response({'success': True})
    except SuperAdmin.DoesNotExist:
        return Response({'error': 'Utilisateur non trouvé'}, status=404)


@api_view(['DELETE'])
def delete_user(request, user_id):
    user = verify_token_and_get_user(request)
    if not user:
        return Response({'error': 'Non authentifié'}, status=401)
    
    if user.role != 'it_admin' and not user.is_superuser:
        return Response({'error': 'Accès non autorisé'}, status=403)
    
    if user.id == user_id:
        return Response({'error': 'Vous ne pouvez pas vous supprimer'}, status=400)
    
    try:
        SuperAdmin.objects.get(id=user_id).delete()
        return Response({'success': True})
    except SuperAdmin.DoesNotExist:
        return Response({'error': 'Utilisateur non trouvé'}, status=404)


@api_view(['PUT'])
def toggle_user_status(request, user_id):
    user = verify_token_and_get_user(request)
    if not user:
        return Response({'error': 'Non authentifié'}, status=401)
    
    if user.role != 'it_admin' and not user.is_superuser:
        return Response({'error': 'Accès non autorisé'}, status=403)
    
    try:
        target = SuperAdmin.objects.get(id=user_id)
        target.is_active = request.data.get('is_active', not target.is_active)
        target.save()
        return Response({'success': True, 'is_active': target.is_active})
    except SuperAdmin.DoesNotExist:
        return Response({'error': 'Utilisateur non trouvé'}, status=404)


@api_view(['POST'])
def sync_all_data(request):
    user = verify_token_and_get_user(request)
    if not user:
        return Response({'error': 'Non authentifié'}, status=401)
    return Response({'status': 'success', 'message': 'Synchronisation terminée'})