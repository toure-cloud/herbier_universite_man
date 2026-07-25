import os
from pathlib import Path

# ============================================
# CONFIGURATION DE BASE
# ============================================

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-admin-key')
DEBUG = os.environ.get('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = ['*']

# ============================================
# APPLICATIONS
# ============================================

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

# ============================================
# MIDDLEWARES
# ============================================

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

# ============================================
# URLS ET TEMPLATES
# ============================================

ROOT_URLCONF = 'admin_auth.urls'

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

WSGI_APPLICATION = 'admin_auth.wsgi.application'

# ============================================
# BASE DE DONNÉES
# ============================================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ============================================
# AUTHENTIFICATION
# ============================================

AUTH_PASSWORD_VALIDATORS = []

# ============================================
# INTERNATIONALISATION
# ============================================

LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Africa/Abidjan'
USE_I18N = True
USE_TZ = True

# ============================================
# FICHIERS STATIQUES
# ============================================

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# ============================================
# FICHIERS MÉDIAS
# ============================================

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ============================================
# CORS - ✅ CORRIGÉ POUR LA PRODUCTION
# ============================================

# ✅ En développement, autoriser tout
if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True
else:
    CORS_ALLOWED_ORIGINS = [
        'https://herbier-admin-frontend.onrender.com',
        'https://herbier-frontend.onrender.com',
        'https://herbier-admin-backend.onrender.com',
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
]

# ============================================
# AUTRES
# ============================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
PUBLIC_API_URL = os.environ.get('PUBLIC_API_URL', 'http://localhost:8000/api')

# ✅ Créer les dossiers nécessaires
os.makedirs(os.path.join(BASE_DIR, 'static'), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, 'staticfiles'), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, 'media'), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, 'media/plantes'), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, 'media/equipe'), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, 'media/partenaires'), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, 'media/slides'), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, 'media/projets'), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, 'media/activites'), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, 'media/temoignages'), exist_ok=True)

# ✅ WhiteNoise pour les fichiers statiques
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'