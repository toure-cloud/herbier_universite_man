from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone

class SuperAdminManager(models.Manager):
    def create_user(self, email, nom, telephone, password=None, **extra_fields):
        if not email:
            raise ValueError('L\'email est obligatoire')
        if not telephone:
            raise ValueError('Le numéro de téléphone est obligatoire')
        if not nom:
            raise ValueError('Le nom est obligatoire')
        
        user = self.model(
            email=email.lower(),
            nom=nom,
            telephone=telephone,
            **extra_fields
        )
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, nom, telephone, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, nom, telephone, password, **extra_fields)

class SuperAdmin(models.Model):
    email = models.EmailField(unique=True)
    nom = models.CharField(max_length=200)
    telephone = models.CharField(max_length=20)
    pays_code = models.CharField(max_length=10, default='+225')
    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom', 'telephone']
    
    objects = SuperAdminManager()
    
    class Meta:
        db_table = 'super_admin'
    
    def __str__(self):
        return f"{self.nom} - {self.email}"
    
    def set_password(self, raw_password):
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

class OTPCode(models.Model):
    user = models.ForeignKey(SuperAdmin, on_delete=models.CASCADE, related_name='otp_codes')
    code = models.CharField(max_length=6)
    type = models.CharField(max_length=20, choices=[('email', 'Email'), ('sms', 'SMS')], default='email')
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    
    def __str__(self):
        return f"OTP pour {self.user.email} - {self.code}"
    
    def is_valid(self):
        return not self.is_used and self.expires_at > timezone.now()
