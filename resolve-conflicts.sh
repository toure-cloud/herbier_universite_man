#!/bin/bash

echo "=== Résolution des conflits Git ==="

# Abandonner tout rebase en cours
git rebase --abort 2>/dev/null

# Revenir à l'état précédent
git reset --hard HEAD

# Supprimer le dossier problématique
rm -rf herbier_universite_man

# Ajouter tous les fichiers
git add .

# Committer si nécessaire
git commit -m "Version complète du projet Herbier Universite de Man" || echo "Déjà commit"

# Forcer le push
echo "Push forcé vers GitHub..."
git push origin main --force-with-lease

echo ""
echo "=== Vérification ==="
git status
echo ""
echo "✅ Terminé !"
