import streamlit as st
import folium
from streamlit_folium import folium_static
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import re
from pathlib import Path
import csv

# Constants
POSTAL_CODE_PATTERN = r'^[A-Z]\d[A-Z]\s?\d[A-Z]\d$'
CSV_FILE_PATH = Path('data/CanadianPostalCodes202403.csv')
INITIAL_LOCATION = [46.8139, -71.2080]

@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_postal_codes():
    """Load postal codes from CSV file"""
    f = None
    try:
        f = open(CSV_FILE_PATH, 'r', encoding='utf-8')
        reader = csv.reader(f)
        return list(reader)
    except FileNotFoundError:
        st.error(f"Le fichier {CSV_FILE_PATH} n'a pas été trouvé.")
        return []
    except Exception as e:
        st.error(f"Erreur lors de la lecture du fichier CSV: {e}")
        return []
    finally:
        if f is not None:
            f.close()

def is_valid_postal_code(code):
    """Vérifie si le code postal est au format valide."""
    if not code:
        return False
    return bool(re.match(POSTAL_CODE_PATTERN, code.upper()))

@st.cache_data(ttl=3600)
def get_coordinates_from_postal_code(postal_code, locations):
    """Obtenir les coordonnées à partir d'un code postal."""
    try:
        for location in locations:
            if postal_code == location[0] and len(location) >= 6:
                return float(location[4]), float(location[5]), location[3]
        return None, None, None
    except (ValueError, IndexError) as e:
        st.warning(f"Erreur de format dans les données pour le code postal {postal_code}: {e}")
        return None, None, None

@st.cache_data(ttl=3600)
def get_coordinates_from_city(city):
    """Obtenir les coordonnées à partir d'un nom de ville."""
    geolocator = Nominatim(user_agent="quebec_postal_app")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=2)
    
    try:
        location = geocode(f"{city}, Quebec, Canada")
        if location:
            return location.latitude, location.longitude, location.address
    except Exception as e:
        st.warning(f"Erreur de géolocalisation pour {city}: {e}")
    m = folium.Map(location=INITIAL_LOCATION, zoom_start=6)
    pass  # m is not used, so we can remove this line
def create_map_from_locations(locations_data, postal_codes_data):
    """Créer une carte avec des marqueurs pour chaque localisation."""
    m = folium.Map(location=[46.8139, -71.2080], zoom_start=6)
    
    with st.spinner("Création des marqueurs..."):
        progress_bar = st.progress(0)
        processed_locations = set()
        
        for i, (identifier, location_type) in enumerate(locations_data):
            if identifier not in processed_locations:
                processed_locations.add(identifier)
                coords = get_coordinates(identifier, location_type, postal_codes_data)
                if all(coords):
                    add_marker_to_map(m, coords, identifier, location_type)
            progress_bar.progress((i + 1) / len(locations_data))
    
    return m

def get_coordinates(identifier, location_type, postal_codes_data):
    """Obtenir les coordonnées en fonction du type de localisation."""
    if location_type == 'postal_code':
        if not is_valid_postal_code(identifier):
            st.warning(f"Code postal invalide ignoré : {identifier}")
            return None, None, None
        return get_coordinates_from_postal_code(identifier, postal_codes_data)
    else:
        return get_coordinates_from_city(identifier)

def add_marker_to_map(m, coords, identifier, location_type):
    """Ajouter un marqueur à la carte."""
    folium.Marker(
        [coords[0], coords[1]],
        popup=f"{'Code postal' if location_type == 'postal_code' else 'Ville'}: {identifier}<br>Adresse: {coords[2]}",
        icon=folium.Icon(color='red' if location_type == 'postal_code' else 'blue', 
                         icon='info-sign')
    ).add_to(m)

def main():
    st.set_page_config(page_title="Visualisation Codes Postaux Québec", layout="wide")
    
    st.title("Visualisation des Codes Postaux et Villes du Québec")
    
    st.markdown("""
    ### Instructions :
    - Entrez soit des codes postaux (un par ligne) ou des noms de villes (une par ligne)
    - Format des codes postaux accepté : G0J 1J0 ou G0J1J0
    """)

    # Charger les données des codes postaux
    postal_codes_data = load_postal_codes()
    if not postal_codes_data:
        st.error("Impossible de continuer sans les données des codes postaux.")
        return

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Recherche par villes")
        cities_input = st.text_area(
            "Entrez les noms des villes (une par ligne)",
            height=150,
            help="Example: Montréal",
            key="cities"
        )

    with col2:
        st.subheader("Recherche par codes postaux")
        postal_codes_input = st.text_area(
            "Entrez les codes postaux (un par ligne)",
            height=150,
            help="Example: G0J 1J0",
            key="postal_codes"
        )

        if st.button("Afficher la carte"):
            if st.button("Afficher la carte"):
                locations_data = get_locations_data(postal_codes_input, cities_input)
                
                if not locations_data:
                    st.error("Veuillez entrer au moins un code postal ou une ville.")
                    return
        
                try:
                    with st.spinner("Création de la carte en cours..."):
                        m = create_map_from_locations(locations_data, postal_codes_data)
                        folium_static(m)
                        st.success(f"Traitement terminé! {len(locations_data)} localisations traitées.")
                except Exception as e:
                    st.error(f"Une erreur est survenue lors de la création de la carte: {e}")
    
    def get_locations_data(postal_codes_input, cities_input):
        """Obtenir les données de localisation à partir des entrées utilisateur."""
        postal_codes = [(code.strip().upper(), 'postal_code') 
                       for code in postal_codes_input.split('\n') 
                       if code.strip()]
        
        cities = [(city.strip(), 'city') 
                  for city in cities_input.split('\n') 
                  if city.strip()]
        
        return postal_codes + cities
if __name__ == "__main__":
    main()