#!/bin/bash

echo "========================================="
echo "ANALYSE DES CONNEXIONS HERBIER"
echo "========================================="
echo ""

echo "1. FICHIERS DE CONFIGURATION FRONTEND"
echo "----------------------------------------"

echo -e "\n📁 admin-frontend/src/services/api.js:"
if [ -f "admin-frontend/src/services/api.js" ]; then
    cat "admin-frontend/src/services/api.js"
else
    echo "❌ Fichier non trouvé"
fi

echo -e "\n📁 admin-frontend/.env:"
if [ -f "admin-frontend/.env" ]; then
    cat "admin-frontend/.env"
else
    echo "❌ Fichier non trouvé"
fi

echo -e "\n📁 admin-frontend/.env.production:"
if [ -f "admin-frontend/.env.production" ]; then
    cat "admin-frontend/.env.production"
else
    echo "❌ Fichier non trouvé"
fi

echo -e "\n📁 frontend/src/services/api.js:"
if [ -f "frontend/src/services/api.js" ]; then
    cat "frontend/src/services/api.js"
else
    echo "❌ Fichier non trouvé"
fi

echo -e "\n2. FICHIERS DE CONFIGURATION BACKEND"
echo "----------------------------------------"

echo -e "\n📁 admin-backend/admin_auth/settings.py (extrait CORS):"
if [ -f "admin-backend/admin_auth/settings.py" ]; then
    grep -A 10 "CORS" "admin-backend/admin_auth/settings.py"
else
    echo "❌ Fichier non trouvé"
fi

echo -e "\n📁 admin-backend/admin_auth/urls.py:"
if [ -f "admin-backend/admin_auth/urls.py" ]; then
    cat "admin-backend/admin_auth/urls.py"
else
    echo "❌ Fichier non trouvé"
fi

echo -e "\n📁 admin-backend/api/urls.py:"
if [ -f "admin-backend/api/urls.py" ]; then
    cat "admin-backend/api/urls.py"
else
    echo "❌ Fichier non trouvé"
fi

echo -e "\n📁 admin-backend/api/views.py (extrait create_superadmin):"
if [ -f "admin-backend/api/views.py" ]; then
    grep -A 20 "def create_superadmin" "admin-backend/api/views.py"
else
    echo "❌ Fichier non trouvé"
fi

echo -e "\n3. TEST DE CONNEXION"
echo "----------------------------------------"

echo -e "\n🔗 Test API health (local):"
curl -s http://localhost:8001/api/health/ 2>/dev/null || echo "❌ Serveur admin non démarré"

echo -e "\n🔗 Test API health (production):"
curl -s https://herbier-admin-backend.onrender.com/api/health/ 2>/dev/null || echo "❌ Serveur production inaccessible"

echo -e "\n4. RÉSUMÉ DES URLS"
echo "----------------------------------------"
echo "Local admin API: http://localhost:8001/api/"
echo "Production admin API: https://herbier-admin-backend.onrender.com/api/"
echo "Local frontend admin: http://localhost:5174"
echo "Production frontend admin: https://herbier-admin-frontend.onrender.com"

