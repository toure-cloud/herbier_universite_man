from django.urls import path
from . import views

urlpatterns = [
    # Synchronisation
    path('sync-all/', views.sync_all_data, name='sync_all'),
    path('sync/<str:endpoint>/', views.sync_endpoint, name='sync_endpoint'),
    path('push/<str:endpoint>/', views.push_to_public_api, name='push_to_public'),
    path('sync-logs/', views.get_sync_logs, name='sync_logs'),
    
    # Dashboard et stats
    path('stats/', views.get_stats, name='stats'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    # SuperAdmin
    path('superadmins/', views.SuperAdminViewSet.as_view({'get': 'list', 'post': 'create'}), name='superadmins'),
]
