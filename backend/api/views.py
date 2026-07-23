import requests
from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from django.db.models import Q, Count
from django.http import HttpResponse
import time
from .models import (
    Plante, Equipe, Partenaire, Slide, Projet, ProjetTimeline,
    Activite, Temoignage, Publication, FAQ, ContactMessage,
    Statistique, Methodologie, FamilleBotanique, GenreBotanique, HerbierStats
)
from .serializers import (
    PlanteSerializer, EquipeSerializer, PartenaireSerializer,
    SlideSerializer, ProjetSerializer, ProjetTimelineSerializer,
    ActiviteSerializer, TemoignageSerializer, PublicationSerializer,
    FAQSerializer, ContactMessageSerializer, StatistiqueSerializer,
    MethodologieSerializer, FamilleBotaniqueSerializer, GenreBotaniqueSerializer
)

# ✅ URL de l'admin-backend
ADMIN_API_URL = getattr(settings, 'ADMIN_API_URL', 'http://localhost:8001/api')


# ========================================================
# ✅ FONCTION PROXY AVEC RETRY ET FALLBACK
# ========================================================
def proxy_to_admin_backend(request, endpoint, item_id=None):
    """Proxy a read-only endpoint from the admin backend to the public API."""
    base_url = f"{ADMIN_API_URL.rstrip('/')}/{endpoint.lstrip('/')}"
    url = f"{base_url}/{item_id}/" if item_id is not None else base_url

    # Gérer les paramètres dans l'endpoint
    if '?' in endpoint:
        parts = endpoint.split('?')
        endpoint_path = parts[0]
        endpoint_params = parts[1] if len(parts) > 1 else ''
        url = f"{ADMIN_API_URL.rstrip('/')}/{endpoint_path.lstrip('/')}"
        if item_id is not None:
            url = f"{url}/{item_id}/"
        if endpoint_params:
            url = f"{url}?{endpoint_params}"

    try:
        query_params = getattr(request, 'query_params', request.GET)
        print(f"🔍 Proxy vers: {url}")
        
        # ✅ Essayer avec timeout plus long (30 secondes)
        response = requests.get(url, params=query_params, timeout=30)
        response.raise_for_status()
        payload = response.json() if response.content else []
        return Response(payload, status=response.status_code)
        
    except requests.exceptions.Timeout:
        print(f"⏰ Timeout vers {url} - utilisation du fallback local")
        return get_local_fallback(endpoint, request)
        
    except requests.exceptions.ConnectionError:
        print(f"🔌 Erreur de connexion vers {url} - utilisation du fallback local")
        return get_local_fallback(endpoint, request)
        
    except requests.RequestException as e:
        print(f"❌ Erreur proxy vers {url}: {str(e)}")
        return get_local_fallback(endpoint, request)


# ========================================================
# ✅ FONCTION DE FALLBACK LOCAL
# ========================================================
def get_local_fallback(endpoint, request):
    """Retourne les données locales en cas d'échec du proxy"""
    
    # Mapping des endpoints vers les modèles locaux
    fallbacks = {
        'plantes': Plante.objects.filter(actif=True),
        'equipe': Equipe.objects.filter(actif=True),
        'partenaires': Partenaire.objects.filter(actif=True),
        'slides': Slide.objects.filter(actif=True),
        'projets': Projet.objects.all(),
        'activites': Activite.objects.filter(actif=True),
        'temoignages': Temoignage.objects.filter(actif=True),
        'publications': Publication.objects.filter(actif=True),
        'faqs': FAQ.objects.filter(actif=True),
        'statistiques': Statistique.objects.filter(actif=True),
        'methodologie': Methodologie.objects.filter(actif=True),
    }
    
    # Mapping des serializers
    serializers_map = {
        'plantes': PlanteSerializer,
        'equipe': EquipeSerializer,
        'partenaires': PartenaireSerializer,
        'slides': SlideSerializer,
        'projets': ProjetSerializer,
        'activites': ActiviteSerializer,
        'temoignages': TemoignageSerializer,
        'publications': PublicationSerializer,
        'faqs': FAQSerializer,
        'statistiques': StatistiqueSerializer,
        'methodologie': MethodologieSerializer,
    }
    
    # Extraire le nom de l'endpoint sans paramètres
    endpoint_name = endpoint.split('?')[0].split('/')[0]
    
    if endpoint_name in fallbacks:
        queryset = fallbacks[endpoint_name]
        serializer_class = serializers_map.get(endpoint_name)
        if serializer_class:
            serializer = serializer_class(queryset, many=True, context={'request': request})
            return Response(serializer.data)
    
    # Fallback par défaut
    return Response([], status=200)


# ========================================================
# ✅ VIEWSETS POUR LE SITE PUBLIC
# ========================================================

class EquipeViewSet(viewsets.ModelViewSet):
    queryset = Equipe.objects.filter(actif=True)
    serializer_class = EquipeSerializer

    def list(self, request, *args, **kwargs):
        return proxy_to_admin_backend(request, 'equipe')

    def retrieve(self, request, *args, **kwargs):
        return proxy_to_admin_backend(request, 'equipe', item_id=kwargs.get('pk'))


class PartenaireViewSet(viewsets.ModelViewSet):
    queryset = Partenaire.objects.filter(actif=True)
    serializer_class = PartenaireSerializer

    def list(self, request, *args, **kwargs):
        """Récupère la liste des partenaires depuis l'admin-backend avec fallback local"""
        return proxy_to_admin_backend(request, 'partenaires')

    def retrieve(self, request, *args, **kwargs):
        """Récupère un partenaire spécifique depuis l'admin-backend"""
        return proxy_to_admin_backend(request, 'partenaires', item_id=kwargs.get('pk'))


class SlideViewSet(viewsets.ModelViewSet):
    queryset = Slide.objects.filter(actif=True)
    serializer_class = SlideSerializer

    def list(self, request, *args, **kwargs):
        return proxy_to_admin_backend(request, 'slides')

    def retrieve(self, request, *args, **kwargs):
        return proxy_to_admin_backend(request, 'slides', item_id=kwargs.get('pk'))


class ProjetViewSet(viewsets.ModelViewSet):
    queryset = Projet.objects.all()
    serializer_class = ProjetSerializer

    def list(self, request, *args, **kwargs):
        return proxy_to_admin_backend(request, 'projets')

    def retrieve(self, request, *args, **kwargs):
        return proxy_to_admin_backend(request, 'projets', item_id=kwargs.get('pk'))
    
    @action(detail=False, methods=['get'])
    def by_categorie(self, request):
        categorie = request.query_params.get('categorie', '')
        if categorie:
            return proxy_to_admin_backend(request, f'projets?categorie={categorie}')
        return Response([])
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        return proxy_to_admin_backend(request, 'projets?featured=true')


class ProjetTimelineViewSet(viewsets.ModelViewSet):
    queryset = ProjetTimeline.objects.all()
    serializer_class = ProjetTimelineSerializer


class ActiviteViewSet(viewsets.ModelViewSet):
    queryset = Activite.objects.filter(actif=True)
    serializer_class = ActiviteSerializer

    def list(self, request, *args, **kwargs):
        return proxy_to_admin_backend(request, 'activites')

    def retrieve(self, request, *args, **kwargs):
        return proxy_to_admin_backend(request, 'activites', item_id=kwargs.get('pk'))


class TemoignageViewSet(viewsets.ModelViewSet):
    queryset = Temoignage.objects.filter(actif=True)
    serializer_class = TemoignageSerializer

    def list(self, request, *args, **kwargs):
        return proxy_to_admin_backend(request, 'temoignages')

    def retrieve(self, request, *args, **kwargs):
        return proxy_to_admin_backend(request, 'temoignages', item_id=kwargs.get('pk'))


class PublicationViewSet(viewsets.ModelViewSet):
    queryset = Publication.objects.filter(actif=True)
    serializer_class = PublicationSerializer

    def list(self, request, *args, **kwargs):
        return proxy_to_admin_backend(request, 'publications')

    def retrieve(self, request, *args, **kwargs):
        return proxy_to_admin_backend(request, 'publications', item_id=kwargs.get('pk'))


class FAQViewSet(viewsets.ModelViewSet):
    queryset = FAQ.objects.filter(actif=True)
    serializer_class = FAQSerializer

    def list(self, request, *args, **kwargs):
        return proxy_to_admin_backend(request, 'faqs')

    def retrieve(self, request, *args, **kwargs):
        return proxy_to_admin_backend(request, 'faqs', item_id=kwargs.get('pk'))


class ContactMessageViewSet(viewsets.ModelViewSet):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    
    def create(self, request, *args, **kwargs):
        try:
            response = requests.post(
                f"{ADMIN_API_URL}/submit-contact/",
                json=request.data,
                timeout=10
            )
            if response.status_code == 201:
                return Response(response.json(), status=status.HTTP_201_CREATED)
        except requests.RequestException:
            pass
        
        # Fallback: sauvegarder localement
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {'message': 'Votre message a été envoyé avec succès !', 'success': True},
            status=status.HTTP_201_CREATED
        )


class StatistiqueViewSet(viewsets.ModelViewSet):
    queryset = Statistique.objects.filter(actif=True)
    serializer_class = StatistiqueSerializer

    def list(self, request, *args, **kwargs):
        return proxy_to_admin_backend(request, 'statistiques')

    def retrieve(self, request, *args, **kwargs):
        return proxy_to_admin_backend(request, 'statistiques', item_id=kwargs.get('pk'))


class MethodologieViewSet(viewsets.ModelViewSet):
    queryset = Methodologie.objects.filter(actif=True)
    serializer_class = MethodologieSerializer

    def list(self, request, *args, **kwargs):
        return proxy_to_admin_backend(request, 'methodologie')

    def retrieve(self, request, *args, **kwargs):
        return proxy_to_admin_backend(request, 'methodologie', item_id=kwargs.get('pk'))


# ========================================================
# ✅ VIEWSETS POUR L'HERBIER AVANCÉ
# ========================================================

class PlanteViewSet(viewsets.ModelViewSet):
    queryset = Plante.objects.filter(actif=True)
    serializer_class = PlanteSerializer

    def list(self, request, *args, **kwargs):
        return proxy_to_admin_backend(request, 'plantes')

    def retrieve(self, request, *args, **kwargs):
        return proxy_to_admin_backend(request, 'plantes', item_id=kwargs.get('pk'))
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('q', '')
        if query:
            return proxy_to_admin_backend(request, f'plantes/search?q={query}')
        return Response([])
    
    @action(detail=False, methods=['get'])
    def by_famille(self, request):
        famille_id = request.query_params.get('famille_id', '')
        if famille_id:
            return proxy_to_admin_backend(request, f'plantes/by_famille?famille_id={famille_id}')
        return Response([])
    
    @action(detail=False, methods=['get'])
    def by_genre(self, request):
        genre_id = request.query_params.get('genre_id', '')
        if genre_id:
            return proxy_to_admin_backend(request, f'plantes/by_genre?genre_id={genre_id}')
        return Response([])
    
    @action(detail=False, methods=['get'])
    def featured_plants(self, request):
        return proxy_to_admin_backend(request, 'plantes/featured_plants')
    
    @action(detail=False, methods=['get'])
    def recent_plants(self, request):
        limit = request.query_params.get('limit', 12)
        return proxy_to_admin_backend(request, f'plantes/recent_plants?limit={limit}')
    
    @action(detail=False, methods=['get'])
    def alphabet_index(self, request):
        return proxy_to_admin_backend(request, 'plantes/alphabet_index')


class FamilleBotaniqueViewSet(viewsets.ModelViewSet):
    queryset = FamilleBotanique.objects.all()
    serializer_class = FamilleBotaniqueSerializer


class GenreBotaniqueViewSet(viewsets.ModelViewSet):
    queryset = GenreBotanique.objects.all()
    serializer_class = GenreBotaniqueSerializer


# ========================================================
# ✅ FONCTIONS API
# ========================================================

@api_view(['GET'])
def dashboard_stats(request):
    """Récupère les statistiques depuis l'admin-backend avec fallback local"""
    try:
        response = requests.get(f"{ADMIN_API_URL}/dashboard/", timeout=5)
        if response.status_code == 200:
            return Response(response.json())
    except requests.RequestException:
        pass
    
    # Fallback local
    return Response({
        'total_plantes': Plante.objects.filter(actif=True).count(),
        'total_equipe': Equipe.objects.filter(actif=True).count(),
        'total_partenaires': Partenaire.objects.filter(actif=True).count(),
        'total_projets': Projet.objects.count(),
        'total_slides': Slide.objects.filter(actif=True).count(),
        'total_publications': Publication.objects.filter(actif=True).count(),
        'total_temoignages': Temoignage.objects.filter(actif=True).count(),
        'total_messages': ContactMessage.objects.filter(lu=False).count(),
    })


@api_view(['GET'])
def get_activites_data(request):
    """Récupère les données des activités depuis l'admin-backend"""
    try:
        response = requests.get(f"{ADMIN_API_URL}/activites-data/", timeout=5)
        if response.status_code == 200:
            return Response(response.json())
    except requests.RequestException:
        pass
    
    # Fallback local
    return Response({
        'activites': ActiviteSerializer(Activite.objects.filter(actif=True), many=True).data,
        'temoignages': TemoignageSerializer(Temoignage.objects.filter(actif=True), many=True).data,
        'publications': PublicationSerializer(Publication.objects.filter(actif=True)[:5], many=True).data,
        'statistiques': StatistiqueSerializer(Statistique.objects.filter(actif=True), many=True).data,
        'faqs': FAQSerializer(FAQ.objects.filter(actif=True), many=True).data,
        'methodologie': MethodologieSerializer(Methodologie.objects.filter(actif=True), many=True).data,
    })


@api_view(['GET'])
def get_projets_data(request):
    """Récupère les données des projets depuis l'admin-backend"""
    try:
        response = requests.get(f"{ADMIN_API_URL}/projets-data/", timeout=5)
        if response.status_code == 200:
            return Response(response.json())
    except requests.RequestException:
        pass
    
    # Fallback local
    return Response({
        'projets': ProjetSerializer(Projet.objects.all(), many=True).data,
        'timeline': ProjetTimelineSerializer(ProjetTimeline.objects.all(), many=True).data,
        'statistiques': StatistiqueSerializer(Statistique.objects.filter(actif=True), many=True).data,
    })


@api_view(['GET'])
def get_contact_data(request):
    """Récupère les données de contact depuis l'admin-backend"""
    try:
        response = requests.get(f"{ADMIN_API_URL}/contact-data/", timeout=5)
        if response.status_code == 200:
            return Response(response.json())
    except requests.RequestException:
        pass
    
    # Fallback local
    return Response({
        'equipe': EquipeSerializer(Equipe.objects.filter(actif=True), many=True).data,
        'faqs': FAQSerializer(FAQ.objects.filter(actif=True), many=True).data,
        'partenaires': PartenaireSerializer(Partenaire.objects.filter(actif=True), many=True).data,
    })


@api_view(['POST'])
def submit_contact(request):
    """Soumet un message de contact"""
    try:
        response = requests.post(
            f"{ADMIN_API_URL}/submit-contact/",
            json=request.data,
            timeout=10
        )
        if response.status_code == 201:
            return Response(response.json(), status=201)
    except requests.RequestException:
        pass
    
    # Fallback: sauvegarder localement
    serializer = ContactMessageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'success': True,
            'message': 'Votre message a été envoyé avec succès !'
        }, status=status.HTTP_201_CREATED)
    return Response({
        'success': False,
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def herbier_stats(request):
    """Récupère les statistiques de l'herbier"""
    try:
        response = requests.get(f"{ADMIN_API_URL}/herbier-stats/", timeout=5)
        if response.status_code == 200:
            return Response(response.json())
    except requests.RequestException:
        pass
    
    # Fallback local
    stats = HerbierStats.update_stats()
    return Response({
        'total_plantes': stats.total_plantes,
        'total_familles': stats.total_familles,
        'total_genres': stats.total_genres,
        'total_images': stats.total_images,
        'dernier_ajout': stats.dernier_ajout,
        'date_mise_a_jour': stats.date_mise_a_jour
    })


@api_view(['GET'])
def search_suggestions(request):
    """Recherche des suggestions"""
    query = request.query_params.get('q', '')
    if not query:
        return Response([])
    
    try:
        limit = request.query_params.get('limit', 10)
        response = requests.get(
            f"{ADMIN_API_URL}/search-suggestions/?q={query}&limit={limit}",
            timeout=5
        )
        if response.status_code == 200:
            return Response(response.json())
    except requests.RequestException:
        pass
    
    # Fallback local
    suggestions = []
    plantes = Plante.objects.filter(nom__icontains=query, actif=True)[:10]
    for p in plantes:
        suggestions.append({'type': 'nom', 'value': p.nom, 'label': f"🌿 {p.nom}"})
    return Response(suggestions)


@api_view(['GET'])
def export_herbier(request):
    """Exporte l'herbier"""
    format_export = request.query_params.get('format', 'json')
    
    try:
        response = requests.get(
            f"{ADMIN_API_URL}/export-herbier/?format={format_export}",
            timeout=10
        )
        if response.status_code == 200:
            if format_export == 'csv':
                csv_response = HttpResponse(response.content, content_type='text/csv')
                csv_response['Content-Disposition'] = 'attachment; filename="herbier_export.csv"'
                return csv_response
            return Response(response.json())
    except requests.RequestException:
        pass
    
    # Fallback local
    if format_export == 'csv':
        import csv
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="herbier_export.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['ID', 'Nom', 'Nom scientifique', 'Famille', 'Genre', 'Description'])
        
        for plante in Plante.objects.filter(actif=True):
            writer.writerow([
                plante.id, plante.nom, plante.nom_scientifique,
                plante.famille.nom if plante.famille else '',
                plante.genre.nom if plante.genre else '',
                plante.description
            ])
        return response
    
    plantes = Plante.objects.filter(actif=True).values(
        'id', 'nom', 'nom_scientifique', 'famille__nom', 'genre__nom',
        'description', 'habitat', 'statut_conservation', 'date_creation'
    )
    return Response(list(plantes))


@api_view(['GET'])
def get_slide_images(request):
    """Récupère les images des slides"""
    try:
        response = requests.get(f"{ADMIN_API_URL}/slide-images/", timeout=5)
        if response.status_code == 200:
            return Response(response.json())
    except requests.RequestException:
        pass
    
    # Fallback local
    slides = Slide.objects.filter(actif=True).order_by('ordre')
    data = []
    for slide in slides:
        data.append({
            'id': slide.id,
            'titre': slide.titre,
            'texte_botanique': slide.texte_botanique,
            'image': slide.image.url if slide.image else slide.image_url
        })
    return Response(data)


@api_view(['GET'])
def generate_alphabet_index(request):
    """Génère l'index alphabétique"""
    try:
        response = requests.get(f"{ADMIN_API_URL}/generate-alphabet-index/", timeout=5)
        if response.status_code == 200:
            return Response(response.json())
    except requests.RequestException:
        pass
    
    # Fallback local
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    index = []
    for letter in alphabet:
        count = Plante.objects.filter(nom__istartswith=letter, actif=True).count()
        if count > 0:
            index.append({'letter': letter, 'count': count})
    return Response(index)


@api_view(['GET'])
def get_stats_herbier(request):
    """Récupère les statistiques de l'herbier"""
    try:
        response = requests.get(f"{ADMIN_API_URL}/get-stats-herbier/", timeout=5)
        if response.status_code == 200:
            return Response(response.json())
    except requests.RequestException:
        pass
    
    # Fallback local
    return Response({
        'total_plantes': Plante.objects.filter(actif=True).count(),
        'total_familles': FamilleBotanique.objects.count(),
        'total_genres': GenreBotanique.objects.count(),
        'total_images': Plante.objects.filter(actif=True, image__isnull=False).count(),
        'dernier_ajout': Plante.objects.filter(actif=True).order_by('-date_creation').first().date_creation if Plante.objects.filter(actif=True).exists() else None,
    })