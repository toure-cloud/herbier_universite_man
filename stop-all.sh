#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

echo "=== Arrêt de tous les serveurs ==="

LOG_DIR="$HOME/Bureau/herbier_universite_man/logs"

# Arrêter les processus via les fichiers PID
if [ -d "$LOG_DIR" ]; then
    for pid_file in $LOG_DIR/*.pid; do
        if [ -f "$pid_file" ]; then
            pid=$(cat "$pid_file")
            service_name=$(basename "$pid_file" .pid)
            if kill -0 $pid 2>/dev/null; then
                kill $pid
                echo -e "${GREEN}✓ $service_name arrêté${NC}"
            else
                echo "⚠️ $service_name n'était pas en cours d'exécution"
            fi
            rm -f "$pid_file"
        fi
    done
fi

# Arrêter les processus restants
pkill -f "python manage.py runserver" 2>/dev/null
pkill -f "npm run dev" 2>/dev/null
pkill -f "vite" 2>/dev/null

echo -e "${GREEN}✅ Tous les serveurs sont arrêtés${NC}"
