import streamlit as st

# initialisation Session State
if 'lang_' not in st.session_state:
    st.session_state['lang_'] = "ZH"

st.title("Bienvenu sur le site PolyTools !")

st.write("Des outils pour tous les besoins au bout des doigts")