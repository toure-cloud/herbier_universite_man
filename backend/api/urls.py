from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

# Routes pour le site public
router.register(r'equipe', views.EquipeViewSet)
router.register(r'partenaires', views.PartenaireViewSet)
router.register(r'slides', views.SlideViewSet)
router.register(r'projets', views.ProjetViewSet)
router.register(r'projets-timeline', views.ProjetTimelineViewSet)
router.register(r'activites', views.ActiviteViewSet)
router.register(r'temoignages', views.TemoignageViewSet)
router.register(r'publications', views.PublicationViewSet)
router.register(r'faqs', views.FAQViewSet)
router.register(r'contacts', views.ContactMessageViewSet)
router.register(r'statistiques', views.StatistiqueViewSet)
router.register(r'methodologie', views.MethodologieViewSet)

# Routes pour l'herbier avancé
router.register(r'plantes', views.PlanteViewSet)
router.register(r'familles', views.FamilleBotaniqueViewSet)
router.register(r'genres', views.GenreBotaniqueViewSet)

urlpatterns = [
    path('', include(router.urls)),
    
    # Routes de recherche pour plantes
    path('rechercher/', views.PlanteViewSet.as_view({'get': 'search'}), name='rechercher_plantes'),
    path('suggestions/', views.search_suggestions, name='suggestions'),
    path('slides-images/', views.get_slide_images, name='slides_images'),
    # Routes d'indexation alphabétique
    path('alphabetique/', views.PlanteViewSet.as_view({'get': 'alphabetique'}), name='alphabetique'),
    path('alphabet-index/', views.PlanteViewSet.as_view({'get': 'alphabet_index'}), name='alphabet_index'),
    path('generate-alphabet-index/', views.generate_alphabet_index, name='generate_alphabet_index'),
    
    # Routes de groupement
    path('familles/liste/', views.PlanteViewSet.as_view({'get': 'familles_list'}), name='familles_list'),
    path('genres/liste/', views.PlanteViewSet.as_view({'get': 'genres_list'}), name='genres_list'),
    path('par-famille/', views.PlanteViewSet.as_view({'get': 'by_famille'}), name='by_famille'),
    path('par-genre/', views.PlanteViewSet.as_view({'get': 'by_genre'}), name='by_genre'),
    
    # Routes de mise en avant
    path('a-la-une/', views.PlanteViewSet.as_view({'get': 'featured_plants'}), name='featured_plants'),
    path('recents/', views.PlanteViewSet.as_view({'get': 'recent_plants'}), name='recent_plants'),
    
    # Routes pour les pages spécifiques
    path('dashboard/', views.dashboard_stats, name='dashboard_stats'),
    path('activites-data/', views.get_activites_data, name='activites_data'),
    path('projets-data/', views.get_projets_data, name='projets_data'),
    path('contact-data/', views.get_contact_data, name='contact_data'),
    path('submit-contact/', views.submit_contact, name='submit_contact'),
    
    # Statistiques et export
    path('herbier-stats/', views.herbier_stats, name='herbier_stats'),
    path('exporter/', views.export_herbier, name='exporter'),
]
