import streamlit as st
import random
import pandas as pd

VALID_LETTERS = ['A', 'B', 'C', 'E', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'R', 'S', 'T', 'V', 'X', 'Y']

# Dict Morse
MORSE_CODE = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..', '0': '-----', '1': '.----', '2': '..---',
    '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...',
    '8': '---..', '9': '----.', ' ': ' '
}

# Dict Morse to text
REVERSE_MORSE = {value: key for key, value in MORSE_CODE.items()}

st.page_link("Home.py", label="Retour", icon=":material/home:")
#st.write(st.session_state) # affiche SessionState pour Debug ...
tab1, tab2, tab3, tab4= st.tabs(["List Tools", "Convertion", "Postal_Gen", "Morse"])

def tab_1(): 
    
    st.header("Deux liste en Une ")
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
    st.header("Tool de conversion")
    pass
    
def generate_canada_postal():
    """Generate a valid Canadian postal code format: A1A 1A1"""
    return f"{random.choice(VALID_LETTERS)}{random.randint(0, 9)}{random.choice(VALID_LETTERS)} {random.randint(0, 9)}{random.choice(VALID_LETTERS)}{random.randint(0, 9)}"

def tab_3():
    st.header("Générateur de code postal")
    
    df = None
    
    with st.form("postal_code", clear_on_submit=True):
        x_postal_code = st.number_input(
            label="Nombre de génération",
            min_value=1,
            step=1,
            key='gen_postal_code',
            value=1
        )
        num_columns = st.number_input(
            label="Nombre de colonnes",
            min_value=1,
            max_value=10,
            value=1,
            step=1
        )
        submit = st.form_submit_button(label="Générer")
        
        if submit:
            postal_codes = [generate_canada_postal() for _ in range(x_postal_code)]
            rows_needed = (x_postal_code + num_columns - 1) // num_columns
            
            matrix = []
            for i in range(rows_needed):
                row = []
                for j in range(num_columns):
                    index = i + j * rows_needed
                    if index < len(postal_codes):
                        row.append(postal_codes[index])
                    else:
                        row.append("")
                matrix.append(row)
            
            df = pd.DataFrame(matrix, columns=[f"Colonne {i+1}" for i in range(num_columns)])
    
    if df is not None:
        st.dataframe(df, height=1000)  # Ajust as needed
        st.write(f"Nombre total de codes postaux générés : {len(df) * len(df.columns)}")
def text_to_morse(text):
    return ' '.join(MORSE_CODE.get(char.upper(), char) for char in text)

def morse_to_text(morse):
    try:
        return ''.join(REVERSE_MORSE.get(code, '') for code in morse.split())
    except:
        return "Format Morse invalide"

def tab_4():
    st.header("Convertisseur Morse")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Texte vers Morse")
        text_input = st.text_input("Entrez votre texte:", key="text_to_morse")
        if text_input:
            st.code(text_to_morse(text_input))
            
    with col2:
        st.subheader("Morse vers Texte")
        morse_input = st.text_input("Entrez le code Morse (séparé par des espaces):", key="morse_to_text")
        if morse_input:
            st.code(morse_to_text(morse_input))
        st.button("Audio Morse")
        st.write("L'audio Morse fonction a venir ...")
    st.divider()
    st.caption("Guide Morse:")
    num_columns = 5
    morse_items = list(MORSE_CODE.items())
    rows_needed = (len(morse_items) + num_columns - 1) // num_columns

    matrix = []
    for i in range(rows_needed):
        row = []
        for j in range(num_columns):
            index = i + j * rows_needed
            if index < len(morse_items):
                row.append(morse_items[index])
            else:
                row.append(("", ""))
        matrix.append(row)

    df = pd.DataFrame(matrix, columns=[f"Colonne {i+1}" for i in range(num_columns)])
    st.dataframe(df.style.set_properties(**{'width': '100px'}), width=600, hide_index=True)

with tab2:
    st.title("Conversion")
    tab_2()

with tab3:
    st.title("Postal Code Generator")
    tab_3()

with tab4:
    st.title("Morse Converter")
    tab_4()