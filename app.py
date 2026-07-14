import calendar
import json
import os
import streamlit as st

# 1. Configurazione Pagina
st.set_page_config(
    page_title="Calendario Ferie - OROPLAC",
    layout="wide"
)

# File locale per il salvataggio dei dati
DATA_FILE = "ferie_data.json"

# Funzioni caricamento/salvataggio dati
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

# Inizializzazione Session State
if "ferie_data" not in st.session_state:
    st.session_state.ferie_data = load_data()

if "current_year" not in st.session_state:
    st.session_state.current_year = 2026

if "current_month" not in st.session_state:
    st.session_state.current_month = 7  # Luglio

# Configurazione Utenti (da image_7a076b.png)
USERS = {
    "MARTELLI": {"initial": "M", "color": "#00b0f0", "text_color": "#ffffff"},
    "FILARDO": {"initial": "F", "color": "#ffd700", "text_color": "#000000"},
    "CIAPPI": {"initial": "C", "color": "#e63946", "text_color": "#ffffff"}
}

MESI = [
    "GENNAIO", "FEBBRAIO", "MARZO", "APRILE", "MAGGIO", "GIUGNO",
    "LUGLIO", "AGOSTO", "SETTEMBRE", "OTTOBRE", "NOVEMBRE", "DICEMBRE"
]

# Stili CSS Avanzati per il nuovo Layout Moderno (ispirato a image_7b0367.png)
st.markdown("""
    <style>
    /* Titolo del Mese */
    .month-title {
        text-align: center;
        font-size: 22px;
        font-weight: 700;
        background-color: #1e293b;
        color: #ffffff !important;
        padding: 12px;
        border-radius: 8px;
        margin-bottom: 15px;
        letter-spacing: 1px;
    }

    /* Intestazione Giorni della Settimana */
    .day-header {
        text-align: center;
        font-weight: 700;
        font-size: 13px;
        background-color: #0f172a;
        color: #94a3b8;
        padding: 8px;
        border-radius: 6px;
        margin-bottom: 8px;
    }

    /* Contenitore della Card del Giorno */
    .day-card {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 8px 4px;
        min-height: 85px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 8px;
    }

    /* Pulsante Giorno Custom */
    .stButton > button {
        width: 100%;
        border-radius: 6px;
        font-weight: bold;
        background-color: #334155;
        color: #ffffff;
        border: none;
        padding: 4px 0px;
    }
    
    .stButton > button:hover {
        background-color: #475569;
        color: #ffffff;
    }

    /* Legenda */
    .legend-card {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
    }
    
    .legend-item {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 10px;
        font-weight: 600;
        color: #f8fafc;
    }

    .badge-square {
        width: 28px;
        height: 28px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 5px;
        font-weight: bold;
        font-size: 13px;
    }
    </style>
""", unsafe_allow_html=True)

# Layout Principale
col_sidebar, col_main = st.columns([1, 3.2])

# --- SIDEBAR: SELEZIONE DIPENDENTE E LEGENDA ---
with col_sidebar:
    st.markdown("<h3 style='color: #f8fafc;'>👤 Selezione Operatore</h3>", unsafe_allow_html=True)
    
    selected_user = st.radio(
        "Chi sta inserendo le ferie?",
        options=list(USERS.keys()),
        format_func=lambda user: f"{user} ({USERS[user]['initial']})"
    )

    u_info = USERS[selected_user]
    st.markdown(
        f"""
        <div style="background-color: {u_info['color']}; color: {u_info['text_color']}; 
                    padding: 10px; text-align: center; font-weight: bold; border-radius: 8px; margin-top: 10px;">
            SELEZIONATO: {selected_user} [{u_info['initial']}]
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)
    
    # BOX LEGENDA (ispirato all'immagine image_7b0367.png)
    st.markdown("<h4 style='color: #cbd5e1;'>📌 Legenda Colori</h4>", unsafe_allow_html=True)
    legend_html = "<div class='legend-card'>"
    for name, info in USERS.items():
        legend_html += f"""
        <div class='legend-item'>
            <div class='badge-square' style='background-color: {info["color"]}; color: {info["text_color"]};'>
                {info["initial"]}
            </div>
            <span>{name}</span>
        </div>
        """
    legend_html += "</div>"
    st.markdown(legend_html, unsafe_allow_html=True)

    # Pulsante Reset
    if st.button("🗑️ Reset Dati Ferie"):
        st.session_state.ferie_data = {}
        save_data({})
        st.rerun()

# --- MAIN: CALENDARIO RACCHIUSO ---
with col_main:
    # Controlli Navigazione Mese/Anno
    col_nav1, col_nav2, col_nav3 = st.columns([1, 2.5, 1])
    
    with col_nav1:
        if st.button("◄ Mese Prec."):
            if st.session_state.current_month == 1:
                st.session_state.current_month = 12
                st.session_state.current_year -= 1
            else:
                st.session_state.current_month -= 1
            st.rerun()

    with col_nav3:
        if st.button("Mese Succ. ►"):
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
                    # Spazio vuoto per giorni fuori mese
                    st.markdown("<div style='min-height: 85px;'></div>", unsafe_allow_html=True)
                else:
                    date_key = f"{st.session_state.current_year}-{st.session_state.current_month:02d}-{day:02d}"
                    active_users = st.session_state.ferie_data.get(date_key, [])

                    # Costruzione Badge Visivi dentro la Card
                    badges_list = []
                    for user in active_users:
                        if user in USERS:
                            info = USERS[user]
                            badges_list.append(
                                f'<span style="background-color: {info["color"]}; color: {info["text_color"]}; '
                                f'padding: 3px 6px; font-size: 11px; font-weight: bold; border-radius: 4px; '
                                f'margin: 1px; display: inline-block;">{info["initial"]}</span>'
                            )
                    
                    badges_html = "".join(badges_list) if badges_list else "&nbsp;"

                    # Renderizziamo il Pulsante e sotto i Badge delimitati
                    if st.button(f"{day}", key=f"btn_{date_key}"):
                        if date_key not in st.session_state.ferie_data:
                            st.session_state.ferie_data[date_key] = []
                        
                        if selected_user in st.session_state.ferie_data[date_key]:
                            st.session_state.ferie_data[date_key].remove(selected_user)
                        else:
                            st.session_state.ferie_data[date_key].append(selected_user)
                        
                        save_data(st.session_state.ferie_data)
                        st.rerun()

                    # Contenitore sotto il bottone con bordo sottile per racchiudere le icone
                    st.markdown(
                        f"""
                        <div style="text-align: center; background-color: #0f172a; padding: 4px; 
                                    border-radius: 6px; border: 1px solid #334155; margin-top: -8px; min-height: 28px;">
                            {badges_html}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
