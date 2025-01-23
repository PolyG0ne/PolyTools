import streamlit as st
import folium
from streamlit_folium import folium_static
import re
from pathlib import Path
import sqlite3

POSTAL_CODE_PATTERN = r'^[A-Z]\d[A-Z]\s?\d[A-Z]\d$'
DB_FILE_PATH = Path('data/postal_codes.db')
INITIAL_LOCATION = [48.45207841277754, -68.52372144956752]

@st.cache_data(ttl=3600)
def load_postal_codes():
    try:
        conn = sqlite3.connect(DB_FILE_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM postal_codes')
        columns = [description[0] for description in cursor.description]
        data = cursor.fetchall()
        conn.close()
        
        return [dict(zip(columns, row)) for row in data]
    except Exception as e:
        st.error(f"Erreur de lecture de la base de données: {e}")
        return []

def is_valid_postal_code(code):
    if not code:
        return False
    return bool(re.match(POSTAL_CODE_PATTERN, code.upper()))

def get_coordinates_from_data(identifier, postal_codes_data):
    identifier = identifier.strip()

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
            pass
    
    cleaned_identifier = identifier.upper().replace(' ', '')
    
    if is_valid_postal_code(cleaned_identifier):
        conn = sqlite3.connect(DB_FILE_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM postal_codes 
            WHERE REPLACE(postal_code, " ", "") = ?
        ''', (cleaned_identifier,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'lat': float(result[4]),  # LATITUDE
                'lon': float(result[5]),  # LONGITUDE
                'type': 'postal_code',
                'address': f"{result[1]}, {result[2]}"  # CITY, PROVINCE_ABBR
            }
    
    # Recherche par ville
    conn = sqlite3.connect(DB_FILE_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM postal_codes 
        WHERE UPPER(city) = ? 
        LIMIT 1
    ''', (identifier.upper(),))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return {
            'lat': float(result[4]),
            'lon': float(result[5]),
            'type': 'city',
            'address': f"{result[1]}, {result[2]}"
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
                icon=folium.Icon(color='green' if location['type'] == 'coordinates' else 'red' if location['type'] == 'postal_code' else 'blue', icon='info-sign')
            ).add_to(m)
    
    return m

def main():
   if "text_content" not in st.session_state:
       st.session_state.text_content = ""
    
   st.title("Visualisation sur Folium")
   
   st.markdown("""
   ### Instructions:
   - Entrez des codes postaux, des noms de villes ou des coordonnées (un par ligne)
   - Format de code postal accepté: G0J 1J0, G0J1J0, g0j 1j0, g0j1j0
   - Format de ville accepté: Nom de la ville (ex: Montréal, Quebec)
   - Format de coordonnées accepté: Latitude, Longitude (ex: 48.4498, -68.5289 / 48.44988218305047, -68.52894936844488)
   """)

   postal_codes_data = load_postal_codes()
   if not postal_codes_data:
       return

   if st.button("Effacer", type="primary"):
       st.session_state.text_content = ""
       st.rerun()

   locations_input = st.text_area(
       "Codes postaux ou villes (un par ligne)", 
       value=st.session_state.text_content,
       height=150,
       help="Exemple:\nG0J 1J0\nMontréal\nQuébec",
       key="locations_input"
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