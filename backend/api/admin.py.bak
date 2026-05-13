from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Count
from .models import (
    Plante, Equipe, Partenaire, Slide, Projet, ProjetTimeline,
    Activite, Temoignage, Publication, FAQ, ContactMessage,
    Statistique, Methodologie, FamilleBotanique, GenreBotanique, HerbierStats
)

# ==================== ADMIN POUR LE MODÈLE PLANTE ====================

@admin.register(Plante)
class PlanteAdmin(admin.ModelAdmin):
    list_display = ('nom', 'famille', 'genre', 'statut_conservation', 'publie', 'featured', 'date_creation', 'apercu_image')
    list_filter = ('famille', 'genre', 'statut_conservation', 'publie', 'featured', 'pays', 'region')
    search_fields = ('nom', 'nom_scientifique', 'famille', 'genre', 'description', 'habitat', 'lieu_collecte', 'tags')
    list_editable = ('publie', 'featured')
    readonly_fields = ('date_creation', 'date_modification')
    list_per_page = 25
    
    fieldsets = (
        ('Informations de base', {
            'fields': ('nom', 'nom_scientifique', 'famille', 'genre', 'description', 'description_courte')
        }),
        ('Caractéristiques', {
            'fields': ('habitat', 'lieu_collecte', ('altitude_min', 'altitude_max'), ('floraison_debut', 'floraison_fin'), ('hauteur_min', 'hauteur_max'))
        }),
        ('Conservation', {
            'fields': ('statut_conservation', 'population_tendance', 'menaces')
        }),
        ('Localisation', {
            'fields': ('pays', 'region', 'localisation_specifique', ('coordonnees_lat', 'coordonnees_lon'))
        }),
        ('Médias', {
            'fields': ('image', 'images_galerie', 'illustration')
        }),
        ('Métadonnées', {
            'fields': ('tags', 'auteur', 'publie', 'featured')
        }),
        ('Dates', {
            'fields': ('date_creation', 'date_modification'),
            'classes': ('collapse',)
        }),
    )
    
    def apercu_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 5px; object-fit: cover;"/>', obj.image.url)
        return "Pas d'image"
    apercu_image.short_description = 'Image'
    
    actions = ['publier_selection', 'depublier_selection', 'mettre_a_la_une']
    
    @admin.action(description="Publier la sélection")
    def publier_selection(self, request, queryset):
        queryset.update(publie=True)
    
    @admin.action(description="Dépublier la sélection")
    def depublier_selection(self, request, queryset):
        queryset.update(publie=False)
    
    @admin.action(description="Mettre à la une")
    def mettre_a_la_une(self, request, queryset):
        queryset.update(featured=True)

# ==================== ADMIN POUR LES AUTRES MODÈLES ====================

@admin.register(Equipe)
class EquipeAdmin(admin.ModelAdmin):
    list_display = ('nom', 'poste', 'email', 'ordre', 'apercu_photo')
    list_editable = ('ordre',)
    search_fields = ('nom', 'poste', 'specialite')
    list_filter = ('poste',)
    
    def apercu_photo(self, obj):
        if obj.photo:
            return format_html('<img src="{}" width="40" height="40" style="border-radius: 50%; object-fit: cover;"/>', obj.photo.url)
        return "Pas de photo"
    apercu_photo.short_description = 'Photo'

@admin.register(Partenaire)
class PartenaireAdmin(admin.ModelAdmin):
    list_display = ('nom', 'site_web', 'ordre', 'apercu_logo')
    list_editable = ('ordre',)
    search_fields = ('nom',)
    
    def apercu_logo(self, obj):
        if obj.logo:
            return format_html('<img src="{}" width="40" height="40" style="border-radius: 5px; object-fit: contain;"/>', obj.logo.url)
        return "Pas de logo"
    apercu_logo.short_description = 'Logo'

@admin.register(Slide)
class SlideAdmin(admin.ModelAdmin):
    list_display = ('titre', 'ordre', 'actif', 'apercu_image')
    list_editable = ('ordre', 'actif')
    search_fields = ('titre',)
    
    def apercu_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="80" height="50" style="border-radius: 5px; object-fit: cover;"/>', obj.image.url)
        return "Pas d'image"
    apercu_image.short_description = 'Image'

@admin.register(Projet)
class ProjetAdmin(admin.ModelAdmin):
    list_display = ('titre', 'categorie', 'statut', 'featured', 'annee', 'apercu_image')
    list_editable = ('featured',)
    list_filter = ('categorie', 'statut', 'annee')
    search_fields = ('titre', 'description')
    fieldsets = (
        ('Informations principales', {
            'fields': ('titre', 'categorie', 'statut', 'featured', 'annee')
        }),
        ('Descriptions', {
            'fields': ('description', 'description_longue')
        }),
        ('Localisation et partenaires', {
            'fields': ('lieu', 'partenaires', 'beneficiaires')
        }),
        ('Finances et durée', {
            'fields': ('budget', 'duree', 'impact', 'progression')
        }),
        ('Médias', {
            'fields': ('image', 'images_galerie', 'caption')
        }),
        ('Tags et dates', {
            'fields': ('tags', 'date_debut', 'date_fin', 'objectifs', 'resultats')
        }),
    )
    
    def apercu_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 5px; object-fit: cover;"/>', obj.image.url)
        return "Pas d'image"
    apercu_image.short_description = 'Image'

@admin.register(ProjetTimeline)
class ProjetTimelineAdmin(admin.ModelAdmin):
    list_display = ('titre', 'annee', 'projet', 'ordre')
    list_editable = ('ordre',)
    list_filter = ('annee',)
    search_fields = ('titre', 'description')

@admin.register(Activite)
class ActiviteAdmin(admin.ModelAdmin):
    list_display = ('titre', 'titre_court', 'ordre', 'actif')
    list_editable = ('ordre', 'actif')
    search_fields = ('titre', 'description_courte')
    fieldsets = (
        ('Informations', {
            'fields': ('titre', 'titre_court', 'icon', 'ordre', 'actif')
        }),
        ('Descriptions', {
            'fields': ('description_courte', 'description_longue')
        }),
        ('Points forts', {
            'fields': ('points_forts',)
        }),
        ('Média', {
            'fields': ('image', 'caption')
        }),
    )

@admin.register(Temoignage)
class TemoignageAdmin(admin.ModelAdmin):
    list_display = ('nom', 'organisation', 'poste', 'note', 'ordre', 'actif')
    list_editable = ('ordre', 'actif')
    search_fields = ('nom', 'organisation')
    list_filter = ('note', 'actif')

@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ('titre', 'journal', 'annee', 'auteurs_courts')
    search_fields = ('titre', 'auteurs', 'journal')
    list_filter = ('annee',)
    
    def auteurs_courts(self, obj):
        return obj.auteurs[:50] + '...' if len(obj.auteurs) > 50 else obj.auteurs
    auteurs_courts.short_description = 'Auteurs'

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'ordre', 'actif')
    list_editable = ('ordre', 'actif')
    search_fields = ('question',)

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('nom', 'email', 'sujet', 'date_envoi', 'lu')
    list_editable = ('lu',)
    list_filter = ('sujet', 'lu', 'date_envoi')
    search_fields = ('nom', 'email', 'message')
    readonly_fields = ('date_envoi',)

@admin.register(Statistique)
class StatistiqueAdmin(admin.ModelAdmin):
    list_display = ('titre', 'valeur', 'unite', 'ordre', 'actif')
    list_editable = ('ordre', 'actif')
    search_fields = ('titre',)

@admin.register(Methodologie)
class MethodologieAdmin(admin.ModelAdmin):
    list_display = ('titre', 'ordre', 'actif')
    list_editable = ('ordre', 'actif')
    search_fields = ('titre',)

# ==================== ADMIN POUR LES NOUVEAUX MODÈLES ====================

@admin.register(FamilleBotanique)
class FamilleBotaniqueAdmin(admin.ModelAdmin):
    list_display = ('nom', 'nombre_especes', 'apercu_image')
    search_fields = ('nom',)
    
    def apercu_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="40" height="40" style="border-radius: 5px; object-fit: cover;"/>', obj.image.url)
        return "-"
    apercu_image.short_description = 'Image'
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        obj.update_especes_count()

@admin.register(GenreBotanique)
class GenreBotaniqueAdmin(admin.ModelAdmin):
    list_display = ('nom', 'famille', 'nombre_especes')
    list_filter = ('famille',)
    search_fields = ('nom',)
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        obj.update_especes_count()

@admin.register(HerbierStats)
class HerbierStatsAdmin(admin.ModelAdmin):
    list_display = ('total_plantes', 'total_familles', 'total_genres', 'total_images', 'dernier_ajout', 'derniere_mise_a_jour')
    readonly_fields = ('total_plantes', 'total_familles', 'total_genres', 'total_images', 'dernier_ajout', 'derniere_mise_a_jour')
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
