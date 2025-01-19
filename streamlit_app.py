import streamlit as st
from fonctions import converter

# initialisation Session State
if 'list_convert' not in st.session_state:
    st.session_state['list_convert'] = None
if 'choice' not in st.session_state:
    st.session_state['choice'] = None

st.write(st.session_state) # affiche SessionState pour Debug ...
tab1, tab2, tab3 = st.tabs(["List Tools", "Convertion", "Notes"])

def tab_1():
    
    st.title("Deux liste en Une ")
    with st.form("list_form", clear_on_submit=True):
        list_1 = st.text_input(label="Première Liste:", value="", key='list1', max_chars=None, placeholder="Liste séparé par \" , \" - Exemple : Cravate, Marteau, Broche")
        list_2 = st.text_input(label="Deuxième Liste:", value="", key='list2', max_chars=None, placeholder="Liste séparé par \" , \" - Exemple : Chat, Chien, Oiseau", on_change=None)
        
        submit= st.form_submit_button(label="Envoyé", on_click=None, icon=":material/send:")
        
    if submit:
        list_1_split = list_1.split(",")
        list_2_split = list_2.split(",")
        
        list_jointed = []
        count = 0
        try:
            for item in list_1_split:
                list_jointed.append(f"{item}{list_2_split[count]}")
                count += 1
        except IndexError:
            st.error("Même nombre de virgule pour les 2 listes - LA LISTE N'EST PAS CONFORME")
        st.code(list_jointed, language="None", line_numbers=False)

def tab_2():
    convert_choice = st.pills(label="Types",
            options=converter.option_types,
            key='list_convert', on_change=converter.call_back,) #max_selections=1)

    if convert_choice != []:
        if convert_choice == ["Longueurs"]:
            choice_cm = st.multiselect(label="CM", key='choice',
            options=["MM", "CM", "Metres", "Pieds", "Pouces", ], on_change=converter.call_back, max_selections=None)

with tab1:
    st.header("Creating List")
    tab_1()

with tab2:
    st.header("Conversion")
    tab_2()
    
