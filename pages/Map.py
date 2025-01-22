import streamlit as st
import folium
from streamlit_folium import folium_static
from geopy.geocoders import Nominatim
import re
from pathlib import Path
import csv

POSTAL_CODE_PATTERN = r'^[A-Z]\d[A-Z]\s?\d[A-Z]\d$'
CSV_FILE_PATH = Path('data/CanadianPostalCodes202403.csv')
INITIAL_LOCATION = [46.8139, -71.2080]

@st.cache_data(ttl=3600)
def load_postal_codes():
    try:
        with open(CSV_FILE_PATH, 'r', encoding='utf-8') as f:
            return list(csv.reader(f))
    except Exception as e:
        st.error(f"Erreur de lecture du fichier CSV: {e}")
        return []

def is_valid_postal_code(code):
    if not code:
        return False
    return bool(re.match(POSTAL_CODE_PATTERN, code.upper()))

@st.cache_data(ttl=3600)
def get_coordinates_from_postal_code(postal_code, locations):
    try:
        for location in locations:
            if postal_code == location[0] and len(location) >= 6:
                return float(location[4]), float(location[5]), location[3]
        return None, None, None
    except (ValueError, IndexError) as e:
        st.warning(f"Erreur de format pour le code postal {postal_code}: {e}")
        return None, None, None

@st.cache_data(ttl=3600, show_spinner=False)
def get_coordinates_from_city(city):
    geolocator = Nominatim(user_agent="quebec_postal_app")
    try:
        location = geolocator.geocode(f"{city}, Quebec, Canada", timeout=10)
        if location:
            return location.latitude, location.longitude, location.address
        return None, None, None
    except Exception as e:
        st.warning(f"Erreur de géolocalisation pour {city}: {e}")
        return None, None, None

def create_map_from_locations(locations_data, postal_codes_data):
    m = folium.Map(location=INITIAL_LOCATION, zoom_start=6)
    status_placeholder = st.empty()
    
    with st.spinner("Création des marqueurs..."):
        processed = set()
        for i, (identifier, location_type) in enumerate(locations_data):
            if identifier not in processed:
                processed.add(identifier)
                coords = get_coordinates(identifier, location_type, postal_codes_data)
                if all(coords):
                    add_marker_to_map(m, coords, identifier, location_type)
                status_placeholder.progress((i + 1) / len(locations_data))
    
    status_placeholder.empty()
    return m

def get_coordinates(identifier, location_type, postal_codes_data):
    if location_type == 'postal_code':
        if not is_valid_postal_code(identifier):
            st.warning(f"Code postal invalide: {identifier}")
            return None, None, None
        return get_coordinates_from_postal_code(identifier, postal_codes_data)
    return get_coordinates_from_city(identifier)

def add_marker_to_map(m, coords, identifier, location_type):
    folium.Marker(
        [coords[0], coords[1]],
        popup=f"{'Code postal' if location_type == 'postal_code' else 'Ville'}: {identifier}<br>Adresse: {coords[2]}",
        icon=folium.Icon(color='red' if location_type == 'postal_code' else 'blue', icon='info-sign')
    ).add_to(m)

def validate_input(text, input_type):
    if input_type == 'postal_code':
        return bool(re.match(POSTAL_CODE_PATTERN, text.upper()))
    return len(text.strip()) >= 2

def get_locations_data(postal_codes_input, cities_input):
    postal_codes = [(code.strip().upper(), 'postal_code') 
                    for code in postal_codes_input.split('\n') 
                    if code.strip() and validate_input(code, 'postal_code')]
    
    cities = [(city.strip(), 'city') 
              for city in cities_input.split('\n') 
              if city.strip() and validate_input(city, 'city')]
    
    return postal_codes + cities

def main():
    st.set_page_config(page_title="Visualisation Codes Postaux Québec", layout="wide")
    st.title("Visualisation des Codes Postaux et Villes du Québec")
    
    st.markdown("""
    ### Instructions:
    - Entrez des codes postaux (un par ligne) ou des noms de villes
    - Format accepté: G0J 1J0 ou G0J1J0
    """)

    postal_codes_data = load_postal_codes()
    if not postal_codes_data:
        return

    col1, col2 = st.columns(2)
    with col1:
        cities_input = st.text_area("Villes (une par ligne)", height=150, help="Example: Montréal", key="cities")
    with col2:
        postal_codes_input = st.text_area("Codes postaux (un par ligne)", height=150, help="Example: G0J 1J0", key="postal_codes")

    if st.button("Afficher la carte"):
        locations_data = get_locations_data(postal_codes_input, cities_input)
        if not locations_data:
            st.error("Veuillez entrer au moins un code postal ou une ville valide.")
            return

        try:
            with st.spinner("Création de la carte..."):
                m = create_map_from_locations(locations_data, postal_codes_data)
                folium_static(m)
                st.success(f"{len(locations_data)} localisations affichées.")
        except Exception as e:
            st.error(f"Erreur lors de la création de la carte: {e}")

if __name__ == "__main__":
    main()