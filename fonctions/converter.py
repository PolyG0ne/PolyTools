import streamlit as st
import pandas as pd


#########
# MORSE #
#########

MORSE_CODE = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..', '0': '-----', '1': '.----', '2': '..---',
    '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...',
    '8': '---..', '9': '----.', ' ': ' '
}

REVERSE_MORSE = {value: key for key, value in MORSE_CODE.items()}

def text_to_morse(text):
    return ' '.join(MORSE_CODE.get(char.upper(), char) for char in text)

def morse_to_text(morse):
    return ''.join(REVERSE_MORSE.get(code, '') if code != '' else ' ' for code in morse.split(' '))

def morse():
    st.header("Text -> Morse & Morse -> Text")
    phrase_convert=st.text_input("text -> morse", placeholder="Texte, Phrase, Chiffre.. etc")

    if phrase_convert:
        st.write("Result : ")
        st.code(text_to_morse(phrase_convert))

    morse_convert=st.text_input("morse -> text", placeholder="Morse...")

    if morse_convert:
        st.code(morse_to_text(morse_convert))
    ## ------ # 
    ## Guide Morse #
    st.divider()
    st.caption("Guide Morse:")
    morse_items = list(MORSE_CODE.items())
    morse_df = pd.DataFrame(morse_items, columns=['Caractère', 'Mot'])
    st.dataframe(morse_df, width=175, hide_index=True)
    #st.code(MORSE_CODE, wrap_lines=True)

#########
# ALPHA #
#########

def alpha():

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

    st.header("Alphabet Phonetique")

    st.subheader("Texte -> Phonétique")
    text_input = st.text_input("Entrez votre texte:", key="text_to_alpha", placeholder="Text..")
    if text_input:
        alpha_output = ' '.join(PHONETIC_DICT.get(c.upper(), c) for c in text_input)
        st.code(alpha_output)
   
    st.subheader("Phonétique -> Texte")
    alpha_input = st.text_input("Entrez le texte phonétique (ex: Alpha Bravo):", key="alpha_to_text", placeholder="mots alpha")
    if alpha_input:
        reverse_dict = {v: k for k, v in PHONETIC_DICT.items()}
        text_output = ''.join(reverse_dict.get(word, word) for word in alpha_input.split())
        st.code(text_output)

    st.divider()
    st.caption("Guide Alphabet Phonétique:")
    phonetic_items = list(PHONETIC_DICT.items())
    phonetic_df = pd.DataFrame(phonetic_items, columns=['Caractère', 'Mot'])
    st.dataframe(phonetic_df, width=175, hide_index=True)
    #st.code(PHONETIC_DICT, wrap_lines=True, line_numbers=False)

########
# CODE #
########

def code():
    import base64
    import urllib.parse
    import html

    st.header("Convertisseur Code")

    st.subheader("Texte -> Code")
    text_input = st.text_input("Entrez votre texte:", key="text_to_code")
    encoding = st.selectbox("Sélectionnez l'encodage:", ['Base64', 'Binaire', 'URL', 'HTML'], key="encoding")

    if text_input:
        if encoding == 'Base64':
            encoded = base64.b64encode(text_input.encode()).decode()
        elif encoding == 'Binaire':
            encoded = ' '.join(format(ord(c), '08b') for c in text_input)
        elif encoding == 'URL':
            encoded = urllib.parse.quote(text_input)
        elif encoding == 'HTML':
            encoded = html.escape(text_input)
        st.code(encoded)
            

    st.subheader("Code -> Texte")
    code_input = st.text_input("Entrez le code:", key="code_to_text")
    decoding = st.selectbox("Sélectionnez le décodage:",['Base64', 'Binaire', 'URL', 'HTML'], key="decoding")
    
    if code_input:
        try:
            if decoding == 'Base64':
                decoded = base64.b64decode(code_input).decode()
            elif decoding == 'Binaire':
                decoded =  ''.join(chr(int(b, 2)) for b in code_input.split())
            elif decoding == 'URL':
                decoded = urllib.parse.unquote(code_input)
            elif decoding == 'HTML':
                decoded = html.unescape(code_input)
            st.code(decoded)
        except Exception as e:
            st.error(f"Erreur de décodage: {str(e)}")

##########
# VOLUME #
##########

dict_convert = {
    'Litre': 1,
    'Gallon US': 0.264172,
    'Millilitre': 1000,
    'Once liquide': 33.814,
    'Pinte': 2.11338,
    'Quart': 1.05669,
    'Tasse': 4.22675,
    'Cuillère à soupe': 67.628,
    'Cuillère à thé': 202.884
}

def converting(input_val, choice_input, choice_convert):
    factor_input = dict_convert[choice_input]
    factor_convert = dict_convert[choice_convert]
    volume_output = input_val / factor_input * factor_convert
    return volume_output

def volume():
    st.header("Convertisseur de Volume")

    choice = st.selectbox("Volume : ", dict_convert.keys())
    volume_input = st.number_input("Quantité : ")
    convert_choice = st.selectbox("Convertir en :", 
                                [key for key in dict_convert.keys() if key != choice])

    if st.button("Convertir"):  # Correction du bouton
        result = converting(volume_input, choice, convert_choice)
        st.write(f"{volume_input} {choice} = {result:.4f} {convert_choice}")