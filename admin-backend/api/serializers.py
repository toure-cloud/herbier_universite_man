from rest_framework import serializers
from .models import SuperAdmin

class SuperAdminCreateSerializer(serializers.Serializer):
    nom = serializers.CharField(max_length=200)
    email = serializers.EmailField()
    telephone = serializers.CharField(max_length=20)
    pays_code = serializers.CharField(max_length=10, default='+225')
    password = serializers.CharField(write_only=True, min_length=6)
    password2 = serializers.CharField(write_only=True)
    
    def validate_email(self, value):
        # Vérifier si l'email existe déjà
        if SuperAdmin.objects.filter(email=value).exists():
            raise serializers.ValidationError("Cet email est déjà utilisé. Veuillez en utiliser un autre.")
        return value
    
    def validate_telephone(self, value):
        # Nettoyer le téléphone
        value = re.sub(r'\D', '', value)
        
        # Vérifier la longueur
        if len(value) < 8 or len(value) > 12:
            raise serializers.ValidationError("Le numéro de téléphone doit contenir entre 8 et 12 chiffres.")
        
        # Vérifier si le téléphone existe déjà
        if SuperAdmin.objects.filter(telephone=value).exists():
            raise serializers.ValidationError("Ce numéro de téléphone est déjà utilisé. Veuillez en utiliser un autre.")
        
        return value
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Les mots de passe ne correspondent pas."})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        telephone = validated_data.pop('telephone')
        user = SuperAdmin.objects.create_user(
            **validated_data,
            telephone=telephone
        )
        return user

class SuperAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuperAdmin
        fields = ['id', 'email', 'nom', 'telephone', 'pays_code', 'date_joined', 'last_login']
        read_only_fields = ['id', 'date_joined', 'last_login']

