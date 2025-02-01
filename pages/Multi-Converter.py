import streamlit as st
from fonctions.converter import morse, alpha, code, volume, distance, surface

if "conversion_choice" not in st.session_state:
    st.session_state.conversion_choice = ""

st.title("Multi-Converter")
st.header("Tools de conversion")

conversion_choice = st.selectbox("Choix de la conversion", ['--', 'Morse', 'Alpha', 'Code', 'Volume', 'Distance', 'Surface' ])
# , 'Binaire', 'Signe',
#     'Code', 'Poids', 'Longueur', 'Température',
#     'Volume', 'Vitesse', 'Pression', 'Energie',
#     'Surface', 'Angle'

if conversion_choice == "--":
    st.write("--")

if conversion_choice == "Morse":
    morse()

if conversion_choice == "Alpha":
    alpha()

if conversion_choice == "Code":
    code()

if conversion_choice == "Volume":
    volume()

if conversion_choice == "Distance":
    distance()

if conversion_choice == "Surface":
    surface()