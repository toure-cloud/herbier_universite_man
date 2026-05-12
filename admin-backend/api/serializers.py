from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import SuperAdmin, OTPCode, HerbierData, LoginHistory, AuditLog
import re

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = SuperAdmin
        fields = ['id', 'email', 'nom', 'telephone', 'is_active', 'is_superuser', 'password', 'password2', 'created_by']
        read_only_fields = ['id', 'created_by']
    
    def validate_telephone(self, value):
        value = value.strip()
        phone_pattern = re.compile(r'^(\+225|0)?[0-9]{8,10}$')
        if not phone_pattern.match(value):
            raise serializers.ValidationError("Format de téléphone invalide")
        if SuperAdmin.objects.filter(telephone=value).exists():
            raise serializers.ValidationError("Ce numéro est déjà utilisé")
        return value
    
    def validate_email(self, value):
        if SuperAdmin.objects.filter(email=value).exists():
            raise serializers.ValidationError("Cet email est déjà utilisé")
        return value
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Les mots de passe ne correspondent pas"})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = SuperAdmin.objects.create_user(**validated_data)
        return user

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuperAdmin
        fields = ['id', 'email', 'nom', 'telephone', 'is_active', 'is_superuser']
        read_only_fields = ['id']

class UserListSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.nom', read_only=True)
    
    class Meta:
        model = SuperAdmin
        fields = ['id', 'email', 'nom', 'telephone', 'is_active', 'is_superuser', 'date_joined', 'last_login', 'created_by', 'created_by_name']

class AuditLogSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.nom', read_only=True)
    
    class Meta:
        model = AuditLog
        fields = '__all__'

class SuperAdminLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class OTPVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)

class HerbierDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = HerbierData
        fields = '__all__'
        read_only_fields = ['updated_at', 'updated_by']

class LoginHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginHistory
        fields = ['id', 'ip_address', 'user_agent', 'login_time', 'success']
