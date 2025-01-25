import streamlit as st
import folium
from streamlit_folium import folium_static
import re
from pathlib import Path
import sqlite3
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
import logging
from typing import Optional, Dict, Any, List, Tuple
from dataclasses import dataclass
from functools import lru_cache

# Configuration
@dataclass
class Config:
    POSTAL_CODE_PATTERN: str = r'^[A-Z]\d[A-Z]\s?\d[A-Z]\d$'
    DB_FILE_PATH: Path = Path('data/postal_codes.db')
    INITIAL_LOCATION: Tuple[float, float] = (48.45207841277754, -68.52372144956752)
    BATCH_SIZE: int = 25
    MAX_WORKERS: int = 4

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self, db_path: Path):
        self.db_path = db_path
        sqlite3.register_adapter(bool, int)
        sqlite3.register_converter("BOOLEAN", lambda v: bool(int(v)))

    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(
            self.db_path,
            check_same_thread=False,
            timeout=30,
            isolation_level=None
        )
        try:
            yield conn
        finally:
            conn.close()

    def initialize(self) -> bool:
        if not self.db_path.exists():
            logger.error(f"Database not found: {self.db_path}")
            st.error(f"Database not found: {self.db_path}")
            return False
        return True

    def create_indexes(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_postal_code ON postal_codes(postal_code)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_city ON postal_codes(city)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_geolocation ON postal_codes(latitude, longitude)')

class LocationService:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    @staticmethod
    def validate_coordinates(lat: float, lon: float) -> bool:
        return -90 <= lat <= 90 and -180 <= lon <= 180

    @staticmethod
    def sanitize_input(text: str) -> str:
        return re.sub(r'[^\w\s,-]', '', text)

    @staticmethod
    def is_valid_postal_code(code: str) -> bool:
        if not code or len(code.replace(' ', '')) != 6:
            return False
        return bool(re.match(Config.POSTAL_CODE_PATTERN, code.upper()))

    def get_coordinates(self, identifier: str) -> Optional[Dict[str, Any]]:
        try:
            identifier = identifier.strip()
            
            # Check if input is coordinates
            if ',' in identifier:
                try:
                    lat, lon = map(float, map(str.strip, identifier.split(',')))
                    if self.validate_coordinates(lat, lon):
                        return {
                            'lat': lat,
                            'lon': lon,
                            'type': 'coordinates',
                            'address': f"Coordinates: {lat}, {lon}"
                        }
                except ValueError:
                    pass

            with self.db_manager.get_connection() as conn:
                cursor = conn.cursor()
                cleaned_identifier = self.sanitize_input(identifier.upper().replace(' ', ''))
                
                if self.is_valid_postal_code(cleaned_identifier):
                    cursor.execute('''
                        SELECT * FROM postal_codes INDEXED BY idx_postal_code
                        WHERE REPLACE(postal_code, " ", "") = ?
                    ''', (cleaned_identifier,))
                    result = cursor.fetchone()
                    
                    if result:
                        return {
                            'lat': float(result[4]),
                            'lon': float(result[5]),
                            'type': 'postal_code',
                            'address': f"{result[1]}, {result[2]}"
                        }
                
                cursor.execute('''
                    SELECT * FROM postal_codes INDEXED BY idx_city
                    WHERE UPPER(city) = ? 
                    LIMIT 1
                ''', (identifier.upper(),))
                result = cursor.fetchone()
                
                if result:
                    return {
                        'lat': float(result[4]),
                        'lon': float(result[5]),
                        'type': 'city',
                        'address': f"{result[1]}, {result[2]}"
                    }
            
            return None
        except Exception as e:
            logger.error(f"Error getting coordinates: {e}")
            return None

class MapService:
    def __init__(self, location_service: LocationService):
        self.location_service = location_service

    def process_location_batch(self, locations_batch: List[str]) -> List[Tuple[str, Optional[Dict[str, Any]]]]:
        return [(loc, self.location_service.get_coordinates(loc)) for loc in locations_batch]

    def create_map(self, locations: List[str]) -> folium.Map:
        m = folium.Map(location=Config.INITIAL_LOCATION, zoom_start=7)
        
        batch_size = min(Config.BATCH_SIZE, max(1, len(locations) // Config.MAX_WORKERS))
        batches = [locations[i:i+batch_size] for i in range(0, len(locations), batch_size)]
        
        progress_bar = st.progress(0)
        
        with ThreadPoolExecutor(max_workers=Config.MAX_WORKERS) as executor:
            futures = [executor.submit(self.process_location_batch, batch) for batch in batches]
            results = []
            
            for i, future in enumerate(futures):
                try:
                    results.extend(future.result())
                    progress_bar.progress((i + 1) / len(batches))
                except Exception as e:
                    logger.error(f"Batch processing error: {e}")

        for identifier, location in results:
            if location:
                folium.Marker(
                    [location['lat'], location['lon']],
                    popup=f"{'Postal Code' if location['type'] == 'postal_code' else 'City'}: {identifier}<br>Address: {location['address']}",
                    icon=folium.Icon(
                        color='green' if location['type'] == 'coordinates' 
                        else 'red' if location['type'] == 'postal_code' 
                        else 'blue',
                        icon='info-sign'
                    )
                ).add_to(m)
        
        return m

class StreamlitApp:
    def __init__(self):
        self.db_manager = DatabaseManager(Config.DB_FILE_PATH)
        self.location_service = LocationService(self.db_manager)
        self.map_service = MapService(self.location_service)

    def initialize(self) -> bool:
        if not self.db_manager.initialize():
            return False
        self.db_manager.create_indexes()
        return True

    def run(self):
        if not self.initialize():
            return

        st.set_page_config(
            page_title="Map visualisation",
            layout="wide"
        )

        st.title("Postal Code Visualization")
        
        locations_input = st.text_area(
            "Entrez une liste de codes postaux, villes ou coordonnées (un par ligne):",
            height=150,
            help="Format: Code postal (G0J 1J0) ou Ville (Montréal) ou Coordonnées (45.5017, -73.5673)"
        )

        if st.button("Show Map", type="primary"):
            locations = [loc.strip() for loc in locations_input.split('\n') if loc.strip()]
            if locations:
                with st.spinner("Creating map..."):
                    try:
                        m = self.map_service.create_map(locations)
                        folium_static(m, width=800, height=600)
                        st.caption('data source: https://codes-postaux.cybo.com/ ')
                    except Exception as e:
                        st.error(f"Error creating map: {e}")
            else:
                st.warning("Please enter at least one location.")

if __name__ == "__main__":
    app = StreamlitApp()
    app.run()