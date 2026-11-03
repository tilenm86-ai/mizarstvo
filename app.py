import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.title("🪚 Mizarski Kalkulator: 3D Masivni Prikaz in Krojni List")
st.write("Izberi prostor, vnesi omaro, določi nastavitve utora (odmik za obešala in globino), ABS robove ter preveri 3D model.")

# --- 1. KORAK: IZBIRA PROJEKTA (PROSTORA) ---
vrsta_projekta = st.sidebar.selectbox(
    "Izberi prostor", 
    ["Kuhinja", "Dnevna soba", "Spalnica / Garderoba", "Kopalnica"]
)

if vrsta_projekta == "Kuhinja":
    mozne_omare = ["Spodnja omarica s policami in vrati", "Spodnja omarica z vrati", "Viseča omarica", "Visoka omara za aparat"]
elif vrsta_projekta == "Dnevna soba":
    mozne_omare = ["TV komoda", "Nizek regal s policami", "Viseča vitrina", "Visoka knjižna omara"]
elif vrsta_projekta == "Spalnica / Garderoba":
    mozne_omare = ["Garderobna omara z drogom za obešanje", "Omara s policami", "Visoka garderobna omara", "Predalnik (komoda)"]
else:
    mozne_omare = ["Kopalniška omarica pod umivalnikom", "Visoka kopalniška omara z ogledalom"]

# --- 2. KORAK: VNOS ELEMENTA ---
st.sidebar.divider()
st.sidebar.header("➕ Dodaj element v projekt")
ime_elementa = st.sidebar.text_input("Naziv elementa", value="Omarica 1")

tip_elementa = st.sidebar.selectbox("Vrsta omare za ta prostor", mozne_omare)

debelina = st.sidebar.number_input("Debelina materiala (mm)", value=18, step=1)

ima_police = "polic" in tip_elementa or "knjižna" in tip_elementa
ima_vrata = "vrati" in tip_elementa or "vitrina" in tip_elementa or "omara" in tip_elementa

stevilo_polic = 0
if ima_police:
    stevilo_polic = st.sidebar.slider("Število polic", min_value=1, max_value=10, value=2)

col1, col2, col3 = st.sidebar.columns(3)
with col1:
    sirina = st.number_input("Širina (mm)", value=800, step=10)
with col2:
    visina = st.number_input("Višina (mm)", value=720, step=10)
with col3:
    globina = st.number_input("Globina (mm)", value=550, step=10)

# --- 3. KORAK: NASTAVITVE HRBTA, UTORA IN ROBOV (ABS) ---
st.sidebar.subheader("⚙️ Konstrukcija hrbta, utora in ABS")
nacin_hrbta = st.sidebar.selectbox(
    "Vgradnja hrbta", 
    [
        "V utoru: Samo stranice (strop in pod brez utora)",
        "V utoru: Vsi elementi (stranice, strop, pod)"
    ]
)

# Samodejni predlog odmika utora glede na tip omare (pri visečih več, pri navadnih manj)
privzeti_odmik = 20 if "Viseča" in tip_elementa or "vitrina" in tip_elementa else 10

odmik_utora_zadaj = st.sidebar.slider("Odmik utora od zadnjega roba (mm)", min_value=5, max_value=35, value=privzeti_odmik, help="Za viseče omare z obešali nastavi npr. 20-25 mm")
debelina_utora = st.sidebar.slider("Debelina utora (širina reza v mm)", min_value=4, max_value=8, value=6)
globina_utora = st.sidebar.slider("Globina utora (v globino materiala v mm)", min_value=4, max_value=15, value=6)

# Prikaz opozorila o preostanku materiala zadaj za privijačenje
preostanek_mesa = debelina - globina_utora
if preostanek_mesa < 4:
    st.sidebar.warning(f"⚠️ Pozor! Zadaj za privijačenje ostane samo {preostanek_mesa} mm materiala.")
else:
    st.sidebar.info(f"ℹ️ Zadaj za privijačenje ostane {preostanek_mesa} mm materiala.")

# Odmik stropa/poda je možen SAMO takrat, ko so utori samo v stranicah (vse do 30 mm)
if "Samo stranice" in nacin_hrbta:
    odmik_hrbta = st.sidebar.slider("Odmik stropa/poda zadaj (mm)", min_value=0, max_value=30, value=5, key="oh_in")
else:
    odmik_hrbta = 0  # Ko so vsi v falcu, ni odmika

zracnost_polic_sirina = st.sidebar.slider("Zračnost police širina - skupaj (mm)", min_value=0, max_value=10, value=2, key="zp_in")
odmik_police_globina = st.sidebar.slider("Koliko je polica krajša od globine omare (mm)", min_value=10, max_value=50, value=25, key="op_in")

st.sidebar.markdown("---")
st.sidebar.markdown("**Izbira ABS robov za stranici:**")
abs_str_spredaj = st.sidebar.checkbox("Stranica: Sprednji rob", value=True)
abs_str_zgornji = st.sidebar.checkbox("Stranica: Zgornji rob", value=False)
abs_str_spodnji = st.sidebar.checkbox("Stranica: Spodnji rob", value=False)

st.sidebar.markdown("**Izbira ABS robov za ostale dele:**")
abs_strop_pod = st.sidebar.checkbox("Strop / Pod: ABS prednji rob", value=True)
abs_polica = st.sidebar.checkbox("Police: ABS prednji rob", value=True)
abs_vrata = st.sidebar.checkbox("Vrata: ABS na vseh 4 straneh", value=True)

if st.sidebar.button("💾 Shrani omaro v projekt"):
    if "elements" not in st.session_state:
        st.session_state.elements = []
        
    st.session_state.elements.append({
        "Projekt": vrsta_projekta,
        "Naziv": ime_elementa,
        "Tip": tip_elementa,
        "Širina": sirina,
        "Višina": visina,
        "Globina": globina,
        "Police": stevilo_polic,
        "Vrata": ima_vrata,
        "Debelina": debelina,
        "Nacin_Hrbta": nacin_hrbta,
        "Odmik_Utora_Zadaj": odmik_utora_zadaj,
        "Debelina_Utora": debelina_utora,
        "Globina_Utora": globina_utora,
        "Odmik_Hrbta": odmik_hrbta,
        "Zracnost_Polic": zracnost_polic_sirina,
        "Odmik_Police_G": odmik_police_globina,
        "ABS_Str_Spredaj": abs_str_spredaj,
        "ABS_Str_Zgornji": abs_str_zgornji,
        "ABS_Str_Spodnji": abs_str_spodnji,
        "ABS_StropPod": abs_strop_pod,
        "ABS_Polica": abs_polica,
        "ABS_Vrata": abs_vrata
    })
    st.sidebar.success(f"Dodano: {ime_elementa}")

# --- GLAVNI ZASLON ---
if "elements" not in st.session_state:
    st.session_state.elements = []

st.subheader(f"📋 Seznam elementov za projekt: {vrsta_projekta}")

if len(st.session_state.elements) > 0:
    for i, el in enumerate(st.session_state.elements):
        c1, c2 = st.columns([5, 1])
        with c1:
            naziv_p = el.get('Naziv', 'Element')
            projekt_p = el.get('Projekt',
