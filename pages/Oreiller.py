import streamlit as st
import json
import datetime
import pandas as pd
from traduction import traduction# fichier traduction.py qui incluts les traductions 

date_today = datetime.datetime.now()
formatted_now = date_today.strftime("%Y-%m-%d | %H:%M")
st.page_link("Home.py", label="Retour", icon=":material/home:")
st.title(traduction.dict_lang[st.session_state['lang_']]['titre-oreiller'])

# Charger les données depuis le fichier JSON
try:
    with open("oreiller.json", "r") as f:
        data = json.load(f)
except FileNotFoundError:
    data = []

# Fonction pour enregistrer les modifications dans le fichier JSON
def save_data(df):
    df.to_json("oreiller.json", orient='records', indent=4)

def save_session(json):
    json.dump("oreiller.json", indent=4, encoding='utf-8')

with st.form(key="oreiller_form", clear_on_submit=True):
    nombre_oreiller = st.radio(traduction.dict_lang[st.session_state['lang_']]['Qut'], ["1", "2", "3", "4", "5", "6", "7"], horizontal=True)
    num_chambre = st.number_input(label=traduction.dict_lang[st.session_state['lang_']]['ch'], placeholder="1000 ou 4010 exemple", step=1)
    date = st.date_input(traduction.dict_lang[st.session_state['lang_']]['cl_qt'])
    commentaire = st.text_area(label=traduction.dict_lang[st.session_state['lang_']]['com'])
    initial = st.text_input(traduction.dict_lang[st.session_state['lang_']]['init'])
    today = st.text_input(label=traduction.dict_lang[st.session_state['lang_']]['now'], value=formatted_now, disabled=True)
    submit = st.form_submit_button(label=traduction.dict_lang[st.session_state['lang_']]['save'], icon=":material/check:")

    if submit:
        data.append({"Qte": int(nombre_oreiller), "Ch.": num_chambre, "Départ": str(date), "Ini.": initial.upper(),
                     "Date": today, "Comm.": commentaire, "Recup.": False})
        with open("oreiller.json", "w") as f:
            json.dump(data, f)

st.write(datetime.datetime.now())

df = pd.DataFrame(data)

st.table(data=df)

st.dataframe(data=df, hide_index=True)

# Afficher l'éditeur de données avec la case à cocher
edited_df = st.data_editor(data=df, key='edit_df', hide_index=True)

save_button = st.button(label="Save")

if save_button:
    save_data(edited_df)
    #st.session_state.qt_or = 
    st.success("Modifications enregistrées !")