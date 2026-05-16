from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

class SuperAdminManager(BaseUserManager):
    def create_user(self, email, nom, telephone, password=None, **extra_fields):
        if not email:
            raise ValueError('L\'email est obligatoire')
        if not telephone:
            raise ValueError('Le numéro de téléphone est obligatoire')
        if not nom:
            raise ValueError('Le nom est obligatoire')
        
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

class SuperAdmin(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name="Email")
    nom = models.CharField(max_length=200, verbose_name="Nom complet")
    telephone = models.CharField(max_length=20, verbose_name="Numéro de téléphone")
    pays_code = models.CharField(max_length=10, default='+225', verbose_name="Code pays")
    is_active = models.BooleanField(default=False, verbose_name="Compte actif")
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True, blank=True)
    
    # Ajouter related_name pour éviter les conflits
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='superadmin_set',
        related_query_name='superadmin',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='superadmin_set',
        related_query_name='superadmin',
    )
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom', 'telephone']
    
    objects = SuperAdminManager()
    
    class Meta:
        verbose_name = "Super Administrateur"
        verbose_name_plural = "Super Administrateurs"
    
    def __str__(self):
        return f"{self.nom} - {self.email}"
    
    def get_full_telephone(self):
        return f"{self.pays_code}{self.telephone}"

class OTPCode(models.Model):
    user = models.ForeignKey(SuperAdmin, on_delete=models.CASCADE, related_name='otp_codes')
    code = models.CharField(max_length=6)
    type = models.CharField(max_length=20, choices=[('email', 'Email'), ('sms', 'SMS')], default='email')
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"OTP pour {self.user.email} - {self.code}"
    
    def is_valid(self):
        return not self.is_used and self.expires_at > timezone.now()

class APICache(models.Model):
    endpoint = models.CharField(max_length=200, unique=True)
    data = models.JSONField()
    last_update = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.endpoint

class APISyncLog(models.Model):
    action = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=[('SUCCESS', 'Succès'), ('ERROR', 'Erreur')])
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.action} - {self.status} - {self.created_at}"
