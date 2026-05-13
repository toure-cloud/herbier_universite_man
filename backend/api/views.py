from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.http import HttpResponse
from .models import (
    Plante, Equipe, Partenaire, Slide, Projet, ProjetTimeline,
    Activite, Temoignage, Publication, FAQ, ContactMessage,
    Statistique, Methodologie, FamilleBotanique, GenreBotanique, HerbierStats
)
from .serializers import (
    PlanteSerializer, PlanteListSerializer, EquipeSerializer, PartenaireSerializer,
    SlideSerializer, ProjetSerializer, ProjetTimelineSerializer,
    ActiviteSerializer, TemoignageSerializer, PublicationSerializer,
    FAQSerializer, ContactMessageSerializer, StatistiqueSerializer,
    MethodologieSerializer, FamilleBotaniqueSerializer, GenreBotaniqueSerializer,
    HerbierStatsSerializer
)

# ==================== VIEWSETS POUR LE SITE PUBLIC ====================

class EquipeViewSet(viewsets.ModelViewSet):
    queryset = Equipe.objects.all()
    serializer_class = EquipeSerializer

class PartenaireViewSet(viewsets.ModelViewSet):
    queryset = Partenaire.objects.all()
    serializer_class = PartenaireSerializer

class SlideViewSet(viewsets.ModelViewSet):
    queryset = Slide.objects.filter(actif=True)
    serializer_class = SlideSerializer

class ProjetViewSet(viewsets.ModelViewSet):
    queryset = Projet.objects.all()
    serializer_class = ProjetSerializer
    
    @action(detail=False, methods=['get'])
    def by_categorie(self, request):
        categorie = request.query_params.get('categorie', '')
        if categorie:
            projets = self.queryset.filter(categorie=categorie)
            serializer = self.get_serializer(projets, many=True)
            return Response(serializer.data)
        return Response([])
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        projets = self.queryset.filter(featured=True)
        serializer = self.get_serializer(projets, many=True)
        return Response(serializer.data)

class ProjetTimelineViewSet(viewsets.ModelViewSet):
    queryset = ProjetTimeline.objects.all()
    serializer_class = ProjetTimelineSerializer

class ActiviteViewSet(viewsets.ModelViewSet):
    queryset = Activite.objects.filter(actif=True)
    serializer_class = ActiviteSerializer

class TemoignageViewSet(viewsets.ModelViewSet):
    queryset = Temoignage.objects.filter(actif=True)
    serializer_class = TemoignageSerializer

class PublicationViewSet(viewsets.ModelViewSet):
    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer

class FAQViewSet(viewsets.ModelViewSet):
    queryset = FAQ.objects.filter(actif=True)
    serializer_class = FAQSerializer

class ContactMessageViewSet(viewsets.ModelViewSet):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    
    def create(self, request, *args, **kwargs):
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

class MethodologieViewSet(viewsets.ModelViewSet):
    queryset = Methodologie.objects.filter(actif=True)
    serializer_class = MethodologieSerializer

# ==================== VIEWSETS POUR L'HERBIER AVANCÉ ====================

class PlanteViewSet(viewsets.ModelViewSet):
    queryset = Plante.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'list':
            return PlanteListSerializer
        return PlanteSerializer
    
    def get_queryset(self):
        queryset = Plante.objects.filter(publie=True)
        
        # Filtres
        famille = self.request.query_params.get('famille', None)
        genre = self.request.query_params.get('genre', None)
        statut = self.request.query_params.get('statut', None)
        pays = self.request.query_params.get('pays', None)
        featured = self.request.query_params.get('featured', None)
        
        if famille:
            queryset = queryset.filter(famille__icontains=famille)
        if genre:
            queryset = queryset.filter(genre__icontains=genre)
        if statut:
            queryset = queryset.filter(statut_conservation=statut)
        if pays:
            queryset = queryset.filter(pays__icontains=pays)
        if featured == 'true':
            queryset = queryset.filter(featured=True)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """Recherche avancée"""
        query = request.query_params.get('q', '')
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 12))
        
        if not query:
            return Response({'results': [], 'total': 0, 'pages': 0})
        
        plantes = Plante.objects.filter(
            Q(nom__icontains=query) |
            Q(nom_scientifique__icontains=query) |
            Q(famille__icontains=query) |
            Q(genre__icontains=query) |
            Q(description__icontains=query) |
            Q(description_courte__icontains=query) |
            Q(habitat__icontains=query) |
            Q(lieu_collecte__icontains=query) |
            Q(tags__icontains=query) |
            Q(pays__icontains=query) |
            Q(region__icontains=query)
        ).filter(publie=True)
        
        paginator = Paginator(plantes, page_size)
        page_obj = paginator.get_page(page)
        
        serializer = PlanteListSerializer(page_obj, many=True)
        
        return Response({
            'results': serializer.data,
            'total': paginator.count,
            'page': page,
            'pages': paginator.num_pages,
            'page_size': page_size
        })
    
    @action(detail=False, methods=['get'])
    def by_famille(self, request):
        """Grouper les plantes par famille"""
        famille = request.query_params.get('famille', '')
        if famille:
            plantes = self.get_queryset().filter(famille=famille)
            serializer = PlanteListSerializer(plantes, many=True)
            return Response(serializer.data)
        return Response([])
    
    @action(detail=False, methods=['get'])
    def by_genre(self, request):
        """Grouper les plantes par genre"""
        genre = request.query_params.get('genre', '')
        if genre:
            plantes = self.get_queryset().filter(genre=genre)
            serializer = PlanteListSerializer(plantes, many=True)
            return Response(serializer.data)
        return Response([])
    
    @action(detail=False, methods=['get'])
    def alphabetique(self, request):
        """Liste alphabétique des plantes"""
        lettre = request.query_params.get('lettre', '')
        plantes = self.get_queryset()
        
        if lettre:
            if lettre == '#':
                plantes = plantes.filter(nom__regex=r'^[^a-zA-Z]')
            else:
                plantes = plantes.filter(nom__istartswith=lettre)
        
        plantes = plantes.order_by('nom')
        serializer = PlanteListSerializer(plantes, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def alphabet_index(self, request):
        """Index alphabétique des plantes"""
        lettres = []
        plantes = Plante.objects.filter(publie=True).values('nom')
        
        for plante in plantes:
            first_char = plante['nom'][0].upper() if plante['nom'] else ''
            if first_char and first_char not in lettres:
                if first_char.isalpha():
                    lettres.append(first_char)
        
        lettres.sort()
        
        # Ajouter les nombres/l'autre
        autres = Plante.objects.filter(publie=True, nom__regex=r'^[^a-zA-Z]').exists()
        if autres:
            lettres.append('#')
        
        return Response(lettres)
    
    @action(detail=False, methods=['get'])
    def familles_list(self, request):
        """Liste des familles avec comptage"""
        familles = Plante.objects.filter(publie=True)\
            .values('famille')\
            .annotate(total=Count('id'))\
            .order_by('famille')
        
        return Response(familles)
    
    @action(detail=False, methods=['get'])
    def genres_list(self, request):
        """Liste des genres avec comptage"""
        genres = Plante.objects.filter(publie=True, genre__isnull=False)\
            .exclude(genre='')\
            .values('genre')\
            .annotate(total=Count('id'))\
            .order_by('genre')
        
        return Response(genres)
    
    @action(detail=False, methods=['get'])
    def featured_plants(self, request):
        """Plantes à la une"""
        plantes = self.get_queryset().filter(featured=True)[:6]
        serializer = PlanteListSerializer(plantes, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def recent_plants(self, request):
        """Plantes récentes"""
        limit = int(request.query_params.get('limit', 12))
        plantes = self.get_queryset().order_by('-date_creation')[:limit]
        serializer = PlanteListSerializer(plantes, many=True)
        return Response(serializer.data)

class FamilleBotaniqueViewSet(viewsets.ModelViewSet):
    queryset = FamilleBotanique.objects.all()
    serializer_class = FamilleBotaniqueSerializer
    
    @action(detail=True, methods=['get'])
    def plantes(self, request, pk=None):
        famille = self.get_object()
        plantes = Plante.objects.filter(famille=famille.nom, publie=True)
        serializer = PlanteListSerializer(plantes, many=True)
        return Response(serializer.data)

class GenreBotaniqueViewSet(viewsets.ModelViewSet):
    queryset = GenreBotanique.objects.all()
    serializer_class = GenreBotaniqueSerializer
    
    @action(detail=True, methods=['get'])
    def plantes(self, request, pk=None):
        genre = self.get_object()
        plantes = Plante.objects.filter(genre=genre.nom, publie=True)
        serializer = PlanteListSerializer(plantes, many=True)
        return Response(serializer.data)

# ==================== FONCTIONS API ====================

@api_view(['GET'])
def dashboard_stats(request):
    """Statistiques du tableau de bord"""
    stats = {
        'total_plantes': Plante.objects.filter(publie=True).count(),
        'total_equipe': Equipe.objects.count(),
        'total_partenaires': Partenaire.objects.count(),
        'total_projets': Projet.objects.count(),
        'total_slides': Slide.objects.filter(actif=True).count(),
        'total_publications': Publication.objects.count(),
        'total_temoignages': Temoignage.objects.filter(actif=True).count(),
        'total_messages': ContactMessage.objects.filter(lu=False).count(),
    }
    return Response(stats)

@api_view(['GET'])
def get_activites_data(request):
    """Endpoint spécifique pour la page Activités"""
    data = {
        'activites': ActiviteSerializer(Activite.objects.filter(actif=True), many=True).data,
        'temoignages': TemoignageSerializer(Temoignage.objects.filter(actif=True), many=True).data,
        'publications': PublicationSerializer(Publication.objects.all()[:5], many=True).data,
        'statistiques': StatistiqueSerializer(Statistique.objects.filter(actif=True), many=True).data,
        'faqs': FAQSerializer(FAQ.objects.filter(actif=True), many=True).data,
        'methodologie': MethodologieSerializer(Methodologie.objects.filter(actif=True), many=True).data,
    }
    return Response(data)

@api_view(['GET'])
def get_projets_data(request):
    """Endpoint spécifique pour la page Projets"""
    data = {
        'projets': ProjetSerializer(Projet.objects.all(), many=True).data,
        'timeline': ProjetTimelineSerializer(ProjetTimeline.objects.all(), many=True).data,
        'statistiques': StatistiqueSerializer(Statistique.objects.filter(actif=True), many=True).data,
    }
    return Response(data)

@api_view(['GET'])
def get_contact_data(request):
    """Endpoint spécifique pour la page Contact"""
    data = {
        'equipe': EquipeSerializer(Equipe.objects.all(), many=True).data,
        'faqs': FAQSerializer(FAQ.objects.filter(actif=True), many=True).data,
        'partenaires': PartenaireSerializer(Partenaire.objects.all(), many=True).data,
    }
    return Response(data)

@api_view(['POST'])
def submit_contact(request):
    """Endpoint pour l'envoi du formulaire de contact"""
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
    """Statistiques globales de l'herbier"""
    stats = {
        'total_plantes': Plante.objects.filter(publie=True).count(),
        'total_familles': Plante.objects.filter(publie=True).values('famille').distinct().count(),
        'total_genres': Plante.objects.filter(publie=True, genre__isnull=False).exclude(genre='').values('genre').distinct().count(),
        'total_images': Plante.objects.filter(publie=True, image__isnull=False).count(),
        'par_statut': list(Plante.objects.filter(publie=True).values('statut_conservation').annotate(total=Count('id'))),
        'par_famille': list(Plante.objects.filter(publie=True).values('famille').annotate(total=Count('id')).order_by('-total')[:10]),
        'dernier_ajout': Plante.objects.filter(publie=True).order_by('-date_creation').first().date_creation if Plante.objects.filter(publie=True).exists() else None,
    }
    
    # Mettre à jour les stats en base
    HerbierStats.update_stats()
    
    return Response(stats)

@api_view(['GET'])
def search_suggestions(request):
    """Suggestions de recherche en temps réel"""
    query = request.query_params.get('q', '')
    limit = int(request.query_params.get('limit', 10))
    
    if not query:
        return Response([])
    
    suggestions = []
    
    # Suggestions par nom
    plantes_nom = Plante.objects.filter(
        nom__icontains=query, publie=True
    ).values('nom').distinct()[:limit]
    
    for p in plantes_nom:
        suggestions.append({'type': 'nom', 'value': p['nom'], 'label': f"🌿 {p['nom']}"})
    
    # Suggestions par famille
    if len(suggestions) < limit:
        plantes_famille = Plante.objects.filter(
            famille__icontains=query, publie=True
        ).values('famille').distinct()[:limit - len(suggestions)]
        
        for p in plantes_famille:
            suggestions.append({'type': 'famille', 'value': p['famille'], 'label': f"📁 Famille: {p['famille']}"})
    
    # Suggestions par genre
    if len(suggestions) < limit:
        plantes_genre = Plante.objects.filter(
            genre__icontains=query, publie=True
        ).exclude(genre='').values('genre').distinct()[:limit - len(suggestions)]
        
        for p in plantes_genre:
            suggestions.append({'type': 'genre', 'value': p['genre'], 'label': f"🔬 Genre: {p['genre']}"})
    
    return Response(suggestions)

@api_view(['GET'])
def export_herbier(request):
    """Export des données de l'herbier (CSV/JSON)"""
    format_export = request.query_params.get('format', 'json')
    plantes = Plante.objects.filter(publie=True).values(
        'id', 'nom', 'nom_scientifique', 'famille', 'genre',
        'description', 'habitat', 'statut_conservation', 
        'pays', 'region', 'date_creation'
    )
    
    if format_export == 'csv':
        import csv
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="herbier_export.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['ID', 'Nom', 'Nom scientifique', 'Famille', 'Genre', 
                        'Habitat', 'Statut', 'Pays', 'Région', 'Date création'])
        
        for plante in plantes:
            writer.writerow([
                plante['id'], plante['nom'], plante['nom_scientifique'],
                plante['famille'], plante['genre'], plante['habitat'],
                plante['statut_conservation'], plante['pays'],
                plante['region'], plante['date_creation']
            ])
        
        return response
    
    return Response(list(plantes))

@api_view(['GET'])
def generate_alphabet_index(request):
    """Générer l'index alphabétique des plantes"""
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    index = []
    
    for letter in alphabet:
        count = Plante.objects.filter(
            nom__istartswith=letter, publie=True
        ).count()
        
        if count > 0:
            index.append({'letter': letter, 'count': count})
    
    # Ajouter les nombres/autres
    autres_count = Plante.objects.filter(
        nom__regex=r'^[^a-zA-Z]', publie=True
    ).count()
    
    if autres_count > 0:
        index.append({'letter': '#', 'count': autres_count})
    
    return Response(index)

@api_view(['GET'])
def get_slide_images(request):
    """Endpoint pour récupérer les URLs des images des slides"""
    from .models import Slide
    slides = Slide.objects.filter(actif=True).order_by('ordre')
    data = []
    for slide in slides:
        data.append({
            'id': slide.id,
            'titre': slide.titre,
            'texte_botanique': slide.texte_botanique,
            'image': slide.image.url if slide.image else None
        })
    return Response(data)