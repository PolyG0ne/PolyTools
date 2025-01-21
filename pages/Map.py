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
    return bool(re.match(pattern, code.upper()))

@st.cache_data
def get_coordinates_from_postal_code(postal_code):
    """Obtenir les coordonnées à partir d'un code postal."""
    geolocator = Nominatim(user_agent="my_quebec_app")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=2)
    
    postal_code = postal_code.upper()
    if len(postal_code) == 6:
        postal_code = f"{postal_code[:3]} {postal_code[3:]}"
        
    max_retries = 3
    for attempt in range(max_retries):
        try:
            location = geocode(f"{postal_code}, Quebec, Canada")
            if location:
                return location.latitude, location.longitude, location.address
            break
        except Exception as e:
            if attempt == max_retries - 1:
                st.error(f"Erreur lors de la géolocalisation du code postal {postal_code}: {e}")
            continue
    return None, None, None

@st.cache_data
def get_coordinates_from_city(city):
    """Obtenir les coordonnées à partir d'un nom de ville."""
    geolocator = Nominatim(user_agent="my_quebec_app")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=2)
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            location = geocode(f"{city}, Quebec, Canada")
            if location:
                return location.latitude, location.longitude, location.address
            break
        except Exception as e:
            if attempt == max_retries - 1:
                st.error(f"Erreur lors de la géolocalisation de la ville {city}: {e}")
            continue
    return None, None, None

def create_map_from_locations(locations_data):
    """Créer une carte avec des marqueurs pour chaque localisation."""
    # Centrer la carte sur le Québec
    m = folium.Map(location=[46.8139, -71.2080], zoom_start=6)
    
    progress_bar = st.progress(0)
    processed_locations = set()  # Pour éviter les doublons
    
    for i, (identifier, location_type) in enumerate(locations_data):
        if not identifier in processed_locations:
            processed_locations.add(identifier)
            
            if location_type == 'postal_code':
                if not is_valid_quebec_postal_code(identifier):
                    st.warning(f"Code postal invalide ignoré : {identifier}")
                    continue
                coords = get_coordinates_from_postal_code(identifier)
            else:  # city
                coords = get_coordinates_from_city(identifier)
                
            if coords[0] and coords[1]:
                folium.Marker(
                    [coords[0], coords[1]],
                    popup=f"{'Code postal' if location_type == 'postal_code' else 'Ville'}: {identifier}<br>Adresse: {coords[2]}",
                    icon=folium.Icon(color='red' if location_type == 'postal_code' else 'blue', 
                                   icon='info-sign')
                ).add_to(m)
            else:
                st.warning(f"Impossible de trouver les coordonnées pour : {identifier}")
        
        progress_bar.progress((i + 1) / len(locations_data))
    
    return m

def main():
    try:
        st.title("Visualisation des Codes Postaux et Villes du Québec")
        
        st.markdown("""
        ### Instructions :
        - Entrez soit des codes postaux (un par ligne) ou des noms de villes (une par ligne)
        - Format des codes postaux accepté : G5H 1V7 ou G5H1V7
        """)

        # Créer deux colonnes
        col1, col2 = st.columns(2)

        # Colonne pour les codes postaux
        with col1:
            st.subheader("Recherche par codes postaux")
            postal_codes_input = st.text_area(
                "Entrez les codes postaux (un par ligne)",
                height=150,
                help="Example: G5H 1V7",
                key="postal_codes"
            )

        # Colonne pour les villes
        with col2:
            st.subheader("Recherche par villes")
            cities_input = st.text_area(
                "Entrez les noms des villes (une par ligne)",
                height=150,
                help="Example: Montréal",
                key="cities"
            )

        if st.button("Afficher la carte"):
            # Traiter les codes postaux
            postal_codes = [(code.strip(), 'postal_code') for code in postal_codes_input.split('\n') 
                          if code.strip()]
            
            # Traiter les villes
            cities = [(city.strip(), 'city') for city in cities_input.split('\n') 
                     if city.strip()]
            
            # Combiner les deux listes
            locations_data = postal_codes + cities

            if not locations_data:
                st.error("Veuillez entrer au moins un code postal ou une ville.")
            else:
                with st.spinner("Création de la carte en cours..."):
                    # Créer et afficher la carte
                    m = create_map_from_locations(locations_data)
                    folium_static(m)
                    
                    # Afficher les statistiques
                    st.success(f"Traitement terminé! {len(locations_data)} localisations traitées.")

    except Exception as e:
        st.error(f"Une erreur inattendue s'est produite: {str(e)}")
        raise e

if __name__ == "__main__":
    main()
