import streamlit as st
import pandas as pd

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

def text_to_morse(text):
    return ' '.join(MORSE_CODE.get(char.upper(), char) for char in text)

def morse_to_text(morse):
    try:
        return ''.join(REVERSE_MORSE.get(code, '') for code in morse.split())
    except:
        return "Format Morse invalide"
    
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