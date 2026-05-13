from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.conf.urls.static import static

def home(request):
    return JsonResponse({
        'status': 'ok',
        'message': 'Herbier Université de Man API',
        'endpoints': {
            'slides': '/api/slides/',
            'plantes': '/api/plantes/',
            'activites': '/api/activites/',
            'equipe': '/api/equipe/',
            'projets': '/api/projets/',
            'temoignages': '/api/temoignages/',
            'publications': '/api/publications/',
            'faqs': '/api/faqs/',
            'admin': '/admin/'
        }
    })

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
