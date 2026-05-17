from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, viewsets
from django.views.decorators.csrf import csrf_exempt
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
            'dashboard': '/api/dashboard/'
        }
    })

@api_view(['GET'])
def health_check(request):
    return Response({'status': 'healthy', 'timestamp': timezone.now().isoformat()})

# ==================== AUTHENTIFICATION ====================

@csrf_exempt
@api_view(['POST'])
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

@csrf_exempt
@api_view(['POST'])
def create_superadmin(request):
    """Créer un nouveau super administrateur"""
    from .serializers import SuperAdminCreateSerializer
    
    serializer = SuperAdminCreateSerializer(data=request.data)
    if serializer.is_valid():
        try:
            user = serializer.save()
            
            import random
            import string
            from django.utils import timezone
            from .models import OTPCode
            
            code = ''.join(random.choices(string.digits, k=6))
            expires_at = timezone.now() + timezone.timedelta(minutes=10)
            
            OTPCode.objects.create(
                user=user,
                code=code,
                type='email',
                expires_at=expires_at
            )
            
            return Response({
                'success': True,
                'message': 'Compte créé avec succès. Un code de vérification a été envoyé.',
                'email': user.email
            }, status=201)
            
        except Exception as e:
            return Response({
                'success': False,
                'errors': {'general': str(e)}
            }, status=400)
    
    return Response({
        'success': False,
        'errors': serializer.errors
    }, status=400)
    """Connexion - première étape"""
    email = request.data.get('email')
    password = request.data.get('password')
    
    from .models import SuperAdmin
    try:
        user = SuperAdmin.objects.get(email=email)
        if user.check_password(password):
            code = ''.join(random.choices(string.digits, k=6))
            expires_at = timezone.now() + timezone.timedelta(minutes=10)
            
            from .models import OTPCode
            OTPCode.objects.filter(user=user, is_used=False).delete()
            OTPCode.objects.create(
                user=user,
                code=code,
                type='email',
                expires_at=expires_at
            )
            
            return Response({
                'success': True,
                'message': 'Code de vérification envoyé',
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

@csrf_exempt
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
            
            # Générer un token simple
            import hashlib
            token = hashlib.md5(f"{user.email}:{timezone.now()}".encode()).hexdigest()
            
            return Response({
                'success': True,
                'access': token,
                'refresh': token,
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'nom': user.nom,
                    'telephone': user.telephone
                }
            })
        else:
            return Response({
                'success': False,
                'error': 'Code invalide ou expiré'
            }, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def dashboard_stats(request):
    return Response({
        'total_plantes': 0,
        'total_equipe': 0,
        'total_projets': 0,
        'total_slides': 0
    })

# ==================== VIEWSETS ====================

class PlanteViewSet(viewsets.ViewSet):
    def list(self, request):
        return Response({'data': []})
    def create(self, request):
        return Response({'message': 'Créé'}, status=201)

class EquipeViewSet(viewsets.ViewSet):
    def list(self, request):
        return Response({'data': []})
    def create(self, request):
        return Response({'message': 'Créé'}, status=201)

class SlideViewSet(viewsets.ViewSet):
    def list(self, request):
        return Response({'data': []})
    def create(self, request):
        return Response({'message': 'Créé'}, status=201)

class ProjetViewSet(viewsets.ViewSet):
    def list(self, request):
        return Response({'data': []})
    def create(self, request):
        return Response({'message': 'Créé'}, status=201)

@api_view(['GET'])
def sync_all_data(request):
    return Response({'status': 'success'})

@api_view(['GET'])
def sync_endpoint(request, endpoint):
    return Response({'status': 'success'})

@api_view(['GET'])
def get_sync_logs(request):
    return Response([])
