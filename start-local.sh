#!/bin/bash

GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo "=== Démarrage des serveurs locaux ==="

LOG_DIR="$HOME/Bureau/herbier_universite_man/logs"
mkdir -p $LOG_DIR

start_server() {
    local name=$1
    local cmd=$2
    local log_file="$LOG_DIR/$name.log"
    
    echo "   Démarrage de $name..."
    eval "$cmd > $log_file 2>&1 &"
    echo $! > "$LOG_DIR/$name.pid"
    sleep 2
}

# Arrêter les serveurs existants
pkill -f "python manage.py runserver" 2>/dev/null
pkill -f "npm run dev" 2>/dev/null
sleep 2

# Démarrer les serveurs
start_server "backend_public" "cd ~/Bureau/herbier_universite_man/backend && source venv/bin/activate && python manage.py runserver 8000"
start_server "backend_admin" "cd ~/Bureau/herbier_universite_man/admin-backend && source venv/bin/activate && python manage.py runserver 8001"
start_server "frontend_public" "cd ~/Bureau/herbier_universite_man/frontend && npm run dev"
start_server "frontend_admin" "cd ~/Bureau/herbier_universite_man/admin-frontend && npm run dev -- --port 5174"

echo ""
echo -e "${GREEN}✅ Serveurs démarrés${NC}"
echo ""
echo -e "${BLUE}📍 Accès :${NC}"
echo "   - Site public: http://localhost:5173"
echo "   - API publique: http://localhost:8000/api/"
echo "   - Admin frontend: http://localhost:5174"
echo "   - Admin API: http://localhost:8001/api/"
echo ""
echo -e "${BLUE}Pour arrêter : ./stop-all.sh${NC}"
