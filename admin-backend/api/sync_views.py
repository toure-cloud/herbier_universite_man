from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import requests
from django.conf import settings

PUBLIC_API_URL = getattr(settings, 'PUBLIC_API_URL', 'http://localhost:8000')

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def sync_all_to_public(request):
    """Synchroniser toutes les données vers l'API publique"""
    data = request.data
    
    endpoints = {
        'plantes': '/api/plantes/',
        'equipe': '/api/equipe/',
        'projets': '/api/projets/',
        'slides': '/api/slides/',
        'activites': '/api/activites/'
    }
    
    results = {}
    
    for key, endpoint in endpoints.items():
        if key in data:
            try:
                # Pour chaque élément, faire un POST ou PUT
                for item in data[key]:
                    item_id = item.get('id')
                    if item_id:
                        # Vérifier si existe déjà
                        check = requests.get(f"{PUBLIC_API_URL}{endpoint}{item_id}/")
                        if check.status_code == 200:
                            requests.put(f"{PUBLIC_API_URL}{endpoint}{item_id}/", json=item)
                        else:
                            requests.post(f"{PUBLIC_API_URL}{endpoint}", json=item)
                    else:
                        requests.post(f"{PUBLIC_API_URL}{endpoint}", json=item)
                results[key] = "success"
            except Exception as e:
                results[key] = f"error: {str(e)}"
    
    return Response({'status': 'ok', 'results': results})
