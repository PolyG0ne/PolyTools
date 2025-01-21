import streamlit as st
import folium
from streamlit_folium import folium_static
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import re
import sys

def is_valid_quebec_postal_code(code):
    """Vérifie si le code postal est au format québécois valide."""
    pattern = r'^[A-Z]\d[A-Z]\s?\d[A-Z]\d$'
    # Accepte le format avec ou sans espace
    return bool(re.match(pattern, code.upper()))

@st.cache_data
def get_coordinates(postal_code):
    """Obtenir les coordonnées à partir d'un code postal."""
    geolocator = Nominatim(user_agent="my_quebec_app")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=2)
    
    # Standardiser le format (ajouter espace si absent)
    postal_code = postal_code.upper()
    if len(postal_code) == 6:
        postal_code = f"{postal_code[:3]} {postal_code[3:]}"
        st.info(postal_code)
        
    max_retries = 3
    for attempt in range(max_retries):
        try:
            # Ajouter 'Quebec, Canada' pour plus de précision
            location = geocode(f"{postal_code}") #, Quebec, Canada")
            if location:
                return location.latitude, location.longitude
            break
        except Exception as e:
            if attempt == max_retries - 1:
                st.error(f"Erreur lors de la géolocalisation du code postal {postal_code}: {e}")
            continue
    return None, None

def create_map(postal_codes):
    """Créer une carte avec des marqueurs pour chaque code postal."""
    # Centrer la carte sur le Québec
    m = folium.Map(location=[46.8139, -71.2080], zoom_start=6)
    
    progress_bar = st.progress(0)
    processed_codes = set()  # Pour éviter les doublons
    
    for i, code in enumerate(postal_codes):
        if not code in processed_codes:
            processed_codes.add(code)
            
            if not is_valid_quebec_postal_code(code):
                st.warning(f"Code postal invalide ignoré : {code}")
                continue
                
            coords = get_coordinates(code)
            if coords[0] and coords[1]:
                folium.Marker(
                    coords,
                    popup=f"Code postal: {code}",
                    icon=folium.Icon(color='red', icon='info-sign')
                ).add_to(m)
            else:
                st.warning(f"Impossible de trouver les coordonnées pour : {code}")
        
        progress_bar.progress((i + 1) / len(postal_codes))
    
    return m

def main():
    try:
        st.title("Visualisation des Codes Postaux du Québec")
        
        st.markdown("""
        ### Instructions :
        - Entrez les codes postaux québécois (un par ligne)
        - Format accepté : G5H 1V7 ou G5H1V7
        """)

        # Saisie des codes postaux
        postal_codes_input = st.text_area(
            "Entrez les codes postaux (un par ligne)",
            height=150,
            help="Example: G5H 1V7"
        )

        if postal_codes_input:
            # Convertir l'entrée en liste et nettoyer les données
            postal_codes = [code.strip() for code in postal_codes_input.split('\n') 
                          if code.strip()]

            if st.button("Afficher la carte"):
                if not postal_codes:
                    st.error("Veuillez entrer au moins un code postal valide.")
                else:
                    with st.spinner("Création de la carte en cours..."):
                        # Créer et afficher la carte
                        m = create_map(postal_codes)
                        folium_static(m)
                        
                        # Afficher les statistiques
                        st.success(f"Traitement terminé! {len(postal_codes)} codes postaux traités.")

    except Exception as e:
        st.error(f"Une erreur inattendue s'est produite: {str(e)}")
        raise e

if __name__ == "__main__":
    main()
