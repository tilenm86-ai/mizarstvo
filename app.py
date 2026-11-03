import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(layout="wide")

st.title("🪚 Mizarski Kalkulator: 3D, Krojni List in 2D Tehnični Pledi")
st.write("Izberi prostor, vnesi omaro, določi nastavitve utora in ABS robove ter preveri izrise.")

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
globina_utora = st.sidebar.slider("Globina utora (v globino materiala v mm)", min_value=4, max_value=15, value=6, key="input_glob_utora")

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
        "Zracnost_Visina_Hrbta": zracnost_visina_hrbta,
        "Odmik_Hrbta": odmik_hrbta,
        "Zracnost_Polic": zracnost_polic_sirina,
        "Odmik_Police_G": odmik_police_globina,
        "Izbrani_Robovi_Stranice": izbrani_robovi_stranice,
        "Izbrani_Robovi_StropPod": izbrani_robovi_strop_pod,
        "ABS_Polica": abs_polica_izbira,
        "ABS_Vrata": abs_vrata_izbira
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

    # --- 3D MASIVNI PRIKAZ ---
    st.subheader("🧊 3D predogled elementa (Z možnostjo približevanja in vrtenja)")
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
    dodaj_kvader(fig, w_3d - d_3d, w_3d, 0, depth_3d, 0, h_3d, '#CD853F', 'Desna stranica')

    if "Vsi elementi" in nacin_h_3d:
        globina_stropa_poda = depth_3d
    else:
        globina_stropa_poda = depth_3d - oh_3d

    dodaj_kvader(fig, d_3d, w_3d - d_3d, 0, globina_stropa_poda, 0, d_3d, '#DEB887', 'Pod')
    dodaj_kvader(fig, d_3d, w_3d - d_3d, 0, globina_stropa_poda, h_3d - d_3d, h_3d, '#F4A460', 'Strop')

    hrbelt_xmin = d_3d - gutora_3d
    hrbelt_xmax = w_3d - d_3d + gutora_3d
    hrbelt_y_zacetek = depth_3d - ouz_3d
    hrbelt_y_konec = depth_3d - ouz_3d + 5  
    
    if "Vsi elementi" in nacin_h_3d:
        hrbelt_zmin = d_3d - gutora_3d
        hrbelt_zmax = h_3d - d_3d + gutora_3d
    else:
        hrbelt_zmin = 0
        hrbelt_zmax = h_3d

    dodaj_kvader(fig, hrbelt_xmin, hrbelt_xmax, hrbelt_y_zacetek, hrbelt_y_konec, hrbelt_zmin, hrbelt_zmax, '#B0C4DE', 'Hrbet (5mm)')

    if st_polic_3d > 0:
        notranja_visina = h_3d - (2 * d_3d)
        korak_visine = notranja_visina / (st_polic_3d + 1)
        sirina_kosa = w_3d - (2 * d_3d)
        sirina_police = sirina_kosa - zp_3d
        
        globina_police_3d = depth_3d - gutora_3d - opg_3d - (oh_3d if "Samo stranice" in nacin_h_3d else 0)
        zacetek_y_police = depth_3d - gutora_3d - opg_3d - globina_police_3d
        x_zacetek = d_3d + (zp_3d / 2)

        for p_idx in range(st_polic_3d):
            z_pos = d_3d + (p_idx + 1) * korak_visine
            dodaj_kvader(fig, x_zacetek, x_zacetek + sirina_police, zacetek_y_police, zacetek_y_police + globina_police_3d, z_pos, z_pos + d_3d, '#20B2AA', f'Polica {p_idx+1}')

    fig.update_layout(
        scene=dict(
            xaxis_title='Širina (mm)',
            yaxis_title='Globina (mm)',
            zaxis_title='Višina (mm)',
            aspectmode='data',
            camera=dict(eye=dict(x=1.5, y=1.8, z=1.2))
        ),
        margin=dict(l=0, r=0, b=0, t=0),
        height=550,
        dragmode='orbit'
    )

    st.plotly_chart(fig, use_container_width=True)
    st.info("💡 Namig: Za približevanje (zoom) uporabi kolesce miške ali prste. Za vrtenje modela klikni in povleci.")

    # --- 2D TEHNIČNI PREREZI (Z ČRTKANIMI ČRTAMI ZA STROP, POD IN POLICE) ---
    with st.expander("📐 Pokaži 2D tehnične poglede (Spredaj, Stranski prerez, Od zgoraj s črtkanimi črtami)"):
        tab_spredaj, tab_stran, tab_zgoraj = st.tabs(["Pogled od spredaj", "Pogled od strani", "Pogled od zgoraj (Tloris)"])
        
        # 1. SPREDAJ
        with tab_spredaj:
            st.write("Skica omare gledano od spredaj (z zarisom notranjih elementov in polic s črtkano črto).")
            fig_front = go.Figure()
            # Stranici
            fig_front.add_shape(type="rect", x0=0, y0=0, x1=d_3d, y1=h_3d, line=dict(color="#A0522D", width=2), fillcolor="#CD853F", opacity=0.7)
            fig_front.add_shape(type="rect", x0=w_3d-d_3d, y0=0, x1=w_3d, y1=h_3d, line=dict(color="#A0522D", width=2), fillcolor="#CD853F", opacity=0.7)
            
            # Pod in strop (s črtkastim robom / poudarkom)
            fig_front.add_shape(type="rect", x0=d_3d, y0=0, x1=w_3d-d_3d, y1=d_3d, line=dict(color="black", width=1.5, dash="dash"), fillcolor="#DEB887", opacity=0.8)
            fig_front.add_shape(type="rect", x0=d_3d, y0=h_3d-d_3d, x1=w_3d-d_3d, y1=h_3d, line=dict(color="black", width=1.5, dash="dash"), fillcolor="#F4A460", opacity=0.8)
            
            # Police s črtkano obrobo
            if st_polic_3d > 0:
                notranja_visina = h_3d - (2 * d_3d)
                korak_visine = notranja_visina / (st_polic_3d + 1)
                sirina_kosa = w_3d - (2 * d_3d)
                sirina_police = sirina_kosa - zp_3d
                x_zacetek = d_3d + (zp_3d / 2)
                for p_idx in range(st_polic_3d):
                    z_pos = d_3d + (p_idx + 1) * korak_visine
                    fig_front.add_shape(type="rect", x0=x_zacetek, y0=z_pos, x1=x_zacetek + sirina_police, y1=z_pos + d_3d, line=dict(color="black", width=1.5, dash="dash"), fillcolor="#20B2AA", opacity=0.8)

            fig_front.update_layout(
                xaxis_title="Širina (mm)", yaxis_title="Višina (mm)", height=400,
                xaxis=dict(range=[-50, w_3d + 50]), yaxis=dict(range=[-50, h_3d + 50], scaleanchor="x", scaleratio=1), showlegend=False
            )
            st.plotly_chart(fig_front, use_container_width=True)

        # 2. STRANI
        with tab_stran:
            st.write("Stranski prerez omare (s črtkanimi črtami za utor in police).")
            fig_side = go.Figure()
            fig_side.add_shape(type="rect", x0=0, y0=0, x1=depth_3d, y1=h_3d, line=dict(color="#A0522D", width=2), fillcolor="#CD853F", opacity=0.6)
            
            ut_y_zacetek = depth_3d - ouz_3d
            if "Vsi elementi" in nacin_h_3d:
                ut_z_min = d_3d - gutora_3d
                ut_z_max = h_3d - d_3d + gutora_3d
            else:
                ut_z_min = 0
                ut_z_max = h_3d

            # Utor s črtkano modro črto
            fig_side.add_shape(type="rect", x0=ut_y_zacetek, y0=ut_z_min,
                             x1=ut_y_zacetek + debelina_utora, y1=ut_z_max,
                             line=dict(color="blue", width=1.5, dash="dash"), fillcolor="#B0C4DE", opacity=0.8)

            # Police s črtkano obrobo od strani
            if st_polic_3d > 0:
                notranja_visina = h_3d - (2 * d_3d)
                korak_visine = notranja_visina / (st_polic_3d + 1)
                globina_police_2d = depth_3d - gutora_3d - opg_3d - (oh_3d if "Samo stranice" in nacin_h_3d else 0)
                zacetek_y_pol_2d = depth_3d - gutora_3d - opg_3d - globina_police_2d

                for p_idx in range(st_polic_3d):
                    z_pos = d_3d + (p_idx + 1) * korak_visine
                    fig_side.add_shape(type="rect", x0=zacetek_y_pol_2d, y0=z_pos, x1=zacetek_y_pol_2d + globina_police_2d, y1=z_pos + d_3d, line=dict(color="black", width=1.5, dash="dash"), fillcolor="#20B2AA", opacity=0.8)

            fig_side.update_layout(
                xaxis_title="Globina (mm)", yaxis_title="Višina (mm)", height=400,
                xaxis=dict(range=[-50, depth_3d + 50]), yaxis=dict(range=[-50, h_3d + 50], scaleanchor="x", scaleratio=1), showlegend=False
            )
            st.plotly_chart(fig_side, use_container_width=True)

        # 3. OD ZGORAJ (TLORIS)
        with tab_zgoraj:
            st.write("Tloris omare gledano od zgoraj (s črtkastimi linijami za hrbet in strop).")
            fig_top = go.Figure()
            fig_top.add_shape(type="rect", x0=0, y0=0, x1=d_3d, y1=depth_3d, line=dict(color="#A0522D", width=2), fillcolor="#CD853F", opacity=0.7)
            fig_top.add_shape(type="rect", x0=w_3d-d_3d, y0=0, x1=w_3d, y1=depth_3d, line=dict(color="#A0522D", width=2), fillcolor="#CD853F", opacity=0.7)
            
            # Strop s črtkanim robom
            fig_top.add_shape(type="rect", x0=d_3d, y0=0, x1=w_3d-d_3d, y1=globina_stropa_poda, line=dict(color="black", width=1.5, dash="dash"), fillcolor="#F4A460", opacity=0.7)
            
            # Hrbet s črtkano modro črto
            fig_top.add_shape(type="rect", x0=d_3d-gutora_3d, y0=depth_3d-ouz_3d, x1=w_3d-d_3d+gutora_3d, y1=depth_3d-ouz_3d+5, line=dict(color="blue", width=1.5, dash="dash"), fillcolor="#B0C4DE", opacity=0.8)

            fig_top.update_layout(
                xaxis_title="Širina (mm)", yaxis_title="Globina (mm)", height=400,
                xaxis=dict(range=[-50, w_3d + 50]), yaxis=dict(range=[-50, depth_3d + 50], scaleanchor="x", scaleratio=1), showlegend=False
            )
            st.plotly_chart(fig_top, use_container_width=True)

    st.divider()

    # --- 4. IZRAČUN ---
    if st.button("🧮 Izračunaj skupni krojni list in robne trakove", type="primary", key="gumb_izracun"):
        vsi_kosi = []
        for el in st.session_state.elements:
            d = el.get("Debelina", 18)
            s = el.get("Širina", 800)
            v = el.get("Višina", 720)
            g = el.get("Globina", 550)
            naziv = el.get("Naziv", "Element")
            st_polic = el.get("Police", 0)
            ima_v = el.get("Vrata", False)
            
            nacin_h = el.get("Nacin_Hrbta", "")
            gutora = el.get("Globina_Utora", 6)
            oh = el.get("Odmik_Hrbta", 0)
            zp = el.get("Zracnost_Polic", 2)
            opg = el.get("Odmik_Police_G", 25)
            zracnost_v_hrbta = el.get("Zracnost_Visina_Hrbta", 2)

            izbrani_r_str = el.get("Izbrani_Robovi_Stranice", [])
            abs_s = ", ".join(izbrani_r_str) if izbrani_r_str else "Brez"

            izbrani_r_sp = el.get("Izbrani_Robovi_StropPod", [])
            abs_sp = ", ".join(izbrani_r_sp) if izbrani_r_sp else "Brez"

            abs_p = "1x sprednji rob" if el.get("ABS_Polica") == "Da (1x rob)" else "Brez"
            abs_v = "Vse 4 strani" if el.get("ABS_Vrata") == "Vse 4 strani" else "Brez"

            # 1. Stranici
            vsi_kosi.append({"Omarica": naziv, "Del": "Stranica", "Količina": 2, "Širina (mm)": g, "Dolžina/Višina (mm)": v, "Robni trak (ABS)": abs_s})
            
            # 2. Strop in pod
            sirina_kosa = s - (2 * d)
            if "Vsi elementi" in nacin_h:
                globina_stropa_poda = g + gutora
            else:
                globina_stropa_poda = g - oh

            vsi_kosi.append({"Omarica": naziv, "Del": "Strop / Pod", "Količina": 2, "Širina (mm)": globina_stropa_poda, "Dolžina/Višina (mm)": sirina_kosa, "Robni trak (ABS)": abs_sp})
            
            # 3. Hrbtni del
            zracnost_sirina_hrbta = 2  
            
            if "Samo stranice" in nacin_h:
                sirina_hrbta = (s - (2 * d)) + (2 * gutora) - zracnost_sirina_hrbta
                visina_hrbta = v - zracnost_v_hrbta
            else:
                sirina_hrbta = (s - (2 * d)) + (2 * gutora) - zracnost_sirina_hrbta
                visina_hrbta = (v - (2 * d)) + (2 * gutora) - zracnost_v_hrbta
                
            vsi_kosi.append({"Omarica": naziv, "Del": "Hrbtni del (MDF/HDF 5mm)", "Količina": 1, "Širina (mm)": sirina_hrbta, "Dolžina/Višina (mm)": visina_hrbta, "Robni trak (ABS)": "Brez"})
            
            # 4. Police
            if st_polic > 0:
                sirina_police = sirina_kosa - zp
                globina_police = g - gutora - opg - oh
                vsi_kosi.append({"Omarica": naziv, "Del": "Police", "Količina": st_polic, "Širina (mm)": globina_police, "Dolžina/Višina (mm)": sirina_police, "Robni trak (ABS)": abs_p})
            
            # 5. Vrata
            if ima_v:
                visina_vrat = v - 4
                sirina_vrat = (s / 2) - 3 if s > 600 else s - 4
                strop_kosov = 2 if s > 600 else 1
                vsi_kosi.append({"Omarica": naziv, "Del": "Vrata", "Količina": strop_kosov, "Širina (mm)": sirina_vrat, "Dolžina/Višina (mm)": visina_vrat, "Robni trak (ABS)": abs_v})

        st.success("Krojni list z vsemi nastavitvami uspešno izračunan!")
        df_skupaj = pd.DataFrame(vsi_kosi)
        st.dataframe(df_skupaj, use_container_width=True)
else:
    st.info("V projektu še ni elementov. Izberite prostor in dodajte prvo omaro v stranskem meniju.")
