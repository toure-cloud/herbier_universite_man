from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone

class SuperAdminManager(models.Manager):
    def create_user(self, email, nom, telephone, password=None, role='admin', **extra_fields):
        if not email:
            raise ValueError('L\'email est obligatoire')
        if not telephone:
            raise ValueError('Le numéro de téléphone est obligatoire')
        if not nom:
            raise ValueError('Le nom est obligatoire')
        
        email = email.lower()
        user = self.model(
            email=email,
            nom=nom,
            telephone=telephone,
            role=role,
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
        extra_fields.setdefault('role', 'it_admin')
        return self.create_user(email, nom, telephone, password, **extra_fields)

class SuperAdmin(models.Model):
    ROLE_CHOICES = [
        ('it_admin', 'IT Administrator'),
        ('admin', 'Administrateur'),
        ('viewer', 'Visualisateur'),
    ]
    
    email = models.EmailField(unique=True)
    nom = models.CharField(max_length=200)
    telephone = models.CharField(max_length=20)
    pays_code = models.CharField(max_length=10, default='+225')
    password = models.CharField(max_length=128)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='admin')
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom', 'telephone']
    
    objects = SuperAdminManager()
    
    def __str__(self):
        return f"{self.nom} ({self.get_role_display()})"
    
    def set_password(self, raw_password):
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

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

class UserToken(models.Model):
    user = models.ForeignKey(SuperAdmin, on_delete=models.CASCADE, related_name='tokens')
    token = models.CharField(max_length=200, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Token pour {self.user.email}"
    
    def is_valid(self):
        return self.is_active and self.expires_at > timezone.now()

# ========== MODÈLES POUR LES DONNÉES ==========

# ✅ CORRECTION : Utilisation de ImageField au lieu de TextField
class Plante(models.Model):
    nom = models.CharField(max_length=200)
    famille = models.CharField(max_length=200, blank=True, null=True)
    nom_scientifique = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    habitat = models.CharField(max_length=300, blank=True, null=True)
    statut_conservation = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='plantes/', blank=True, null=True)  # ✅ CORRECTION
    actif = models.BooleanField(default=True)
    date_creation = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name = "Plante"
        verbose_name_plural = "Plantes"
        ordering = ['nom']
    
    def __str__(self):
        return self.nom

class Equipe(models.Model):
    nom = models.CharField(max_length=200)
    poste = models.CharField(max_length=200)
    email = models.EmailField(blank=True, null=True)
    specialite = models.CharField(max_length=200, blank=True, null=True)
    photo = models.ImageField(upload_to='equipe/', blank=True, null=True)  # ✅ CORRECTION
    ordre = models.IntegerField(default=0)
    actif = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Membre de l'équipe"
        verbose_name_plural = "Membres de l'équipe"
        ordering = ['ordre', 'nom']
    
    def __str__(self):
        return self.nom

class Slide(models.Model):
    titre = models.CharField(max_length=200)
    texte_botanique = models.TextField()
    image = models.ImageField(upload_to='slides/', blank=True, null=True)  # ✅ CORRECTION
    ordre = models.IntegerField(default=0)
    actif = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Slide"
        verbose_name_plural = "Slides"
        ordering = ['ordre']
    
    def __str__(self):
        return self.titre

class Projet(models.Model):
    CATEGORIE_CHOICES = [
        ('recherche', 'Recherche'),
        ('conservation', 'Conservation'),
        ('formation', 'Formation'),
        ('developpement', 'Développement'),
    ]
    
    STATUT_CHOICES = [
        ('termine', 'Terminé'),
        ('encours', 'En cours'),
        ('planifie', 'Planifié'),
    ]
    
    titre = models.CharField(max_length=200)
    categorie = models.CharField(max_length=50, choices=CATEGORIE_CHOICES, default='recherche')
    statut = models.CharField(max_length=50, choices=STATUT_CHOICES, default='encours')
    annee = models.CharField(max_length=50, blank=True, null=True)
    lieu = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='projets/', blank=True, null=True)  # ✅ CORRECTION
    
    class Meta:
        verbose_name = "Projet"
        verbose_name_plural = "Projets"
        ordering = ['-annee']
    
    def __str__(self):
        return self.titre

class Activite(models.Model):
    titre = models.CharField(max_length=200)
    titre_court = models.CharField(max_length=100)
    description_courte = models.TextField()
    description_longue = models.TextField(blank=True, null=True)
    icon = models.CharField(max_length=100, default='fas fa-leaf')
    image = models.ImageField(upload_to='activites/', blank=True, null=True)  # ✅ AJOUT
    ordre = models.IntegerField(default=0)
    actif = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Activité"
        verbose_name_plural = "Activités"
        ordering = ['ordre', 'titre']
    
    def __str__(self):
        return self.titre

class Partenaire(models.Model):
    nom = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to='partenaires/', blank=True, null=True)  # ✅ CORRECTION
    site_web = models.URLField(blank=True, null=True)
    type = models.CharField(max_length=100, blank=True, null=True)
    ordre = models.IntegerField(default=0)
    actif = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Partenaire"
        verbose_name_plural = "Partenaires"
        ordering = ['ordre', 'nom']
    
    def __str__(self):
        return self.nom

class Temoignage(models.Model):
    nom = models.CharField(max_length=200)
    poste = models.CharField(max_length=200)
    organisation = models.CharField(max_length=200)
    texte = models.TextField()
    photo = models.ImageField(upload_to='temoignages/', blank=True, null=True)  # ✅ CORRECTION
    note = models.IntegerField(default=5)
    ordre = models.IntegerField(default=0)
    actif = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Témoignage"
        verbose_name_plural = "Témoignages"
        ordering = ['ordre', 'nom']
    
    def __str__(self):
        return f"{self.nom} - {self.organisation}"

class Publication(models.Model):
    titre = models.CharField(max_length=300)
    auteurs = models.CharField(max_length=500)
    journal = models.CharField(max_length=200)
    annee = models.IntegerField()
    lien = models.URLField(blank=True, null=True)
    actif = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Publication"
        verbose_name_plural = "Publications"
        ordering = ['-annee']
    
    def __str__(self):
        return f"{self.titre} ({self.annee})"

class FAQ(models.Model):
    question = models.CharField(max_length=300)
    reponse = models.TextField()
    ordre = models.IntegerField(default=0)
    actif = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"
        ordering = ['ordre', 'question']
    
    def __str__(self):
        return self.question

class Statistique(models.Model):
    titre = models.CharField(max_length=100)
    valeur = models.CharField(max_length=50)
    unite = models.CharField(max_length=20, blank=True, null=True)
    icon = models.CharField(max_length=100, default='fas fa-chart-line')
    ordre = models.IntegerField(default=0)
    actif = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Statistique"
        verbose_name_plural = "Statistiques"
        ordering = ['ordre', 'titre']
    
    def __str__(self):
        return f"{self.titre}: {self.valeur}{self.unite or ''}"

class Methodologie(models.Model):
    titre = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(max_length=100, default='fas fa-clipboard-list')
    ordre = models.IntegerField(default=0)
    actif = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Étape de méthodologie"
        verbose_name_plural = "Étapes de méthodologie"
        ordering = ['ordre', 'titre']
    
    def __str__(self):
        return self.titre