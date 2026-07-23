from django.db import models
from django.utils import timezone

# ========== MODÈLES PRINCIPAUX ==========

class FamilleBotanique(models.Model):
    """Modèle pour les familles botaniques"""
    nom = models.CharField(max_length=200, unique=True, verbose_name="Nom de la famille")
    nom_latin = models.CharField(max_length=200, blank=True, verbose_name="Nom latin")
    description = models.TextField(blank=True, verbose_name="Description")
    caracteristiques = models.TextField(blank=True, verbose_name="Caractéristiques")
    image = models.ImageField(upload_to='familles/', blank=True, null=True, verbose_name="Image représentative")
    ordre = models.CharField(max_length=200, blank=True, verbose_name="Ordre botanique")
    nombre_especes = models.IntegerField(default=0, verbose_name="Nombre d'espèces")
    
    class Meta:
        verbose_name = "Famille botanique"
        verbose_name_plural = "Familles botaniques"
        ordering = ['nom']
    
    def __str__(self):
        return self.nom

class GenreBotanique(models.Model):
    """Modèle pour les genres botaniques"""
    nom = models.CharField(max_length=200, unique=True, verbose_name="Nom du genre")
    nom_latin = models.CharField(max_length=200, blank=True, verbose_name="Nom latin")
    famille = models.ForeignKey(FamilleBotanique, on_delete=models.CASCADE, related_name='genres', verbose_name="Famille")
    description = models.TextField(blank=True, verbose_name="Description")
    nombre_especes = models.IntegerField(default=0, verbose_name="Nombre d'espèces")
    
    class Meta:
        verbose_name = "Genre botanique"
        verbose_name_plural = "Genres botaniques"
        ordering = ['nom']
    
    def __str__(self):
        return self.nom

class Plante(models.Model):
    """Modèle principal pour les plantes"""
    nom = models.CharField(max_length=200, verbose_name="Nom de la plante")
    nom_scientifique = models.CharField(max_length=200, blank=True, verbose_name="Nom scientifique")
    famille = models.ForeignKey(FamilleBotanique, on_delete=models.SET_NULL, null=True, blank=True, related_name='plantes', verbose_name="Famille")
    genre = models.ForeignKey(GenreBotanique, on_delete=models.SET_NULL, null=True, blank=True, related_name='plantes', verbose_name="Genre")
    description = models.TextField(verbose_name="Description")
    habitat = models.TextField(blank=True, verbose_name="Habitat")
    distribution = models.CharField(max_length=500, blank=True, verbose_name="Distribution")
    statut_conservation = models.CharField(max_length=100, blank=True, verbose_name="Statut de conservation")
    usages = models.TextField(blank=True, verbose_name="Usages traditionnels")
    image = models.ImageField(upload_to='plantes/', blank=True, null=True, verbose_name="Image principale")
    images_galerie = models.JSONField(default=list, blank=True, verbose_name="Galerie d'images")
    featured = models.BooleanField(default=False, verbose_name="À la une")
    actif = models.BooleanField(default=True, verbose_name="Actif")
    date_creation = models.DateTimeField(default=timezone.now, verbose_name="Date d'ajout")
    
    class Meta:
        verbose_name = "Plante"
        verbose_name_plural = "Plantes"
        ordering = ['nom']
    
    def __str__(self):
        return self.nom

# ========== MODÈLES POUR L'ÉQUIPE ET PARTENAIRES ==========

class Equipe(models.Model):
    nom = models.CharField(max_length=200, verbose_name="Nom complet")
    photo = models.ImageField(upload_to='equipe/', blank=True, null=True, verbose_name="Photo")
    poste = models.CharField(max_length=200, verbose_name="Poste/Fonction")
    email = models.EmailField(blank=True, verbose_name="Email")
    telephone = models.CharField(max_length=50, blank=True, verbose_name="Téléphone")
    specialite = models.CharField(max_length=200, blank=True, verbose_name="Spécialité")
    bio = models.TextField(blank=True, verbose_name="Biographie")
    ordre = models.IntegerField(default=0, verbose_name="Ordre d'affichage")
    actif = models.BooleanField(default=True, verbose_name="Actif")
    
    class Meta:
        verbose_name = "Membre de l'équipe"
        verbose_name_plural = "Membres de l'équipe"
        ordering = ['ordre', 'nom']
    
    def __str__(self):
        return self.nom

class Partenaire(models.Model):
    nom = models.CharField(max_length=200, verbose_name="Nom du partenaire")
    logo = models.ImageField(upload_to='partenaires/', blank=True, null=True, verbose_name="Logo")
    site_web = models.URLField(blank=True, verbose_name="Site web")
    description = models.TextField(blank=True, verbose_name="Description")
    type = models.CharField(max_length=100, blank=True, verbose_name="Type de partenaire")
    ordre = models.IntegerField(default=0, verbose_name="Ordre d'affichage")
    actif = models.BooleanField(default=True, verbose_name="Actif")
    
    class Meta:
        verbose_name = "Partenaire"
        verbose_name_plural = "Partenaires"
        ordering = ['ordre', 'nom']
    
    def __str__(self):
        return self.nom

# ========== MODÈLES POUR LES SLIDES ==========

class Slide(models.Model):
    titre = models.CharField(max_length=200, verbose_name="Titre")
    texte_botanique = models.TextField(verbose_name="Texte botanique")
    image = models.ImageField(upload_to='slides/', blank=True, null=True, verbose_name="Image")
    image_url = models.URLField(blank=True, null=True, verbose_name="URL de l'image externe")
    lien = models.URLField(blank=True, verbose_name="Lien associé")
    ordre = models.IntegerField(default=0, verbose_name="Ordre d'affichage")
    actif = models.BooleanField(default=True, verbose_name="Actif")
    
    class Meta:
        verbose_name = "Slide"
        verbose_name_plural = "Slides"
        ordering = ['ordre']
    
    def __str__(self):
        return self.titre

# ========== MODÈLES POUR LES PROJETS ==========

class Projet(models.Model):
    STATUT_CHOICES = [
        ('termine', 'Terminé'),
        ('encours', 'En cours'),
        ('planifie', 'Planifié'),
    ]
    
    CATEGORIE_CHOICES = [
        ('recherche', 'Recherche'),
        ('conservation', 'Conservation'),
        ('formation', 'Formation'),
        ('developpement', 'Développement'),
    ]
    
    titre = models.CharField(max_length=200, verbose_name="Titre du projet")
    description = models.TextField(verbose_name="Description courte")
    description_longue = models.TextField(blank=True, verbose_name="Description détaillée")
    categorie = models.CharField(max_length=50, choices=CATEGORIE_CHOICES, default='recherche', verbose_name="Catégorie")
    statut = models.CharField(max_length=50, choices=STATUT_CHOICES, default='encours', verbose_name="Statut")
    featured = models.BooleanField(default=False, verbose_name="Projet à la une")
    annee = models.CharField(max_length=50, verbose_name="Année ou période")
    lieu = models.CharField(max_length=200, verbose_name="Lieu")
    partenaires = models.IntegerField(default=0, verbose_name="Nombre de partenaires")
    beneficiaires = models.CharField(max_length=100, blank=True, verbose_name="Bénéficiaires")
    budget = models.CharField(max_length=100, blank=True, verbose_name="Budget")
    duree = models.CharField(max_length=100, blank=True, verbose_name="Durée")
    impact = models.CharField(max_length=200, blank=True, verbose_name="Impact")
    progression = models.IntegerField(default=0, verbose_name="Progression (%)")
    image = models.ImageField(upload_to='projets/', blank=True, null=True, verbose_name="Image principale")
    images_galerie = models.JSONField(default=list, blank=True, verbose_name="Images de la galerie")
    tags = models.CharField(max_length=500, blank=True, verbose_name="Tags")
    caption = models.CharField(max_length=200, blank=True, verbose_name="Légende")
    date_debut = models.DateField(null=True, blank=True)
    date_fin = models.DateField(null=True, blank=True)
    objectifs = models.TextField(blank=True, verbose_name="Objectifs")
    resultats = models.TextField(blank=True, verbose_name="Résultats")
    
    class Meta:
        verbose_name = "Projet"
        verbose_name_plural = "Projets"
        ordering = ['-featured', '-annee']
    
    def __str__(self):
        return self.titre

class ProjetTimeline(models.Model):
    projet = models.ForeignKey(Projet, on_delete=models.CASCADE, related_name='timeline', verbose_name="Projet")
    annee = models.IntegerField(verbose_name="Année")
    titre = models.CharField(max_length=200, verbose_name="Titre")
    description = models.TextField(verbose_name="Description")
    ordre = models.IntegerField(default=0, verbose_name="Ordre")
    
    class Meta:
        verbose_name = "Étape du projet"
        verbose_name_plural = "Étapes des projets"
        ordering = ['projet', 'annee', 'ordre']
    
    def __str__(self):
        return f"{self.projet.titre} - {self.annee}: {self.titre}"

# ========== MODÈLES POUR LES ACTIVITÉS ==========

class Activite(models.Model):
    titre = models.CharField(max_length=200, verbose_name="Titre")
    titre_court = models.CharField(max_length=100, verbose_name="Titre court")
    description_courte = models.TextField(verbose_name="Description courte")
    description_longue = models.TextField(verbose_name="Description détaillée")
    icon = models.CharField(max_length=100, verbose_name="Icône Font Awesome", default="fas fa-leaf")
    image = models.ImageField(upload_to='activites/', blank=True, null=True, verbose_name="Image")
    caption = models.CharField(max_length=200, blank=True, verbose_name="Légende")
    points_forts = models.TextField(blank=True, verbose_name="Points forts (un par ligne)")
    ordre = models.IntegerField(default=0, verbose_name="Ordre d'affichage")
    actif = models.BooleanField(default=True, verbose_name="Actif")
    
    class Meta:
        verbose_name = "Activité"
        verbose_name_plural = "Activités"
        ordering = ['ordre', 'titre']
    
    def __str__(self):
        return self.titre
    
    def get_points_forts_list(self):
        if not self.points_forts:
            return []
        return [point.strip() for point in self.points_forts.split('\n') if point.strip()]

# ========== MODÈLES POUR LES TÉMOIGNAGES ==========

class Temoignage(models.Model):
    nom = models.CharField(max_length=200, verbose_name="Nom")
    poste = models.CharField(max_length=200, verbose_name="Poste")
    organisation = models.CharField(max_length=200, verbose_name="Organisation")
    texte = models.TextField(verbose_name="Témoignage")
    photo = models.ImageField(upload_to='temoignages/', blank=True, null=True, verbose_name="Photo")
    note = models.IntegerField(default=5, verbose_name="Note (/5)")
    ordre = models.IntegerField(default=0, verbose_name="Ordre d'affichage")
    actif = models.BooleanField(default=True, verbose_name="Actif")
    
    class Meta:
        verbose_name = "Témoignage"
        verbose_name_plural = "Témoignages"
        ordering = ['ordre', 'nom']
    
    def __str__(self):
        return f"{self.nom} - {self.organisation}"

# ========== MODÈLES POUR LES PUBLICATIONS ==========

class Publication(models.Model):
    titre = models.CharField(max_length=300, verbose_name="Titre")
    auteurs = models.CharField(max_length=500, verbose_name="Auteurs")
    journal = models.CharField(max_length=200, verbose_name="Journal/Revue")
    annee = models.IntegerField(verbose_name="Année")
    lien = models.URLField(blank=True, null=True, verbose_name="Lien")
    doi = models.CharField(max_length=100, blank=True, null=True, verbose_name="DOI")
    resume = models.TextField(blank=True, null=True, verbose_name="Résumé")
    image = models.ImageField(upload_to='publications/', blank=True, null=True, verbose_name="Image")
    ordre = models.IntegerField(default=0, verbose_name="Ordre d'affichage")
    actif = models.BooleanField(default=True, verbose_name="Actif")
    
    class Meta:
        verbose_name = "Publication"
        verbose_name_plural = "Publications"
        ordering = ['-annee', 'ordre']
    
    def __str__(self):
        return f"{self.titre} ({self.annee})"

# ========== MODÈLES POUR LES FAQ ==========

class FAQ(models.Model):
    question = models.CharField(max_length=300, verbose_name="Question")
    reponse = models.TextField(verbose_name="Réponse")
    ordre = models.IntegerField(default=0, verbose_name="Ordre d'affichage")
    actif = models.BooleanField(default=True, verbose_name="Actif")
    
    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"
        ordering = ['ordre', 'question']
    
    def __str__(self):
        return self.question

# ========== MODÈLES POUR LES CONTACTS ==========

class ContactMessage(models.Model):
    SUJET_CHOICES = [
        ('information', 'Demande d\'information'),
        ('collaboration', 'Proposition de collaboration'),
        ('projet', 'Soumission de projet'),
        ('stage', 'Demande de stage'),
        ('autre', 'Autre'),
    ]
    
    nom = models.CharField(max_length=200, verbose_name="Nom complet")
    email = models.EmailField(verbose_name="Email")
    telephone = models.CharField(max_length=50, blank=True, verbose_name="Téléphone")
    sujet = models.CharField(max_length=50, choices=SUJET_CHOICES, default='information', verbose_name="Sujet")
    message = models.TextField(verbose_name="Message")
    date_envoi = models.DateTimeField(default=timezone.now, verbose_name="Date d'envoi")
    lu = models.BooleanField(default=False, verbose_name="Lu")
    
    class Meta:
        verbose_name = "Message de contact"
        verbose_name_plural = "Messages de contact"
        ordering = ['-date_envoi']
    
    def __str__(self):
        return f"{self.nom} - {self.get_sujet_display()}"

# ========== MODÈLES POUR LES STATISTIQUES ==========

class Statistique(models.Model):
    titre = models.CharField(max_length=100, verbose_name="Titre")
    valeur = models.CharField(max_length=50, verbose_name="Valeur")
    unite = models.CharField(max_length=20, blank=True, null=True, verbose_name="Unité")
    icon = models.CharField(max_length=100, verbose_name="Icône", default="fas fa-chart-line")
    ordre = models.IntegerField(default=0, verbose_name="Ordre")
    actif = models.BooleanField(default=True, verbose_name="Actif")
    
    class Meta:
        verbose_name = "Statistique"
        verbose_name_plural = "Statistiques"
        ordering = ['ordre', 'titre']
    
    def __str__(self):
        return f"{self.titre}: {self.valeur}{self.unite or ''}"

# ========== MODÈLES POUR LA MÉTHODOLOGIE ==========

class Methodologie(models.Model):
    titre = models.CharField(max_length=200, verbose_name="Titre")
    description = models.TextField(verbose_name="Description")
    icon = models.CharField(max_length=100, verbose_name="Icône", default="fas fa-clipboard-list")
    ordre = models.IntegerField(default=0, verbose_name="Ordre")
    actif = models.BooleanField(default=True, verbose_name="Actif")
    
    class Meta:
        verbose_name = "Étape de méthodologie"
        verbose_name_plural = "Étapes de méthodologie"
        ordering = ['ordre', 'titre']
    
    def __str__(self):
        return self.titre

class HerbierStats(models.Model):
    """Statistiques globales de l'herbier"""
    total_plantes = models.IntegerField(default=0)
    total_familles = models.IntegerField(default=0)
    total_genres = models.IntegerField(default=0)
    total_images = models.IntegerField(default=0)
    dernier_ajout = models.DateTimeField(null=True, blank=True)
    date_mise_a_jour = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name = "Statistique Herbier"
        verbose_name_plural = "Statistiques Herbier"
    
    def __str__(self):
        return f"Stats Herbier - {self.date_mise_a_jour.date()}"
    
    @classmethod
    def update_stats(cls):
        from django.db.models import Count
        stats, created = cls.objects.get_or_create(id=1)
        
        stats.total_plantes = Plante.objects.filter(actif=True).count()
        stats.total_familles = FamilleBotanique.objects.count()
        stats.total_genres = GenreBotanique.objects.count()
        stats.total_images = Plante.objects.filter(actif=True, image__isnull=False).count()
        
        dernier = Plante.objects.filter(actif=True).order_by('-date_creation').first()
        if dernier:
            stats.dernier_ajout = dernier.date_creation
        
        stats.date_mise_a_jour = timezone.now()
        stats.save()
        return stats
