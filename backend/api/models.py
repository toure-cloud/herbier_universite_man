from django.db import models
from django.utils import timezone

class Slide(models.Model):
    titre = models.CharField(max_length=200, verbose_name="Titre")
    texte_botanique = models.TextField(verbose_name="Texte botanique")
    image = models.ImageField(upload_to='slides/', blank=True, null=True)
    image_url = models.URLField(blank=True, null=True, verbose_name="URL de l'image externe")
    ordre = models.IntegerField(default=0)
    actif = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['ordre']
    
    def __str__(self):
        return self.titre
