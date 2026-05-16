from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.utils import timezone
from .models import SuperAdmin, OTPCode, APICache, APISyncLog
from .serializers import (
    SuperAdminCreateSerializer, SuperAdminLoginSerializer,
    OTPVerifySerializer, SuperAdminSerializer
)
import random
import string

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
@permission_classes([AllowAny])
def create_superadmin(request):
    """Créer un nouveau super administrateur"""
    serializer = SuperAdminCreateSerializer(data=request.data)
    
    if serializer.is_valid():
        try:
            user = serializer.save()
            
            # Générer le code OTP
            code = generate_otp()
            expires_at = timezone.now() + timezone.timedelta(minutes=10)
            
            OTPCode.objects.create(
                user=user,
                code=code,
                type='email',
                expires_at=expires_at
            )
            
            # Envoyer le code par email
            email_sent = send_otp_email(user.email, code)
            
            return Response({
                'success': True,
                'message': 'Compte créé avec succès. Un code de vérification a été envoyé à votre email.',
                'email': user.email,
                'code_envoye': email_sent,
                'test_code': code if not email_sent else None  # Pour le développement
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
@permission_classes([AllowAny])
def login_superadmin(request):
    """Connexion - première étape"""
    serializer = SuperAdminLoginSerializer(data=request.data)
    
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        
        user = authenticate_manual(username=email, password=password)
        
        if user and user.is_superuser:
            # Générer un nouveau code OTP
            code = generate_otp()
            expires_at = timezone.now() + timezone.timedelta(minutes=10)
            
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
    
    return Response({
        'success': False,
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def verify_2fa(request):
    """Vérification du code OTP"""
    serializer = OTPVerifySerializer(data=request.data)
    
    if serializer.is_valid():
        email = serializer.validated_data['email']
        code = serializer.validated_data['code']
        
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
                    'user': SuperAdminSerializer(user).data
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
    
    return Response({
        'success': False,
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
def get_current_user(request):
    """Récupérer l'utilisateur connecté"""
    serializer = SuperAdminSerializer(request.user)
    return Response(serializer.data)

@api_view(['GET'])
def api_root(request):
    return Response({
        'message': 'API Admin Herbier Universite de Man',
        'version': '1.0.0',
        'endpoints': {
            'create-superadmin': '/api/create-superadmin/',
            'login': '/api/login/',
            'verify-2fa': '/api/verify-2fa/',
            'me': '/api/me/'
        }
    })
