from rest_framework import serializers
from .models import (
    Plante, Equipe, Partenaire, Slide, Projet, ProjetTimeline,
    Activite, Temoignage, Publication, FAQ, ContactMessage,
    Statistique, Methodologie, FamilleBotanique, GenreBotanique, HerbierStats
)


def build_absolute_uri(serializer, path):
    """Construit une URL absolue pour un fichier media."""
    if not path:
        return None
    request = serializer.context.get('request')
    if request is not None:
        return request.build_absolute_uri(path)
    # Fallback si pas de request dans le contexte
    return path


class ActiviteSerializer(serializers.ModelSerializer):
    points_forts_list = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Activite
        fields = '__all__'

    def get_points_forts_list(self, obj):
        return obj.get_points_forts_list()

    def get_image(self, obj):
        if obj.image:
            return build_absolute_uri(self, obj.image.url)
        return None


class TemoignageSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()

    class Meta:
        model = Temoignage
        fields = '__all__'

    def get_photo(self, obj):
        if obj.photo:
            return build_absolute_uri(self, obj.photo.url)
        return None


class ProjetSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Projet
        fields = '__all__'

    def get_image(self, obj):
        if obj.image:
            return build_absolute_uri(self, obj.image.url)
        return None


class PlanteSerializer(serializers.ModelSerializer):
    famille_nom = serializers.CharField(source='famille.nom', read_only=True, allow_null=True)
    genre_nom = serializers.CharField(source='genre.nom', read_only=True, allow_null=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Plante
        fields = '__all__'

    def get_image(self, obj):
        if obj.image:
            return build_absolute_uri(self, obj.image.url)
        return None


class SlideSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Slide
        fields = '__all__'

    def get_image(self, obj):
        # Priorité à image_url externe, sinon fichier uploadé
        if obj.image_url:
            return obj.image_url
        if obj.image:
            return build_absolute_uri(self, obj.image.url)
        return None


class EquipeSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()

    class Meta:
        model = Equipe
        fields = '__all__'

    def get_photo(self, obj):
        if obj.photo:
            return build_absolute_uri(self, obj.photo.url)
        return None


class PartenaireSerializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()

    class Meta:
        model = Partenaire
        fields = '__all__'

    def get_logo(self, obj):
        if obj.logo:
            return build_absolute_uri(self, obj.logo.url)
        return None


# Les autres serializers restent inchangés
class FamilleBotaniqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = FamilleBotanique
        fields = '__all__'


class GenreBotaniqueSerializer(serializers.ModelSerializer):
    famille_nom = serializers.CharField(source='famille.nom', read_only=True)

    class Meta:
        model = GenreBotanique
        fields = '__all__'


class ProjetTimelineSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjetTimeline
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