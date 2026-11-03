import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.title("🪚 Mizarski Kalkulator: 3D Prikaz z Hrbtom in ABS")
st.write("Izberi prostor, vnesi omaro, določi ABS robove ter preveri 3D barvni model in krojni list.")

# --- 1. KORAK: IZBIRA PROJEKTA (PROSTORA) ---
st.sidebar.header("📁 Vrsta projekta")
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

# --- 3. KORAK: NASTAVITve HRBTA IN ROBOV (ABS) ---
st.sidebar.subheader("⚙️ Konstrukcija hrbta in ABS robovi")
nacin_hrbta = st.sidebar.selectbox(
    "Vgradnja hrbta", 
    ["Prislonjen zadaj (brez utora)", "V utoru / falcu (stranice in strop/pod)"]
)

globina_utora = 6
if "utor" in nacin_hrbta:
    globina_utora = st.sidebar.slider("Globina utora / falca (mm)", min_value=4, max_value=10, value=6)

odmik_hrbta = st.sidebar.slider("Odmik stropa/poda zadaj (mm)", min_value=0, max_value=15, value=5, key="oh_in")
zracnost_polic_sirina = st.sidebar.slider("Zračnost police širina - skupaj (mm)", min_value=0, max_value=10, value=2, key="zp_in")
odmik_police_globina = st.sidebar.slider("Koliko je polica krajša od globine omare (mm)", min_value=10, max_value=50, value=25, key="op_in")

st.sidebar.markdown("---")
st.sidebar.markdown("**Izbira ABS robov za elemente:**")
abs_stranica = st.sidebar.checkbox("Stranici: ABS sprednji dolgi rob", value=True)
abs_strop_pod = st.sidebar.checkbox("Strop / Pod: ABS prednji kratek rob", value=True)
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
        "Globina_Utora": globina_utora,
        "Odmik_Hrbta": odmik_hrbta,
        "Zracnost_Polic": zracnost_polic_sirina,
        "Odmik_Police_G": odmik_police_globina,
        "ABS_Stranica": abs_stranica,
        "ABS_StropPod": abs_strop_pod,
        "ABS_Polica": abs_polica,
        "ABS_Vrata": abs_vrata
