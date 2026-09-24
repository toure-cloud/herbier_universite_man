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
    SuperAdmin, AuditLog,
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
    statut_conservation_label = serializers.CharField(
        source='get_statut_conservation_display',
        read_only=True
    )

    class Meta:
        model = Plante
        fields = [
            'id',
            'nom_scientifique', 'famille', 'nom_vernaculaire',
            'type_morphologique', 'type_biologique',
            'affinite_chorologique', 'affinite_ecologique',
            'statut_conservation', 'statut_conservation_label',
            'lieu_collecte', 'habitat', 'description',
            'image', 'images_galerie',
            'actif', 'date_creation',
        ]
        read_only_fields = ['id', 'date_creation']

    def validate_nom_scientifique(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Le nom scientifique est obligatoire")
        return value.strip()

    def create(self, validated_data):
        # Traiter les images de la galerie (gallery_0, gallery_1, ...)
        request = self.context.get('request')
        galerie_chemins = []

        if request and request.FILES:
            for key, fichier in request.FILES.items():
                if key.startswith('gallery_'):
                    # Sauvegarder le fichier dans media/plantes/galerie/
                    chemin = self._save_gallery_file(fichier)
                    if chemin:
                        galerie_chemins.append(chemin)

        if galerie_chemins:
            validated_data['images_galerie'] = galerie_chemins

        return super().create(validated_data)

    def update(self, instance, validated_data):
        request = self.context.get('request')

        # Galerie existante conservée (envoyée en JSON dans 'images_galerie_existing')
        existing_raw = request.data.get('images_galerie_existing') if request else None
        existing_list = []
        if existing_raw:
            try:
                import json
                existing_list = json.loads(existing_raw)
                if not isinstance(existing_list, list):
                    existing_list = []
            except (ValueError, TypeError):
                existing_list = []

        # Nouvelles images
        new_paths = []
        if request and request.FILES:
            for key, fichier in request.FILES.items():
                if key.startswith('gallery_'):
                    chemin = self._save_gallery_file(fichier)
                    if chemin:
                        new_paths.append(chemin)

        if existing_list or new_paths:
            validated_data['images_galerie'] = existing_list + new_paths

        return super().update(instance, validated_data)

    def _save_gallery_file(self, fichier):
        """Sauvegarde un fichier dans media/plantes/galerie/ et retourne son chemin relatif."""
        import os
        from django.core.files.storage import default_storage
        from django.core.files.base import ContentFile

        try:
            # Générer un nom de fichier unique
            import uuid
            ext = os.path.splitext(fichier.name)[1] or '.jpg'
            nom = f"plantes/galerie/{uuid.uuid4().hex}{ext}"

            # Sauvegarder
            chemin = default_storage.save(nom, ContentFile(fichier.read()))
            return f"/media/{chemin}"
        except Exception as e:
            import logging
            logging.getLogger(__name__).error(f"Erreur sauvegarde image galerie: {e}")
            return None

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
        fields = [
            'id', 'titre', 'categorie', 'statut',
            'annee', 'lieu', 'description', 'description_longue',
            'progression', 'partenaires_count', 'budget',
            'image', 'images_galerie',
        ]
        read_only_fields = ['id']

    def validate_titre(self, value):
        if not value or value.strip() == '':
            raise serializers.ValidationError("Le titre est obligatoire")
        return value.strip()

    def create(self, validated_data):
        # ✅ Toujours définir images_galerie (jamais None)
        if not validated_data.get('images_galerie'):
            validated_data['images_galerie'] = []

        # Traiter les images de la galerie envoyées en FormData
        request = self.context.get('request')
        galerie_chemins = list(validated_data.get('images_galerie', []))

        if request and request.FILES:
            # Image principale
            if 'image' in request.FILES:
                validated_data['image'] = request.FILES['image']

            # Galerie : accepte gallery_0, gallery_1, ... ou images_0, ...
            for key, fichier in request.FILES.items():
                if key == 'images' or key.startswith('gallery_') or key.startswith('images_'):
                    chemin = self._save_gallery_file(fichier)
                    if chemin:
                        galerie_chemins.append(chemin)

        validated_data['images_galerie'] = galerie_chemins
        return super().create(validated_data)

    def update(self, instance, validated_data):
        request = self.context.get('request')

        # Image principale
        if request and 'image' in request.FILES:
            validated_data['image'] = request.FILES['image']

        # Images existantes conservées (envoyées en JSON dans 'existing_images')
        existing_raw = request.data.get('existing_images') if request else None
        existing_list = []
        if existing_raw:
            try:
                import json
                existing_list = json.loads(existing_raw)
                if not isinstance(existing_list, list):
                    existing_list = []
            except (ValueError, TypeError):
                existing_list = []

        # Nouvelles images
        new_paths = []
        if request and request.FILES:
            for key, fichier in request.FILES.items():
                if key == 'images' or key.startswith('gallery_') or key.startswith('images_'):
                    chemin = self._save_gallery_file(fichier)
                    if chemin:
                        new_paths.append(chemin)

        # ✅ Toujours une liste (jamais None)
        if existing_list or new_paths or (request and 'existing_images' in request.data):
            validated_data['images_galerie'] = existing_list + new_paths
        elif 'images_galerie' in validated_data and validated_data['images_galerie'] is None:
            validated_data['images_galerie'] = []

        return super().update(instance, validated_data)

    def _save_gallery_file(self, fichier):
        """Sauvegarde dans media/projets/galerie/"""
        import os
        import uuid
        import logging
        from django.core.files.storage import default_storage
        from django.core.files.base import ContentFile

        try:
            ext = os.path.splitext(fichier.name)[1] or '.jpg'
            nom = f"projets/galerie/{uuid.uuid4().hex}{ext}"
            chemin = default_storage.save(nom, ContentFile(fichier.read()))
            return f"/media/{chemin}"
        except Exception as e:
            logging.getLogger(__name__).error(f"Erreur sauvegarde galerie projet: {e}")
            return None
        return value.strip()

class ActiviteSerializer(FileUploadMixin, serializers.ModelSerializer):
    class Meta:
        model = Activite
        fields = [
            'id', 'titre', 'titre_court',
            'description_courte', 'description_longue',
            'icon', 'image', 'images_galerie',
            'caption', 'points_forts',
            'ordre', 'actif',
        ]
        read_only_fields = ['id']

    def validate_titre(self, value):
        if not value or value.strip() == '':
            raise serializers.ValidationError("Le titre est obligatoire")
        return value.strip()

    def create(self, validated_data):
        # Traiter les images multiples envoyées en FormData (images_0, images_1, ...)
        request = self.context.get('request')
        galerie_chemins = []

        if request and request.FILES:
            for key, fichier in request.FILES.items():
                # Accepte "images" ou "images_0", "images_1", etc.
                if key == 'images' or key.startswith('images_'):
                    chemin = self._save_gallery_file(fichier)
                    if chemin:
                        galerie_chemins.append(chemin)

        if galerie_chemins:
            validated_data['images_galerie'] = galerie_chemins

        return super().create(validated_data)

    def update(self, instance, validated_data):
        request = self.context.get('request')

        # Images existantes conservées (envoyées en JSON dans 'existing_images')
        existing_raw = request.data.get('existing_images') if request else None
        existing_list = []
        if existing_raw:
            try:
                import json
                existing_list = json.loads(existing_raw)
                if not isinstance(existing_list, list):
                    existing_list = []
            except (ValueError, TypeError):
                existing_list = []

        # Nouvelles images
        new_paths = []
        if request and request.FILES:
            for key, fichier in request.FILES.items():
                if key == 'images' or key.startswith('images_'):
                    chemin = self._save_gallery_file(fichier)
                    if chemin:
                        new_paths.append(chemin)

        # Si l'admin a touché à la galerie (nouvelles images OU suppression)
        if existing_list or new_paths or 'existing_images' in request.data:
            validated_data['images_galerie'] = existing_list + new_paths

        return super().update(instance, validated_data)

    def _save_gallery_file(self, fichier):
        """Sauvegarde un fichier dans media/activites/galerie/"""
        import os
        import uuid
        import logging
        from django.core.files.storage import default_storage
        from django.core.files.base import ContentFile

        try:
            ext = os.path.splitext(fichier.name)[1] or '.jpg'
            nom = f"activites/galerie/{uuid.uuid4().hex}{ext}"
            chemin = default_storage.save(nom, ContentFile(fichier.read()))
            return f"/media/{chemin}"
        except Exception as e:
            logging.getLogger(__name__).error(f"Erreur sauvegarde image galerie activité: {e}")
            return None

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
    
    # ==================== SERIALIZER AUDIT ====================

class AuditLogSerializer(serializers.ModelSerializer):
    user_nom = serializers.CharField(source='user.nom', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)
    action_label = serializers.CharField(source='get_action_display', read_only=True)

    class Meta:
        model = AuditLog
        fields = [
            'id', 'user', 'user_nom', 'user_email',
            'action', 'action_label',
            'model_name', 'object_id', 'object_repr',
            'details', 'ip_address', 'user_agent', 'created_at',
        ]
        read_only_fields = fields