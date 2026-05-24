#!/bin/bash

echo "=== Démarrage des serveurs Herbier ==="

# Backend public
cd ~/Bureau/herbier_universite_man/backend
source venv/bin/activate
python manage.py runserver 8000 > /tmp/backend.log 2>&1 &
echo "✅ Backend public démarré (PID: $!) - http://localhost:8000"

# Backend admin
cd ~/Bureau/herbier_universite_man/admin-backend
source venv/bin/activate
python manage.py runserver 8001 > /tmp/admin-backend.log 2>&1 &
echo "✅ Admin backend démarré (PID: $!) - http://localhost:8001"

# Frontend public
cd ~/Bureau/herbier_universite_man/frontend
npm run dev > /tmp/frontend.log 2>&1 &
echo "✅ Frontend public démarré (PID: $!) - http://localhost:5173"

# Frontend admin
cd ~/Bureau/herbier_universite_man/admin-frontend
npm run dev -- --port 5174 > /tmp/admin-frontend.log 2>&1 &
echo "✅ Admin frontend démarré (PID: $!) - http://localhost:5174"

echo ""
echo "📍 Accès :"
echo "   - Site public: http://localhost:5173"
echo "   - API publique: http://localhost:8000/api"
echo "   - Admin frontend: http://localhost:5174"
echo "   - Admin API: http://localhost:8001/api"
echo ""
echo "📝 Logs :"
echo "   - tail -f /tmp/backend.log"
echo "   - tail -f /tmp/admin-backend.log"
echo ""
echo "Appuyez sur Ctrl+C pour arrêter"

wait
