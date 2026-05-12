from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone
import random
import string
import re

def validate_phone_number(value):
    phone_pattern = re.compile(r'^(\+225|0)?[0-9]{8,10}$')
    if not phone_pattern.match(value):
        raise ValueError('Numéro de téléphone invalide')
    return value

class SuperAdminManager(BaseUserManager):
    def create_user(self, email, nom, telephone, password=None, **extra_fields):
        if not email:
            raise ValueError('L\'email est obligatoire')
        if not telephone:
            raise ValueError('Le numéro de téléphone est obligatoire')
        
        email = self.normalize_email(email)
        user = self.model(email=email, nom=nom, telephone=telephone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, nom, telephone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, nom, telephone, password, **extra_fields)

class SuperAdmin(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Email")
    nom = models.CharField(max_length=200, verbose_name="Nom complet")
    telephone = models.CharField(max_length=20, unique=True, verbose_name="Numéro de téléphone", validators=[validate_phone_number])
    is_active = models.BooleanField(default=False, verbose_name="Compte actif")
    is_verified = models.BooleanField(default=False, verbose_name="Email vérifié")
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='created_users', verbose_name="Créé par")
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom', 'telephone']
    
    objects = SuperAdminManager()
    
    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
        ordering = ['-date_joined']
    
    def __str__(self):
        return f"{self.nom} - {self.email}"
    
    @property
    def is_super_admin(self):
        return self.is_superuser

class OTPCode(models.Model):
    user = models.ForeignKey(SuperAdmin, on_delete=models.CASCADE, related_name='otp_codes')
    code = models.CharField(max_length=6, verbose_name="Code OTP")
    type = models.CharField(max_length=20, choices=[('email', 'Email'), ('sms', 'SMS')], default='email')
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    
    def is_valid(self):
        return not self.is_used and self.expires_at > timezone.now()

class AuditLog(models.Model):
    ACTION_CHOICES = [
        ('create', 'Création'),
        ('update', 'Modification'),
        ('delete', 'Suppression'),
        ('login', 'Connexion'),
        ('logout', 'Déconnexion'),
    ]
    
    user = models.ForeignKey(SuperAdmin, on_delete=models.CASCADE, related_name='audit_logs')
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    model_name = models.CharField(max_length=100)
    object_id = models.IntegerField(null=True, blank=True)
    object_name = models.CharField(max_length=200, blank=True)
    changes = models.JSONField(default=dict, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Journal d'audit"
        verbose_name_plural = "Journaux d'audit"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.action} - {self.model_name}"

class HerbierData(models.Model):
    plantes = models.JSONField(default=list, verbose_name="Plantes")
    equipe = models.JSONField(default=list, verbose_name="Équipe")
    partenaires = models.JSONField(default=list, verbose_name="Partenaires")
    slides = models.JSONField(default=list, verbose_name="Slides")
    projets = models.JSONField(default=list, verbose_name="Projets")
    activites = models.JSONField(default=list, verbose_name="Activités")
    temoignages = models.JSONField(default=list, verbose_name="Témoignages")
    publications = models.JSONField(default=list, verbose_name="Publications")
    faqs = models.JSONField(default=list, verbose_name="FAQs")
    statistiques = models.JSONField(default=list, verbose_name="Statistiques")
    methodologie = models.JSONField(default=list, verbose_name="Méthodologie")
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(SuperAdmin, on_delete=models.SET_NULL, null=True, related_name='updates')
    
    class Meta:
        verbose_name = "Donnée Herbier"
        verbose_name_plural = "Données Herbier"
    
    @classmethod
    def get_current_data(cls):
        obj, created = cls.objects.get_or_create(id=1)
        return obj

class LoginHistory(models.Model):
    user = models.ForeignKey(SuperAdmin, on_delete=models.CASCADE, related_name='login_history')
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    login_time = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-login_time']
