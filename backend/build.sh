#!/bin/bash
echo "🔨 Build du backend public..."

# Installer les dépendances
pip install -r requirements.txt

# Appliquer les migrations
python manage.py makemigrations --noinput
python manage.py migrate --noinput

# Collecter les fichiers statiques
python manage.py collectstatic --noinput

echo "✅ Build terminé !"
