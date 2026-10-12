import os
import json
import random
from google import genai

# 1. Configurer l'accès avec la NOUVELLE librairie
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# 2. Liste des métiers à cibler (Ultra-segmentée SEO Local & CRM)
niches = [
    # Top classiques
    "Boulangerie", "Coiffeur", "Fleuriste", "Restaurant", "Institut de beaute", 
    "Pharmacie", "Opticien", "Agence immobiliere", "Salle de sport",
    
    # Attente Captive & Santé
    "Centre d imagerie medicale", "Laboratoire d analyses", "Kinesitherapeute", 
    "Osteopathe", "Centre dentaire", "Cordonnier et cle minute", 
    "Reparation de smartphone", "Auto ecole", "Laverie automatique",
    
    # Alimentaire de spécialité & Haute fréquence
    "Pizzeria a emporter", "Kebab et restauration rapide", "Primeur", 
    "Fromagerie", "Boucherie Charcuterie", "Chocolatier", 
    "Epicerie fine", "Cave a bieres", "Boutique de Bubble Tea", "Caviste",
    
    # Habitat & Panier moyen élevé
    "Pisciniste", "Constructeur de maisons", "Magasin de meubles", 
    "Cuisiniste", "Paysagiste", "Installateur de climatisation", "Bijouterie",
    
    # Beauté & Transformation
    "Salon de tatouage et piercing", "Centre d epilation laser", 
    "Bar a ongles", "Centre de cryotherapie", "Spa et Thalasso", "Barbier",
    
    # Loisirs & Tourisme
    "Trampoline park", "Laser game", "Karting indoor", "Bowling", 
    "Camping", "Escape game", "Studio de yoga et pilates", "Hotel et chambre d hotes",
    
    # Mobilité & Véhicules
    "Centre pare-brise", "Concessionnaire moto", "Station de lavage auto", 
    "Specialiste pneu", "Garage automobile", "Centre de controle technique",
    
    # Animaux
    "Animalerie", "Toiletteur canin", "Clinique veterinaire",
    
    # Secteurs restreints (Shadow ban Ads)
    "Magasin de CBD", "Boutique de cigarette electronique"
]
niche = random.choice(niches)

print(f"Génération de la page pour : {niche}")

# 3. Le prompt envoyé à l'IA
prompt = f"""
Agis comme un expert SEO et copywriter B2B. Génère le contenu d'une Landing Page pour l'outil 'Spin To Keep' qui cible la thématique : {niche}.
L'outil permet de créer des jeux concours par QR Code en magasin pour récolter des avis Google et collecter des données clients (CRM).
Renvoie UNIQUEMENT un objet JSON valide avec les clés exactes suivantes, sans aucun autre texte avant ou après :
"SEO_TITLE", "SEO_DESC", "KEYWORD", "HERO_H1", "HERO_SUB", "SEO_H2_PROBLEMATIQUE", "SEO_P_PROBLEMATIQUE_1", "SEO_P_PROBLEMATIQUE_2", "BENEFITS_H2", "ICON_1", "BENEFIT_1_TITLE", "BENEFIT_1_DESC", "ICON_2", "BENEFIT_2_TITLE", "BENEFIT_2_DESC", "ICON_3", "BENEFIT_3_TITLE", "BENEFIT_3_DESC", "CAS_USAGE_H2", "CAS_USAGE_DESC", "FAQ_Q1", "FAQ_A1", "FAQ_Q2", "FAQ_A2", "FAQ_Q3", "FAQ_A3"

IMPORTANT : Pour les clés "ICON_1", "ICON_2" et "ICON_3", tu dois renvoyer UNIQUEMENT un seul émoji (par exemple : ✨, 🏆, 📈, 🚀). Ne renvoie surtout pas de texte ou de nom d'icône.
"""

try:
    # 4. Demander à l'IA (Nouvelle syntaxe)
    response = client.models.generate_content(
        model='gemini-3.8-flash',
        contents=prompt,
    )
    
    # Nettoyer la réponse pour garder juste le JSON
    texte_json = response.text.replace('```json', '').replace('```', '').strip()
    data = json.loads(texte_json)
    
    # 5. Lire ton template HTML
    with open("seo_template.html", "r", encoding="utf-8") as f:
        html = f.read()
        
    # 6. Remplacer les balises par le texte de l'IA
    for key, value in data.items():
        html = html.replace("{{" + key + "}}", str(value))
        
    # 7. Créer le dossier avec le nom du métier et sauvegarder la page
    dossier = niche.lower().replace(" ", "-").replace("é", "e").replace("è", "e").replace("'", "-")
    os.makedirs(dossier, exist_ok=True)
    
    with open(f"{dossier}/index.html", "w", encoding="utf-8") as f:
        f.write(html)
        
    print(f"Succès ! Page créée dans : {dossier}/index.html")
    
except Exception as e:
    print(f"Erreur lors de la génération : {e}")
