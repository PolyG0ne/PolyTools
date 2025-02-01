import streamlit as st
import pandas as pd

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

    # st.code([item for item in MORSE_CODE.items()], wrap_lines=True)

    st.code(MORSE_CODE, wrap_lines=True)
