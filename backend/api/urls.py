from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'plantes', views.PlanteViewSet)
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
router.register(r'familles', views.FamilleBotaniqueViewSet)
router.register(r'genres', views.GenreBotaniqueViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('dashboard/', views.dashboard_stats, name='dashboard_stats'),
    path('activites-data/', views.get_activites_data, name='activites_data'),
    path('projets-data/', views.get_projets_data, name='projets_data'),
    path('contact-data/', views.get_contact_data, name='contact_data'),
    path('submit-contact/', views.submit_contact, name='submit_contact'),
    path('herbier-stats/', views.herbier_stats, name='herbier_stats'),
    path('search-suggestions/', views.search_suggestions, name='search_suggestions'),
    path('export-herbier/', views.export_herbier, name='export_herbier'),
    path('slide-images/', views.get_slide_images, name='slide_images'),
    path('generate-alphabet-index/', views.generate_alphabet_index, name='generate_alphabet_index'),
]
