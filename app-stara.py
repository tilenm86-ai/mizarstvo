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

st.title("🪚 Mizarski Kalkulator: 3D, 2D Risbe s Črtkanimi Črtami in Krojni List")
st.write("Vnesi podatke o omarici, preveri 3D predogled ter 2D tehnične izrise z vsemi notranjimi elementi.")

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
with col1:
    sirina = st.sidebar.number_input("Širina (mm)", value=800, step=10, key="input_sirina")
with col2:
    visina = st.sidebar.number_input("Višina (mm)", value=720, step=10, key="input_visina")
with col3:
    globina = st.sidebar.number_input("Globina (mm)", value=550, step=10, key="input_globina")

st.sidebar.subheader("⚙️ Konstrukcija hrbta, utora in ABS")
nacin_hrbta = st.sidebar.selectbox(
    "Vgradnja hrbta", 
    [
        "V utoru: Samo stranice (strop in pod brez utora)",
        "V utoru: Vsi elementi (stranice, strop, pod)"
    ],
    key="input_nacin_hrbta"
)

privzeti_odmik = 5
odmik_utora_zadaj = st.sidebar.slider("Odmik utora od zadnjega roba (mm)", min_value=5, max_value=35, value=privzeti_odmik, key="input_odmik_utora")
debelina_utora = st.sidebar.slider("Debelina utora (širina reza v mm)", min_value=4, max_value=8, value=5, key="input_deb_utora")
globina_utora = st.sidebar.slider("Globina utora (v globino materiala v mm)", min_value=4, max_value=15, value=13, key="input_globina_utora")
zracnost_visina_hrbta = st.sidebar.slider("Zračnost za višino hrbta (mm)", min_value=0, max_value=10, value=2, key="input_zracnost_v_hrbta")

preostanek_mesa = debelina - globina_utora
if preostanek_mesa < 4:
    st.sidebar.warning("⚠️ Pozor! Zadaj za privijačenje ostane samo " + str(preostanek_mesa) + " mm materiala.")
else:
    st.sidebar.info("ℹ️ Zadaj za privijačenje ostane " + str(preostanek_mesa) + " mm materiala.")

if "Samo stranice" in nacin_hrbta:
    odmik_hrbta = st.sidebar.slider("Odmik stropa/poda zadaj (mm)", min_value=0, max_value=30, value=5, key="input_odmik_hrbta")
else:
    odmik_hrbta = 0

zracnost_polic_sirina = st.sidebar.slider("Zračnost police širina - skupaj (mm)", min_value=0, max_value=10, value=2, key="input_zracnost")
odmik_police_globina = st.sidebar.slider("Koliko je polica krajša od globine omare (mm)", min_value=10, max_value=50, value=25, key="input_odmik_pol")

st.sidebar.markdown("---")
st.sidebar.markdown("**Izbira ABS robov:**")
izbrani_robovi_stranice = st.sidebar.multiselect("Stranica - ABS robovi", ["Sprednji", "Zgornji", "Spodnji", "Zadnji"], default=["Sprednji"], key="ms_stranica")
izbrani_robovi_strop_pod = st.sidebar.multiselect("Strop / Pod - ABS robovi", ["Sprednji", "Zadnji"], default=["Sprednji"], key="ms_strop_pod")
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
    st.sidebar.success("Posodobljeno: " + ime_elementa)

st.subheader("📋 Seznam elementov za projekt: " + vrsta_projekta)

if len(st.session_state.elements) > 0:
    for i, el in enumerate(st.session_state.elements):
        c1, c2 = st.columns([5, 1])
        with c1:
            naziv_p = el.get("Naziv", "Element")
            projekt_p = el.get("Projekt", "Kuhinja")
            tip_p = el.get("Tip", "Omarica")
            s_p = el.get("Širina", 0)
            v_p = el.get("Višina", 0)
            g_p = el.get("Globina", 0)
            pol_p = el.get("Police", 0)
            st.write(f"**{i+1}. {naziv_p}** ({projekt_p} ➔ *{tip_p}*) — Š: {s_p} mm, V: {v_p} mm, G: {g_p} mm | Police: {pol_p}")
        with c2:
            if st.button("❌", key="del_" + str(i)):
                st.session_state.elements = []
                st.rerun()

    if st.button("🗑️ Počisti cel projekt", key="gumb_pocisti"):
        st.session_state.elements = []
        st.rerun()

    st.divider()

    def dodaj_kvader(fig, x_min, x_max, y_min, y_max, z_min, z_max, color, name):
        fig.add_trace(go.Mesh3d(
            x=[x_min, x_max, x_max, x_min, x_min, x_max, x_max, x_min],
            y=[y_min, y_min, y_max, y_max, y_min, y_min, y_max, y_max],
            z=[z_min, z_min, z_min, z_min, z_max, z_max, z_max, z_max],
            i=[0, 0, 4, 4, 0, 0, 2, 2, 0, 0, 1, 1],
            j=[1, 2, 5, 6, 1, 5, 3, 7, 3, 7, 2, 6],
            k=[2, 3, 6, 7, 5, 4, 7, 6, 7, 4, 6, 5],
            color=color, opacity=0.9, name=name, showscale=False
        ))

    with st.expander("🧊 Pokaži 3D predogled omare", expanded=True):
        izbran_indeks = st.selectbox("Izberi element za 3D prikaz", range(len(st.session_state.elements)), format_func=lambda x: st.session_state.elements[x]["Naziv"], key="select_3d_index")
        
        el_3d = st.session_state.elements[izbran_indeks]
        d_3d, w_3d, h_3d, depth_3d = el_3d["Debelina"], el_3d["Širina"], el_3d["Višina"], el_3d["Globina"]
        st_polic_3d, opg_3d, zp_3d = el_3d["Police"], el_3d["Odmik_Police_G"], el_3d["Zracnost_Polic"]
        nacin_h_3d, ouz_3d = el_3d["Nacin_Hrbta"], el_3d.get("Odmik_Utora_Zadaj", 5)
        gutora_3d, oh_3d = el_3d["Globina_Utora"], el_3d["Odmik_Hrbta"]

        fig = go.Figure()
        dodaj_kvader(fig, 0, d_3d, 0, depth_3d, 0, h_3d, "#A0522D", "Leva stranica")
        dodaj_kvader(fig, w_3d - d_3d, w_3d, 0, depth_3d, 0, h_3d, "#CD853F", "Desna stranica")

        globina_stropa_poda = depth_3d if "Vsi elementi" in nacin_h_3d else (depth_3d - oh_3d)
        dodaj_kvader(fig, d_3d, w_3d - d_3d, 0, globina_stropa_poda, 0, d_3d, "#DEB887", "Pod")
        dodaj_kvader(fig, d_3d, w_3d - d_3d, 0, globina_stropa_poda, h_3d - d_3d, h_3d, "#F4A460", "Strop")

        hrbelt_xmin, hrbelt_xmax = d_3d - gutora_3d, w_3d - d_3d + gutora_3d
        hrbelt_y_zacetek, hrbelt_y_konec = depth_3d - ouz_3d, depth_3d - ouz_3d + 5
        hrbelt_zmin = (d_3d - gutora_3d) if "Vsi elementi" in nacin_h_3d else 0
        hrbelt_zmax = (h_3d - d_3d + gutora_3d) if "Vsi elementi" in nacin_h_3d else h_3d
        dodaj_kvader(fig, hrbelt_xmin, hrbelt_xmax, hrbelt_y_zacetek, hrbelt_y_konec, hrbelt_zmin, hrbelt_zmax, "#B0C4DE", "Hrbet (5mm)")

        if st_polic_3d > 0:
            notranja_visina = h_3d - (2 * d_3d)
            korak_visine = notranja_visina / (st_polic_3d + 1)
            sirina_police = (w_3d - (2 * d_3d)) - zp_3d
            globina_police_3d = depth_3d - gutora_3d - opg_3d - (oh_3d if "Samo stranice" in nacin_h_3d else 0)
            zacetek_y_police = depth_3d - gutora_3d - opg_3d - globina_police_3d
            x_zacetek = d_3d + (zp_3d / 2)

            for p_idx in range(st_polic_3d):
                z_pos = d_3d + (p_idx + 1) * korak_visine
                dodaj_kvader(fig, x_zacetek, x_zacetek + sirina_police, zacetek_y_police, zacetek_y_police + globina_police_3d, z_pos, z_pos + d_3d, "#20B2AA", f"Polica {p_idx+1}")

        fig.update_layout(
            scene={"xaxis_title": "Širina (mm)", "yaxis_title": "Globina (mm)", "zaxis_title": "Višina (mm)", "aspectmode": "data", "camera": {"eye": {"x": 1.5, "y": 1.8, "z": 1.2}}},
            margin={"l": 0, "r": 0, "b": 0, "t": 0}, height=550, dragmode="orbit"
        )
        st.plotly_chart(fig, use_container_width=True)

    with st.expander("📐 Pokaži delavniške 2D tehnične risbe s črtkanimi črtami", expanded=True):
        tab_spredaj, tab_stran, tab_zgoraj = st.tabs(["Pogled od spredaj", "Pogled od strani", "Pogled od zgoraj (Tloris)"])
        
        with tab_spredaj:
            fig_front = go.Figure()
            s_c, f_c = "#A0522D", "#CD853F"
            fig_front.add_shape(type="rect", x0=0, y0=0, x1=d_3d, y1=h_3d, line_color=s_c, line_width=2, fillcolor=f_c, opacity=0.7)
            fig_front.add_shape(type="rect", x0=w_3d-d_3d, y0=0, x1=w_3d, y1=h_3d, line_color=s_c, line_width=2, fillcolor=f_c, opacity=0.7)
            fig_front.add_shape(type="rect", x0=d_3d, y0=0, x1=w_3d-d_3d, y1=d_3d, line_color="black", line_width=1.5, line_dash="dash", fillcolor="#DEB887", opacity=0.8)
            fig_front.add_shape(type="rect", x0=d_3d, y0=h_3d-d_3d, x1=w_3d-d_3d, y1=h_3d, line_color="black", line_width=1.5, line_dash="dash", fillcolor="#F4A460", opacity=0.8)
            
            if st_polic_3d > 0:
                notranja_visina = h_3d - (2 * d_3d)
                korak_visine = notranja_visina / (st_polic_3d + 1)
                sirina_police = (w_3d - (2 * d_3d)) - zp_3d
                x_zacetek = d_3d + (zp_3d / 2)
                for p_idx in range(st_polic_3d):
                    z_pos = d_3d + (p_idx + 1) * korak_visine
                    fig_front.add_shape(type="rect", x0=x_zacetek, y0=z_pos, x1=x_zacetek + sirina_police, y1=z_pos + d_3d, line_color="black", line_width=1.5, line_dash="dash", fillcolor="#20B2AA", opacity=0.8)

            fig_front.update_layout(
                xaxis_title="Širina (mm)", yaxis_title="Višina (mm)", height=450,
                xaxis={"range": [-20, w_3d + 20]},
                yaxis={"scaleanchor": "x", "scaleratio": 1, "range": [-20, h_3d + 20]},
                showlegend=False
            )
            st.plotly_chart(fig_front, use_container_width=True)

        with tab_stran:
            fig_side = go.Figure()
            fig_side.add_shape(type="rect", x0=0, y0=0, x1=depth_3d, y1=h_3d, line_color=s_c, line_width=2, fillcolor=f_c, opacity=0.4)
            fig_side.add_shape(type="rect", x0=0, y0=0, x1=globina_stropa_poda, y1=d_3d, line_color="black", line_width=1.5, line_dash="dash", fillcolor="#DEB887", opacity=0.8)
            fig_side.add_shape(type="rect", x0=0, y0=h_3d-d_3d, x1=globina_stropa_poda, y1=h_3d, line_color="black", line_width=1.5, line_dash="dash", fillcolor="#F4A460", opacity=0.8)
            
            ut_y_zacetek = depth_3d - ouz_3d
            ut_z_min = (d_3d - gutora_3d) if "Vsi elementi" in nacin_h_3d else 0
            ut_z_max = (h_3d - d_3d + gutora_3d) if "Vsi elementi" in nacin_h_3d else h_3d
            fig_side.add_shape(type="rect", x0=ut_y_zacetek, y0=ut_z_min, x1=ut_y_zacetek + debelina_utora, y1=ut_z_max, line_color="blue", line_width=1.5, line_dash="dash", fillcolor="#B0C4DE", opacity=0.8)

            if st_polic_3d > 0:
                notranja_visina = h_3d - (2 * d_3d)
                korak_visine = notranja_visina / (st_polic_3d + 1)
                globina_police_2d = depth_3d - gutora_3d - opg_3d - (oh_3d if "Samo stranice" in nacin_h_3d else 0)
                zacetek_y_pol_2d = ut_y_zacetek - opg_3d - globina_police_2d
                for p_idx in range(st_polic_3d):
                    z_pos = d_3d + (p_idx + 1) * korak_visine
                    fig_side.add_shape(type="rect", x0=zacetek_y_pol_2d, y0=z_pos, x1=zacetek_y_pol_2d + globina_police_2d, y1=z_pos + d_3d, line_color="black", line_width=1.5, line_dash="dash", fillcolor="#20B2AA", opacity=0.8)

            fig_side.update_layout(
                xaxis_title="Globina (mm)", yaxis_title="Višina (mm)", height=450,
                xaxis={"range": [-20, depth_3d + 20]},
                yaxis={"scaleanchor": "x", "scaleratio": 1, "range": [-20, h_3d + 20]},
                showlegend=False
            )
            st.plotly_chart(fig_side, use_container_width=True)

        with tab_zgoraj:
            fig_top = go.Figure()
            fig_top.add_shape(type="rect", x0=0, y0=0, x1=d_3d, y1=depth_3d, line_color=s_c, line_width=2, fillcolor=f_c, opacity=0.7)
            fig_top.add_shape(type="rect", x0=w_3d-d_3d, y0=0, x1=w_3d, y1=depth_3d, line_color=s_c, line_width=2, fillcolor=f_c, opacity=0.7)
            fig_top.add_shape(type="rect", x0=d_3d, y0=0, x1=w_3d-d_3d, y1=globina_stropa_poda, line_color="black", line_width=1.5, line_dash="dash", fillcolor="#F4A460", opacity=0.7)
            fig_top.add_shape(type="rect", x0=d_3d-gutora_3d, y0=depth_3d-ouz_3d, x1=w_3d-d_3d+gutora_3d, y1=depth_3d-ouz_3d+5, line_color="blue", line_width=1.5, line_dash="dash", fillcolor="#B0C4DE", opacity=0.8)
            
            fig_top.update_layout(
                xaxis_title="Širina (mm)", yaxis_title="Globina (mm)", height=450,
                xaxis={"range": [-20, w_3d + 20]},
                yaxis={"scaleanchor": "x", "scaleratio": 1, "range": [-20, depth_3d + 20]},
                showlegend=False
            )
            st.plotly_chart(fig_top, use_container_width=True)

    st.divider()

    if st.button("🧮 Izračunaj skupni krojni list in robne trakove", type="primary", key="gumb_izracun"):
        vsi_kosi = []
        for el in st.session_state.elements:
            d, s, v, g = el["Debelina"], el["Širina"], el["Višina"], el["Globina"]
            naziv, st_polic, ima_v = el["Naziv"], el["Police"], el["Vrata"]
            nacin_h, gutora, oh = el["Nacin_Hrbta"], el["Globina_Utora"], el["Odmik_Hrbta"]
            zp, opg, zracnost_v_hrbta = el["Zracnost_Polic"], el["Odmik_Police_G"], el["Zracnost_Visina_Hrbta"]

            abs_s = ", ".join(el.get("Izbrani_Robovi_Stranice", [])) or "Brez"
            abs_sp = ", ".join(el.get("Izbrani_Robovi_StropPod", [])) or "Brez"
            abs_p = "1x sprednji rob" if el.get("ABS_Polica") == "Da (1x rob)" else "Brez"
            abs_v = "Vse 4 strani" if el.get("ABS_Vrata") == "Vse 4 strani" else "Brez"

            vsi_kosi.append({"Omarica": naziv, "Del": "Stranica", "Količina": 2, "Širina (mm)": g, "Dolžina/Višina (mm)": v, "Robni trak (ABS)": abs_s})
            
            sirina_kosa = s - (2 * d)
            globina_stropa_poda = (g + gutora) if "Vsi elementi" in nacin_h else (g - oh)
            vsi_kosi.append({"Omarica": naziv, "Del": "Strop / Pod", "Količina": 2, "Širina (mm)": globina_stropa_poda, "Dolžina/Višina (mm)": sirina_kosa, "Robni trak (ABS)": abs_sp})
            
            sirina_hrbta = (s - (2 * d)) + (2 * gutora) - 2
            visina_hrbta = (v - zracnost_v_hrbta) if "Samo stranice" in nacin_h else ((v - (2 * d)) + (2 * gutora) - zracnost_v_hrbta)
            vsi_kosi.append({"Omarica": naziv, "Del": "Hrbtni del (MDF/HDF 5mm)", "Količina": 1, "Širina (mm)": sirina_hrbta, "Dolžina/Višina (mm)": visina_hrbta, "Robni trak (ABS)": "Brez"})
            
            if st_polic > 0:
                sirina_police = sirina_kosa - zp
                globina_police = g - gutora - opg - oh
                vsi_kosi.append({"Omarica": naziv, "Del": "Police", "Količina": st_polic, "Širina (mm)": globina_police, "Dolžina/Višina (mm)": sirina_police, "Robni trak (ABS)": abs_p})
            
            if ima_v:
                visina_vrat = v - 4
                sirina_vrat = (s / 2) - 3 if s > 600 else s - 4
                strop_kosov = 2 if s > 600 else 1
                vsi_kosi.append({"Omarica": naziv, "Del": "Vrata", "Količina": strop_kosov, "Širina (mm)": sirina_vrat, "Dolžina/Višina (mm)": visina_vrat, "Robni trak (ABS)": abs_v})

        st.success("Krojni list z vsemi nastavitvami uspešno izračunan!")
        st.dataframe(pd.DataFrame(vsi_kosi), use_container_width=True)

