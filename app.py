import calendar
import json
import os
import streamlit as st

# 1. Configurazione della pagina
st.set_page_config(
    page_title="Calendario Ferie - OROPLAC",
    layout="wide"
)

# File locale per il salvataggio dei dati
DATA_FILE = "ferie_data.json"

# Funzioni per caricare e salvare i dati su file JSON
def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Inizializzazione dello Stato della Sessione
if "ferie_data" not in st.session_state:
    st.session_state.ferie_data = load_data()

if "current_year" not in st.session_state:
    st.session_state.current_year = 2026

if "current_month" not in st.session_state:
    st.session_state.current_month = 7  # Luglio

# Definizione Utenti e Colori (da image_7a076b.png)
USERS = {
    "MARTELLI": {"initial": "M", "color": "#00b0f0", "text_color": "#000000"},
    "FILARDO": {"initial": "F", "color": "#ffff00", "text_color": "#000000"},
    "CIAPPI": {"initial": "C", "color": "#ff0000", "text_color": "#ffffff"}
}

MESI = [
    "GENNAIO", "FEBBRAIO", "MARZO", "APRILE", "MAGGIO", "GIUGNO",
    "LUGLIO", "AGOSTO", "SETTEMBRE", "OTTOBRE", "NOVEMBRE", "DICEMBRE"
]

# Stili CSS Custom
st.markdown("""
    <style>
    .stButton > button {
        width: 100%;
        border-radius: 4px;
        font-weight: bold;
    }
    .month-title {
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        background-color: #e0e0e0;
        color: #000000 !important; /* Testo nero ben visibile */
        padding: 10px;
        border: 1px solid #b0b0b0;
        border-radius: 5px;
        margin-bottom: 10px;
    }
    .day-header {
        text-align: center;
        font-weight: bold;
        background-color: #333333;
        color: white;
        padding: 5px;
        border-radius: 3px;
    }
    </style>
""", unsafe_allow_html=True)

# Layout Principale
col_sidebar, col_main = st.columns([1, 3])

# --- SIDEBAR: SELEZIONE PERSONA E CONTROLLI ---
with col_sidebar:
    st.subheader("📋 Selezione Dipendente")
    selected_user = st.radio(
        "Scegli chi sta inserendo le ferie:",
        options=list(USERS.keys()),
        format_func=lambda user: f"{user} ({USERS[user]['initial']})"
    )

    # Anteprima Colore Utente
    u_info = USERS[selected_user]
    st.markdown(
        f"""
        <div style="background-color: {u_info['color']}; color: {u_info['text_color']}; 
                    padding: 10px; text-align: center; font-weight: bold; border-radius: 5px; border: 1px solid #000;">
            Selezionato: {selected_user} [{u_info['initial']}]
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    # Reset totale
    if st.button("🗑️ Cancella Tutti i Dati"):
        st.session_state.ferie_data = {}
        save_data({})
        st.rerun()

# --- MAIN: CALENDARIO ---
with col_main:
    # Controlli Navigazione Mese/Anno
    col_nav1, col_nav2, col_nav3 = st.columns([1, 3, 1])
    
    with col_nav1:
        if st.button("◄ Mese Precedente"):
            if st.session_state.current_month == 1:
                st.session_state.current_month = 12
                st.session_state.current_year -= 1
            else:
                st.session_state.current_month -= 1
            st.rerun()

    with col_nav3:
        if st.button("Mese Successivo ►"):
            if st.session_state.current_month == 12:
                st.session_state.current_month = 1
                st.session_state.current_year += 1
            else:
                st.session_state.current_month += 1
            st.rerun()

    with col_nav2:
        nome_mese = MESI[st.session_state.current_month - 1]
        st.markdown(
            f"<div class='month-title'>{nome_mese} {st.session_state.current_year}</div>", 
            unsafe_allow_html=True
        )

    # Intestazione Giorni della Settimana
    headers = ["LUN", "MAR", "MER", "GIO", "VEN", "SAB", "DOM"]
    cols_head = st.columns(7)
    for idx, h in enumerate(headers):
        cols_head[idx].markdown(f"<div class='day-header'>{h}</div>", unsafe_allow_html=True)

    # Matrice del Mese
    cal = calendar.Calendar(firstweekday=0) # 0 = Lunedì
    month_days = cal.monthdayscalendar(st.session_state.current_year, st.session_state.current_month)

    for week in month_days:
        cols = st.columns(7)
        for day_idx, day in enumerate(week):
            with cols[day_idx]:
                if day == 0:
                    st.write("") # Giorno vuoto fuori mese
                else:
                    # Chiave univoca data YYYY-MM-DD
                    date_key = f"{st.session_state.current_year}-{st.session_state.current_month:02d}-{day:02d}"
                    
                    # Recupera persone in ferie per questa data
                    active_users = st.session_state.ferie_data.get(date_key, [])

                    # Pulsante per la selezione/deselezione del giorno
                    if st.button(f"**{day}**", key=f"btn_{date_key}"):
                        if date_key not in st.session_state.ferie_data:
                            st.session_state.ferie_data[date_key] = []
                        
                        if selected_user in st.session_state.ferie_data[date_key]:
                            st.session_state.ferie_data[date_key].remove(selected_user)
                        else:
                            st.session_state.ferie_data[date_key].append(selected_user)
                        
                        save_data(st.session_state.ferie_data)
                        st.rerun()

                    # Costruzione Badge Visivi Affiancati (senza andare a capo)
                    badges_list = []
                    for user in active_users:
                        if user in USERS:
                            info = USERS[user]
                            badges_list.append(
                                f'<span style="background-color: {info["color"]}; color: {info["text_color"]}; '
                                f'padding: 2px 6px; font-size: 11px; font-weight: bold; border-radius: 3px; '
                                f'margin: 1px; display: inline-block;">{info["initial"]}</span>'
                            )

                    # Rendering HTML dei badge sotto il pulsante del giorno
                    if badges_list:
                        badges_html = "".join(badges_list)
                        st.markdown(
                            f'<div style="text-align: center; margin-top: 4px; line-height: 1.2;">{badges_html}</div>', 
                            unsafe_allow_html=True
                        )
