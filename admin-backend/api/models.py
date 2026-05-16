from django.db import models
from django.utils import timezone
import requests
from django.conf import settings

class SuperAdmin(models.Model):
    email = models.EmailField(unique=True)
    nom = models.CharField(max_length=200)
    telephone = models.CharField(max_length=20)
    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.nom} - {self.email}"

class APICache(models.Model):
    """Cache pour les données récupérées de l'API publique"""
    endpoint = models.CharField(max_length=200, unique=True)
    data = models.JSONField()
    last_update = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.endpoint

class APISyncLog(models.Model):
    """Log des synchronisations avec l'API publique"""
    action = models.CharField(max_length=100)
    status = models.CharField(max_length=20)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.action} - {self.status} - {self.created_at}"
