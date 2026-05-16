#!/bin/bash

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}    Herbier Université de Man - Déploiement    ${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Fonction pour afficher les étapes
step() {
    echo -e "${GREEN}➜ $1${NC}"
}

# Fonction pour afficher les erreurs
error() {
    echo -e "${RED}✗ $1${NC}"
}

# Fonction pour afficher les succès
success() {
    echo -e "${GREEN}✓ $1${NC}"
}

# ============================================
# ÉTAPE 1: Push vers GitHub
# ============================================
step "1. Push vers GitHub"

cd ~/Bureau/herbier_universite_man

# Vérifier les modifications
if [[ -n $(git status -s) ]]; then
    echo "   Modifications détectées :"
    git status -s
    echo ""
    
    # Demander le message de commit
    read -p "   Message de commit (ou Entrée pour auto): " commit_msg
    if [[ -z "$commit_msg" ]]; then
        commit_msg="Mise à jour $(date '+%Y-%m-%d %H:%M:%S')"
    fi
    
    # Ajouter et committer
    git add .
    git commit -m "$commit_msg"
    echo "   ✅ Commit effectué"
    
    # Pousser vers GitHub
    git push origin main
    echo "   ✅ Push vers GitHub effectué"
else
    echo "   Aucune modification à pousser"
fi

echo ""

# ============================================
# ÉTAPE 2: Déploiement sur Render (CLI)
# ============================================
step "2. Déploiement sur Render"

# Vérifier si render CLI est installé
if ! command -v render &> /dev/null; then
    echo "   ⚠️ Render CLI non installé"
    echo "   Pour l'installer: npm install -g @render/cli"
    echo "   Déploiement manuel requis sur dashboard.render.com"
else
    # Déployer le backend public
    echo "   Déploiement du backend public..."
    cd ~/Bureau/herbier_universite_man/backend
    render deploy --name herbier-backend || echo "   ⚠️ Déploiement backend manuel requis"
    
    # Déployer le frontend public
    echo "   Déploiement du frontend public..."
    cd ~/Bureau/herbier_universite_man/frontend
    render deploy --name herbier-frontend || echo "   ⚠️ Déploiement frontend manuel requis"
fi

echo ""

# ============================================
# ÉTAPE 3: Démarrer les serveurs locaux
# ============================================
step "3. Démarrage des serveurs locaux"

# Créer un fichier de logs
LOG_DIR="$HOME/Bureau/herbier_universite_man/logs"
mkdir -p $LOG_DIR

# Fonction pour démarrer un serveur
start_server() {
    local name=$1
    local cmd=$2
    local log_file="$LOG_DIR/$name.log"
    
    echo "   Démarrage de $name..."
    eval "$cmd > $log_file 2>&1 &"
    echo $! > "$LOG_DIR/$name.pid"
    sleep 2
    if ps -p $(cat "$LOG_DIR/$name.pid") > /dev/null 2>&1; then
        success "   $name démarré (PID: $(cat "$LOG_DIR/$name.pid"))"
    else
        error "   $name n'a pas démarré, vérifiez $log_file"
    fi
}

# Démarrer les serveurs
start_server "backend_public" "cd ~/Bureau/herbier_universite_man/backend && source venv/bin/activate && python manage.py runserver 8000"
sleep 2

start_server "backend_admin" "cd ~/Bureau/herbier_universite_man/admin-backend && source venv/bin/activate && python manage.py runserver 8001"
sleep 2

start_server "frontend_public" "cd ~/Bureau/herbier_universite_man/frontend && npm run dev"
sleep 2

start_server "frontend_admin" "cd ~/Bureau/herbier_universite_man/admin-frontend && npm run dev -- --port 5174"

echo ""

# ============================================
# RÉCAPITULATIF
# ============================================
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}✅ Tous les serveurs sont démarrés !${NC}"
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
echo "      - Site public: https://herbier-universite-man.onrender.com"
echo "      - API publique: https://herbier-universite-man.onrender.com/api/"
echo ""
echo -e "${YELLOW}📝 Logs : $LOG_DIR/${NC}"
echo ""
echo -e "${BLUE}Commandes utiles :${NC}"
echo "   - Voir les processus: ps aux | grep -E 'python|npm|node'"
echo "   - Arrêter tous les serveurs: ./stop-all.sh"
echo "   - Voir les logs: tail -f $LOG_DIR/nom_du_service.log"
echo ""
echo -e "${YELLOW}Appuyez sur Ctrl+C pour arrêter les serveurs${NC}"
echo ""

# Attendre l'interruption
wait
