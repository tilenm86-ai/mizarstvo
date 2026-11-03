import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(layout="wide")

# --- CSS STIL ZA ŠIRŠI STRANSKI MENI IN LAŽJE SKROLANJE ---
st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            min-width: 380px;
            max-width: 450px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🪚 Mizarski Kalkulator: 3D, Krojni List in Tehnične 2D Risbe s Kotami")
st.write("Izberi prostor, vnesi omaro, določi nastavitve utora in ABS robove ter preveri prave tehnične izrise.")

# --- AVTOMATSKA PRIVZETA OMARICA OB ZAČETKU ---
if "elements" not in st.session_state:
    st.session_state.elements = [{
        "Projekt": "Kuhinja",
        "Naziv": "Omarica 1",
        "Tip": "Spodnja omarica s policami in vrati",
        "Širina": 800,
        "Višina": 720,
        "Globina": 550,
        "Police": 2,
        "Vrata": True,
        "Debelina": 18,
        "Nacin_Hrbta": "V utoru: Vsi elementi (stranice, strop, pod)",
        "Odmik_Utora_Zadaj": 10,
        "Debelina_Utora": 6,
        "Globina_Utora": 13,
        "Zracnost_Visina_Hrbta": 2,
        "Odmik_Hrbta": 0,
        "Zracnost_Polic": 2,
        "Odmik_Police_G": 25,
        "Izbrani_Robovi_Stranice": ["Sprednji"],
        "Izbrani_Robovi_StropPod": ["Sprednji"],
        "ABS_Polica": "Da (1x rob)",
        "ABS_Vrata": "Vse 4 strani"
    }]

# --- 1. KORAK: IZBIRA PROJEKTA (PROSTORA) ---
vrsta_projekta = st.sidebar.selectbox(
    "Izberi prostor", 
    ["Kuhinja", "Dnevna soba", "Spalnica / Garderoba", "Kopalnica"],
    key="vrsta_projekta"
)

if vrsta_projekta == "Kuhinja":
    mozne_omare = ["Spodnja omarica s policami in vrati", "Spodnja omarica z vrati", "Viseča omarica", "Visoka omara za aparat"]
elif vrsta_projekta == "Dnevna soba":
    mozne_omare = ["TV komoda", "Nizek regal s policami", "Viseča vitrina", "Visoka knjižna omara"]
elif vrsta_projekta == "Spalnica / Garderoba":
    mozne_omare = ["Garderobna omara z drogom za obešanje", "Omara s policami", "Visoka garderobna omara", "Predalnik (komoda)"]
else:
    mozne_omare = ["Kopalniška omarica pod umivalnikom", "Visoka kopalniška omara z ogledalom"]

# --- 2. KORAK: VNOS ELEMENTA V STRANSKEM MENIJU ---
st.sidebar.divider()
st.sidebar.header("➕ Dodaj element v projekt")
ime_elementa = st.sidebar.text_input("Naziv elementa", value="Omarica 1", key="input_ime")
tip_elementa = st.sidebar.selectbox("Vrsta omare za ta prostor", mozne_omare, key="input_tip")
debelina = st.sidebar.number_input("Debelina materiala (mm)", value=18, step=1, key="input_debelina")

ima_police = "polic" in tip_elementa or "knjižna" in tip_elementa
ima_vrata = "vrati" in tip_elementa or "vitrina" in tip_elementa or "omara" in tip_elementa

stevilo_polic = 0
if ima_police:
    stevilo_polic = st.sidebar.slider("Število polic", min_value=1, max_value=10, value=2, key="input_police")

col1, col2, col3 = st.sidebar.columns(3)
with col1:
    sirina = st.sidebar.number_input("Širina (
