from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import JsonResponse
import json

@csrf_exempt
@require_POST
def create_superadmin(request):
    """Créer un nouveau super administrateur"""
    from .serializers import SuperAdminCreateSerializer
    from .models import OTPCode
    import random
    import string
    from django.utils import timezone
    
    if request.content_type == 'application/json':
        data = json.loads(request.body.decode('utf-8') or '{}')
    else:
        data = request.POST
    
    serializer = SuperAdminCreateSerializer(data=data)
    if serializer.is_valid():
        try:
            user = serializer.save()
            
            # Générer le code OTP
            code = ''.join(random.choices(string.digits, k=6))
            expires_at = timezone.now() + timezone.timedelta(minutes=10)
            
            OTPCode.objects.create(
                user=user,
                code=code,
                type='sms',
                expires_at=expires_at
            )
            
            # Envoyer le code par SMS
            send_sms(user.telephone, code)
            
            return JsonResponse({
                'success': True,
                'message': 'Compte créé avec succès. Un code de vérification a été envoyé par SMS.',
                'telephone': user.telephone
            }, status=201)
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'errors': {'general': str(e)}
            }, status=400)
    
    return JsonResponse({
        'success': False,
        'errors': serializer.errors
    }, status=400)
