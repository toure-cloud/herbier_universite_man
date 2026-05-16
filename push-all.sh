#!/bin/bash

echo "=== Push vers GitHub ==="
echo ""

cd ~/Bureau/herbier_universite_man

# Vérifier les modifications
echo "1. Vérification des fichiers modifiés..."
git status -s

echo ""
echo "2. Ajout de tous les fichiers..."
git add .

echo ""
echo "3. Création du commit..."
DATE=$(date '+%Y-%m-%d %H:%M:%S')
git commit -m "Mise à jour $DATE"

echo ""
echo "4. Push vers GitHub..."
git push origin main

echo ""
echo "✅ Push terminé avec succès !"
echo ""
echo "🌐 Voir sur GitHub: https://github.com/toure-cloud/herbier_universite_man"
