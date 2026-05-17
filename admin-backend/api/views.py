from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, viewsets
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.utils import timezone
import random
import string

# ==================== FONCTIONS DE BASE ====================

@api_view(['GET'])
def api_root(request):
    return Response({
        'status': 'ok',
        'message': 'Admin API Herbier Universite de Man',
        'version': '1.0.0',
        'endpoints': {
            'health': '/api/health/',
            'create_superadmin': '/api/create-superadmin/',
            'login': '/api/login/',
            'verify_2fa': '/api/verify-2fa/',
            'logout': '/api/logout/',
            'me': '/api/me/',
            'dashboard': '/api/dashboard/',
            'plantes': '/api/plantes/',
            'equipe': '/api/equipe/',
            'slides': '/api/slides/',
            'projets': '/api/projets/'
        }
    })

@api_view(['GET'])
def health_check(request):
    return Response({'status': 'healthy', 'timestamp': timezone.now().isoformat()})

# ==================== FONCTIONS D'AUTHENTIFICATION ====================

def generate_otp():
    return ''.join(random.choices(string.digits, k=6))

def send_otp_email(email, code):
    """Envoyer le code OTP par email"""
    subject = "Code d'authentification - Herbier Université de Man"
    message = f"""
    Bonjour,
    
    Votre code d'authentification unique est : {code}
    
    Ce code est valable pendant 10 minutes.
    
    Cordialement,
    L'équipe de l'Herbier Université de Man
    """
    try:
        send_mail(subject, message, 'noreply@herbier-man.ci', [email])
        return True
    except Exception as e:
        print(f"Erreur envoi email: {e}")
        return False

@api_view(['POST'])
def create_superadmin(request):
    """Créer un nouveau super administrateur"""
    from .serializers import SuperAdminCreateSerializer
    
    serializer = SuperAdminCreateSerializer(data=request.data)
    if serializer.is_valid():
        try:
            user = serializer.save()
            
            # Générer le code OTP
            code = generate_otp()
            expires_at = timezone.now() + timezone.timedelta(minutes=10)
            
            from .models import OTPCode
            OTPCode.objects.create(
                user=user,
                code=code,
                type='email',
                expires_at=expires_at
            )
            
            # Envoyer le code par email
            send_otp_email(user.email, code)
            
            return Response({
                'success': True,
                'message': 'Compte créé avec succès. Un code de vérification a été envoyé à votre email.',
                'email': user.email
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({
                'success': False,
                'errors': {'general': str(e)}
            }, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({
        'success': False,
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_superadmin(request):
    """Connexion - première étape"""
    email = request.data.get('email')
    password = request.data.get('password')
    
    from .models import SuperAdmin
    try:
        user = SuperAdmin.objects.get(email=email)
        if user.check_password(password):
            # Générer un nouveau code OTP
            code = generate_otp()
            expires_at = timezone.now() + timezone.timedelta(minutes=10)
            
            from .models import OTPCode
            OTPCode.objects.filter(user=user, is_used=False).delete()
            OTPCode.objects.create(
                user=user,
                code=code,
                type='email',
                expires_at=expires_at
            )
            
            send_otp_email(user.email, code)
            
            return Response({
                'success': True,
                'message': 'Code de vérification envoyé à votre email',
                'email': user.email,
                'requires_2fa': True
            })
        else:
            return Response({
                'success': False,
                'error': 'Email ou mot de passe incorrect'
            }, status=status.HTTP_401_UNAUTHORIZED)
    except SuperAdmin.DoesNotExist:
        return Response({
            'success': False,
            'error': 'Email ou mot de passe incorrect'
        }, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def verify_2fa(request):
    """Vérification du code OTP"""
    email = request.data.get('email')
    code = request.data.get('code')
    
    from .models import SuperAdmin, OTPCode
    
    try:
        user = SuperAdmin.objects.get(email=email)
        otp = OTPCode.objects.filter(user=user, code=code, is_used=False).first()
        
        if otp and otp.is_valid():
            otp.is_used = True
            otp.save()
            
            user.is_active = True
            user.save()
            
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'success': True,
                'message': 'Authentification réussie',
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'nom': user.nom,
                    'telephone': user.telephone,
                    'pays_code': user.pays_code
                }
            })
        else:
            return Response({
                'success': False,
                'error': 'Code invalide ou expiré'
            }, status=status.HTTP_401_UNAUTHORIZED)
            
    except SuperAdmin.DoesNotExist:
        return Response({
            'success': False,
            'error': 'Utilisateur non trouvé'
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def logout_superadmin(request):
    """Déconnexion"""
    try:
        refresh_token = request.data.get('refresh')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        return Response({'success': True, 'message': 'Déconnecté'})
    except Exception as e:
        return Response({'success': False, 'error': str(e)}, status=400)

@api_view(['GET'])
def get_current_user(request):
    """Récupérer l'utilisateur connecté"""
    if request.user.is_authenticated:
        from .serializers import SuperAdminSerializer
        serializer = SuperAdminSerializer(request.user)
        return Response(serializer.data)
    return Response({'error': 'Non authentifié'}, status=401)

# ==================== VIEWSETS POUR LES DONNÉES ====================

class PlanteViewSet(viewsets.ViewSet):
    def list(self, request):
        return Response({'message': 'Liste des plantes', 'data': []})
    
    def create(self, request):
        return Response({'message': 'Plante créée', 'data': request.data}, status=201)

class EquipeViewSet(viewsets.ViewSet):
    def list(self, request):
        return Response({'message': 'Liste équipe', 'data': []})
    
    def create(self, request):
        return Response({'message': 'Membre créé', 'data': request.data}, status=201)

class SlideViewSet(viewsets.ViewSet):
    def list(self, request):
        return Response({'message': 'Liste slides', 'data': []})
    
    def create(self, request):
        return Response({'message': 'Slide créé', 'data': request.data}, status=201)

class ProjetViewSet(viewsets.ViewSet):
    def list(self, request):
        return Response({'message': 'Liste projets', 'data': []})
    
    def create(self, request):
        return Response({'message': 'Projet créé', 'data': request.data}, status=201)

# ==================== FONCTIONS DASHBOARD ET SYNC ====================

@api_view(['GET'])
def dashboard_stats(request):
    """Statistiques du tableau de bord"""
    from .models import SuperAdmin
    return Response({
        'total_plantes': 0,
        'total_equipe': 0,
        'total_projets': 0,
        'total_slides': 0,
        'total_admins': SuperAdmin.objects.count()
    })

@api_view(['GET'])
def sync_all_data(request):
    """Synchroniser toutes les données"""
    return Response({
        'status': 'success',
        'message': 'Synchronisation terminée',
        'synced': ['plantes', 'equipe', 'slides', 'projets']
    })

@api_view(['GET'])
def sync_endpoint(request, endpoint):
    """Synchroniser un endpoint spécifique"""
    return Response({
        'status': 'success',
        'endpoint': endpoint,
        'message': f'Synchronisation de {endpoint} terminée'
    })

@api_view(['GET'])
def get_sync_logs(request):
    """Récupérer les logs de synchronisation"""
    return Response([])
