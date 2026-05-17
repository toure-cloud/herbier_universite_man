from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse

@api_view(['GET'])
def api_root(request):
    return Response({
        'status': 'ok',
        'message': 'Admin API Herbier Universite de Man',
        'version': '1.0.0',
        'endpoints': {
            'admin': '/admin/',
            'api_root': '/api/',
            'health': '/api/health/',
            'create_superadmin': '/api/create-superadmin/',
            'login': '/api/login/',
            'verify_2fa': '/api/verify-2fa/'
        }
    })

@api_view(['GET'])
def health_check(request):
    return Response({'status': 'healthy', 'port': 10000})
