#!/bin/bash

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}=== Statut des serveurs ===${NC}"
echo ""

check_port() {
    local port=$1
    local name=$2
    if lsof -ti:$port > /dev/null 2>&1; then
        echo -e "${GREEN}✅ $name (port $port) - EN COURS${NC}"
    else
        echo -e "${RED}❌ $name (port $port) - ARRÊTÉ${NC}"
    fi
}

check_port 8000 "Backend public"
check_port 8001 "Admin backend"
check_port 5173 "Frontend public"
check_port 5174 "Admin frontend"

echo ""
echo -e "${YELLOW}Processus:${NC}"
ps aux | grep -E "python|npm|node" | grep -v grep | grep -E "manage.py|vite|dev" | awk '{print "  - " $11 " " $12 " " $13}'
