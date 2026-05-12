from rest_framework import serializers
from .models import (
    Plante, Equipe, Partenaire, Slide, Projet, ProjetTimeline,
    Activite, Temoignage, Publication, FAQ, ContactMessage,
    Statistique, Methodologie, FamilleBotanique, GenreBotanique, HerbierStats
)

# ==================== SERIALIZERS POUR LE SITE PUBLIC ====================

class PlanteSerializer(serializers.ModelSerializer):
    tags_list = serializers.SerializerMethodField()
    images_list = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()
    statut_conservation_label = serializers.SerializerMethodField()
    
    class Meta:
        model = Plante
        fields = '__all__'
    
    def get_tags_list(self, obj):
        return obj.get_tags_list()
    
    def get_images_list(self, obj):
        return obj.get_images_list()
    
    def get_full_name(self, obj):
        return obj.get_full_name()
    
    def get_statut_conservation_label(self, obj):
        return dict(Plante.STATUT_CONSERVATION_CHOICES).get(obj.statut_conservation, '')

class PlanteListSerializer(serializers.ModelSerializer):
    """Serializer simplifié pour les listes"""
    class Meta:
        model = Plante
        fields = ['id', 'nom', 'nom_scientifique', 'famille', 'genre', 
                  'description_courte', 'habitat', 'statut_conservation', 
                  'image', 'date_creation', 'publie', 'featured']

class EquipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipe
        fields = '__all__'

class PartenaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partenaire
        fields = '__all__'

class SlideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slide
        fields = '__all__'

class ProjetTimelineSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjetTimeline
        fields = '__all__'

class ProjetSerializer(serializers.ModelSerializer):
    tags_list = serializers.SerializerMethodField()
    timeline = ProjetTimelineSerializer(many=True, read_only=True)
    
    class Meta:
        model = Projet
        fields = '__all__'
    
    def get_tags_list(self, obj):
        return obj.get_tags_list()

class ActiviteSerializer(serializers.ModelSerializer):
    points_forts_list = serializers.SerializerMethodField()
    
    class Meta:
        model = Activite
        fields = '__all__'
    
    def get_points_forts_list(self, obj):
        return obj.get_points_forts_list()

class TemoignageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Temoignage
        fields = '__all__'

class PublicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publication
        fields = '__all__'

class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = '__all__'

class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = '__all__'
        read_only_fields = ('date_envoi', 'lu')

class StatistiqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statistique
        fields = '__all__'

class MethodologieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Methodologie
        fields = '__all__'

# ==================== SERIALIZERS POUR L'HERBIER AVANCÉ ====================

class FamilleBotaniqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = FamilleBotanique
        fields = '__all__'

class GenreBotaniqueSerializer(serializers.ModelSerializer):
    famille_nom = serializers.CharField(source='famille.nom', read_only=True)
    
    class Meta:
        model = GenreBotanique
        fields = '__all__'

class HerbierStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HerbierStats
        fields = '__all__'
