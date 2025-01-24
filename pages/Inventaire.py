import streamlit as st
import pandas as pd
from pathlib import Path
import sqlite3

DB_FILE_PATH = Path('data/inventaire.db')

def init_database():
    # Création du dossier data s'il n'existe pas
    DB_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(DB_FILE_PATH)
    cursor = conn.cursor()
    
    # Création de la table si elle n'existe pas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventaire (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            product_number TEXT,
            number_of_boxes INTEGER NOT NULL,
            quantity_in_box INTEGER NOT NULL,
            total_quantity INTEGER NOT NULL,
            stored_emplacement TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()

@st.cache_data(ttl=3600)  # Mise à jour de st.cache à st.cache_data
def load_data():
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM inventaire')
        columns = [description[0] for description in cursor.description]
        data = cursor.fetchall()
        
        return pd.DataFrame(data, columns=columns)
    except Exception as e:
        st.error(f"Erreur de lecture de la base de données: {e}")
        return pd.DataFrame()
    finally:
        if conn:
            conn.close()

def show_inventaire_form():
    data = load_data()
    
    if not data.empty:
        st.dataframe(data)  # Utilisation de st.dataframe au lieu de st.write
    
    # Formulaire toujours affiché, pas seulement quand data est vide
    with st.form(key="inventaire_form"):
        id = st.number_input("ID", min_value=0, step=1)
        name = st.text_input("Nom")
        product_number = st.text_input("Numéro de produit")
        number_of_boxes = st.number_input("Nombre de boîtes", min_value=0, step=1)
        quantity_in_box = st.number_input("Quantité par boîte", min_value=0, step=1)
        total_quantity = number_of_boxes * quantity_in_box
        stored_emplacement = st.selectbox(
            "Emplacement", 
            ["Ch 2003", "Ancienne Buanderie", "Buanderie", "Cuisine", "Salle de pause", "Vestiaire"]
        )
        
        submitted = st.form_submit_button("Ajouter")
        
        if submitted:
            conn = None
            try:
                conn = sqlite3.connect(DB_FILE_PATH)
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO inventaire 
                    (id, name, product_number, number_of_boxes, quantity_in_box, total_quantity, stored_emplacement)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (id, name, product_number, number_of_boxes, quantity_in_box, total_quantity, stored_emplacement))
                conn.commit()
                st.success("Données ajoutées avec succès.")
                st.rerun()  # Rafraîchit la page pour montrer les nouvelles données
            except sqlite3.IntegrityError:
                st.error("Erreur: ID déjà existant.")
            except Exception as e:
                st.error(f"Erreur lors de l'ajout des données: {e}")
            finally:
                if conn:
                    conn.close()

def show_update_form():
    with st.form(key="update_form"):
        id = st.number_input("ID", min_value=0, step=1)
        number_of_boxes = st.number_input("Nombre de boîtes", min_value=0, step=1)
        quantity_in_box = st.number_input("Quantité par boîte", min_value=0, step=1)
        total_quantity = number_of_boxes * quantity_in_box
        
        submitted = st.form_submit_button("Mettre à jour")
        
        if submitted:
            conn = None
            try:
                conn = sqlite3.connect(DB_FILE_PATH)
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE inventaire 
                    SET number_of_boxes = ?, quantity_in_box = ?, total_quantity = ?
                    WHERE id = ?
                ''', (number_of_boxes, quantity_in_box, total_quantity, id))
                
                if cursor.rowcount == 0:
                    st.error("Aucun enregistrement trouvé avec cet ID.")
                else:
                    conn.commit()
                    st.success("Données mises à jour avec succès.")
                    st.rerun()
            except Exception as e:
                st.error(f"Erreur lors de la mise à jour des données: {e}")
            finally:
                if conn:
                    conn.close()

def main():
    # Initialisation de la base de données
    init_database()
    
    tab_1, tab_2 = st.tabs(["Inventaire", "Mise à jour"])
    
    with tab_1:
        show_inventaire_form()
    
    with tab_2:
        show_update_form()

if __name__ == "__main__":
    main()