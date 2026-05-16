from django.urls import path
from . import views

urlpatterns = [
    path('create-superadmin/', views.create_superadmin, name='create_superadmin'),
    path('login/', views.login_superadmin, name='login'),
    path('verify-2fa/', views.verify_2fa, name='verify_2fa'),
    path('logout/', views.logout_superadmin, name='logout'),
    path('me/', views.get_current_user, name='me'),
]
