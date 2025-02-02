import streamlit as st
from datetime import datetime, timedelta
import json
import os
import time
#import smtplib
#from email.mime.text import MIMEText
#from email.mime.multipart import MIMEMultipart

# Configuration de la page
st.set_page_config(page_title="Gestionnaire de Chronomètres", layout="wide")

class ChronoManager:
    def __init__(self):
        self.file_path = "chronos.json"
        self.chronos = {}
        self.load_chronos()

    def load_chronos(self):
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, 'r') as f:
                    data = json.load(f)
                    for name, chrono_info in data.items():
                        if isinstance(chrono_info, dict):
                            self.chronos[name] = {
                                'duration': timedelta(seconds=float(chrono_info['duration_seconds'])),
                                'start_time': datetime.fromisoformat(chrono_info['start_time']),
                                'notification_sent': chrono_info.get('notification_sent', False)
                            }
        except Exception as e:
            st.error(f"Erreur lors du chargement des chronos: {str(e)}")
            self.chronos = {}

    def save_chronos(self):
        try:
            data = {}
            for name, chrono in self.chronos.items():
                data[name] = {
                    'duration_seconds': chrono['duration'].total_seconds(),
                    'start_time': chrono['start_time'].isoformat(),
                    'notification_sent': chrono.get('notification_sent', False)
                }
            with open(self.file_path, 'w') as f:
                json.dump(data, f)
        except Exception as e:
            st.error(f"Erreur lors de la sauvegarde des chronos: {str(e)}")

    def add_chrono(self, name, duration):
        """Ajoute un nouveau chronomètre"""
        if name not in self.chronos:
            self.chronos[name] = {
                'duration': duration,
                'start_time': datetime.now(),
                'notification_sent': False
            }
            self.save_chronos()
            return True
        return False

    def remove_chrono(self, name):
        """Supprime un chronomètre"""
        if name in self.chronos:
            del self.chronos[name]
            self.save_chronos()

    def get_remaining_time(self, name):
        """Obtient le temps restant pour un chronomètre"""
        if name not in self.chronos:
            return timedelta()
        
        chrono = self.chronos[name]
        elapsed = datetime.now() - chrono['start_time']
        remaining = chrono['duration'] - elapsed
        
        return remaining if remaining.total_seconds() > 0 else timedelta()

# Initialisation du gestionnaire dans session_state
if 'chrono_manager' not in st.session_state:
    st.session_state.chrono_manager = ChronoManager()

# Titre de l'application
st.title("🕒 Gestionnaire de Chronomètres")

# Formulaire d'ajout de chronomètre
with st.form("add_chrono_form"):
    st.subheader("Ajouter un nouveau chronomètre")
    name = st.text_input("Nom du chronomètre")
   # phone = st.text_input("Numéro de téléphone Bell (format: 1234567890)")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        hours = st.number_input("Heures", min_value=0, max_value=23, step=1)
    with col2:
        minutes = st.number_input("Minutes", min_value=0, max_value=59, step=1)
    with col3:
        seconds = st.number_input("Secondes", min_value=0, max_value=59, step=1)
    
    submitted = st.form_submit_button("Ajouter")
    
    if submitted:
        if not name:
            st.error("Veuillez entrer un nom pour le chronomètre")
        elif hours == 0 and minutes == 0 and seconds == 0:
            st.error("Veuillez entrer une durée supérieure à 0")
        else:
            duration = timedelta(hours=hours, minutes=minutes, seconds=seconds)
            # Nettoie le numéro de téléphone
            
            if st.session_state.chrono_manager.add_chrono(name, duration):
                pass
            else:
                st.error(f"Un chronomètre avec le nom '{name}' existe déjà")

# Affichage et gestion des chronomètres existants
st.subheader("Chronomètres en cours")

# Container pour les chronos
for name in list(st.session_state.chrono_manager.chronos.keys()):
    remaining_time = st.session_state.chrono_manager.get_remaining_time(name)
    is_expired = remaining_time.total_seconds() <= 0
    chrono = st.session_state.chrono_manager.chronos[name]
    
    with st.container():
        col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
        
        with col1:
            if is_expired:
                st.markdown(f"### 🔴 {name}")
            else:
                st.markdown(f"### ⏳ {name}")
                
        with col2:
            if is_expired:
                st.markdown("""
                    <div style='color: red; font-weight: bold;'>
                        Temps écoulé!
                    </div>
                """, unsafe_allow_html=True)
            else:
                hours = int(remaining_time.total_seconds() // 3600)
                minutes = int((remaining_time.total_seconds() % 3600) // 60)
                seconds = int(remaining_time.total_seconds() % 60)
                st.markdown(f"**{hours:02d}:{minutes:02d}:{seconds:02d}**")
        
        with col3:
            if chrono.get('phone_number'):
                st.text(f"📱 {chrono['phone_number']}")
        
        with col4:
            if st.button("Supprimer", key=f"delete_{name}"):
                st.session_state.chrono_manager.remove_chrono(name)
                
time.sleep(1)
st.rerun()