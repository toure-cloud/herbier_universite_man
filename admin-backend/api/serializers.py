from rest_framework import serializers
from .models import SuperAdmin

class SuperAdminCreateSerializer(serializers.Serializer):
    nom = serializers.CharField(max_length=200)
    email = serializers.EmailField()
    telephone = serializers.CharField(max_length=20)
    pays_code = serializers.CharField(max_length=10, default='+225')
    password = serializers.CharField(write_only=True, min_length=6)
    password2 = serializers.CharField(write_only=True)
    role = serializers.CharField(max_length=20, default='admin')
    
    def validate_email(self, value):
        if SuperAdmin.objects.filter(email=value).exists():
            raise serializers.ValidationError("Cet email est déjà utilisé")
        return value
    
    def validate_telephone(self, value):
        import re
        value = re.sub(r'[\s\-]', '', value)
        if not value.isdigit():
            raise serializers.ValidationError("Le numéro doit contenir uniquement des chiffres")
        if len(value) < 8 or len(value) > 12:
            raise serializers.ValidationError("Le numéro doit contenir entre 8 et 12 chiffres")
        return value
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Les mots de passe ne correspondent pas"})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        telephone = validated_data.pop('telephone')
        role = validated_data.pop('role', 'admin')
        user = SuperAdmin.objects.create_user(
            **validated_data,
            telephone=telephone,
            role=role
        )
        return user

class SuperAdminUpdateSerializer(serializers.Serializer):
    nom = serializers.CharField(max_length=200, required=False)
    telephone = serializers.CharField(max_length=20, required=False)
    pays_code = serializers.CharField(max_length=10, required=False)
    role = serializers.CharField(max_length=20, required=False)
    is_active = serializers.BooleanField(required=False)
    
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class SuperAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuperAdmin
        fields = ['id', 'email', 'nom', 'telephone', 'pays_code', 'role', 'is_active', 'date_joined', 'last_login']
        read_only_fields = ['id', 'date_joined', 'last_login', 'email']
