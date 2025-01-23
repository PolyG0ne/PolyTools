import streamlit as st
import folium
from streamlit_folium import folium_static
from geopy.geocoders import Nominatim
import re
from pathlib import Path
import csv

POSTAL_CODE_PATTERN = r'^[A-Z]\d[A-Z]\s?\d[A-Z]\d$'
CSV_FILE_PATH = Path('data/CanadianPostalCodes202403.csv')
INITIAL_LOCATION = [48.45207841277754, -68.52372144956752]

@st.cache_data(ttl=3600)
def load_postal_codes():
    try:
        with open(CSV_FILE_PATH, 'r', encoding='utf-8') as f:
            return list(csv.DictReader(f))
    except Exception as e:
        st.error(f"Erreur de lecture du fichier CSV: {e}")
        return []

def is_valid_postal_code(code):
    if not code:
        return False
    return bool(re.match(POSTAL_CODE_PATTERN, code.upper()))

def get_coordinates_from_data(identifier, postal_codes_data):
    identifier = identifier.strip()

    # Try coordinates format first
    if ',' in identifier:
        try:
            lat_str, lon_str = map(str.strip, identifier.split(','))
            lat, lon = float(lat_str), float(lon_str)
            if -90 <= lat <= 90 and -180 <= lon <= 180:
                return {
                    'lat': lat,
                    'lon': lon,
                    'type': 'coordinates',
                    'address': f"Coordonnées: {lat}, {lon}"
                }
        except ValueError:
            pass  # Not valid coordinates, continue with other checks
    
    # Clean postal code
    cleaned_identifier = identifier.upper().replace(' ', '')
    
    # Try postal code
    if is_valid_postal_code(cleaned_identifier):
        for location in postal_codes_data:
            if location['POSTAL_CODE'].replace(' ', '') == cleaned_identifier:
                return {
                    'lat': float(location['LATITUDE']),
                    'lon': float(location['LONGITUDE']),
                    'type': 'postal_code',
                    'address': f"{location['CITY']}, {location['PROVINCE_ABBR']}"
                }
    
    # Try city
    for location in postal_codes_data:
        if location['CITY'].upper() == identifier.upper():
            return {
                'lat': float(location['LATITUDE']),
                'lon': float(location['LONGITUDE']),
                'type': 'city',
                'address': f"{location['CITY']}, {location['PROVINCE_ABBR']}"
            }
    
    return None

def create_map(locations_data, postal_codes_data):
    m = folium.Map(location=INITIAL_LOCATION, zoom_start=7)
    
    for identifier in locations_data:
        location = get_coordinates_from_data(identifier, postal_codes_data)
        if location:
            folium.Marker(
                [location['lat'], location['lon']],
                popup=f"{'Code postal' if location['type'] == 'postal_code' else 'Ville'}: {identifier}<br>Adresse: {location['address']}",
                #icon=folium.Icon(color='red' if location['type'] == 'postal_code' else 'blue', icon='info-sign')
                icon=folium.Icon(color='green' if location['type'] == 'coordinates' else 'red' if location['type'] == 'postal_code' else 'blue', icon='info-sign')
            ).add_to(m)
    
    return m

def main():
    st.set_page_config(page_title="Visualisation Codes Postaux et Villes", layout="wide")
    st.title("Visualisation sur Folium")
    
    st.markdown("""
    ### Instructions:
    - Entrez des codes postaux, des noms de villes ou des coordonnées (un par ligne)
    - Format de code postal accepté: G0J 1J0 ou G0J1J0
    - Format de ville accepté: Nom de la ville (ex: Montréal, Quebec)
    - Format de coordonnées accepté: Latitude, Longitude (ex: 46.8139, -71.2080 ou 48.45207841277754, -68.52372144956752) ..
    """)

    postal_codes_data = load_postal_codes()
    if not postal_codes_data:
        return

    locations_input = st.text_area(
        "Codes postaux ou villes (un par ligne)",
        height=150,
        help="Exemple:\nG0J 1J0\nMontréal\nQuébec",
        key="locations"
    )

    if st.button("Afficher la carte"):
        locations = [loc.strip() for loc in locations_input.split('\n') if loc.strip()]
        
        if not locations:
            st.error("Veuillez entrer au moins un code postal ou une ville valide.")
            return

        try:
            with st.spinner("Création de la carte..."):
                m = create_map(locations, postal_codes_data)
                folium_static(m, width=1000, height=500)
                st.success(f"{len(locations)} localisations recherchées.")
        except Exception as e:
            st.error(f"Erreur lors de la création de la carte: {e}")

if __name__ == "__main__":
    main()
