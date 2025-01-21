import streamlit as st

st.title(":material/glyphs:")
st.write("Page pour tester du code")
st.divider()

if 'name' not in st.session_state:
    st.session_state.name = ''

name = st.text_input("Enter your name : ", on_change=None)

def named(name):
    st.session_state.name = name

name_record = st.button("Save",on_click=named, args=[name])
st.write(st.session_state.name)


if name_record:
    st.write("le if du bouton est True")