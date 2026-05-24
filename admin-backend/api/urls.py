from django.urls import path
from . import views

urlpatterns = [
    # Endpoints de base
    path('', views.api_root, name='api_root'),
    path('health/', views.health_check, name='health'),
    
    # Endpoints d'authentification
    path('create-superadmin/', views.create_superadmin, name='create_superadmin'),
    path('login/', views.login_superadmin, name='login'),
    path('verify-2fa/', views.verify_2fa, name='verify_2fa'),
    path('logout/', views.logout_superadmin, name='logout'),
    path('me/', views.get_current_user, name='me'),
    path('resend-code/', views.resend_code, name='resend_code'),
    path('verify-2fa/', views.verify_2fa, name='verify_2fa'),
    # Endpoints de données
    path('plantes/', views.PlanteViewSet.as_view({'get': 'list', 'post': 'create'}), name='plantes'),
    path('equipe/', views.EquipeViewSet.as_view({'get': 'list', 'post': 'create'}), name='equipe'),
    path('slides/', views.SlideViewSet.as_view({'get': 'list', 'post': 'create'}), name='slides'),
    path('projets/', views.ProjetViewSet.as_view({'get': 'list', 'post': 'create'}), name='projets'),
    path('dashboard/', views.dashboard_stats, name='dashboard_stats'),
    
    # Endpoints de synchronisation
    path('sync-all/', views.sync_all_data, name='sync_all'),
    path('sync/<str:endpoint>/', views.sync_endpoint, name='sync_endpoint'),
    path('sync-logs/', views.get_sync_logs, name='sync_logs'),
]
