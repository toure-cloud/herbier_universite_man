from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, viewsets
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import random
import string

@api_view(['GET'])
def api_root(request):
    return Response({'status': 'ok', 'message': 'API Admin Herbier'})

@api_view(['GET'])
def health_check(request):
    return Response({'status': 'healthy'})

@csrf_exempt
@api_view(['POST'])
def create_superadmin(request):
    from .serializers import SuperAdminCreateSerializer
    from .models import OTPCode
    
    serializer = SuperAdminCreateSerializer(data=request.data)
    if serializer.is_valid():
        try:
            user = serializer.save()
            code = ''.join(random.choices(string.digits, k=6))
            expires_at = timezone.now() + timezone.timedelta(minutes=10)
            OTPCode.objects.create(user=user, code=code, type='email', expires_at=expires_at)
            return Response({'success': True, 'message': 'Compte créé', 'email': user.email}, status=201)
        except Exception as e:
            return Response({'success': False, 'errors': {'general': str(e)}}, status=400)
    return Response({'success': False, 'errors': serializer.errors}, status=400)

@csrf_exempt
@api_view(['POST'])
def login_superadmin(request):
    from .models import SuperAdmin, OTPCode
    try:
        user = SuperAdmin.objects.get(email=request.data.get('email'))
        if user.check_password(request.data.get('password')):
            code = ''.join(random.choices(string.digits, k=6))
            expires_at = timezone.now() + timezone.timedelta(minutes=10)
            OTPCode.objects.filter(user=user, is_used=False).delete()
            OTPCode.objects.create(user=user, code=code, type='email', expires_at=expires_at)
            return Response({'success': True, 'requires_2fa': True, 'email': user.email})
        return Response({'success': False, 'error': 'Identifiants incorrects'}, status=401)
    except SuperAdmin.DoesNotExist:
        return Response({'success': False, 'error': 'Identifiants incorrects'}, status=401)

@csrf_exempt
@api_view(['POST'])
def verify_2fa(request):
    from .models import SuperAdmin, OTPCode
    try:
        user = SuperAdmin.objects.get(email=request.data.get('email'))
        otp = OTPCode.objects.filter(user=user, code=request.data.get('code'), is_used=False).first()
        if otp and otp.is_valid():
            otp.is_used = True
            otp.save()
            user.is_active = True
            user.save()
            import hashlib
            token = hashlib.md5(f"{user.email}:{timezone.now()}".encode()).hexdigest()
            return Response({'success': True, 'access': token, 'refresh': token, 'user': {'email': user.email, 'nom': user.nom}})
        return Response({'success': False, 'error': 'Code invalide'}, status=401)
    except Exception as e:
        return Response({'success': False, 'error': str(e)}, status=400)

@api_view(['POST'])
def logout_superadmin(request):
    return Response({'success': True})

@api_view(['GET'])
def get_current_user(request):
    return Response({'error': 'Non authentifié'}, status=401)

class PlanteViewSet(viewsets.ViewSet):
    def list(self, request): return Response({'data': []})
    def create(self, request): return Response({'message': 'Créé'}, status=201)

class EquipeViewSet(viewsets.ViewSet):
    def list(self, request): return Response({'data': []})
    def create(self, request): return Response({'message': 'Créé'}, status=201)

class SlideViewSet(viewsets.ViewSet):
    def list(self, request): return Response({'data': []})
    def create(self, request): return Response({'message': 'Créé'}, status=201)

class ProjetViewSet(viewsets.ViewSet):
    def list(self, request): return Response({'data': []})
    def create(self, request): return Response({'message': 'Créé'}, status=201)

@api_view(['GET'])
def dashboard_stats(request):
    from .models import SuperAdmin
    return Response({'total_admins': SuperAdmin.objects.count()})

@api_view(['GET'])
def sync_all_data(request): return Response({'status': 'success'})
@api_view(['GET'])
def sync_endpoint(request, endpoint): return Response({'status': 'success'})
@api_view(['GET'])
def get_sync_logs(request): return Response([])
