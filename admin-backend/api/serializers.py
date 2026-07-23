# api/serializers.py
import os
import uuid
import re

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from rest_framework import serializers
from .models import (
    Partenaire, Plante, Equipe, Slide, Projet, Activite, 
    Temoignage, Publication, FAQ, Statistique, Methodologie,
    SuperAdmin
)

# ==================== SERIALIZERS DES MODÈLES ====================

class FileUploadMixin:
    image_fields = ('image', 'photo', 'logo')

    def _normalize_media_url(self, value):
        """Normalise l'URL du média"""
        if not value:
            return ''
        
        if isinstance(value, str) and value.startswith(('http://', 'https://', 'data:')):
            return value
        
        if isinstance(value, str) and value.startswith(('media/', '/media/')):
            if self.context.get('request'):
                return self.context['request'].build_absolute_uri('/' + value.lstrip('/'))
            base_url = getattr(settings, 'MEDIA_BASE_URL', None) or getattr(settings, 'BASE_URL', None) or 'http://localhost:8001'
            return f"{base_url.rstrip('/')}/{value.lstrip('/')}"
        
        return value

    def to_internal_value(self, data):
        """Convertit les données entrantes en données internes"""
        if not data:
            return {}
        
        # Gérer QueryDict (multipart/form-data)
        if hasattr(data, 'dict'):
            payload = data.dict()
        elif hasattr(data, 'copy'):
            payload = data.copy()
        elif isinstance(data, dict):
            payload = data.copy()
        else:
            return super().to_internal_value(data)

        processed_data = {}
        
        for key, value in payload.items():
            # ✅ Passer les fichiers tels quels - DRF utilisera upload_to du modèle
            if key in self.image_fields and hasattr(value, 'read') and hasattr(value, 'size'):
                if getattr(value, 'size', 0) > 0:
                    processed_data[key] = value
                else:
                    continue
            else:
                processed_data[key] = value

        return super().to_internal_value(processed_data)

    def to_representation(self, instance):
        """Convertit les URLs des images en URLs absolues"""
        data = super().to_representation(instance)
        request = self.context.get('request')
        
        for field in self.image_fields:
            if field in data and data[field]:
                if isinstance(data[field], str) and not data[field].startswith(('http://', 'https://', 'data:')):
                    if request:
                        data[field] = request.build_absolute_uri(data[field])
                    else:
                        base_url = getattr(settings, 'BASE_URL', 'http://localhost:8001')
                        data[field] = f"{base_url.rstrip('/')}{data[field]}"
        
        return data


# ==================== SERIALIZERS SPÉCIFIQUES ====================

class PlanteSerializer(FileUploadMixin, serializers.ModelSerializer):
    class Meta:
        model = Plante
        fields = ['id', 'nom', 'famille', 'nom_scientifique', 'description', 
                  'habitat', 'statut_conservation', 'image', 'actif', 'date_creation']
        read_only_fields = ['id', 'date_creation']
    
    def validate_nom(self, value):
        if not value or value.strip() == '':
            raise serializers.ValidationError("Le nom est obligatoire")
        return value.strip()
    
    def validate(self, data):
        if not data.get('nom'):
            raise serializers.ValidationError({"nom": "Le nom est obligatoire"})
        return data


class EquipeSerializer(FileUploadMixin, serializers.ModelSerializer):
    class Meta:
        model = Equipe
        fields = ['id', 'nom', 'poste', 'email', 'specialite', 'photo', 'ordre', 'actif']
        read_only_fields = ['id']
    
    def validate_nom(self, value):
        if not value or value.strip() == '':
            raise serializers.ValidationError("Le nom est obligatoire")
        return value.strip()
    
    def validate_poste(self, value):
        if not value or value.strip() == '':
            raise serializers.ValidationError("Le poste est obligatoire")
        return value.strip()


class SlideSerializer(FileUploadMixin, serializers.ModelSerializer):
    class Meta:
        model = Slide
        fields = ['id', 'titre', 'texte_botanique', 'image', 'ordre', 'actif']
        read_only_fields = ['id']
    
    def validate_titre(self, value):
        if not value or value.strip() == '':
            raise serializers.ValidationError("Le titre est obligatoire")
        return value.strip()
    
    def validate_texte_botanique(self, value):
        if not value or value.strip() == '':
            raise serializers.ValidationError("Le texte botanique est obligatoire")
        return value.strip()


class ProjetSerializer(FileUploadMixin, serializers.ModelSerializer):
    class Meta:
        model = Projet
        fields = ['id', 'titre', 'categorie', 'statut', 'annee', 'lieu', 'description', 'image']
        read_only_fields = ['id']
    
    def validate_titre(self, value):
        if not value or value.strip() == '':
            raise serializers.ValidationError("Le titre est obligatoire")
        return value.strip()


class ActiviteSerializer(FileUploadMixin, serializers.ModelSerializer):
    class Meta:
        model = Activite
        fields = ['id', 'titre', 'titre_court', 'description_courte', 
                  'description_longue', 'icon', 'image', 'ordre', 'actif']
        read_only_fields = ['id']
    
    def validate_titre(self, value):
        if not value or value.strip() == '':
            raise serializers.ValidationError("Le titre est obligatoire")
        return value.strip()
    
    def validate_titre_court(self, value):
        if not value or value.strip() == '':
            raise serializers.ValidationError("Le titre court est obligatoire")
        return value.strip()
    
    def validate_description_courte(self, value):
        if not value or value.strip() == '':
            raise serializers.ValidationError("La description courte est obligatoire")
        return value.strip()
    
    def validate(self, data):
        required_fields = ['titre', 'titre_court', 'description_courte']
        for field in required_fields:
            if not data.get(field):
                raise serializers.ValidationError({field: f"Le champ {field} est obligatoire"})
        return data


class TemoignageSerializer(FileUploadMixin, serializers.ModelSerializer):
    class Meta:
        model = Temoignage
        fields = ['id', 'nom', 'poste', 'organisation', 'texte', 'photo', 'note', 'ordre', 'actif']
        read_only_fields = ['id']
    
    def validate_nom(self, value):
        if not value or value.strip() == '':
            raise serializers.ValidationError("Le nom est obligatoire")
        return value.strip()
    
    def validate_texte(self, value):
        if not value or value.strip() == '':
            raise serializers.ValidationError("Le texte est obligatoire")
        return value.strip()


class PublicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publication
        fields = ['id', 'titre', 'auteurs', 'journal', 'annee', 'lien', 'actif']
        read_only_fields = ['id']
    
    def validate_titre(self, value):
        if not value or value.strip() == '':
            raise serializers.ValidationError("Le titre est obligatoire")
        return value.strip()
    
    def validate_auteurs(self, value):
        if not value or value.strip() == '':
            raise serializers.ValidationError("Les auteurs sont obligatoires")
        return value.strip()
    
    def validate_annee(self, value):
        if not value:
            raise serializers.ValidationError("L'année est obligatoire")
        if value < 1900 or value > 2100:
            raise serializers.ValidationError("L'année doit être entre 1900 et 2100")
        return value


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['id', 'question', 'reponse', 'ordre', 'actif']
        read_only_fields = ['id']
    
    def validate_question(self, value):
        if not value or value.strip() == '':
            raise serializers.ValidationError("La question est obligatoire")
        return value.strip()
    
    def validate_reponse(self, value):
        if not value or value.strip() == '':
            raise serializers.ValidationError("La réponse est obligatoire")
        return value.strip()


class StatistiqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statistique
        fields = ['id', 'titre', 'valeur', 'unite', 'icon', 'ordre', 'actif']
        read_only_fields = ['id']
    
    def validate_titre(self, value):
        if not value or value.strip() == '':
            raise serializers.ValidationError("Le titre est obligatoire")
        return value.strip()
    
    def validate_valeur(self, value):
        if not value or value.strip() == '':
            raise serializers.ValidationError("La valeur est obligatoire")
        return value.strip()


class MethodologieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Methodologie
        fields = ['id', 'titre', 'description', 'icon', 'ordre', 'actif']
        read_only_fields = ['id']
    
    def validate_titre(self, value):
        if not value or value.strip() == '':
            raise serializers.ValidationError("Le titre est obligatoire")
        return value.strip()
    
    def validate_description(self, value):
        if not value or value.strip() == '':
            raise serializers.ValidationError("La description est obligatoire")
        return value.strip()


# ==================== SERIALIZERS POUR L'AUTHENTIFICATION ====================

class SuperAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuperAdmin
        fields = ['id', 'email', 'nom', 'telephone', 'pays_code', 'role', 'is_active', 
                  'is_staff', 'is_superuser', 'date_joined', 'last_login']
        read_only_fields = ['id', 'date_joined', 'last_login', 'is_staff', 'is_superuser']


class SuperAdminCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = SuperAdmin
        fields = ['id', 'email', 'nom', 'telephone', 'pays_code', 'role', 'password', 'password2']
        read_only_fields = ['id']
    
    def validate(self, data):
        if data.get('password') != data.get('password2'):
            raise serializers.ValidationError({"password": "Les mots de passe ne correspondent pas"})
        
        if SuperAdmin.objects.filter(email=data.get('email')).exists():
            raise serializers.ValidationError({"email": "Cet email est déjà utilisé"})
        
        return data
    
    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = SuperAdmin(**validated_data)
        user.set_password(password)
        user.save()
        return user


class PartenaireSerializer(FileUploadMixin, serializers.ModelSerializer):
    class Meta:
        model = Partenaire
        fields = ['id', 'nom', 'description', 'logo', 'site_web', 'type', 'ordre', 'actif']
        read_only_fields = ['id']
    
    def validate_nom(self, value):
        if not value or value.strip() == '':
            raise serializers.ValidationError("Le nom est obligatoire")
        return value.strip()