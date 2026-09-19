from django.contrib import admin
from .models import (
    Plante, FamilleBotanique, GenreBotanique, Equipe, Partenaire,
    Slide, Projet, ProjetTimeline, Activite, Temoignage,
    Publication, FAQ, ContactMessage, Statistique, Methodologie
)

@admin.register(Plante)
class PlanteAdmin(admin.ModelAdmin):
    list_display = ('nom_scientifique', 'nom_vernaculaire', 'famille', 'statut_conservation', 'actif', 'date_creation')
    list_filter = ('statut_conservation', 'actif', 'famille', 'type_morphologique', 'type_biologique')
    search_fields = ('nom_scientifique', 'nom_vernaculaire', 'famille__nom', 'lieu_collecte')
    readonly_fields = ('date_creation',)
    list_per_page = 25

    fieldsets = (
        ('Identification', {
            'fields': ('nom_scientifique', 'nom_vernaculaire', 'famille', 'genre')
        }),
        ('Classification', {
            'fields': ('type_morphologique', 'type_biologique', 'affinite_chorologique', 'affinite_ecologique')
        }),
        ('Conservation', {
            'fields': ('statut_conservation',)
        }),
        ('Localisation et description', {
            'fields': ('lieu_collecte', 'habitat', 'description', 'distribution', 'usages')
        }),
        ('Images', {
            'fields': ('image', 'images_galerie')
        }),
        ('Métadonnées', {
            'fields': ('featured', 'actif', 'date_creation')
        }),
    )

@admin.register(FamilleBotanique)
class FamilleBotaniqueAdmin(admin.ModelAdmin):
    list_display = ('nom', 'nom_latin', 'nombre_especes')
    search_fields = ('nom', 'nom_latin')

@admin.register(GenreBotanique)
class GenreBotaniqueAdmin(admin.ModelAdmin):
    list_display = ('nom', 'nom_latin', 'famille')
    search_fields = ('nom', 'nom_latin')
    list_filter = ('famille',)

@admin.register(Equipe)
class EquipeAdmin(admin.ModelAdmin):
    list_display = ('nom', 'poste', 'email', 'ordre', 'actif')
    list_editable = ('ordre', 'actif')
    search_fields = ('nom', 'poste', 'email')

@admin.register(Partenaire)
class PartenaireAdmin(admin.ModelAdmin):
    list_display = ('nom', 'site_web', 'type', 'ordre', 'actif')
    list_editable = ('ordre', 'actif')
    search_fields = ('nom',)

@admin.register(Slide)
class SlideAdmin(admin.ModelAdmin):
    list_display = ('titre', 'ordre', 'actif')
    list_editable = ('ordre', 'actif')
    search_fields = ('titre',)

@admin.register(Projet)
class ProjetAdmin(admin.ModelAdmin):
    list_display = ('titre', 'categorie', 'statut', 'annee', 'featured')
    list_editable = ('featured',)
    list_filter = ('categorie', 'statut', 'annee')
    search_fields = ('titre', 'description')

@admin.register(ProjetTimeline)
class ProjetTimelineAdmin(admin.ModelAdmin):
    list_display = ('titre', 'annee', 'projet', 'ordre')
    list_editable = ('ordre',)
    list_filter = ('annee',)
    search_fields = ('titre',)

@admin.register(Activite)
class ActiviteAdmin(admin.ModelAdmin):
    list_display = ('titre', 'titre_court', 'ordre', 'actif')
    list_editable = ('ordre', 'actif')
    search_fields = ('titre',)

@admin.register(Temoignage)
class TemoignageAdmin(admin.ModelAdmin):
    list_display = ('nom', 'organisation', 'poste', 'note', 'ordre', 'actif')
    list_editable = ('ordre', 'actif', 'note')
    search_fields = ('nom', 'organisation')

@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ('titre', 'journal', 'annee', 'actif')
    list_editable = ('actif',)
    list_filter = ('annee', 'actif')
    search_fields = ('titre', 'auteurs')

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
