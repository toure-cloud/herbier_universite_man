# api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Création du routeur pour les ViewSets
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
    # ==================== ROUTES PRINCIPALES ====================
    path('', views.api_root, name='api-root'),
    path('health/', views.health_check, name='health-check'),
    path('stats/', views.dashboard_stats, name='dashboard-stats'),
    path('activites-data/', views.get_activites_data, name='activites-data'),

    # ==================== AUTHENTIFICATION SÉPARÉE ====================
    # SuperIT
    path('it/login/', views.it_login, name='it-login'),
    # Admin lambda
    path('admin/login/', views.admin_login, name='admin-login'),

    # Commun
    path('verify-2fa/', views.verify_2fa, name='verify-2fa'),
    path('resend-code/', views.resend_code, name='resend-code'),
    path('logout/', views.logout_view, name='logout'),
    path('me/', views.me_view, name='me'),
        # ==================== CONTACT (SuperIT) ====================
    path('contact-messages/', views.contact_messages, name='contact-messages'),
    path('contact-messages/stats/', views.contact_messages_stats, name='contact-messages-stats'),
    path('contact-messages/<int:message_id>/', views.contact_message_detail, name='contact-message-detail'),

    # Mot de passe oublié
    path('forgot-password/', views.forgot_password, name='forgot-password'),
    path('reset-password/', views.reset_password, name='reset-password'),

    # Ancien endpoint (rétrocompatibilité)
    path('create-superadmin/', views.create_superadmin, name='create-superadmin'),
    path('totp/setup/', views.totp_setup, name='totp-setup'),
    path('totp/verify-setup/', views.totp_verify_setup, name='totp-verify-setup'),
    path('totp/disable/', views.totp_disable, name='totp-disable'),

    # ==================== GESTION DES UTILISATEURS (SuperIT) ====================
    path('users/', views.list_users, name='list-users'),
    path('users/create/', views.create_user, name='create-user'),
    path('users/<int:user_id>/', views.update_user, name='update-user'),
    path('users/<int:user_id>/delete/', views.delete_user, name='delete-user'),

    # ==================== AUDIT (SuperIT) ====================
    path('audit/logs/', views.list_audit_logs, name='audit-logs'),
    path('me/activity/', views.my_activity, name='my-activity'),

    # ==================== SYNC ====================
    path('sync-all/', views.sync_all, name='sync-all'),

    # ==================== MÉDIAS ====================
    path('test-media/', views.test_media, name='test-media'),
    path('media/<path:path>', views.serve_media, name='serve_media'),
    
]

# ✅ Routes du router
urlpatterns += router.urls
