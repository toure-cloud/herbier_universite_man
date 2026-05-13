#!/bin/bash

echo "=== Correction du build Railway ==="

# 1. Créer le Dockerfile
cat > Dockerfile.railway << 'DOCKER'
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .

RUN mkdir -p staticfiles media
RUN python manage.py collectstatic --noinput || true

EXPOSE 8000

CMD ["gunicorn", "herbier_backend.wsgi:application", "--bind", "0.0.0.0:8000"]
DOCKER

# 2. Créer railway.json avec Docker builder
cat > railway.json << 'RAILWAY'
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "DOCKERFILE",
    "dockerfilePath": "Dockerfile.railway"
  }
}
RAILWAY

# 3. Simplifier requirements.txt
cat > backend/requirements.txt << 'REQUIREMENTS'
Django
djangorestframework
django-cors-headers
Pillow
whitenoise
gunicorn
psycopg2-binary
django-storages
boto3
REQUIREMENTS

echo "✅ Fichiers mis à jour"
echo ""
echo "Poussez ces changements sur GitHub:"
echo "  git add ."
echo "  git commit -m 'Fix: Passage à Docker builder'"
echo "  git push origin main"
echo ""
echo "Ensuite, sur Railway:"
echo "  1. Allez dans Settings du projet"
echo "  2. Changez le Builder de 'Nixpacks' à 'Dockerfile'"
echo "  3. Redéployez"
