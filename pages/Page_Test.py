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

if __name__ == "__main__":
    main()