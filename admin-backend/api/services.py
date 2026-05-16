import requests
from django.conf import settings
from .models import APICache, APISyncLog

# Configuration des URLs des APIs
PUBLIC_API_URL = "https://herbier-universite-man.onrender.com/api"
# Pour le développement local
if settings.DEBUG:
    PUBLIC_API_URL = "http://localhost:8000/api"

class APIService:
    """Service de communication avec l'API publique"""
    
    @staticmethod
    def get(endpoint, use_cache=True):
        """Récupérer des données depuis l'API publique"""
        cache_key = f"{endpoint}"
        
        # Vérifier le cache
        if use_cache:
            try:
                cache = APICache.objects.get(endpoint=cache_key)
                # Cache valide pour 5 minutes
                if cache.last_update > timezone.now() - timedelta(minutes=5):
                    return cache.data
            except APICache.DoesNotExist:
                pass
        
        # Appel API
        try:
            url = f"{PUBLIC_API_URL}/{endpoint}"
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            # Mettre en cache
            if use_cache:
                APICache.objects.update_or_create(
                    endpoint=cache_key,
                    defaults={'data': data}
                )
            
            return data
        except Exception as e:
            APISyncLog.objects.create(
                action=f"GET {endpoint}",
                status="ERROR",
                message=str(e)
            )
            return None
    
    @staticmethod
    def post(endpoint, data):
        """Envoyer des données à l'API publique"""
        try:
            url = f"{PUBLIC_API_URL}/{endpoint}"
            response = requests.post(url, json=data, timeout=30)
            response.raise_for_status()
            
            APISyncLog.objects.create(
                action=f"POST {endpoint}",
                status="SUCCESS",
                message="Données synchronisées"
            )
            return response.json()
        except Exception as e:
            APISyncLog.objects.create(
                action=f"POST {endpoint}",
                status="ERROR",
                message=str(e)
            )
            return None
    
    @staticmethod
    def put(endpoint, data, id=None):
        """Mettre à jour des données sur l'API publique"""
        url_endpoint = f"{endpoint}/{id}" if id else endpoint
        try:
            url = f"{PUBLIC_API_URL}/{url_endpoint}"
            response = requests.put(url, json=data, timeout=30)
            response.raise_for_status()
            
            APISyncLog.objects.create(
                action=f"PUT {url_endpoint}",
                status="SUCCESS",
                message="Données mises à jour"
            )
            return response.json()
        except Exception as e:
            APISyncLog.objects.create(
                action=f"PUT {url_endpoint}",
                status="ERROR",
                message=str(e)
            )
            return None
    
    @staticmethod
    def delete(endpoint, id):
        """Supprimer des données sur l'API publique"""
        try:
            url = f"{PUBLIC_API_URL}/{endpoint}/{id}"
            response = requests.delete(url, timeout=30)
            response.raise_for_status()
            
            APISyncLog.objects.create(
                action=f"DELETE {endpoint}/{id}",
                status="SUCCESS",
                message="Données supprimées"
            )
            return True
        except Exception as e:
            APISyncLog.objects.create(
                action=f"DELETE {endpoint}/{id}",
                status="ERROR",
                message=str(e)
            )
            return False

# Import pour les timedelta
from django.utils import timezone
from datetime import timedelta
