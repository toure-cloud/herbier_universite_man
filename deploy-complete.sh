#!/bin/bash

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}   Déploiement complet Herbier${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

cd ~/Bureau/herbier_universite_man

# 1. Push vers GitHub
echo -e "${YELLOW}1. Push vers GitHub...${NC}"
git add .
git commit -m "Déploiement $(date '+%Y-%m-%d %H:%M:%S')"
git push origin main
echo -e "${GREEN}✅ Push effectué${NC}"
echo ""

# 2. Démarrage des serveurs locaux (optionnel)
echo -e "${YELLOW}2. Démarrage des serveurs locaux...${NC}"

# Arrêter les serveurs existants
pkill -f "python manage.py runserver" 2>/dev/null
pkill -f "npm run dev" 2>/dev/null
pkill -f "vite" 2>/dev/null
sleep 2

# Démarrer backend public
cd ~/Bureau/herbier_universite_man/backend
source venv/bin/activate
python manage.py runserver 8000 > /tmp/backend.log 2>&1 &
BACKEND_PID=$!
echo -e "${GREEN}   ✅ Backend public démarré (PID: $BACKEND_PID) - http://localhost:8000${NC}"

# Démarrer backend admin
cd ~/Bureau/herbier_universite_man/admin-backend
source venv/bin/activate
python manage.py runserver 8001 > /tmp/admin-backend.log 2>&1 &
ADMIN_BACKEND_PID=$!
echo -e "${GREEN}   ✅ Admin backend démarré (PID: $ADMIN_BACKEND_PID) - http://localhost:8001${NC}"

# Démarrer frontend public
cd ~/Bureau/herbier_universite_man/frontend
npm run dev > /tmp/frontend.log 2>&1 &
FRONTEND_PID=$!
echo -e "${GREEN}   ✅ Frontend public démarré (PID: $FRONTEND_PID) - http://localhost:5173${NC}"

# Démarrer frontend admin
cd ~/Bureau/herbier_universite_man/admin-frontend
npm run dev -- --port 5174 > /tmp/admin-frontend.log 2>&1 &
ADMIN_FRONTEND_PID=$!
echo -e "${GREEN}   ✅ Admin frontend démarré (PID: $ADMIN_FRONTEND_PID) - http://localhost:5174${NC}"

echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}✅ Déploiement terminé avec succès !${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "${YELLOW}📍 Accès aux services :${NC}"
echo ""
echo -e "   🌿 ${GREEN}SITE PUBLIC${NC}"
echo "      - Frontend: http://localhost:5173"
echo "      - API: http://localhost:8000/api/"
echo "      - Admin Django: http://localhost:8000/admin"
echo ""
echo -e "   🔧 ${GREEN}ADMINISTRATION${NC}"
echo "      - Frontend Admin: http://localhost:5174"
echo "      - API Admin: http://localhost:8001/api/"
echo ""
echo -e "   ☁️ ${GREEN}RENDER (Production)${NC}"
echo "      - Site public: https://herbier-frontend.onrender.com"
echo "      - API publique: https://herbier-backend.onrender.com/api/"
echo "      - Admin frontend: https://herbier-admin-frontend.onrender.com"
echo "      - Admin API: https://herbier-admin-backend.onrender.com/api/"
echo ""
echo -e "${YELLOW}📝 Pour arrêter tous les serveurs : ./stop-all.sh${NC}"
echo ""

# Sauvegarder les PIDs
echo "$BACKEND_PID" > /tmp/backend.pid
echo "$ADMIN_BACKEND_PID" > /tmp/admin-backend.pid
echo "$FRONTEND_PID" > /tmp/frontend.pid
echo "$ADMIN_FRONTEND_PID" > /tmp/admin-frontend.pid

