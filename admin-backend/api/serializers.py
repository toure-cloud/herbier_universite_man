from rest_framework import serializers
from .models import SuperAdmin, OTPCode
import re

class SuperAdminCreateSerializer(serializers.Serializer):
    nom = serializers.CharField(max_length=200)
    email = serializers.EmailField()
    telephone = serializers.CharField(max_length=20)
    pays_code = serializers.CharField(max_length=10, default='+225')
    password = serializers.CharField(write_only=True, min_length=6)
    password2 = serializers.CharField(write_only=True)
    
    # Liste des pays supportés avec leurs longueurs
    COUNTRY_PHONE_LENGTHS = {
        '+225': 10, '+33': 9, '+221': 9, '+237': 9, '+223': 8, '+226': 8,
        '+224': 9, '+228': 8, '+229': 8, '+227': 8, '+241': 9, '+243': 9,
        '+212': 9, '+216': 8, '+213': 9, '+233': 9, '+234': 10, '+254': 9,
        '+27': 9, '+20': 10, '+32': 9, '+41': 9, '+352': 9, '+377': 8,
        '+49': 10, '+34': 9, '+39': 10, '+351': 9, '+44': 10, '+353': 9,
        '+31': 9, '+46': 9, '+47': 8, '+45': 8, '+358': 9, '+48': 9,
        '+420': 9, '+43': 9, '+30': 10, '+7': 10, '+1': 10, '+52': 10,
        '+55': 11, '+54': 10, '+56': 9, '+57': 10, '+86': 11, '+91': 10,
        '+81': 10, '+82': 10, '+61': 9
    }
    
    def validate_email(self, value):
        if SuperAdmin.objects.filter(email=value).exists():
            raise serializers.ValidationError("Cet email est déjà utilisé")
        return value
    
    def validate_telephone(self, value):
        # Supprimer les espaces et tirets
        value = re.sub(r'[\s\-]', '', value)
        if not value.isdigit():
            raise serializers.ValidationError("Le numéro de téléphone doit contenir uniquement des chiffres")
        return value
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Les mots de passe ne correspondent pas"})
        
        # Vérifier la longueur du téléphone selon le pays
        pays_code = attrs.get('pays_code', '+225')
        expected_length = self.COUNTRY_PHONE_LENGTHS.get(pays_code, 10)
        telephone = attrs.get('telephone', '')
        
        if len(telephone) != expected_length:
            raise serializers.ValidationError({
                "telephone": f"Le numéro doit contenir {expected_length} chiffres pour ce pays"
            })
        
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        telephone = validated_data.pop('telephone')
        
        user = SuperAdmin.objects.create_user(
            **validated_data,
            telephone=telephone
        )
        return user

class SuperAdminLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class OTPVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)

class SuperAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuperAdmin
        fields = ['id', 'email', 'nom', 'telephone', 'pays_code', 'date_joined', 'last_login']
        read_only_fields = ['id', 'date_joined', 'last_login']
