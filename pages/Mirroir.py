import streamlit as st
from pages.fonctions.config_miroir import ReflectionSimulator

if __name__ == "__main__":
    st.set_page_config(
        page_title="Simulateur de Réflexion 3D",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    simulator = ReflectionSimulator()
    simulator.run()