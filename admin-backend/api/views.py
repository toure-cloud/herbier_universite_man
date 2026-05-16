from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import SuperAdmin, APICache, APISyncLog
from .serializers import SuperAdminSerializer
from .services import APIService
import requests

class SuperAdminViewSet(viewsets.ModelViewSet):
    queryset = SuperAdmin.objects.all()
    serializer_class = SuperAdminSerializer

@api_view(['GET'])
def sync_all_data(request):
    """Synchroniser toutes les données depuis l'API publique"""
    endpoints = ['plantes', 'equipe', 'partenaires', 'slides', 'projets', 'activites', 'temoignages', 'publications', 'faqs', 'statistiques']
    
    results = {}
    for endpoint in endpoints:
        data = APIService.get(endpoint, use_cache=False)
        results[endpoint] = "OK" if data else "ERROR"
    
    return Response({
        'status': 'success',
        'synced': results,
        'message': 'Synchronisation terminée'
    })

@api_view(['GET'])
def sync_endpoint(request, endpoint):
    """Synchroniser un endpoint spécifique"""
    data = APIService.get(endpoint, use_cache=False)
    if data:
        return Response({'status': 'success', 'data': data})
    return Response({'status': 'error', 'message': 'Erreur de synchronisation'}, status=400)

@api_view(['POST'])
def push_to_public_api(request, endpoint):
    """Pousser des données vers l'API publique"""
    data = request.data
    result = APIService.post(endpoint, data)
    if result:
        return Response({'status': 'success', 'data': result})
    return Response({'status': 'error', 'message': 'Erreur lors de l\'envoi'}, status=400)

@api_view(['GET'])
def get_sync_logs(request):
    """Récupérer les logs de synchronisation"""
    logs = APISyncLog.objects.all().order_by('-created_at')[:50]
    return Response([
        {
            'action': log.action,
            'status': log.status,
            'message': log.message,
            'created_at': log.created_at.isoformat()
        }
        for log in logs
    ])

@api_view(['GET'])
def get_stats(request):
    """Récupérer les statistiques depuis l'API publique"""
    stats = APIService.get('dashboard/')
    if stats:
        return Response(stats)
    return Response({'error': 'Impossible de récupérer les stats'}, status=400)

# Dashboard admin
@api_view(['GET'])
def admin_dashboard(request):
    """Tableau de bord admin avec statistiques"""
    # Données depuis l'API publique
    plantes = APIService.get('plantes')
    equipe = APIService.get('equipe')
    projets = APIService.get('projets')
    slides = APIService.get('slides')
    
    # Statistiques
    stats = {
        'total_plantes': len(plantes) if plantes else 0,
        'total_equipe': len(equipe) if equipe else 0,
        'total_projets': len(projets) if projets else 0,
        'total_slides': len(slides) if slides else 0,
        'sync_logs': APISyncLog.objects.count(),
        'last_sync': APISyncLog.objects.filter(status='SUCCESS').first().created_at if APISyncLog.objects.exists() else None
    }
    
    return Response(stats)
