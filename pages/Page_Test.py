import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime

# Configuration de la page
st.set_page_config(page_title="Visualisation 3D Interactive", layout="wide")

# Contrôles dans la barre latérale
st.sidebar.header("Paramètres de visualisation")

# Contrôles pour la génération de données
n_points = st.sidebar.slider("Nombre de points", 10, 1000, 100)
noise_level = st.sidebar.slider("Niveau de bruit", 0.1, 5.0, 1.0)

# Contrôles pour la caméra
camera_x = st.sidebar.slider("Camera X", -5.0, 5.0, 1.5)
camera_y = st.sidebar.slider("Camera Y", -5.0, 5.0, 1.5)
camera_z = st.sidebar.slider("Camera Z", -5.0, 5.0, 1.5)

# Contrôles pour l'apparence
point_size = st.sidebar.slider("Taille des points", 1, 20, 5)
opacity = st.sidebar.slider("Opacité", 0.1, 1.0, 0.8)

# Sélection des catégories
categories = st.sidebar.multiselect(
    "Catégories à afficher",
    ["A", "B", "C"],
    default=["A", "B", "C"]
)

# Bouton pour générer de nouvelles données
if st.sidebar.button("Générer nouvelles données"):
    # Génération des données
    df = pd.DataFrame({
        'x': np.random.normal(0, noise_level, n_points),
        'y': np.random.normal(0, noise_level, n_points),
        'z': np.random.normal(0, noise_level, n_points),
        'category': np.random.choice(categories, n_points)
    })
    
    # Filtrage des données selon les catégories sélectionnées
    df = df[df['category'].isin(categories)]
    
    # Création du graphique 3D
    fig = px.scatter_3d(
        df, 
        x='x', 
        y='y', 
        z='z',
        color='category',
        title='Visualisation 3D Interactive',
        labels={'x': 'Axe X', 'y': 'Axe Y', 'z': 'Axe Z'}
    )
    
    # Configuration du layout
    fig.update_traces(marker_size=point_size, opacity=opacity)
    fig.update_layout(
        scene=dict(
            camera=dict(
                up=dict(x=0, y=0, z=1),
                center=dict(x=0, y=0, z=0),
                eye=dict(x=camera_x, y=camera_y, z=camera_z)
            )
        ),
        height=700
    )
    
    # Affichage du graphique
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Cliquez sur 'Générer nouvelles données' pour visualiser le graphique")
