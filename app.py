import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.title("🪚 Mizarski Kalkulator: 3D Masivni Prikaz in Krojni List")
st.write("Izberi prostor, vnesi omaro, določi ABS robove ter preveri 3D model s prikazom debelin elementov.")

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
            projekt_p = el.get('Projekt', 'Kuhinja')
            tip_p = el.get('Tip', 'Omarica')
            s_p = el.get('Širina', 0)
            v_p = el.get('Višina', 0)
            g_p = el.get('Globina', 0)
            pol_p = el.get('Police', 0)
            
            st.write(f"**{i+1}. {naziv_p}** ({projekt_p} ➔ *{tip_p}*) — Š: {s_p} mm, V: {v_p} mm, G: {g_p} mm | Police: {pol_p}")
        with c2:
            if st.button("❌", key=f"del_{i}"):
                st.session_state.elements.pop(i)
                st.rerun()

    if st.button("🗑️ Počisti cel projekt"):
        st.session_state.elements = []
        st.rerun()

    st.divider()

    # --- POMOŽNA FUNKCIJA ZA 3D MASIVNI KVADER (Z DEBELINO) ---
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

    # --- 3D MASIVNI PRIKAZ ---
    st.subheader("🧊 3D predogled elementa (Z vsemi debelinami materialov)")
    izbran_indeks = st.selectbox("Izberi element za 3D prikaz", range(len(st.session_state.elements)), format_func=lambda x: st.session_state.elements[x]["Naziv"])
    
    el_3d = st.session_state.elements[izbran_indeks]
    d_3d = el_3d["Debelina"]
    w_3d = el_3d["Širina"]
    h_3d = el_3d["Višina"]
    depth_3d = el_3d["Globina"]
    st_polic_3d = el_3d["Police"]
    opg_3d = el_3d["Odmik_Police_G"]
    zp_3d = el_3d["Zracnost_Polic"]
    nacin_h_3d = el_3d["Nacin_Hrbta"]

    fig = go.Figure()

    # 1. Leva stranica (masiven blok)
    dodaj_kvader(fig, 0, d_3d, 0, depth_3d, 0, h_3d, '#A0522D', 'Leva stranica')

    # 2. Desna stranica (masiven blok)
    dodaj_kvader(fig, w_3d - d_3d, w_3d, 0, depth_3d, 0, h_3d, '#CD853F', 'Desna stranica')

    # 3. Pod (med stranicama)
    globina_stropa_poda = depth_3d - el_3d["Odmik_Hrbta"]
    dodaj_kvader(fig, d_3d, w_3d - d_3d, 0, globina_stropa_poda, 0, d_3d, '#DEB887', 'Pod')

    # 4. Strop (med stranicama)
    dodaj_kvader(fig, d_3d, w_3d - d_3d, 0, globina_stropa_poda, h_3d - d_3d, h_3d, '#F4A460', 'Strop')

    # 5. Hrbet (HDF 5mm zadaj)
    if "utor" in nacin_h_3d:
        hrbelt_xmin = d_3d - el_3d["Globina_Utora"]
        hrbelt_xmax = w_3d - d_3d + el_3d["Globina_Utora"]
        hrbelt_zmin = -el_3d["Globina_Utora"]
        hrbelt_zmax = h_3d + el_3d["Globina_Utora"]
    else:
        hrbelt_xmin = d_3d
        hrbelt_xmax = w_3d - d_3d
        hrbelt_zmin = d_3d
        hrbelt_zmax = h_3d - d_3d

    dodaj_kvader(fig, hrbelt_xmin, hrbelt_xmax, depth_3d - 5, depth_3d, hrbelt_zmin, hrbelt_zmax, '#B0C4DE', 'Hrbet (5mm)')

    # 6. Police (pomaknjene nazaj proti hrbtu z upoštevanjem opg_3d)
    if st_polic_3d > 0:
        notranja_visina = h_3d - (2 * d_3d)
        korak_visine = notranja_visina / (st_polic_3d + 1)
        sirina_kosa = w_3d - (2 * d_3d)
        sirina_police = sirina_kosa - zp_3d
        
        # Police so pomaknjene od spredaj nazaj (zajemajo globino od 0 do globina_police)
        globina_police = depth_3d - opg_3d
        x_zacetek = d_3d + (zp_3d / 2)

        for p_idx in range(st_polic_3d):
            z_pos = d_3d + (p_idx + 1) * korak_visine
            dodaj_kvader(fig, x_zacetek, x_zacetek + sirina_police, 0, globina_police, z_pos, z_pos + d_3d, '#20B2AA', f'Polica {p_idx+1}')

    fig.update_layout(
        scene=dict(
            xaxis_title='Širina (mm)',
            yaxis_title='Globina (mm)',
            zaxis_title='Višina (mm)',
            aspectmode='data'
        ),
        margin=dict(l=0, r=0, b=0, t=0),
        height=550
    )

    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # --- 4. IZRAČUN ---
    if st.button("🧮 Izračunaj skupni krojni list in robne trakove", type="primary"):
        vsi_kosi = []
        for el in st.session_state.elements:
            d = el.get("Debelina", 18)
            s = el.get("Širina", 800)
            v = el.get("Višina", 720)
            g = el.get("Globina", 550)
            naziv = el.get("Naziv", "Element")
            st_polic = el.get("Police", 0)
            ima_v = el.get("Vrata", False)
            
            nacin_h = el.get("Nacin_Hrbta", "Prislonjen zadaj (brez utora)")
            g_utora = el.get("Globina_Utora", 6)
            oh = el.get("Odmik_Hrbta", 5)
            zp = el.get("Zracnost_Polic", 2)
            opg = el.get("Odmik_Police_G", 25)

            str_robovi = []
            if el.get("ABS_Str_Spredaj", True): str_robovi.append("Sprednji")
            if el.get("ABS_Str_Zgornji", False): str_robovi.append("Zgornji")
            if el.get("ABS_Str_Spodnji", False): str_robovi.append("Spodnji")
            abs_s = ", ".join(str_robovi) if str_robovi else "Brez"

            abs_sp = "1x prednji rob" if el.get("ABS_StropPod", True) else "Brez"
            abs_p = "1x sprednji rob" if el.get("ABS_Polica", True) else "Brez"
            abs_v = "Vse 4 strani" if el.get("ABS_Vrata", True) else "Brez"

            # 1. Stranici
            vsi_kosi.append({"Omarica": naziv, "Del": "Stranica", "Količina": 2, "Širina (mm)": g, "Dolžina/Višina (mm)": v, "Robni trak (ABS)": abs_s})
            
            # 2. Strop in pod
            sirina_kosa = s - (2 * d)
            globina_stropa_poda = g - oh
            vsi_kosi.append({"Omarica": naziv, "Del": "Strop / Pod", "Količina": 2, "Širina (mm)": globina_stropa_poda, "Dolžina/Višina (mm)": sirina_kosa, "Robni trak (ABS)": abs_sp})
            
            # 3. Hrbtni del
            if "utor" in nacin_h:
                sirina_hrbta = s - (2 * d) + (2 * g_utora)
                visina_hrbta = v + (2 * g_utora)
            else:
                sirina_hrbta = s - (2 * d)
                visina_hrbta = v - (2 * d)
                
            vsi_kosi.append({"Omarica": naziv, "Del": "Hrbtni del (MDF/HDF 5mm)", "Količina": 1, "Širina (mm)": sirina_hrbta, "Dolžina/Višina (mm)": visina_hrbta, "Robni trak (ABS)": "Brez"})
            
            # 4. Police
            if st_polic > 0:
                sirina_police = sirina_kosa - zp
                globina_police = g - opg
                vsi_kosi.append({"Omarica": naziv, "Del": "Police", "Količina": st_polic, "Širina (mm)": globina_police, "Dolžina/Višina (mm)": sirina_police, "Robni trak (ABS)": abs_p})
            
            # 5. Vrata
            if ima_v:
                visina_vrat = v - 4
                sirina_vrat = (s / 2) - 3 if s > 600 else s - 4
                strop_kosov = 2 if s > 600 else 1
                vsi_kosi.append({"Omarica": naziv, "Del": "Vrata", "Količina": strop_kosov, "Širina (mm)": sirina_vrat, "Dolžina/Višina (mm)": visina_vrat, "Robni trak (ABS)": abs_v})

        st.success("Krojni list z izbranimi ABS robovi stranic uspešno izračunan!")
        df_skupaj = pd.DataFrame(vsi_kosi)
        st.dataframe(df_skupaj, use_container_width=True)
else:
    st.info("V projektu še ni elementov. Izberite prostor in dodajte prvo omaro.")
