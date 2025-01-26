import streamlit as st

# initialisation Session State
if 'lang_' not in st.session_state:
    st.session_state.lang_ = "FR"

st.set_page_config(
    page_title="PolyTools",
    page_icon=":gears:",
    layout="wide"
)
st.title("Bienvenu sur le site PolyTools !")

st.write("Des outils pour tous les besoins au bout des doigts")

st.session_state
