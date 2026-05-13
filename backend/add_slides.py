import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'herbier_backend.settings')
django.setup()

from api.models import Slide

# Supprimer les anciens slides
Slide.objects.all().delete()

# Créer de nouveaux slides
slides_data = [
    {
        "titre": "La Biodiversité des Montagnes",
        "texte": "Les montagnes de Man abritent une flore unique et diversifiée.",
        "image_url": "https://picsum.photos/id/104/1920/600"
    },
    {
        "titre": "Collection Botanique",
        "texte": "Notre herbier conserve plus de 5000 spécimens de plantes.",
        "image_url": "https://picsum.photos/id/106/1920/600"
    },
    {
        "titre": "Recherche et Conservation",
        "texte": "Engagés dans la préservation de la flore pour les générations futures.",
        "image_url": "https://picsum.photos/id/13/1920/600"
    }
]

for i, data in enumerate(slides_data):
    slide = Slide(
        titre=data["titre"],
        texte_botanique=data["texte"],
        image_url=data["image_url"],
        ordre=i,
        actif=True
    )
    slide.save()
    print(f"✓ Slide créé: {slide.titre}")

print(f"\n✅ Total: {Slide.objects.count()} slides")
