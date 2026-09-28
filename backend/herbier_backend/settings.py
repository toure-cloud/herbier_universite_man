
from pathlib import Path
import os
import dj_database_url
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-8x9y2z3a4b5c6d7e8f9g0h1i2j3k4l5m6n7o8p9q0r')
# ✅ URL de l'admin-backend, adaptée à l'environnement

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')

# Secret partagé avec l'admin-backend (pour le proxy contact)
SYNC_SECRET = os.environ.get('SYNC_SECRET', 'dev-secret-change-me')
# ============================================================
# ENVIRONNEMENT
# ============================================================

# ✅ DEBUG déterminé en premier (utilisé partout ensuite)
DEBUG = os.environ.get('DEBUG', 'True') == 'True'   # True par défaut en local

# ✅ URL de l'admin-backend, adaptée à l'environnement
if DEBUG:
    _default_admin_url = 'http://localhost:8001/api'
else:
    _default_admin_url = 'https://herbier-admin-backend.onrender.com/api'

ADMIN_API_URL = os.environ.get('ADMIN_API_URL', _default_admin_url)

# URL du backend public lui-même
API_URL = os.environ.get('API_URL', 'https://herbier-backend.onrender.com/api')
BASE_URL = os.environ.get('BASE_URL', 'https://herbier-backend.onrender.com')

# ============================================================
# SÉCURITÉ
# ============================================================

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-change-me-in-production')

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'herbier-universite-man.onrender.com',
    '.onrender.com',
    'herbier-backend.onrender.com',
]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'api',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'herbier_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'herbier_backend.wsgi.application'

# Database
DATABASES = {
    'default': dj_database_url.config(
        default='postgres://herbier_public:public_pass_2026@localhost:5432/herbier_public_db',
        conn_max_age=600,
        conn_health_checks=True,
    )
}
# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Africa/Abidjan'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'  # Correction: ajout du slash
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CORS settings - Correction: enlever les slashes à la fin
CORS_ALLOWED_ORIGINS = [
    # Dev local
    "http://localhost:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
    "http://localhost:3000",
    "http://127.0.0.1:3000",

    # Frontends en production
    "https://herbier-universite-man-frontend.onrender.com",
    "https://herbier-admin-frontend.onrender.com",

    # Backends
    "https://herbier-universite-man.onrender.com",
    "https://herbier-backend.onrender.com",
    "https://herbier-admin-backend.onrender.com",
]

CORS_ALLOW_CREDENTIALS = True


CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:8000",
    "http://localhost:8001",
    "https://herbier-universite-man-frontend.onrender.com",
    "https://herbier-admin-frontend.onrender.com",
    "https://herbier-universite-man.onrender.com",
    "https://herbier-backend.onrender.com",
    "https://herbier-admin-backend.onrender.com",
]

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'x-sync-secret',        # ✅ AJOUTER
]

# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
}

# WhiteNoise configuration
if not DEBUG:
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Configuration CORS pour l'admin-backend


# Permettre les requêtes cross-origin avec credentials
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = False
CORS_EXPOSE_HEADERS = [
    'content-type',
    'content-length',
]

# Ajouter un endpoint pour permettre à l'admin d'accéder aux données
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
}
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'