import calendar
import json
import os
import streamlit as st

# 1. Configurazione Pagina
st.set_page_config(page_title="Calendario Ferie - OROPLAC", layout="wide")

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

# Configurazione Utenti
USERS = {
    "MARTELLI": {"initial": "M", "color": "#00b0f0", "text_color": "#ffffff"},
    "FILARDO": {"initial": "F", "color": "#ffd700", "text_color": "#000000"},
    "CIAPPI": {"initial": "C", "color": "#e63946", "text_color": "#ffffff"},
}

MESI = [
    "GENNAIO",
    "FEBBRAIO",
    "MARZO",
    "APRILE",
    "MAGGIO",
    "GIUGNO",
    "LUGLIO",
    "AGOSTO",
    "SETTEMBRE",
    "OTTOBRE",
    "NOVEMBRE",
    "DICEMBRE",
]

# CSS Perfetto per uniformare il pulsante e la cella
st.markdown(
    """
    <style>
    /* Titolo del Mese */
    .month-title {
        text-align: center;
        font-size: 24px;
        font-weight: 800;
        background-color: #1e293b;
        color: #ffffff !important;
        padding: 10px;
        border-radius: 6px;
        margin-bottom: 10px;
        border: 1px solid #334155;
    }

    /* Intestazione Giorni */
    .day-header {
        text-align: center;
        font-weight: 800;
        font-size: 14px;
        background-color: #0f172a;
        color: #94a3b8;
        padding: 8px;
        border-radius: 4px;
        margin-bottom: 6px;
        border: 1px solid #1e293b;
    }

    /* FORZA IL PULSANTE AD OCCUPARE TUTTA LA CELLA */
    div.stButton > button {
        width: 100% !important;
        height: 85px !important;
        background-color: #1e293b !important;
        color: #ffffff !important;
        border: 2px solid #334155 !important;
        border-radius: 8px !important;
        padding: 4px !important;
        margin: 0px !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: space-between !important;
        align-items: center !important;
        transition: all 0.2s ease-in-out;
    }

    div.stButton > button:hover {
        border-color: #00b0f0 !important;
        background-color: #334155 !important;
    }

    /* Stile Numero Giorno (Grande al Centro/Alto) */
    .day-num-style {
        font-size: 26px;
        font-weight: 900;
        line-height: 1;
        margin-top: 4px;
    }

    /* Contenitore Badge sotto il numero */
    .badges-row {
        display: flex;
        gap: 3px;
        justify-content: center;
        align-items: center;
        margin-bottom: 4px;
        min-height: 20px;
    }

    /* Badge Singolo */
    .badge-pill {
        font-size: 11px;
        font-weight: 800;
        padding: 2px 6px;
        border-radius: 3px;
        line-height: 1;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Layout
col_sidebar, col_main = st.columns([1, 4])

# --- SIDEBAR COMPATTA ---
with col_sidebar:
    st.subheader("👤 Operatore")

    selected_user = st.radio(
        "Seleziona operatore:",
        options=list(USERS.keys()),
        format_func=lambda user: f"{user} ({USERS[user]['initial']})",
    )

    u_info = USERS[selected_user]
    st.markdown(
        f"""
        <div style="background-color: {u_info['color']}; color: {u_info['text_color']}; 
                    padding: 10px; text-align: center; font-size: 15px; font-weight: 800; 
                    border-radius: 6px; margin-top: 8px;">
            IN USO: {selected_user}
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🗑️ Reset Tutto", key="reset_btn"):
        st.session_state.ferie_data = {}
        save_data({})
        st.rerun()

# --- MAIN: CALENDARIO UNIFORME ---
with col_main:
    col_nav1, col_nav2, col_nav3 = st.columns([1, 3, 1])

    with col_nav1:
        if st.button("◄ Prec.", key="btn_prev"):
            if st.session_state.current_month == 1:
                st.session_state.current_month = 12
                st.session_state.current_year -= 1
            else:
                st.session_state.current_month -= 1
            st.rerun()

    with col_nav3:
        if st.button("Succ. ►", key="btn_next"):
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
            unsafe_allow_html=True,
        )

    # Intestazione Giorni
    headers = ["LUN", "MAR", "MER", "GIO", "VEN", "SAB", "DOM"]
    cols_head = st.columns(7)
    for idx, h in enumerate(headers):
        cols_head[idx].markdown(
            f"<div class='day-header'>{h}</div>", unsafe_allow_html=True
        )

    # Matrice Mese
    cal = calendar.Calendar(firstweekday=0)
    month_days = cal.monthdayscalendar(
        st.session_state.current_year, st.session_state.current_month
    )

    for week in month_days:
        cols = st.columns(7)
        for day_idx, day in enumerate(week):
            with cols[day_idx]:
                if day == 0:
                    # Spazio vuoto per allineamento
                    st.markdown(
                        "<div style='height: 85px;'></div>",
                        unsafe_allow_html=True,
                    )
                else:
                    date_key = f"{st.session_state.current_year}-{st.session_state.current_month:02d}-{day:02d}"
                    active_users = st.session_state.ferie_data.get(
                        date_key, []
                    )

                    # Costruzione HTML dei Badge interni al bottone
                    badges_list = []
                    for user in active_users:
                        if user in USERS:
                            info = USERS[user]
                            badges_list.append(
                                f'<span class="badge-pill" style="background-color: {info["color"]}; '
                                f'color: {info["text_color"]};">{info["initial"]}</span>'
                            )

                    badges_html = (
                        "".join(badges_list) if badges_list else "&nbsp;"
                    )

                    # ETICHETTA DEL BOTTONE COMPLETA (Numero Grande + Badge)
                    btn_label = f"""
                    <div class="day-num-style">{day}</div>
                    <div class="badges-row">{badges_html}</div>
                    """

                    # Pulsante Unico e Compatto
                    if st.button(
                        f"{day}", key=f"btn_{date_key}", help=f"Data: {date_key}"
                    ):
                        if date_key not in st.session_state.ferie_data:
                            st.session_state.ferie_data[date_key] = []

                        if (
                            selected_user
                            in st.session_state.ferie_data[date_key]
                        ):
                            st.session_state.ferie_data[date_key].remove(
                                selected_user
                            )
                        else:
                            st.session_state.ferie_data[date_key].append(
                                selected_user
                            )

                        save_data(st.session_state.ferie_data)
                        st.rerun()
