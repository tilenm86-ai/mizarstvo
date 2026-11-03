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
    sirina = st.sidebar.number_input("Širina (mm)", value=800, step=10, key="input_sirina")
with col2:
    visina = st.sidebar.number_input("Višina (mm)", value=720, step=10, key="input_visina")
with col3:
    globina = st.sidebar.number_input("Globina (mm)", value=550, step=10, key="input_globina")

# --- 3. KORAK: NASTAVITVE HRBTA, UTORA IN ROBOV (ABS) V STRANSKEM MENIJU ---
st.sidebar.subheader("⚙️ Konstrukcija hrbta, utora in ABS")
nacin_hrbta = st.sidebar.selectbox(
    "Vgradnja hrbta", 
    [
        "V utoru: Samo stranice (strop in pod brez utora)",
        "V utoru: Vsi elementi (stranice, strop, pod)"
    ],
    key="input_nacin_hrbta"
)

privzeti_odmik = 20 if "Viseča" in tip_elementa or "vitrina" in tip_elementa else 10

odmik_utora_zadaj = st.sidebar.slider("Odmik utora od zadnjega roba (mm)", min_value=5, max_value=35, value=privzeti_odmik, key="input_odmik_utora")
debelina_utora = st.sidebar.slider("Debelina utora (širina reza v mm)", min_value=4, max_value=8, value=6, key="input_deb_utora")
globina_utora = st.sidebar.slider("Globina utora (v globino materiala v mm)", min_value=4, max_value=15, value=13, key="input_globina_utora")

zracnost_visina_hrbta = st.sidebar.slider("Zračnost za višino hrbta (mm)", min_value=0, max_value=10, value=2, key="input_zracnost_v_hrbta")

preostanek_mesa = debelina - globina_utora
if preostanek_mesa < 4:
    st.sidebar.warning(f"⚠️ Pozor! Zadaj za privijačenje ostane samo {preostanek_mesa} mm materiala.")
else:
    st.sidebar.info(f"ℹ️ Zadaj za privijačenje ostane {preostanek_mesa} mm materiala.")

if "Samo stranice" in nacin_hrbta:
    odmik_hrbta = st.sidebar.slider("Odmik stropa/poda zadaj (mm)", min_value=0, max_value=30, value=5, key="input_odmik_hrbta")
else:
    odmik_hrbta = 0

zracnost_polic_sirina = st.sidebar.slider("Zračnost police širina - skupaj (mm)", min_value=0, max_value=10, value=2, key="input_zracnost")
odmik_police_globina = st.sidebar.slider("Koliko je polica krajša od globine omare (mm)", min_value=10, max_value=50, value=25, key="input_odmik_pol")

st.sidebar.markdown("---")
st.sidebar.markdown("**Izbira ABS robov (tapni za izbor):**")

izbrani_robovi_stranice = st.sidebar.multiselect(
    "Stranica - ABS robovi", 
    ["Sprednji", "Zgornji", "Spodnji", "Zadnji"], 
    default=["Sprednji"],
    key="ms_stranica"
)

izbrani_robovi_strop_pod = st.sidebar.multiselect(
    "Strop / Pod - ABS robovi", 
    ["Sprednji", "Zadnji"], 
    default=["Sprednji"],
    key="ms_strop_pod"
)

abs_polica_izbira = st.sidebar.selectbox("Police - Prednji ABS", ["Da (1x rob)", "Brez"], index=0, key="sb_polica")
abs_vrata_izbira = st.sidebar.selectbox("Vrata - ABS robovi", ["Vse 4 strani", "Brez"], index=0, key="sb_vrata")

if st.sidebar.button("💾 Shrani omaro v projekt", key="gumb_shrani"):
    st.session_state.elements = [{
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
        "Zracnost_Visina_Hrbta": zracnost_visina_hrbta,
        "Odmik_Hrbta": odmik_hrbta,
        "Zracnost_Polic": zracnost_polic_sirina,
        "Odmik_Police_G": odmik_police_globina,
        "Izbrani_Robovi_Stranice": izbrani_robovi_stranice,
        "Izbrani_Robovi_StropPod": izbrani_robovi_strop_pod,
        "ABS_Polica": abs_polica_izbira,
        "ABS_Vrata": abs_vrata_izbira
    }]
    st.sidebar.success(f"Posodobljeno: {ime_elementa}")

# --- GLAVNI ZASLON ---
st.subheader(f"📋 Seznam elementov za projekt: {vrsta_projekta}")

if len(st.session_state.elements) > 0:
    for i, el in enumerate(st.session_state.elements):
        c1, c2 = st.columns([5, 1])
        with c1:
            naziv_p = el.get('Naziv', 'Element')
            projekt_p = el.get('Projekt', 'Kuhinja')
            tip_p = el.get('Tip', 'Omarica')
            s_p = el.get('Širina', 0)
            v_p = el.get('Višina', 0)
            g_p = el.get('Globina', 0)
            pol_p = el.get('Police', 0)
            
            st.write(f"**{i+1}. {naziv_p}** ({projekt_p} ➔ *{tip_p}*) — Š: {s_p} mm, V: {v_p} mm, G: {g_p} mm | Police: {pol_p}")
        with c2:
            if st.button("❌", key=f"del_{i}"):
                st.session_state.elements = []
                st.rerun()

    if st.button("🗑️ Počisti cel projekt", key="gumb_pocisti"):
        st.session_state.elements = []
        st.rerun()

    st.divider()

    # --- POMOŽNA FUNKCIJA ZA 3D KVADER ---
    def dodaj_kvader(fig, x_min, x_max, y_min, y_max, z_min, z_max, color, name):
        fig.add_trace(go.Mesh3d(
            x=[x_min, x_max, x_max, x_min, x_min, x_max, x_max, x_min],
            y=[y_min, y_min, y_max, y_max, y_min, y_min, y_max, y_max],
            z=[z_min, z_min, z_min, z_min, z_max, z_max, z_max, z_max],
            i=[0, 0, 4, 4, 0, 0, 2, 2, 0, 0, 1, 1],
            j=[1, 2, 5, 6, 1, 5, 3, 7, 3, 7, 2, 6],
            k=[2, 3, 6, 7, 5, 4, 7, 6, 7, 4, 6, 5],
            color=color,
            opacity=0.9,
            name=name,
            showscale=False
        ))

    # --- POMOŽNE FUNKCIJE ZA RDEČE TEHNIČNE KOTE ---
    def narisi_koto_horizontalno(fig, x_start, x_end, y_pos, tekst):
        sredina = (x_start + x_end) / 2
        # Prekinjena črta z rdečo barvo
        fig.add_trace(go.Scatter(x=[x_start, sredina - 30], y=[y_pos, y_pos], mode="lines", line=dict(color="red", width=1.5), showlegend=False))
        fig.add_trace(go.Scatter(x=[sredina + 30, x_end], y=[y_pos, y_pos], mode="lines", line=dict(color="red", width=1.5), showlegend=False))
        # Besedilo v rdeči barvi
        fig.add_trace(go.Scatter(
            x=[sredina], y=[y_pos],
            mode="text",
            text=[f"<span style='color:red;'><b>{tekst}</b></span>"],
            textposition="middle center",
            showlegend=False
        ))
        # Pomožni podaljški
        fig.add_trace(go.Scatter(x=[x_start, x_start], y=[y_pos - 5, y_pos + 5], mode="lines", line=dict(color="red", width=1), showlegend=False))
        fig.add_trace(go.Scatter(x=[x_end, x_end], y=[y_pos - 5, y_pos + 5], mode="lines", line=dict(color="red", width=1), showlegend=False))

    def narisi_koto_vertikalno(fig, y_start, y_end, x_pos, tekst):
        sredina = (y_start + y_end) / 2
        fig.add_trace(go.Scatter(x=[x_pos, x_pos], y=[y_start, sredina - 25], mode="lines", line=dict(color="red", width=1.5), showlegend=False))
        fig.add_trace(go.Scatter(x=[x_pos, x_pos], y=[sredina + 25, y_end], mode="lines", line=dict(color="red", width=1.5), showlegend=False))
        fig.add_trace(go.Scatter(
            x=[x_pos], y=[sredina],
            mode="text",
            text=[f"<span style='color:red;'><b>{tekst}</b></span>"],
            textposition="middle center",
            showlegend=False
        ))
        fig.add_trace(go.Scatter(x=[x_pos - 5, x_pos + 5], y=[y_start, y_start], mode="lines", line=dict(color="red", width=1), showlegend=False))
        fig.add_trace(go.Scatter(x=[x_pos - 5, x_pos + 5], y=[y_end, y_end], mode="lines", line=dict(color="red", width=1), showlegend=False))

    # --- 3D PREDOGLED V PREDALČKU ---
    with st.expander("🧊 Pokaži 3D predogled omare (Z možnostjo približevanja in vrtenja)"):
        izbran_indeks = st.selectbox("Izberi element za 3D prikaz", range(len(st.session_state.elements)), format_func=lambda x: st.session_state.elements[x]["Naziv"], key="select_3d_index")
        
        el_3d = st.session_state.elements[izbran_indeks]
        d_3d = el_3d["Debelina"]
        w_3d = el_3d["Širina"]
        h_3d = el_3d["Višina"]
        depth_3d = el_3d["Globina"]
        st_polic_3d = el_3d["Police"]
        opg_3d = el_3d["Odmik_Police_G"]
        zp_3d = el_3d["Zracnost_Polic"]
        nacin_h_3d = el_3d["Nacin_Hrbta"]
        ouz_3d = el_3d.get("Odmik_Utora_Zadaj", 10)
        gutora_3d = el_3d["Globina_Utora"]
        oh_3d = el_3d["Odmik_Hrbta"]

        fig = go.Figure()

        dodaj_kvader(fig, 0, d_3d, 0, depth_3d, 0, h_3d, '#A0522D', 'Leva stranica')
        dodaj_kvader(fig, w_3d - d_3d, w_3d, 0
