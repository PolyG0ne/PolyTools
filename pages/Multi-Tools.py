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
tab1, tab2, tab3= st.tabs(["List Tools", "Convertion", "Postal_Gen"])

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
    conversion_choice = st.selectbox("Choix de la conversion", ['Morse', 'Alpha', 'Binaire', 'Signe', 'Code'])
   
    ### Morse ###
    if conversion_choice == 'Morse':
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

        df = pd.DataFrame(matrix)
        st.dataframe(df.style.set_properties(**{'width': '100px'}), width=600, hide_index=True)
    
    ### Alpha ###
    elif conversion_choice == 'Alpha':
        st.header("Convertisseur Alphabet Phonétique")
        
        PHONETIC_DICT = {
            'A': 'Alpha', 'B': 'Bravo', 'C': 'Charlie', 'D': 'Delta',
            'E': 'Echo', 'F': 'Foxtrot', 'G': 'Golf', 'H': 'Hotel',
            'I': 'India', 'J': 'Juliet', 'K': 'Kilo', 'L': 'Lima',
            'M': 'Mike', 'N': 'November', 'O': 'Oscar', 'P': 'Papa',
            'Q': 'Quebec', 'R': 'Romeo', 'S': 'Sierra', 'T': 'Tango',
            'U': 'Uniform', 'V': 'Victor', 'W': 'Whiskey', 'X': 'X-ray',
            'Y': 'Yankee', 'Z': 'Zulu', '0': 'Zero', '1': 'One',
            '2': 'Two', '3': 'Three', '4': 'Four', '5': 'Five',
            '6': 'Six', '7': 'Seven', '8': 'Eight', '9': 'Nine'
        }
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Texte vers Phonétique")
            text_input = st.text_input("Entrez votre texte:", key="text_to_alpha")
            if text_input:
                alpha_output = ' '.join(PHONETIC_DICT.get(c.upper(), c) for c in text_input)
                st.code(alpha_output)
                
        with col2:
            st.subheader("Phonétique vers Texte")
            alpha_input = st.text_input("Entrez le texte phonétique (ex: Alpha Bravo):", key="alpha_to_text")
            if alpha_input:
                reverse_dict = {v: k for k, v in PHONETIC_DICT.items()}
                text_output = ''.join(reverse_dict.get(word, word) for word in alpha_input.split())
                st.code(text_output)
        
        st.divider()
        st.caption("Guide Alphabet Phonétique:")
        phonetic_items = list(PHONETIC_DICT.items())
        phonetic_df = pd.DataFrame(phonetic_items, columns=['Caractère', 'Mot'])
        st.dataframe(phonetic_df, width=300)
    
    ### Binaire ###
    elif conversion_choice == 'Binaire':
        st.header("Convertisseur Binaire")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Texte vers Binaire")
            text_input = st.text_input("Entrez votre texte:", key="text_to_binary")
            if text_input:
                binary_output = ' '.join(format(ord(c), '08b') for c in text_input)
                st.code(binary_output)
                
        with col2:
            st.subheader("Binaire vers Texte")
            binary_input = st.text_input("Entrez le code binaire (séparé par des espaces):", key="binary_to_text")
            if binary_input:
                try:
                    text_output = ''.join(chr(int(b, 2)) for b in binary_input.split())
                    st.code(text_output)
                except ValueError:
                    st.error("Format binaire invalide")
    
    ### Signe ###
    elif conversion_choice == 'Signe':
        st.header("Convertisseur Signe")
        
        SIGN_DICT = {
            'A': '👊', 'B': '🖐️', 'C': '🤏', 'D': '👆', 
            'E': '🫰', 'F': '🤌', 'G': '👌', 'H': '🤞',
            'I': '🤙', 'J': '🤙', 'K': '🫲', 'L': '🤟',
            'M': '✌️', 'N': '👉', 'O': '⭕', 'P': '👇',
            'Q': '👇', 'R': '🤘', 'S': '✊', 'T': '👆',
            'U': '🫰', 'V': '✌️', 'W': '🤘', 'X': '🫰',
            'Y': '🤙', 'Z': '👆'
        }
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Texte vers Signes")
            text_input = st.text_input("Entrez votre texte:", key="text_to_signs")
            if text_input:
                signs_output = ' '.join(SIGN_DICT.get(c.upper(), c) for c in text_input)
                st.write(signs_output)
                
        with col2:
            st.subheader("Signes vers Texte")
            signs_input = st.text_input("Entrez les signes (séparés par des espaces):", key="signs_to_text")
            if signs_input:
                reverse_dict = {v: k for k, v in SIGN_DICT.items()}
                text_output = ''.join(reverse_dict.get(s, s) for s in signs_input.split())
                st.code(text_output)
        
        st.divider()
        st.caption("Guide des signes:")
        sign_items = list(SIGN_DICT.items())
        sign_df = pd.DataFrame(sign_items, columns=['Lettre', 'Signe'])
        st.dataframe(sign_df, width=300)
    
    ### Code ###
    elif conversion_choice == 'Code':
        st.header("Convertisseur Code")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Texte vers Code")
            text_input = st.text_input("Entrez votre texte:", key="text_to_code")
            encoding = st.selectbox("Sélectionnez l'encodage:", 
                                  ['Base64', 'URL', 'HTML'], key="encoding")
            
            if text_input:
                if encoding == 'Base64':
                    import base64
                    encoded = base64.b64encode(text_input.encode()).decode()
                elif encoding == 'URL':
                    import urllib.parse
                    encoded = urllib.parse.quote(text_input)
                elif encoding == 'HTML':
                    import html
                    encoded = html.escape(text_input)
                st.code(encoded)
                
        with col2:
            st.subheader("Code vers Texte")
            code_input = st.text_input("Entrez le code:", key="code_to_text")
            decoding = st.selectbox("Sélectionnez le décodage:",
                                  ['Base64', 'ROT13', 'URL', 'HTML'], key="decoding")
            
            if code_input:
                try:
                    if decoding == 'Base64':
                        decoded = base64.b64decode(code_input).decode()
                    elif decoding == 'ROT13':
                        decoded = int(code_input.decode('rot13')) # fix this
                    elif decoding == 'URL':
                        decoded = urllib.parse.unquote(code_input)
                    elif decoding == 'HTML':
                        decoded = html.unescape(code_input)
                    st.code(decoded)
                except Exception as e:
                    st.error(f"Erreur de décodage: {str(e)}")
    
    else:
        st.write("Choix invalide")
        
def text_to_morse(text):
    return ' '.join(MORSE_CODE.get(char.upper(), char) for char in text)

def morse_to_text(morse):
    try:
        return ''.join(REVERSE_MORSE.get(code, '') for code in morse.split())
    except:
        return "Format Morse invalide"

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

with tab1:
    st.title("List Tools")
    tab_1()

with tab2:
    st.title("Conversion")
    tab_2()

with tab3:
    st.title("Postal Code Generator")
    tab_3()
