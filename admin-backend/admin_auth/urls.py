# admin_auth/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse, Http404
import os
from . import views

def serve_media(request, path):
    """Sert les fichiers médias manuellement"""
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    
    # Sécurité
    if not file_path.startswith(os.path.abspath(settings.MEDIA_ROOT)):
        raise Http404("Accès non autorisé")
    
    if not os.path.exists(file_path):
        raise Http404("Fichier non trouvé")
    
    # Déterminer le content-type
    import mimetypes
    content_type, _ = mimetypes.guess_type(file_path)
    content_type = content_type or 'application/octet-stream'
    
    with open(file_path, 'rb') as f:
        return HttpResponse(f.read(), content_type=content_type)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('', views.root_redirect, name='root-redirect'),
]

# ✅ Servir les médias en développement
if settings.DEBUG:
    # Méthode 1: static()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    # Méthode 2: Vue manuelle (fallback)
    urlpatterns.append(path('media/<path:path>', serve_media))
    