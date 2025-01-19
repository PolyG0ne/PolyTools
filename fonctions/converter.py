import streamlit as st

option_types = ["Longueurs", "Poids", "Distances", "Liquides", "Température"]
option_types1 = ["Truc Chose", "Patente Chouette", "Patente a goss aussi", "Saparlipopette", "Bettrave"]

option_param = []
convert_choice = []

def call_back():
    st.write(st.session_state.list_convert)
    st.write(st.session_state.choice)
