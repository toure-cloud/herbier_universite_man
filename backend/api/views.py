from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.http import HttpResponse
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

# ==================== VIEWSETS POUR LE SITE PUBLIC ====================

class EquipeViewSet(viewsets.ModelViewSet):
    queryset = Equipe.objects.filter(actif=True)
    serializer_class = EquipeSerializer

class PartenaireViewSet(viewsets.ModelViewSet):
    queryset = Partenaire.objects.filter(actif=True)
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
    queryset = Publication.objects.filter(actif=True)
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
    queryset = Plante.objects.filter(actif=True)
    serializer_class = PlanteSerializer
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('q', '')
        if query:
            plantes = self.queryset.filter(
                Q(nom__icontains=query) |
                Q(nom_scientifique__icontains=query) |
                Q(famille__nom__icontains=query) |
                Q(genre__nom__icontains=query) |
                Q(description__icontains=query)
            )
            serializer = self.get_serializer(plantes, many=True)
            return Response(serializer.data)
        return Response([])
    
    @action(detail=False, methods=['get'])
    def by_famille(self, request):
        famille_id = request.query_params.get('famille_id')
        if famille_id:
            plantes = self.queryset.filter(famille_id=famille_id)
            serializer = self.get_serializer(plantes, many=True)
            return Response(serializer.data)
        return Response([])
    
    @action(detail=False, methods=['get'])
    def by_genre(self, request):
        genre_id = request.query_params.get('genre_id')
        if genre_id:
            plantes = self.queryset.filter(genre_id=genre_id)
            serializer = self.get_serializer(plantes, many=True)
            return Response(serializer.data)
        return Response([])
    
    @action(detail=False, methods=['get'])
    def alphabetique(self, request):
        lettre = request.query_params.get('lettre', '')
        plantes = self.queryset
        if lettre:
            plantes = plantes.filter(nom__istartswith=lettre)
        plantes = plantes.order_by('nom')
        serializer = self.get_serializer(plantes, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def featured_plants(self, request):
        plantes = self.queryset.filter(featured=True)[:6]
        serializer = self.get_serializer(plantes, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def recent_plants(self, request):
        limit = int(request.query_params.get('limit', 12))
        plantes = self.queryset.order_by('-date_creation')[:limit]
        serializer = self.get_serializer(plantes, many=True)
        return Response(serializer.data)

class FamilleBotaniqueViewSet(viewsets.ModelViewSet):
    queryset = FamilleBotanique.objects.all()
    serializer_class = FamilleBotaniqueSerializer

class GenreBotaniqueViewSet(viewsets.ModelViewSet):
    queryset = GenreBotanique.objects.all()
    serializer_class = GenreBotaniqueSerializer

# ==================== FONCTIONS API ====================

@api_view(['GET'])
def dashboard_stats(request):
    stats = {
        'total_plantes': Plante.objects.filter(actif=True).count(),
        'total_equipe': Equipe.objects.filter(actif=True).count(),
        'total_partenaires': Partenaire.objects.filter(actif=True).count(),
        'total_projets': Projet.objects.count(),
        'total_slides': Slide.objects.filter(actif=True).count(),
        'total_publications': Publication.objects.filter(actif=True).count(),
        'total_temoignages': Temoignage.objects.filter(actif=True).count(),
        'total_messages': ContactMessage.objects.filter(lu=False).count(),
    }
    return Response(stats)

@api_view(['GET'])
def get_activites_data(request):
    data = {
        'activites': ActiviteSerializer(Activite.objects.filter(actif=True), many=True).data,
        'temoignages': TemoignageSerializer(Temoignage.objects.filter(actif=True), many=True).data,
        'publications': PublicationSerializer(Publication.objects.filter(actif=True)[:5], many=True).data,
        'statistiques': StatistiqueSerializer(Statistique.objects.filter(actif=True), many=True).data,
        'faqs': FAQSerializer(FAQ.objects.filter(actif=True), many=True).data,
        'methodologie': MethodologieSerializer(Methodologie.objects.filter(actif=True), many=True).data,
    }
    return Response(data)

@api_view(['GET'])
def get_projets_data(request):
    data = {
        'projets': ProjetSerializer(Projet.objects.all(), many=True).data,
        'timeline': ProjetTimelineSerializer(ProjetTimeline.objects.all(), many=True).data,
        'statistiques': StatistiqueSerializer(Statistique.objects.filter(actif=True), many=True).data,
    }
    return Response(data)

@api_view(['GET'])
def get_contact_data(request):
    data = {
        'equipe': EquipeSerializer(Equipe.objects.filter(actif=True), many=True).data,
        'faqs': FAQSerializer(FAQ.objects.filter(actif=True), many=True).data,
        'partenaires': PartenaireSerializer(Partenaire.objects.filter(actif=True), many=True).data,
    }
    return Response(data)

@api_view(['POST'])
def submit_contact(request):
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
    query = request.query_params.get('q', '')
    limit = int(request.query_params.get('limit', 10))
    
    if not query:
        return Response([])
    
    suggestions = []
    
    plantes_nom = Plante.objects.filter(
        nom__icontains=query, actif=True
    )[:limit]
    
    for p in plantes_nom:
        suggestions.append({'type': 'nom', 'value': p.nom, 'label': f"🌿 {p.nom}"})
    
    return Response(suggestions)

@api_view(['GET'])
def export_herbier(request):
    format_export = request.query_params.get('format', 'json')
    plantes = Plante.objects.filter(actif=True).values(
        'id', 'nom', 'nom_scientifique', 'famille__nom', 'genre__nom',
        'description', 'habitat', 'statut_conservation', 'date_creation'
    )
    
    if format_export == 'csv':
        import csv
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="herbier_export.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['ID', 'Nom', 'Nom scientifique', 'Famille', 'Genre', 'Description', 'Habitat', 'Statut', 'Date création'])
        
        for plante in plantes:
            writer.writerow([
                plante['id'], plante['nom'], plante['nom_scientifique'],
                plante['famille__nom'], plante['genre__nom'], plante['description'],
                plante['habitat'], plante['statut_conservation'], plante['date_creation']
            ])
        
        return response
    
    return Response(list(plantes))

@api_view(['GET'])
def get_slide_images(request):
    slides = Slide.objects.filter(actif=True).order_by('ordre')
    data = []
    for slide in slides:
        data.append({
            'id': slide.id,
            'titre': slide.titre,
            'texte_botanique': slide.texte_botanique,
            'image': slide.image.url if slide.image else (slide.image_url if slide.image_url else None)
        })
    return Response(data)

@api_view(['GET'])
def generate_alphabet_index(request):
    """Générer l'index alphabétique des plantes"""
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    index = []
    
    # Parcourir les lettres de l'alphabet
    for letter in alphabet:
        count = Plante.objects.filter(
            nom__istartswith=letter, actif=True
        ).count()
        
        if count > 0:
            index.append({'letter': letter, 'count': count})
    
    # Ajouter les nombres/autres caractères
    autres_count = Plante.objects.filter(
        nom__regex=r'^[^A-Za-z]', actif=True
    ).count()
    
    if autres_count > 0:
        index.append({'letter': '#', 'count': autres_count})
    
    return Response(index)

@api_view(['GET'])
def get_stats_herbier(request):
    """Récupérer les statistiques de l'herbier"""
    stats = {
        'total_plantes': Plante.objects.filter(actif=True).count(),
        'total_familles': FamilleBotanique.objects.count(),
        'total_genres': GenreBotanique.objects.count(),
        'total_images': Plante.objects.filter(actif=True, image__isnull=False).count(),
        'dernier_ajout': Plante.objects.filter(actif=True).order_by('-date_creation').first().date_creation if Plante.objects.filter(actif=True).exists() else None,
    }
    return Response(stats)

@api_view(['GET'])
def get_alphabet_index(request):
    """Récupérer l'index alphabétique (alias)"""
    return generate_alphabet_index(request)

# Ajouter ces méthodes à la classe PlanteViewSet si elles n'existent pas
# (Placez-les à l'intérieur de la classe PlanteViewSet)

class PlanteViewSet(viewsets.ModelViewSet):
    queryset = Plante.objects.filter(actif=True)
    serializer_class = PlanteSerializer
    
    # ... autres méthodes existantes ...
    
    @action(detail=False, methods=['get'])
    def alphabet_index(self, request):
        """Index alphabétique des plantes"""
        lettres = []
        lettres_data = []
        
        for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            count = self.queryset.filter(nom__istartswith=letter).count()
            if count > 0:
                lettres.append(letter)
                lettres_data.append({'letter': letter, 'count': count})
        
        # Ajouter les nombres
        autres_count = self.queryset.filter(nom__regex=r'^[^A-Za-z]').count()
        if autres_count > 0:
            lettres_data.append({'letter': '#', 'count': autres_count})
        
        return Response({
            'letters': lettres,
            'data': lettres_data
        })
    
    @action(detail=False, methods=['get'])
    def familles_list(self, request):
        """Liste des familles avec comptage"""
        from django.db.models import Count
        familles = FamilleBotanique.objects.annotate(
            total=Count('plantes')
        ).values('id', 'nom', 'total')
        return Response(list(familles))
    
    @action(detail=False, methods=['get'])
    def genres_list(self, request):
        """Liste des genres avec comptage"""
        from django.db.models import Count
        genres = GenreBotanique.objects.annotate(
            total=Count('plantes')
        ).values('id', 'nom', 'famille__nom', 'total')
        return Response(list(genres))
