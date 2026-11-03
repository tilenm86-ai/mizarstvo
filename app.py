import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.title("🪚 Mizarski Kalkulator: 3D, Krojni List in Tehnične 2D Risbe s Kotami")

if "elements" not in st.session_state:
    st.session_state.elements = [{
        "Projekt": "Kuhinja", "Naziv": "Omarica 1", "Tip": "Spodnja omarica s policami in vrati",
        "Širina": 800, "Višina": 720, "Globina": 550, "Police": 2, "Vrata": True, "Debelina": 18,
        "Nacin_Hrbta": "V utoru: Vsi elementi (stranice, strop, pod)", "Odmik_Utora_Zadaj": 5,
        "Debelina_Utora": 5, "Globina_Utora": 13, "Zracnost_Visina_Hrbta": 2, "Odmik_Hrbta": 0,
        "Zracnost_Polic": 2, "Odmik_Police_G": 25, "Izbrani_Robovi_Stranice": ["Sprednji"],
        "Izbrani_Robovi_StropPod": ["Sprednji"], "ABS_Polica": "Da (1x rob)", "ABS_Vrata": "Vse 4 strani"
    }]

vrsta_projekta = st.sidebar.selectbox("Izberi prostor", ["Kuhinja", "Dnevna soba", "Spalnica / Garderoba", "Kopalnica"], key="vrsta_projekta")

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
with col1:
    sirina = st.sidebar.number_input("Širina (mm)", value=800, step=10, key="input_sirina")
with col2:
    visina = st.sidebar.number_input("Višina (mm)", value=720, step=10, key="input_visina")
with col3:
    globina = st.sidebar.number_input("Globina (mm)", value=550, step=10, key="input_globina")

st.sidebar.subheader("⚙️ Konstrukcija hrbta, utora in ABS")
nacin_hrbta = st.sidebar.selectbox("Vgradnja hrbta", ["V utoru: Samo stranice (strop in pod brez utora)", "V utoru: Vsi elementi (stranice, strop, pod)"], key="input_nacin_hrbta")

odmik_utora_zadaj = st.sidebar.slider("Odmik utora od zadnjega roba (mm)", min_value=5, max_value=35, value=5, key="input_odmik_utora")
debelina_utora = st.sidebar.slider("Debelina utora (širina reza v mm)", min_value=4, max_value=8, value=5, key="input_deb_utora")
globina_utora = st.sidebar.slider("Globina utora (v globino materiala v mm)", min_value=4, max_value=15, value=13, key="input_globina_utora")
zracnost_visina_hrbta = st.sidebar.slider("Zračnost za višino hrbta (mm)", min_value=0, max_value=10, value=2, key="input_zracnost_v_hrbta")

odmik_hrbta = st.sidebar.slider("Odmik stropa/poda zadaj (mm)", min_value=0, max_value=30, value=5, key="input_odmik_hrbta") if "Samo stranice" in nacin_hrbta else 0
zracnost_polic_sirina = st.sidebar.slider("Zračnost police širina - skupaj (mm)", min_value=0, max_value=10, value=2, key="input_zracnost")
odmik_police_globina = st.sidebar.slider("Koliko je polica krajša od globine omare (mm)", min_value=10, max_value=50, value=25, key="input_odmik_pol")

izbrani_robovi_stranice = st.sidebar.multiselect("Stranica - ABS robovi", ["Sprednji", "Zgornji", "Spodnji", "Zadnji"], default=["Sprednji"], key="ms_stranica")
izbrani_robovi_strop_pod = st.sidebar.multiselect("Strop / Pod - ABS robovi", ["Sprednji", "Zadnji"], default=["Sprednji"], key="ms_strop_pod")
abs_polica_izbira = st.sidebar.selectbox("Police - Prednji ABS", ["Da (1x rob)", "Brez"], index=0, key="sb_polica")
abs_vrata_izbira = st.sidebar.selectbox("Vrata - ABS robovi", ["Vse 4 strani", "Brez"], index=0, key="sb_vrata")

if st.sidebar.button("💾 Shrani omaro v projekt", key="gumb_shrani"):
    st.session_state.elements = [{
        "Projekt": vrsta_projekta, "Naziv": ime_elementa, "Tip": tip_elementa, "Širina": sirina, "Višina": visina, "Globina": globina,
        "Police": stevilo_polic, "Vrata": ima_vrata, "Debelina": debelina, "Nacin_Hrbta": nacin_hrbta, "Odmik_Utora_Zadaj": odmik_utora_zadaj,
        "Debelina_Utora": debelina_utora, "Globina_Utora": globina_utora, "Zracnost_Visina_Hrbta": zracnost_visina_hrbta, "Odmik_Hrbta": odmik_hrbta,
        "Zracnost_Polic": zracnost_polic_sirina, "Odmik_Police_G": odmik_police_globina, "Izbrani_Robovi_Stranice": izbrani_robovi_stranice,
        "Izbrani_Robovi_StropPod": izbrani_robovi_strop_pod, "ABS_Polica": abs_polica_izbira, "ABS_Vrata": abs_vrata_izbira
    }]
    st.sidebar.success("Posodobljeno!")

st.subheader("📋 Seznam elementov")
if len(st.session_state.elements) > 0:
    el = st.session_state.elements[0]
    st.write(f"**{el['Naziv']}** ({el['Projekt']} ➔ *{el['Tip']}*) — Š: {el['Širina']} mm, V: {el['Višina']} mm, G: {el['Globina']} mm | Police: {el['Police']}")
    
    if st.button("🧮 Izračunaj krojni list", type="primary"):
        vsi_kosi = []
        d, s, v, g = el["Debelina"], el["Širina"], el["Višina"], el["Globina"]
        
        vsi_kosi.append({"Del": "Stranica", "Količina": 2, "Širina (mm)": g, "Dolžina/Višina (mm)": v, "ABS": ", ".join(el["Izbrani_Robovi_Stranice"])})
        
        glob_sp = (g + el["Globina_Utora"]) if "Vsi elementi" in el["Nacin_Hrbta"] else (g - el["Odmik_Hrbta"])
        vsi_kosi.append({"Del": "Strop / Pod", "Količina": 2, "Širina (mm)": glob_sp, "Dolžina/Višina (mm)": s - (2 * d), "ABS": ", ".join(el["Izbrani_Robovi_StropPod"])})
        
        h_vis = (v - el["Zracnost_Visina_Hrbta"]) if "Samo stranice" in el["Nacin_Hrbta"] else ((v - (2 * d)) + (2 * el["Globina_Utora"]) - el["Zracnost_Visina_Hrbta"])
        vsi_kosi.append({"Del": "Hrbet (5mm)", "Količina": 1, "Širina (mm)": (s - (2 * d)) + (2 * el["Globina_Utora"]) - 2, "Dolžina/Višina (mm)": h_vis, "ABS": "Brez"})
        
        if el["Police"] > 0:
            vsi_kosi.append({"Del": "Police", "Količina": el["Police"], "Širina (mm)": g - el["Globina_Utora"] - el["Odmik_Police_G"] - el["Odmik_Hrbta"], "Dolžina/Višina (mm)": (s - (2 * d)) - el["Zracnost_Polic"], "ABS": "Da" if el["ABS_Polica"] == "Da (1x rob)" else "Brez"})
        
        if el["Vrata"]:
            vsi_kosi.append({"Del": "Vrata", "Količina": (2 if s > 600 else 1), "Širina (mm)": ((s / 2) - 3 if s > 600 else s - 4), "Dolžina/Višina (mm)": v - 4, "ABS": "Vse 4 strani"})

        st.dataframe(pd.DataFrame(vsi_kosi), use_container_width=True)
