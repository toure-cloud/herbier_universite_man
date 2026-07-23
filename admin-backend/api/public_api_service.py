import requests
from django.conf import settings
import json
from .models import APICache, APISyncLog

class PublicAPIService:
    """Service de communication avec l'API publique"""
    
    def __init__(self):
        # URL de base du backend public
        self.base_url = getattr(settings, 'PUBLIC_API_URL', 'http://localhost:8000/api')
        self.timeout = 30
    
    def _make_request(self, method, endpoint, data=None, headers=None):
        """Effectuer une requête vers l'API publique"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        default_headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        if headers:
            default_headers.update(headers)
        
        try:
            if method.upper() == 'GET':
                response = requests.get(url, headers=default_headers, timeout=self.timeout)
            elif method.upper() == 'POST':
                response = requests.post(url, json=data, headers=default_headers, timeout=self.timeout)
            elif method.upper() == 'PUT':
                response = requests.put(url, json=data, headers=default_headers, timeout=self.timeout)
            elif method.upper() == 'DELETE':
                response = requests.delete(url, headers=default_headers, timeout=self.timeout)
            else:
                return None
            
            response.raise_for_status()
            return response.json() if response.content else None
            
        except requests.exceptions.RequestException as e:
            # Enregistrer l'erreur dans les logs
            APISyncLog.objects.create(
                action=f"{method} {endpoint}",
                status="ERROR",
                message=str(e)
            )
            return None
    
    # ==================== MÉTHODES POUR LES PLANTES ====================
    def get_plantes(self, filters=None):
        """Récupérer toutes les plantes"""
        endpoint = "plantes/"
        if filters:
            endpoint += "?" + "&".join([f"{k}={v}" for k, v in filters.items()])
        return self._make_request('GET', endpoint)
    
    def get_plante(self, plante_id):
        """Récupérer une plante par ID"""
        return self._make_request('GET', f"plantes/{plante_id}/")
    
    def create_plante(self, data):
        """Créer une nouvelle plante"""
        return self._make_request('POST', "plantes/", data)
    
    def update_plante(self, plante_id, data):
        """Mettre à jour une plante"""
        return self._make_request('PUT', f"plantes/{plante_id}/", data)
    
    def delete_plante(self, plante_id):
        """Supprimer une plante"""
        return self._make_request('DELETE', f"plantes/{plante_id}/")
    
    # ==================== MÉTHODES POUR L'ÉQUIPE ====================
    def get_equipe(self):
        """Récupérer tous les membres de l'équipe"""
        return self._make_request('GET', "equipe/")
    
    def create_equipe(self, data):
        """Créer un membre de l'équipe"""
        return self._make_request('POST', "equipe/", data)
    
    def update_equipe(self, membre_id, data):
        """Mettre à jour un membre de l'équipe"""
        return self._make_request('PUT', f"equipe/{membre_id}/", data)
    
    def delete_equipe(self, membre_id):
        """Supprimer un membre de l'équipe"""
        return self._make_request('DELETE', f"equipe/{membre_id}/")
    
    # ==================== MÉTHODES POUR LES SLIDES ====================
    def get_slides(self):
        """Récupérer tous les slides"""
        return self._make_request('GET', "slides/")
    
    def create_slide(self, data):
        """Créer un slide"""
        return self._make_request('POST', "slides/", data)
    
    def update_slide(self, slide_id, data):
        """Mettre à jour un slide"""
        return self._make_request('PUT', f"slides/{slide_id}/", data)
    
    def delete_slide(self, slide_id):
        """Supprimer un slide"""
        return self._make_request('DELETE', f"slides/{slide_id}/")
    
    # ==================== MÉTHODES POUR LES PROJETS ====================
    def get_projets(self):
        """Récupérer tous les projets"""
        return self._make_request('GET', "projets/")
    
    def create_projet(self, data):
        """Créer un projet"""
        return self._make_request('POST', "projets/", data)
    
    def update_projet(self, projet_id, data):
        """Mettre à jour un projet"""
        return self._make_request('PUT', f"projets/{projet_id}/", data)
    
    def delete_projet(self, projet_id):
        """Supprimer un projet"""
        return self._make_request('DELETE', f"projets/{projet_id}/")
    
    # ==================== MÉTHODES POUR LES ACTIVITÉS ====================
    def get_activites(self):
        """Récupérer toutes les activités"""
        return self._make_request('GET', "activites/")
    
    def create_activite(self, data):
        """Créer une activité"""
        return self._make_request('POST', "activites/", data)
    
    def update_activite(self, activite_id, data):
        """Mettre à jour une activité"""
        return self._make_request('PUT', f"activites/{activite_id}/", data)
    
    def delete_activite(self, activite_id):
        """Supprimer une activité"""
        return self._make_request('DELETE', f"activites/{activite_id}/")
    
    # ==================== MÉTHODES POUR LES TÉMOIGNAGES ====================
    def get_temoignages(self):
        """Récupérer tous les témoignages"""
        return self._make_request('GET', "temoignages/")
    
    def create_temoignage(self, data):
        """Créer un témoignage"""
        return self._make_request('POST', "temoignages/", data)
    
    def update_temoignage(self, temoignage_id, data):
        """Mettre à jour un témoignage"""
        return self._make_request('PUT', f"temoignages/{temoignage_id}/", data)
    
    def delete_temoignage(self, temoignage_id):
        """Supprimer un témoignage"""
        return self._make_request('DELETE', f"temoignages/{temoignage_id}/")
    
    # ==================== MÉTHODES POUR LES PUBLICATIONS ====================
    def get_publications(self):
        """Récupérer toutes les publications"""
        return self._make_request('GET', "publications/")
    
    def create_publication(self, data):
        """Créer une publication"""
        return self._make_request('POST', "publications/", data)
    
    def update_publication(self, publication_id, data):
        """Mettre à jour une publication"""
        return self._make_request('PUT', f"publications/{publication_id}/", data)
    
    def delete_publication(self, publication_id):
        """Supprimer une publication"""
        return self._make_request('DELETE', f"publications/{publication_id}/")
    
    # ==================== MÉTHODES POUR LES STATISTIQUES ====================
    def get_dashboard_stats(self):
        """Récupérer les statistiques du dashboard"""
        return self._make_request('GET', "dashboard/")
    
    def get_herbier_stats(self):
        """Récupérer les statistiques de l'herbier"""
        return self._make_request('GET', "herbier-stats/")
    
    # ==================== SYNCHRONISATION ====================
    def sync_all_data(self):
        """Synchroniser toutes les données de l'API publique"""
        results = {}
        
        endpoints = {
            'plantes': self.get_plantes,
            'equipe': self.get_equipe,
            'slides': self.get_slides,
            'projets': self.get_projets,
            'activites': self.get_activites,
            'temoignages': self.get_temoignages,
            'publications': self.get_publications,
        }
        
        for name, method in endpoints.items():
            try:
                data = method()
                if data is not None:
                    results[name] = {'status': 'success', 'count': len(data) if isinstance(data, list) else 1}
                    # Mettre en cache
                    APICache.objects.update_or_create(
                        endpoint=name,
                        defaults={'data': data}
                    )
                else:
                    results[name] = {'status': 'error', 'message': 'Failed to fetch'}
            except Exception as e:
                results[name] = {'status': 'error', 'message': str(e)}
        
        # Enregistrer la synchronisation
        APISyncLog.objects.create(
            action="SYNC_ALL",
            status="SUCCESS",
            message=f"Synchronized {len(results)} endpoints"
        )
        
        return results

# Instance singleton
public_api = PublicAPIService()
