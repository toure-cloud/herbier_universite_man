# admin-backend/api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'plantes', views.PlanteViewSet)
router.register(r'equipe', views.EquipeViewSet)
router.register(r'slides', views.SlideViewSet)
router.register(r'projets', views.ProjetViewSet)
router.register(r'activites', views.ActiviteViewSet)
router.register(r'temoignages', views.TemoignageViewSet)
router.register(r'publications', views.PublicationViewSet)
router.register(r'faqs', views.FAQViewSet)
router.register(r'statistiques', views.StatistiqueViewSet)
router.register(r'methodologie', views.MethodologieViewSet)
router.register(r'partenaires', views.PartenaireViewSet)

urlpatterns = [
    # Routes principales
    path('', views.api_root, name='api-root'),
    path('health/', views.health_check, name='health-check'),
    path('stats/', views.dashboard_stats, name='dashboard-stats'),
    
    # Routes d'authentification
    path('create-superadmin/', views.create_superadmin, name='create-superadmin'),
    path('login/', views.login_superadmin, name='login'),
    path('verify-2fa/', views.verify_2fa, name='verify-2fa'),
    path('resend-code/', views.resend_code, name='resend-code'),
    path('logout/', views.logout_superadmin, name='logout'),
    path('me/', views.get_current_user, name='get-current-user'),
    
    # Routes d'administration des utilisateurs
    path('users/', views.get_users, name='get-users'),
    path('users/create/', views.create_user, name='create-user'),
    path('users/<int:user_id>/', views.update_user, name='update-user'),
    path('users/<int:user_id>/delete/', views.delete_user, name='delete-user'),
    path('users/<int:user_id>/toggle-status/', views.toggle_user_status, name='toggle-user-status'),
    
    # Routes batch
    path('plantes/batch/', views.create_multiple_plantes, name='create-multiple-plantes'),
    path('create-multiple-equipe/', views.create_multiple_equipe, name='create-multiple-equipe'),
    path('create-multiple-partenaires/', views.create_multiple_partenaires, name='create-multiple-partenaires'),
    path('sync-all/', views.sync_all_data, name='sync-all'),
    path('forgot-password/', views.forgot_password, name='forgot-password'),
    path('reset-password/', views.reset_password, name='reset-password'),

    path('test-media/', views.test_media, name='test-media'),
    path('media/<path:path>', views.serve_media, name='serve_media'),
    path('admin-users/', views.get_admin_users, name='get-admin-users'),
    # Inclure les routes du router
    path('', include(router.urls)),
]
