import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(layout="wide")

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

VSI_ELEMENTI = "V utoru: Vsi elementi (stranice, strop, pod)"
SAMO_STRANICE = "V utoru: Samo stranice (strop in pod brez utora)"
ZRACNOST_SIRINA_HRBTA = 2


# ---------------------------------------------------------------------------
# Ena sama funkcija za vse mere kosov (3D, 2D risbe in krojni list)
# ---------------------------------------------------------------------------
def izracunaj_mere(el):
    d = el.get("Debelina", 18)
    s = el.get("Širina", 800)
    v = el.get("Višina", 720)
    g = el.get("Globina", 550)
    nacin = el.get("Nacin_Hrbta", VSI_ELEMENTI)
    vsi = "Vsi elementi" in nacin
    gutora = el.get("Globina_Utora", 13)
    deb_utora = el.get("Debelina_Utora", 5)
    ouz = el.get("Odmik_Utora_Zadaj", 5)
    oh = el.get("Odmik_Hrbta", 0)
    zp = el.get("Zracnost_Polic", 2)
    opg = el.get("Odmik_Police_G", 25)
    zr_v = el.get("Zracnost_Visina_Hrbta", 2)
    n_polic = el.get("Police", 0)

    sirina_kosa = s - 2 * d
    globina_sp = g if vsi else g - oh

    # Utor: zadnja ploskev utora je ouz od zadnjega roba, sprednja je debelina utora naprej
    utor_y0 = g - ouz - deb_utora
    utor_y1 = g - ouz
    if vsi:
        utor_z0 = d - gutora
        utor_z1 = v - d + gutora
    else:
        utor_z0 = 0
        utor_z1 = v

    sirina_hrbta = sirina_kosa + 2 * gutora - ZRACNOST_SIRINA_HRBTA
    if vsi:
        visina_hrbta = (v - 2 * d) + 2 * gutora - zr_v
    else:
        visina_hrbta = v - zr_v

    # Police: krajše od globine omare za opg, sprednji rob poravnan z začetkom (y = 0)
    sirina_police = sirina_kosa - zp
    globina_police = g - opg

    polozaji_polic = []
    if n_polic > 0:
        notranja = v - 2 * d
        reža = (notranja - n_polic * d) / (n_polic + 1)
        for i in range(n_polic):
            polozaji_polic.append(d + reža * (i + 1) + d * i)

    return {
        "d": d, "s": s, "v": v, "g": g, "vsi": vsi,
        "gutora": gutora, "deb_utora": deb_utora, "ouz": ouz, "oh": oh,
        "zp": zp, "opg": opg,
        "sirina_kosa": sirina_kosa, "globina_sp": globina_sp,
        "utor_y0": utor_y0, "utor_y1": utor_y1, "utor_z0": utor_z0, "utor_z1": utor_z1,
        "sirina_hrbta": sirina_hrbta, "visina_hrbta": visina_hrbta,
        "sirina_police": sirina_police, "globina_police": globina_police,
        "polozaji_polic": polozaji_polic,
    }


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
        "Nacin_Hrbta": VSI_ELEMENTI,
        "Odmik_Utora_Zadaj": 5,
        "Debelina_Utora": 5,
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
sirina = col1.number_input("Širina (mm)", value=800, step=10, key="input_sirina")
visina = col2.number_input("Višina (mm)", value=720, step=10, key="input_visina
