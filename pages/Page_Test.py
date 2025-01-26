import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime
import time

# Configuration de la page Streamlit
st.set_page_config(page_title="Visualisation 3D en temps réel", layout="wide")

# Fonction pour générer des données 3D aléatoires
def generate_data():
    n_points = 100
    return pd.DataFrame({
        'x': np.random.normal(0, 1, n_points),
        'y': np.random.normal(0, 1, n_points),
        'z': np.random.normal(0, 1, n_points),
        'time': datetime.now(),
        'category': np.random.choice(['A', 'B', 'C'], n_points)
    })

# Création du graphique
placeholder = st.empty()

while True:
    # Génération de nouvelles données
    df = generate_data()
    
    # Création du graphique 3D avec Plotly
    fig = px.scatter_3d(
        df, 
        x='x', 
        y='y', 
        z='z',
        color='category',
        title=f'Visualisation 3D - Mise à jour: {df.time[0].strftime("%H:%M:%S")}',
        labels={'x': 'Axe X', 'y': 'Axe Y', 'z': 'Axe Z'}
    )
    
    # Configuration du layout
    fig.update_layout(
        scene=dict(
            camera=dict(
                up=dict(x=0, y=0, z=1),
                center=dict(x=0, y=0, z=0),
                eye=dict(x=1.5, y=1.5, z=1.5)
            )
        ),
        height=700
    )
    
    # Mise à jour du graphique
    with placeholder.container():
        st.plotly_chart(fig, use_container_width=True)
    
    # Pause avant la prochaine mise à jour
    time.sleep(1)
