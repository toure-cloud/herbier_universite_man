#!/bin/bash

echo "=== Installation de toutes les dépendances du projet Herbier ==="
echo ""

# Frontend Principal
echo "📦 Installation des dépendances du Frontend Principal..."
cd ~/Bureau/herbier_universite_man/frontend
npm install
npm install vue@3 vue-router@4 axios
npm install -D vite @vitejs/plugin-vue
echo "✅ Frontend Principal OK"
echo ""

# Frontend Admin
echo "📦 Installation des dépendances du Frontend Admin..."
cd ~/Bureau/herbier_universite_man/admin-frontend
if [ -f "package.json" ]; then
    npm install
    npm install vue@3 vue-router@4 axios pinia
    npm install -D vite @vitejs/plugin-vue
else
    echo "⚠️ Dossier admin-frontend non trouvé ou package.json manquant"
    echo "Créez d'abord le projet avec: npm create vite@latest admin-frontend -- --template vue"
fi
echo "✅ Frontend Admin OK"
echo ""

# Backend Principal
echo "📦 Installation des dépendances du Backend Principal..."
cd ~/Bureau/herbier_universite_man/backend
if [ -d "venv" ]; then
    source venv/bin/activate
else
    python3 -m venv venv
    source venv/bin/activate
fi
pip install --upgrade pip
pip install django==4.2.5
pip install djangorestframework==3.14.0
pip install django-cors-headers==4.2.0
pip install Pillow==10.0.1
pip install python-decouple==3.8
pip install whitenoise==6.5.0
pip install gunicorn==21.2.0
echo "✅ Backend Principal OK"
echo ""

# Backend Admin
echo "📦 Installation des dépendances du Backend Admin..."
cd ~/Bureau/herbier_universite_man/admin-backend
if [ -d "venv" ]; then
    source venv/bin/activate
else
    python3 -m venv venv
    source venv/bin/activate
fi
pip install --upgrade pip
pip install django==4.2.5
pip install djangorestframework==3.14.0
pip install django-cors-headers==4.2.0
pip install djangorestframework-simplejwt==5.3.0
pip install Pillow==10.0.1
pip install python-decouple==3.8
echo "✅ Backend Admin OK"
echo ""

echo "=== Installation terminée ! ==="
echo ""
echo "Pour démarrer les serveurs:"
echo "1. Backend: cd backend && python manage.py runserver"
echo "2. Frontend: cd frontend && npm run dev"
echo "3. Admin Backend: cd admin-backend && python manage.py runserver 8001"
echo "4. Admin Frontend: cd admin-frontend && npm run dev"
