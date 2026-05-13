from django.contrib import admin
from .models import Plante, Equipe, Partenaire, Slide, Projet, Contact

@admin.register(Plante)
class PlanteAdmin(admin.ModelAdmin):
    list_display = ('nom', 'famille', 'date_creation')
    search_fields = ('nom', 'famille')
    list_filter = ('famille',)

@admin.register(Equipe)
class EquipeAdmin(admin.ModelAdmin):
    list_display = ('nom', 'poste', 'email')
    search_fields = ('nom', 'poste')

@admin.register(Partenaire)
class PartenaireAdmin(admin.ModelAdmin):
    list_display = ('nom', 'site_web')
    search_fields = ('nom',)

@admin.register(Slide)
class SlideAdmin(admin.ModelAdmin):
    list_display = ('titre', 'ordre', 'actif')
    list_editable = ('ordre', 'actif')
    search_fields = ('titre',)

@admin.register(Projet)
class ProjetAdmin(admin.ModelAdmin):
    list_display = ('titre', 'categorie', 'statut', 'annee')
    list_filter = ('categorie', 'statut')
    search_fields = ('titre', 'description')

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('nom', 'email', 'sujet', 'date_envoi', 'lu')
    list_editable = ('lu',)
    list_filter = ('sujet', 'lu')
    search_fields = ('nom', 'email')
