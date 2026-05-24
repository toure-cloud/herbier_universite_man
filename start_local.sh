#!/bin/bash

echo "=== Démarrage de l'environnement de développement ==="

# Backend public
cd ~/Bureau/herbier_universite_man/backend
source venv/bin/activate
export DJANGO_SETTINGS_MODULE=herbier_backend.settings
python manage.py runserver 8000 &
BACKEND_PID=$!
echo "✅ Backend démarré sur http://localhost:8000"

# Backend admin
cd ~/Bureau/herbier_universite_man/admin-backend
source venv/bin/activate
python manage.py runserver 8001 &
ADMIN_BACKEND_PID=$!
echo "✅ Admin backend démarré sur http://localhost:8001"

# Frontend public
cd ~/Bureau/herbier_universite_man/frontend
npm run dev &
FRONTEND_PID=$!
echo "✅ Frontend démarré sur http://localhost:5173"

# Frontend admin
cd ~/Bureau/herbier_universite_man/admin-frontend
npm run dev -- --port 5174 &
ADMIN_FRONTEND_PID=$!
echo "✅ Admin frontend démarré sur http://localhost:5174"

echo ""
echo "📍 Accès :"
echo "   - Site public: http://localhost:5173"
echo "   - API publique: http://localhost:8000/api"
echo "   - Admin frontend: http://localhost:5174"
echo "   - Admin API: http://localhost:8001/api"
echo ""
echo "Appuyez sur Ctrl+C pour arrêter tous les serveurs"

wait
