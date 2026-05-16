#!/bin/bash

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}   Déploiement de l'administration Herbier   ${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

cd ~/Bureau/herbier_universite_man

# 1. Vérifier les fichiers
echo -e "${YELLOW}1. Vérification des fichiers...${NC}"

if [ -f "admin-backend/requirements.txt" ]; then
    echo -e "${GREEN}   ✓ admin-backend/requirements.txt${NC}"
else
    echo "   ✗ admin-backend/requirements.txt manquant"
    exit 1
fi

if [ -f "admin-backend/manage.py" ]; then
    echo -e "${GREEN}   ✓ admin-backend/manage.py${NC}"
else
    echo "   ✗ admin-backend/manage.py manquant"
    exit 1
fi

if [ -f "admin-frontend/package.json" ]; then
    echo -e "${GREEN}   ✓ admin-frontend/package.json${NC}"
else
    echo "   ✗ admin-frontend/package.json manquant"
    exit 1
fi

echo ""

# 2. Configurer admin-backend
echo -e "${YELLOW}2. Configuration admin-backend...${NC}"

mkdir -p admin-backend/admin_auth

cat > admin-backend/admin_auth/settings.py << 'SETTINGS_EOF'
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-admin-key')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = ['*']

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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'admin_db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = []
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Africa/Abidjan'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

CORS_ALLOWED_ORIGINS = [
    "https://herbier-admin-frontend.onrender.com",
    "http://localhost:5174",
]

CORS_ALLOW_CREDENTIALS = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
SETTINGS_EOF

echo -e "${GREEN}   ✓ admin-backend configuré${NC}"

# 3. Configurer admin-frontend
echo -e "${YELLOW}3. Configuration admin-frontend...${NC}"

cat > admin-frontend/.env.production << 'ENV_EOF'
VITE_API_URL=https://herbier-admin-backend.onrender.com
ENV_EOF

echo -e "${GREEN}   ✓ admin-frontend configuré${NC}"
echo ""

# 4. Push vers GitHub
echo -e "${YELLOW}4. Push vers GitHub...${NC}"

git add .
git commit -m "Deploiement administration Herbier $(date '+%Y-%m-%d %H:%M:%S')"
git push origin main

echo -e "${GREEN}   ✓ Push effectué${NC}"
echo ""

# 5. Instructions
echo -e "${BLUE}========================================${NC}"
echo -e "${YELLOW}📋 Créez les services sur Render :${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "1. ${GREEN}Admin Backend${NC} (Web Service):"
echo "   - Root Directory: admin-backend"
echo "   - Build Command: pip install -r requirements.txt"
echo "   - Start Command: gunicorn admin_auth.wsgi:application"
echo ""
echo -e "2. ${GREEN}Admin Frontend${NC} (Static Site):"
echo "   - Root Directory: admin-frontend"
echo "   - Build Command: npm install && npm run build"
echo "   - Publish Directory: dist"
echo ""
echo -e "${GREEN}✅ Configuration terminée !${NC}"
