@csrf_exempt
@api_view(['POST'])
def create_superadmin(request):
    """Créer un nouveau super administrateur"""
    from .serializers import SuperAdminCreateSerializer
    from .models import OTPCode
    import random
    import string
    from django.utils import timezone
    
    serializer = SuperAdminCreateSerializer(data=request.data)
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
            
            return Response({
                'success': True,
                'message': 'Compte créé avec succès. Un code de vérification a été envoyé par SMS.',
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
