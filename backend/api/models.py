from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

# ==================== MODÈLE PLANTE AMÉLIORÉ ====================

class Plante(models.Model):
    STATUT_CONSERVATION_CHOICES = [
        ('LC', 'Préoccupation mineure'),
        ('NT', 'Quasi menacée'),
        ('VU', 'Vulnérable'),
        ('EN', 'En danger'),
        ('CR', 'En danger critique'),
        ('EW', 'Éteint à l\'état sauvage'),
        ('EX', 'Éteint'),
        ('DD', 'Données insuffisantes'),
        ('NE', 'Non évaluée'),
    ]
    
    # Informations de base
    nom = models.CharField(max_length=200, verbose_name="Nom de la plante", db_index=True)
    nom_scientifique = models.CharField(max_length=200, blank=True, verbose_name="Nom scientifique", db_index=True)
    famille = models.CharField(max_length=200, verbose_name="Famille botanique", db_index=True)
    genre = models.CharField(max_length=200, blank=True, verbose_name="Genre", db_index=True)
    
    # Description
    description = models.TextField(verbose_name="Description")
    description_courte = models.CharField(max_length=500, blank=True, verbose_name="Description courte")
    
    # Caractéristiques
    habitat = models.CharField(max_length=300, blank=True, verbose_name="Habitat")
    lieu_collecte = models.CharField(max_length=300, blank=True, verbose_name="Lieu de collecte")
    altitude_min = models.IntegerField(null=True, blank=True, verbose_name="Altitude minimale (m)")
    altitude_max = models.IntegerField(null=True, blank=True, verbose_name="Altitude maximale (m)")
    floraison_debut = models.CharField(max_length=20, blank=True, verbose_name="Début floraison")
    floraison_fin = models.CharField(max_length=20, blank=True, verbose_name="Fin floraison")
    hauteur_min = models.FloatField(null=True, blank=True, verbose_name="Hauteur minimale (m)")
    hauteur_max = models.FloatField(null=True, blank=True, verbose_name="Hauteur maximale (m)")
    
    # Conservation
    statut_conservation = models.CharField(max_length=20, choices=STATUT_CONSERVATION_CHOICES, default='NE', verbose_name="Statut de conservation")
    population_tendance = models.CharField(max_length=50, blank=True, verbose_name="Tendance de la population")
    menaces = models.TextField(blank=True, verbose_name="Menaces")
    
    # Localisation
    pays = models.CharField(max_length=200, blank=True, verbose_name="Pays", db_index=True)
    region = models.CharField(max_length=200, blank=True, verbose_name="Région", db_index=True)
    localisation_specifique = models.CharField(max_length=500, blank=True, verbose_name="Localisation spécifique")
    coordonnees_lat = models.FloatField(null=True, blank=True, verbose_name="Latitude")
    coordonnees_lon = models.FloatField(null=True, blank=True, verbose_name="Longitude")
    
    # Médias
    image = models.ImageField(upload_to='plantes/', blank=True, null=True, verbose_name="Image principale")
    images_galerie = models.JSONField(default=list, blank=True, verbose_name="Images de la galerie")
    illustration = models.ImageField(upload_to='illustrations/', blank=True, null=True, verbose_name="Illustration botanique")
    
    # Métadonnées
    date_creation = models.DateTimeField(default=timezone.now, db_index=True)
    date_modification = models.DateTimeField(auto_now=True)
    auteur = models.CharField(max_length=200, blank=True, verbose_name="Auteur de la fiche")
    tags = models.CharField(max_length=500, blank=True, verbose_name="Tags (séparés par des virgules)", db_index=True)
    
    # Statut
    publie = models.BooleanField(default=True, verbose_name="Publié")
    featured = models.BooleanField(default=False, verbose_name="À la une")
    
    class Meta:
        verbose_name = "Plante"
        verbose_name_plural = "Plantes"
        ordering = ['nom']
        indexes = [
            models.Index(fields=['nom']),
            models.Index(fields=['famille']),
            models.Index(fields=['genre']),
            models.Index(fields=['nom_scientifique']),
            models.Index(fields=['statut_conservation']),
            models.Index(fields=['pays']),
            models.Index(fields=['region']),
            models.Index(fields=['date_creation']),
        ]
    
    def __str__(self):
        return f"{self.nom} ({self.famille})"
    
    def get_tags_list(self):
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
    
    def get_images_list(self):
        return self.images_galerie if self.images_galerie else []
    
    def get_full_name(self):
        if self.nom_scientifique and self.nom_scientifique != self.nom:
            return f"{self.nom} ({self.nom_scientifique})"
        return self.nom

# ==================== MODÈLES EXISTANTS (conservés) ====================

class Equipe(models.Model):
    nom = models.CharField(max_length=200, verbose_name="Nom complet")
    photo = models.ImageField(upload_to='equipe/', verbose_name="Photo", blank=True, null=True)
    poste = models.CharField(max_length=200, verbose_name="Poste/Fonction")
    email = models.EmailField(blank=True, verbose_name="Email")
    specialite = models.CharField(max_length=200, blank=True, verbose_name="Spécialité")
    telephone = models.CharField(max_length=50, blank=True, verbose_name="Téléphone")
    ordre = models.IntegerField(default=0, verbose_name="Ordre d'affichage")
    
    class Meta:
        verbose_name = "Membre de l'équipe"
        verbose_name_plural = "Membres de l'équipe"
        ordering = ['ordre', 'nom']
    
    def __str__(self):
        return self.nom

class Partenaire(models.Model):
    nom = models.CharField(max_length=200, verbose_name="Nom du partenaire")
    logo = models.ImageField(upload_to='partenaires/', verbose_name="Logo", blank=True, null=True)
    site_web = models.URLField(blank=True, verbose_name="Site web")
    description = models.TextField(blank=True, verbose_name="Description")
    ordre = models.IntegerField(default=0, verbose_name="Ordre d'affichage")
    
    class Meta:
        verbose_name = "Partenaire"
        verbose_name_plural = "Partenaires"
        ordering = ['ordre', 'nom']
    
    def __str__(self):
        return self.nom

class Slide(models.Model):
    titre = models.CharField(max_length=200, verbose_name="Titre")
    texte_botanique = models.TextField(verbose_name="Texte botanique")
    image = models.ImageField(upload_to='slides/', verbose_name="Image", blank=True, null=True)
    ordre = models.IntegerField(default=0, verbose_name="Ordre d'affichage")
    actif = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Slide"
        verbose_name_plural = "Slides"
        ordering = ['ordre']
    
    def __str__(self):
        return self.titre

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
        ('autre', 'Autre'),
    ]
    
    titre = models.CharField(max_length=200, verbose_name="Titre du projet")
    description = models.TextField(verbose_name="Description courte")
    description_longue = models.TextField(blank=True, verbose_name="Description détaillée")
    categorie = models.CharField(max_length=50, choices=CATEGORIE_CHOICES, default='recherche')
    statut = models.CharField(max_length=50, choices=STATUT_CHOICES, default='encours')
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
    tags = models.CharField(max_length=500, blank=True, verbose_name="Tags (séparés par des virgules)")
    caption = models.CharField(max_length=200, blank=True, verbose_name="Légende de l'image")
    date_debut = models.DateField(null=True, blank=True)
    date_fin = models.DateField(null=True, blank=True)
    objectifs = models.TextField(blank=True, verbose_name="Objectifs du projet")
    resultats = models.TextField(blank=True, verbose_name="Résultats obtenus")
    
    class Meta:
        verbose_name = "Projet"
        verbose_name_plural = "Projets"
        ordering = ['-featured', '-annee']
    
    def __str__(self):
        return self.titre
    
    def get_tags_list(self):
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]

class ProjetTimeline(models.Model):
    projet = models.ForeignKey(Projet, on_delete=models.CASCADE, related_name='timeline', blank=True, null=True)
    annee = models.IntegerField(verbose_name="Année")
    titre = models.CharField(max_length=200, verbose_name="Titre")
    description = models.TextField(verbose_name="Description")
    ordre = models.IntegerField(default=0, verbose_name="Ordre")
    
    class Meta:
        verbose_name = "Étape du projet"
        verbose_name_plural = "Étapes des projets"
        ordering = ['annee', 'ordre']
    
    def __str__(self):
        return f"{self.annee} - {self.titre}"

class Activite(models.Model):
    titre = models.CharField(max_length=200, verbose_name="Titre")
    titre_court = models.CharField(max_length=100, verbose_name="Titre court")
    description_courte = models.TextField(verbose_name="Description courte")
    description_longue = models.TextField(verbose_name="Description détaillée")
    icon = models.CharField(max_length=100, verbose_name="Icône Font Awesome", default="fas fa-leaf")
    image = models.ImageField(upload_to='activites/', blank=True, null=True, verbose_name="Image")
    caption = models.CharField(max_length=200, blank=True, verbose_name="Légende")
    points_forts = models.TextField(verbose_name="Points forts (un par ligne)", blank=True)
    ordre = models.IntegerField(default=0, verbose_name="Ordre d'affichage")
    actif = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Activité"
        verbose_name_plural = "Activités"
        ordering = ['ordre', 'titre']
    
    def __str__(self):
        return self.titre
    
    def get_points_forts_list(self):
        return [point.strip() for point in self.points_forts.split('\n') if point.strip()]

class Temoignage(models.Model):
    nom = models.CharField(max_length=200, verbose_name="Nom")
    poste = models.CharField(max_length=200, verbose_name="Poste")
    organisation = models.CharField(max_length=200, verbose_name="Organisation")
    texte = models.TextField(verbose_name="Témoignage")
    photo = models.ImageField(upload_to='temoignages/', blank=True, null=True, verbose_name="Photo")
    note = models.IntegerField(default=5, verbose_name="Note (/5)")
    ordre = models.IntegerField(default=0, verbose_name="Ordre d'affichage")
    actif = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Témoignage"
        verbose_name_plural = "Témoignages"
        ordering = ['ordre', 'nom']
    
    def __str__(self):
        return f"{self.nom} - {self.organisation}"

class Publication(models.Model):
    titre = models.CharField(max_length=300, verbose_name="Titre")
    auteurs = models.CharField(max_length=500, verbose_name="Auteurs")
    journal = models.CharField(max_length=200, verbose_name="Journal/Revue")
    annee = models.IntegerField(verbose_name="Année")
    lien = models.URLField(blank=True, verbose_name="Lien")
    doi = models.CharField(max_length=100, blank=True, verbose_name="DOI")
    resume = models.TextField(blank=True, verbose_name="Résumé")
    ordre = models.IntegerField(default=0, verbose_name="Ordre d'affichage")
    
    class Meta:
        verbose_name = "Publication"
        verbose_name_plural = "Publications"
        ordering = ['-annee', 'ordre']
    
    def __str__(self):
        return self.titre

class FAQ(models.Model):
    question = models.CharField(max_length=300, verbose_name="Question")
    reponse = models.TextField(verbose_name="Réponse")
    ordre = models.IntegerField(default=0, verbose_name="Ordre d'affichage")
    actif = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"
        ordering = ['ordre', 'question']
    
    def __str__(self):
        return self.question

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
    sujet = models.CharField(max_length=50, choices=SUJET_CHOICES, default='information')
    message = models.TextField(verbose_name="Message")
    date_envoi = models.DateTimeField(default=timezone.now)
    lu = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "Message de contact"
        verbose_name_plural = "Messages de contact"
        ordering = ['-date_envoi']
    
    def __str__(self):
        return f"{self.nom} - {self.get_sujet_display()}"

class Statistique(models.Model):
    titre = models.CharField(max_length=100, verbose_name="Titre")
    valeur = models.CharField(max_length=50, verbose_name="Valeur")
    unite = models.CharField(max_length=20, blank=True, verbose_name="Unité")
    icon = models.CharField(max_length=100, verbose_name="Icône", default="fas fa-chart-line")
    ordre = models.IntegerField(default=0, verbose_name="Ordre")
    actif = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Statistique"
        verbose_name_plural = "Statistiques"
        ordering = ['ordre', 'titre']
    
    def __str__(self):
        return f"{self.titre}: {self.valeur}{self.unite}"

class Methodologie(models.Model):
    titre = models.CharField(max_length=200, verbose_name="Titre")
    description = models.TextField(verbose_name="Description")
    icon = models.CharField(max_length=100, verbose_name="Icône", default="fas fa-clipboard-list")
    ordre = models.IntegerField(default=0, verbose_name="Ordre")
    actif = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Étape de méthodologie"
        verbose_name_plural = "Étapes de méthodologie"
        ordering = ['ordre', 'titre']
    
    def __str__(self):
        return self.titre

# ==================== NOUVEAUX MODÈLES POUR L'HERBIER ====================

class FamilleBotanique(models.Model):
    nom = models.CharField(max_length=200, unique=True, verbose_name="Nom de la famille")
    description = models.TextField(blank=True, verbose_name="Description")
    image = models.ImageField(upload_to='familles/', blank=True, null=True, verbose_name="Image représentative")
    nombre_especes = models.IntegerField(default=0, verbose_name="Nombre d'espèces")
    
    class Meta:
        verbose_name = "Famille botanique"
        verbose_name_plural = "Familles botaniques"
        ordering = ['nom']
    
    def __str__(self):
        return self.nom
    
    def update_especes_count(self):
        self.nombre_especes = Plante.objects.filter(famille=self.nom, publie=True).count()
        self.save()

class GenreBotanique(models.Model):
    nom = models.CharField(max_length=200, unique=True, verbose_name="Nom du genre")
    famille = models.ForeignKey(FamilleBotanique, on_delete=models.CASCADE, related_name='genres', verbose_name="Famille")
    description = models.TextField(blank=True, verbose_name="Description")
    nombre_especes = models.IntegerField(default=0, verbose_name="Nombre d'espèces")
    
    class Meta:
        verbose_name = "Genre botanique"
        verbose_name_plural = "Genres botaniques"
        ordering = ['nom']
    
    def __str__(self):
        return self.nom

class HerbierStats(models.Model):
    total_plantes = models.IntegerField(default=0)
    total_familles = models.IntegerField(default=0)
    total_genres = models.IntegerField(default=0)
    total_images = models.IntegerField(default=0)
    dernier_ajout = models.DateTimeField(null=True, blank=True)
    derniere_mise_a_jour = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Statistique Herbier"
        verbose_name_plural = "Statistiques Herbier"
    
    def __str__(self):
        return f"Stats Herbier - MAJ {self.derniere_mise_a_jour}"
    
    @classmethod
    def update_stats(cls):
        stats, created = cls.objects.get_or_create(id=1)
        stats.total_plantes = Plante.objects.filter(publie=True).count()
        stats.total_familles = Plante.objects.filter(publie=True).values('famille').distinct().count()
        stats.total_genres = Plante.objects.filter(publie=True, genre__isnull=False).exclude(genre='').values('genre').distinct().count()
        stats.total_images = Plante.objects.filter(publie=True, image__isnull=False).count()
        
        dernier = Plante.objects.filter(publie=True).order_by('-date_creation').first()
        if dernier:
            stats.dernier_ajout = dernier.date_creation
        
        stats.save()
        return stats
