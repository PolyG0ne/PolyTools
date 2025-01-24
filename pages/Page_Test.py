import streamlit as st
import sqlite3
import pandas as pd
from pathlib import Path


st.title("Warning --Test page--")
# Configuration du chemin
CSV_FILE_PATH = Path('data/CanadianPostalCodes202403.csv')
DB_FILE_PATH = Path('data/postal_codes2.db')

def create_database():
    # Création de la base de données SQLite
    conn = sqlite3.connect(DB_FILE_PATH)
    cursor = conn.cursor()
    
    # Création de la table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS postal_codes (
        postal_code TEXT PRIMARY KEY,
        city TEXT,
        province_abbr TEXT,
        time_zone INTEGER,
        latitude REAL,
        longitude REAL
    )
    ''')
    
    # Lecture du CSV
    df = pd.read_csv(CSV_FILE_PATH)
    
    # Insertion des données
    df.to_sql('postal_codes', conn, if_exists='replace', index=False)
    
    conn.commit()
    conn.close()

def search_postal_code(postal_code):
    conn = sqlite3.connect(DB_FILE_PATH)
    cursor = conn.cursor()
    
    # Recherche exacte
    cursor.execute('''
    SELECT * FROM postal_codes 
    WHERE postal_code = ?
    ''', (postal_code.upper(),))
    
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return {
            'postal_code': result[0],
            'city': result[1],
            'province': result[2],
            'time_zone': result[3],
            'latitude': result[4],
            'longitude': result[5]
        }
    return None

# Interface Streamlit
def main():
    st.title("Recherche de Codes Postaux Canadiens")
    
    # Création de la base de données si elle n'existe pas
    if not DB_FILE_PATH.exists():
        create_database()
    
    postal_code = st.text_input("Entrez un code postal:")
    
    if st.button("Rechercher"):
        if postal_code:
            result = search_postal_code(postal_code)
            if result:
                st.write("Résultats:")
                for key, value in result.items():
                    st.write(f"{key}: {value}")
            else:
                st.error("Code postal non trouvé")

st.write("""
H2X 1Y6
M5V 2T6
V6B 4N7
T2P 1J9
K1P 5H9
B3J 3R7
R3C 0G1
S7K 5B7
E1C 4M7
Y1A 6L6

Rimouski
Kingston
Victoria
Fredericton
Charlottetown
Red Deer
Thunder Bay
Trois-Rivières
St. John
Prince George

48.45207841277754, -68.52372144956752 
44.22976710972037, -76.48587831226758
48.42841714646363, -123.36545935255743
45.96336671345439, -66.64062673091888
46.23824771454619, -63.13110351562500
52.26815737376817, -113.81196260452271
48.38233955556270, -89.24472808837891
46.34692761055676, -72.54150390625000
47.56170075451973, -52.71240234375000
53.91728101547621, -122.74658203125000
""")

if __name__ == "__main__":
    main()
