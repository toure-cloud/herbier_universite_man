from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('create-superadmin/', views.create_superadmin, name='create_superadmin'),
    path('login/', views.login_superadmin, name='login'),
    path('verify-2fa/', views.verify_2fa, name='verify_2fa'),
    path('logout/', views.logout_superadmin, name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('herbier-data/', views.manage_herbier_data, name='herbier_data'),
    path('login-history/', views.get_login_history, name='login_history'),
    path('audit-logs/', views.get_audit_logs, name='audit_logs'),
    path('change-password/', views.change_password, name='change_password'),
]
