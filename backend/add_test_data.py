import os
import django
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'herbier_backend.settings')
django.setup()

from api.models import Plante, FamilleBotanique, GenreBotanique, HerbierStats

# Données de test pour les familles
familles_data = [
    {'nom': 'Fabaceae', 'description': 'Famille des légumineuses'},
    {'nom': 'Rubiaceae', 'description': 'Famille du café et du quinquina'},
    {'nom': 'Poaceae', 'description': 'Famille des graminées'},
    {'nom': 'Arecaceae', 'description': 'Famille des palmiers'},
    {'nom': 'Orchidaceae', 'description': 'Famille des orchidées'},
]

for data in familles_data:
    famille, created = FamilleBotanique.objects.get_or_create(nom=data['nom'], defaults=data)
    print(f"✓ Famille: {data['nom']} - {'Créée' if created else 'Existante'}")

# Données de test pour les plantes
plantes_data = [
    {
        'nom': 'Acajou',
        'nom_scientifique': 'Khaya senegalensis',
        'famille': 'Meliaceae',
        'genre': 'Khaya',
        'description': 'Grand arbre à bois précieux, pouvant atteindre 30 mètres de hauteur.',
        'description_courte': 'Arbre à bois précieux des forêts tropicales.',
        'habitat': 'Forêts tropicales humides',
        'statut_conservation': 'VU',
        'pays': "Côte d'Ivoire",
        'region': 'Région de Man',
        'altitude_min': 200,
        'altitude_max': 800,
        'hauteur_max': 30,
        'tags': 'bois précieux, arbre, forêt',
        'publie': True,
        'featured': True
    },
    {
        'nom': 'Iroko',
        'nom_scientifique': 'Milicia excelsa',
        'famille': 'Moraceae',
        'genre': 'Milicia',
        'description': 'Arbre de grande taille, bois très résistant et durable.',
        'description_courte': 'Arbre à bois durable des forêts denses.',
        'habitat': 'Forêts denses humides',
        'statut_conservation': 'VU',
        'pays': "Côte d'Ivoire",
        'region': 'Région de Man',
        'altitude_min': 100,
        'altitude_max': 600,
        'hauteur_max': 45,
        'tags': 'bois durable, construction, arbre',
        'publie': True,
        'featured': True
    },
    {
        'nom': 'Palme à huile',
        'nom_scientifique': 'Elaeis guineensis',
        'famille': 'Arecaceae',
        'genre': 'Elaeis',
        'description': 'Culture importante pour la production d\'huile de palme.',
        'description_courte': 'Palmier oléagineux d\'Afrique.',
        'habitat': 'Zones cultivées, forêts secondaires',
        'statut_conservation': 'LC',
        'pays': "Côte d'Ivoire",
        'region': 'Région de Man',
        'altitude_min': 0,
        'altitude_max': 500,
        'hauteur_max': 20,
        'tags': 'huile, palmier, culture',
        'publie': True,
        'featured': False
    },
    {
        'nom': 'Caféier robusta',
        'nom_scientifique': 'Coffea canephora',
        'famille': 'Rubiaceae',
        'genre': 'Coffea',
        'description': 'Arbuste cultivé pour ses grains de café.',
        'description_courte': 'Plante à café d\'Afrique.',
        'habitat': 'Cultures, forêts ombragées',
        'statut_conservation': 'LC',
        'pays': "Côte d'Ivoire",
        'region': 'Région de Man',
        'altitude_min': 200,
        'altitude_max': 800,
        'hauteur_max': 10,
        'tags': 'café, culture, arbuste',
        'publie': True,
        'featured': False
    },
    {
        'nom': 'Cacaoyer',
        'nom_scientifique': 'Theobroma cacao',
        'famille': 'Malvaceae',
        'genre': 'Theobroma',
        'description': 'Arbuste cultivé pour ses fèves de cacao.',
        'description_courte': 'Plante à cacao d\'Amérique du Sud, cultivée en Afrique.',
        'habitat': 'Cultures sous ombrage',
        'statut_conservation': 'LC',
        'pays': "Côte d'Ivoire",
        'region': 'Région de Man',
        'altitude_min': 100,
        'altitude_max': 600,
        'hauteur_max': 8,
        'tags': 'cacao, chocolat, culture',
        'publie': True,
        'featured': True
    },
]

for data in plantes_data:
    plante, created = Plante.objects.get_or_create(nom=data['nom'], defaults=data)
    print(f"✓ Plante: {data['nom']} - {'Créée' if created else 'Existante'}")

# Mettre à jour les statistiques
HerbierStats.update_stats()
print("\n✅ Données de test ajoutées avec succès !")
print(f"📊 Statistiques: {HerbierStats.objects.get(id=1)}")
