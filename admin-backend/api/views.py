from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, viewsets
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import random
import string


def send_sms(phone_number, code):
    """Envoyer le code OTP par SMS - Affichage console pour les tests"""
    print("\n" + "="*60)
    print("📱 CODE OTP SMS - CONSOLE DE TEST")
    print("="*60)
    print(f"📨 Numéro de téléphone: {phone_number}")
    print(f"🔑 CODE OTP: {code}")
    print("="*60)
    print("⚠️  Utilisez ce code pour la vérification 2FA")
    print("="*60 + "\n")
    return True

# Pour les tests, on peut aussi ajouter une version email
def send_email_otp(email, code):
    """Envoyer le code OTP par email - Affichage console pour les tests"""
    print("\n" + "="*60)
    print("📧 CODE OTP EMAIL - CONSOLE DE TEST")
    print("="*60)
    print(f"📨 Email: {email}")
    print(f"🔑 CODE OTP: {code}")
    print("="*60)
    print("⚠️  Utilisez ce code pour la vérification 2FA")
    print("="*60 + "\n")
    return True


# Importer la fonction SMS
try:
    from .sms_utils import send_sms, send_sms_development
except ImportError:
    # Fallback si sms_utils n'existe pas
    def send_sms(phone, code):
        print(f"📱 SMS (DEV) - {phone}: {code}")
        return True

@api_view(['GET'])
def api_root(request):
    return Response({'status': 'ok', 'message': 'API Admin Herbier'})


@api_view(['GET'])
def health_check(request):
    return Response({'status': 'healthy'})


@csrf_exempt
@api_view(['POST'])
def login_superadmin(request):
    from .models import SuperAdmin, OTPCode
    
    email = request.data.get('email')
    password = request.data.get('password')
    
    try:
        user = SuperAdmin.objects.get(email=email)
        if user.check_password(password):
            code = ''.join(random.choices(string.digits, k=6))
            expires_at = timezone.now() + timezone.timedelta(minutes=10)
            
            # Supprimer les anciens codes
            OTPCode.objects.filter(user=user, is_used=False).delete()
            
            # Créer le nouveau code
            OTPCode.objects.create(
                user=user,
                code=code,
                type='sms',
                expires_at=expires_at
            )
            
            # Envoyer le code par SMS
            send_sms(user.telephone, code)
            
            return Response({
                'success': True,
                'message': 'Code de vérification envoyé par SMS',
                'telephone': user.telephone,
                'requires_2fa': True
            })
        else:
            return Response({
                'success': False,
                'error': 'Identifiants incorrects'
            }, status=401)
    except SuperAdmin.DoesNotExist:
        return Response({
            'success': False,
            'error': 'Identifiants incorrects'
        }, status=401)


@csrf_exempt
@api_view(['POST'])
def create_superadmin(request):
    """Créer un nouveau super administrateur avec vérification d'unicité"""
    from .serializers import SuperAdminCreateSerializer
    
    # Vérifier si l'email existe déjà
    email = request.data.get('email')
    telephone = request.data.get('telephone')
    
    # Nettoyer le téléphone
    if telephone:
        telephone = re.sub(r'\D', '', telephone)
    
    errors = {}
    
    # Vérification email
    if email and SuperAdmin.objects.filter(email=email).exists():
        errors['email'] = 'Cet email est déjà utilisé. Veuillez en utiliser un autre.'
    
    # Vérification téléphone
    if telephone and SuperAdmin.objects.filter(telephone=telephone).exists():
        errors['telephone'] = 'Ce numéro de téléphone est déjà utilisé. Veuillez en utiliser un autre.'
    
    if errors:
        return Response({
            'success': False,
            'errors': errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
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
            
            # Afficher le code dans la console pour les tests
            print("\n" + "="*60)
            print("📧 CODE OTP - INSCRIPTION")
            print("="*60)
            print(f"📨 Email: {user.email}")
            print(f"📞 Téléphone: {user.telephone}")
            print(f"🔑 CODE OTP: {code}")
            print("="*60)
            print("⚠️  Utilisez ce code pour la vérification 2FA")
            print("="*60 + "\n")
            
            return Response({
                'success': True,
                'message': 'Compte créé avec succès. Un code de vérification a été envoyé.',
                'email': user.email,
                'telephone': user.telephone
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


@csrf_exempt
@api_view(['POST'])
def resend_code(request):
    """Renvoyer le code OTP par SMS"""
    from .models import SuperAdmin, OTPCode
    
    telephone = request.data.get('telephone')
    
    if not telephone:
        return Response({
            'success': False,
            'error': 'Numéro de téléphone requis'
        }, status=400)
    
    # Nettoyer le numéro
    telephone = ''.join(filter(str.isdigit, telephone))
    
    try:
        user = SuperAdmin.objects.get(telephone=telephone)
        
        # Générer un nouveau code
        code = ''.join(random.choices(string.digits, k=6))
        expires_at = timezone.now() + timezone.timedelta(minutes=10)
        
        # Supprimer les anciens codes non utilisés
        OTPCode.objects.filter(user=user, is_used=False).delete()
        
        # Créer le nouveau code
        OTPCode.objects.create(
            user=user,
            code=code,
            type='sms',
            expires_at=expires_at
        )
        
        # Envoyer le code par SMS
        send_sms(user.telephone, code)
        
        return Response({
            'success': True,
            'message': 'Un nouveau code a été envoyé par SMS'
        })
        
    except SuperAdmin.DoesNotExist:
        return Response({
            'success': False,
            'error': 'Aucun compte trouvé avec ce numéro'
        }, status=404)
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=400)


@csrf_exempt
@api_view(['POST'])
def verify_2fa(request):
    from .models import SuperAdmin, OTPCode
    import hashlib
    from django.utils import timezone
    
    telephone = request.data.get('telephone')
    code = request.data.get('code')
    
    # Nettoyer le numéro de téléphone (enlever les espaces, tirets, etc.)
    if telephone:
        telephone = ''.join(filter(str.isdigit, telephone))
    
    if not telephone or not code:
        return Response({
            'success': False,
            'error': 'Téléphone et code requis'
        }, status=400)
    
    try:
        # Chercher l'utilisateur par téléphone
        user = SuperAdmin.objects.get(telephone=telephone)
        
        # Chercher le code OTP non utilisé
        otp = OTPCode.objects.filter(
            user=user, 
            code=code, 
            is_used=False
        ).first()
        
        if otp and otp.is_valid():
            # Marquer le code comme utilisé
            otp.is_used = True
            otp.save()
            
            # Activer le compte
            user.is_active = True
            user.save()
            
            # Générer un token simple
            token = hashlib.md5(f"{user.email}:{timezone.now()}".encode()).hexdigest()
            
            return Response({
                'success': True,
                'access': token,
                'refresh': token,
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
            }, status=401)
            
    except SuperAdmin.DoesNotExist:
        return Response({
            'success': False,
            'error': 'Aucun compte trouvé avec ce numéro de téléphone'
        }, status=404)
    except Exception as e:
        return Response({
            'success': False,
            'error': f'Erreur: {str(e)}'
        }, status=400)


@api_view(['POST'])
def logout_superadmin(request):
    return Response({'success': True})


@api_view(['GET'])
def get_current_user(request):
    return Response({'error': 'Non authentifié'}, status=401)


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
def dashboard_stats(request):
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
    return Response({'status': 'success'})


@api_view(['GET'])
def sync_endpoint(request, endpoint): 
    return Response({'status': 'success'})


@api_view(['GET'])
def get_sync_logs(request): 
    return Response([])

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
