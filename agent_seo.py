import os
import json
import random
import google.generativeai as genai

# 1. Configurer l'accès à Gemini
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. Liste des métiers à cibler (tu peux en ajouter d'autres ici !)
niches = ["Boulangerie", "Coiffeur", "Fleuriste", "Restaurant", "Garage automobile", "Institut de beaute", "Pharmacie", "Opticien", "Agence immobiliere", "Salle de sport"]
niche = random.choice(niches)

print(f"Génération de la page pour : {niche}")

# 3. Le prompt envoyé à l'IA
prompt = f"""
Agis comme un expert SEO et copywriter B2B. Génère le contenu d'une Landing Page pour l'outil 'Spin To Keep' qui cible la thématique : {niche}.
L'outil permet de créer des jeux concours par QR Code en magasin pour récolter des avis Google.
Renvoie UNIQUEMENT un objet JSON valide avec les clés exactes suivantes, sans aucun autre texte avant ou après :
"SEO_TITLE", "SEO_DESC", "KEYWORD", "HERO_H1", "HERO_SUB", "SEO_H2_PROBLEMATIQUE", "SEO_P_PROBLEMATIQUE_1", "SEO_P_PROBLEMATIQUE_2", "BENEFITS_H2", "ICON_1", "BENEFIT_1_TITLE", "BENEFIT_1_DESC", "ICON_2", "BENEFIT_2_TITLE", "BENEFIT_2_DESC", "ICON_3", "BENEFIT_3_TITLE", "BENEFIT_3_DESC", "CAS_USAGE_H2", "CAS_USAGE_DESC", "FAQ_Q1", "FAQ_A1", "FAQ_Q2", "FAQ_A2", "FAQ_Q3", "FAQ_A3"
"""

try:
    # 4. Demander à l'IA
    response = model.generate_content(prompt)
    
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
    dossier = niche.lower().replace(" ", "-").replace("é", "e").replace("è", "e")
    os.makedirs(dossier, exist_ok=True)
    
    with open(f"{dossier}/index.html", "w", encoding="utf-8") as f:
        f.write(html)
        
    print(f"Succès ! Page créée dans : {dossier}/index.html")
    
except Exception as e:
    print(f"Erreur lors de la génération : {e}")
