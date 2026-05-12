from rest_framework import viewsets, status  # type: ignore[import]
from rest_framework.decorators import api_view, permission_classes, action  # type: ignore[import]
from rest_framework.response import Response  # type: ignore[import]
from rest_framework.permissions import AllowAny, IsAuthenticated  # type: ignore[import]
from rest_framework_simplejwt.tokens import RefreshToken  # type: ignore[import]
from django.contrib.auth import authenticate  # type: ignore[import]
from django.core.mail import send_mail  # type: ignore[import]
from django.utils import timezone  # type: ignore[import]
from django.db.models import Q  # type: ignore[import]
import random
import string
import re
from .models import SuperAdmin, OTPCode, HerbierData, LoginHistory, AuditLog
from .serializers import (
    UserCreateSerializer, UserUpdateSerializer, UserListSerializer,
    SuperAdminLoginSerializer, OTPVerifySerializer, HerbierDataSerializer,
    LoginHistorySerializer, AuditLogSerializer
)

def generate_otp():
    return ''.join(random.choices(string.digits, k=6))

def send_otp_email(email, code):
    subject = "Code d'authentification - Herbier Université de Man"
    message = f"""
    Bonjour,
    
    Votre code d'authentification unique pour accéder à l'administration de l'Herbier de l'Université de Man est :
    
    🔐 {code}
    
    Ce code est valable pendant 10 minutes.
    
    Cordialement,
    L'équipe de l'Herbier Université de Man
    """
    send_mail(subject, message, 'noreply@herbier-man.ci', [email])

def log_audit(user, action, model_name, object_id=None, object_name='', changes=None):
    AuditLog.objects.create(
        user=user,
        action=action,
        model_name=model_name,
        object_id=object_id,
        object_name=object_name,
        changes=changes or {},
        ip_address=None
    )

# ==================== GESTION DES UTILISATEURS ====================

class UserViewSet(viewsets.ModelViewSet):
    queryset = SuperAdmin.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return UserListSerializer
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return SuperAdmin.objects.all()
        return SuperAdmin.objects.filter(id=user.id)
    
    def perform_create(self, serializer):
        user = serializer.save(created_by=self.request.user)
        log_audit(self.request.user, 'create', 'User', user.id, user.email)
    
    def perform_update(self, serializer):
        old_data = serializer.instance
        user = serializer.save()
        changes = {'old': str(old_data), 'new': str(user)}
        log_audit(self.request.user, 'update', 'User', user.id, user.email, changes)
    
    def perform_destroy(self, instance):
        log_audit(self.request.user, 'delete', 'User', instance.id, instance.email)
        instance.delete()
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = UserListSerializer(request.user)
        return Response(serializer.data)

# ==================== AUTHENTIFICATION ====================

@api_view(['POST'])
@permission_classes([AllowAny])
def create_superadmin(request):
    serializer = UserCreateSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save(is_superuser=True, is_staff=True, is_active=True)
        
        code = generate_otp()
        expires_at = timezone.now() + timezone.timedelta(minutes=10)
        OTPCode.objects.create(user=user, code=code, type='email', expires_at=expires_at)
        send_otp_email(user.email, code)
        
        log_audit(user, 'create', 'SuperAdmin', user.id, user.email)
        
        return Response({
            'success': True,
            'message': 'Compte créé avec succès',
            'email': user.email
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_superadmin(request):
    serializer = SuperAdminLoginSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        user = authenticate(username=email, password=password)
        
        if user and (user.is_superuser or user.is_active):
            code = generate_otp()
            expires_at = timezone.now() + timezone.timedelta(minutes=10)
            OTPCode.objects.filter(user=user, is_used=False).delete()
            OTPCode.objects.create(user=user, code=code, type='email', expires_at=expires_at)
            send_otp_email(user.email, code)
            
            LoginHistory.objects.create(
                user=user,
                ip_address=request.META.get('REMOTE_ADDR'),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                success=True
            )
            log_audit(user, 'login', 'Auth', user.id, user.email)
            
            return Response({
                'success': True,
                'message': 'Code de vérification envoyé',
                'email': user.email,
                'requires_2fa': True
            })
        return Response({'success': False, 'error': 'Email ou mot de passe incorrect'}, status=status.HTTP_401_UNAUTHORIZED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def verify_2fa(request):
    serializer = OTPVerifySerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        code = serializer.validated_data['code']
        
        try:
            user = SuperAdmin.objects.get(email=email)
            otp = OTPCode.objects.filter(user=user, code=code, is_used=False).latest('created_at')
            
            if otp.is_valid():
                otp.is_used = True
                otp.save()
                user.is_active = True
                user.save()
                
                refresh = RefreshToken.for_user(user)
                return Response({
                    'success': True,
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                    'user': {
                        'id': user.id,
                        'email': user.email,
                        'nom': user.nom,
                        'telephone': user.telephone,
                        'is_superuser': user.is_superuser
                    }
                })
            return Response({'success': False, 'error': 'Code invalide ou expiré'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({'success': False, 'error': 'Code invalide'}, status=status.HTTP_401_UNAUTHORIZED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_superadmin(request):
    try:
        refresh_token = request.data.get('refresh')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        log_audit(request.user, 'logout', 'Auth', request.user.id, request.user.email)
        return Response({'success': True, 'message': 'Déconnecté'})
    except Exception as e:
        return Response({'success': False, 'error': str(e)})

# ==================== GESTION DES DONNÉES ====================

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def manage_herbier_data(request):
    data_obj = HerbierData.get_current_data()
    user = request.user
    
    if request.method == 'GET':
        data = {
            'plantes': [p for p in data_obj.plantes if p.get('created_by') == user.id or user.is_superuser],
            'equipe': data_obj.equipe if user.is_superuser else [],
            'partenaires': data_obj.partenaires if user.is_superuser else [],
            'slides': data_obj.slides if user.is_superuser else [],
            'projets': [p for p in data_obj.projets if p.get('created_by') == user.id or user.is_superuser],
            'activites': [a for a in data_obj.activites if a.get('created_by') == user.id or user.is_superuser],
            'temoignages': data_obj.temoignages if user.is_superuser else [],
            'publications': data_obj.publications if user.is_superuser else [],
            'faqs': data_obj.faqs if user.is_superuser else [],
            'statistiques': data_obj.statistiques if user.is_superuser else [],
            'methodologie': data_obj.methodologie if user.is_superuser else [],
        }
        return Response(data)
    
    elif request.method == 'PUT':
        if not user.is_superuser:
            for field in ['plantes', 'projets', 'activites']:
                if field in request.data:
                    existing = getattr(data_obj, field)
                    updated = request.data[field]
                    for item in updated:
                        if item.get('id') not in [e.get('id') for e in existing]:
                            item['created_by'] = user.id
                    setattr(data_obj, field, updated)
        else:
            for field in ['plantes', 'equipe', 'partenaires', 'slides', 'projets', 
                          'activites', 'temoignages', 'publications', 'faqs', 
                          'statistiques', 'methodologie']:
                if field in request.data:
                    setattr(data_obj, field, request.data[field])
        
        data_obj.updated_by = user
        data_obj.save()
        
        log_audit(user, 'update', 'HerbierData', 1, 'Données herbier')
        
        return Response({'success': True, 'message': 'Données mises à jour'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_audit_logs(request):
    if not request.user.is_superuser:
        return Response({'error': 'Accès non autorisé'}, status=status.HTTP_403_FORBIDDEN)
    logs = AuditLog.objects.all()[:100]
    serializer = AuditLogSerializer(logs, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_login_history(request):
    history = LoginHistory.objects.filter(user=request.user)[:50]
    serializer = LoginHistorySerializer(history, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    user = request.user
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')
    
    if not user.check_password(old_password):
        return Response({'error': 'Ancien mot de passe incorrect'}, status=status.HTTP_400_BAD_REQUEST)
    
    user.set_password(new_password)
    user.save()
    log_audit(user, 'update', 'Password', user.id, user.email)
    return Response({'success': True, 'message': 'Mot de passe changé'})
