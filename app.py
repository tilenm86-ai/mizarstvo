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

st.title("🪚 Mizarski Kalkulator: 3D, 2D Risbe in Krojni List")
st.write("Vnesi podatke o omarici, preveri 3D in 2D izrise ter izračunaj krojni list.")

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

vrsta_projekta = st.sidebar.selectbox("Izberi prostor", ["Kuhinja", "Dnevna soba", "Spalnica / Garderoba", "Kopalnica"])
st.sidebar.divider()
ime_elementa = st.sidebar.text_input("Naziv elementa", value="Omarica 1")
tip_elementa = st.sidebar.selectbox("Vrsta omare", ["Spodnja omarica s policami in vrati", "Spodnja omarica z vrati", "Viseča omarica"])
debelina = st.sidebar.number_input("Debelina materiala (mm)", value=18, step=1)
stevilo_polic = st.sidebar.slider("Število polic", min_value=0, max_value=10, value=2)

c1, c2, c3 = st.sidebar.columns(3)
with c1: sirina = st.sidebar.number_input("Širina (mm)", value=800, step=10)
with c2: visina = st.sidebar.number_input("Višina (mm)", value=720, step=10)
with c3: globina = st.sidebar.number_input("Globina (mm)", value=550, step=10)

if st.sidebar.button("💾 Shrani omaro v projekt"):
    st.session_state.elements = [{
        "Projekt": vrsta_projekta,
        "Naziv": ime_elementa,
        "Tip": tip_elementa,
        "Širina": sirina,
        "Višina": visina,
        "Globina": globina,
        "Police": stevilo_polic,
        "Vrata": True,
        "Debelina": debelina,
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
    st.sidebar.success("Shranjeno!")

if len(st.session_state.elements) > 0:
    el = st.session_state.elements[0]
    st.write(f"**Element:** {el['Naziv']} | Š: {el['Širina']} mm, V: {el['Višina']} mm, G: {el['Globina']} mm")

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

    # 3D PREDOGLED
    with st.expander("🧊 Pokaži 3D predogled omare", expanded=True):
        fig = go.Figure()
        d, w, h, g = el["Debelina"], el["Širina"], el["Višina"], el["Globina"]
        dodaj_kvader(fig, 0, d, 0, g, 0, h, "#A0522D", "Leva stranica")
        dodaj_kvader(fig, w - d, w, 0, g, 0, h, "#CD853F", "Desna stranica")
        dodaj_kvader(fig, d, w - d, 0, g, 0, d, "#DEB887", "Pod")
        dodaj_kvader(fig, d, w - d, 0, g, h - d, h, "#F4A460", "Strop")
        
        if el["Police"] > 0:
            notranja_visina = h - (2 * d)
            korak_visine = notranja_visina / (el["Police"] + 1)
            sirina_police = (w - (2 * d)) - 2
            for p_idx in range(el["Police"]):
                z_pos = d + (p_idx + 1) * korak_visine
                dodaj_kvader(fig, d + 1, d + 1 + sirina_police, 5, g - 25, z_pos, z_pos + d, "#20B2AA", f"Polica {p_idx+1}")

        fig.update_layout(scene={"xaxis_title": "Širina", "yaxis_title": "Globina", "zaxis_title": "Višina"}, height=500)
        st.plotly_chart(fig, use_container_width=True)

    # 2D TEHNIČNI IZRISI
    with st.expander("📐 Pokaži delavniške 2D tehnične risbe", expanded=True):
        tab_spredaj, tab_stran, tab_zgoraj = st.tabs(["Pogled od spredaj", "Pogled od strani", "Pogled od zgoraj (Tloris)"])
        
        with tab_spredaj:
            fig_front = go.Figure()
            fig_front.add_shape(type="rect", x0=0, y0=0, x1=d, y1=h, line_color="#A0522D", fillcolor="#CD853F", opacity=0.7)
            fig_front.add_shape(type="rect", x0=w-d, y0=0, x1=w, y1=h, line_color="#A0522D", fillcolor="#CD853F", opacity=0.7)
            fig_front.add_shape(type="rect", x0=d, y0=0, x1=w-d, y1=d, line_color="black", fillcolor="#DEB887", opacity=0.8)
            fig_front.add_shape(type="rect", x0=d, y0=h-d, x1=w-d, y1=h, line_color="black", fillcolor="#F4A460", opacity=0.8)
            fig_front.update_layout(xaxis_title="Širina (mm)", yaxis_title="Višina (mm)", height=400, showlegend=False)
            st.plotly_chart(fig_front, use_container_width=True)

        with tab_stran:
            fig_side = go.Figure()
            fig_side.add_shape(type="rect", x0=0, y0=0, x1=g, y1=h, line_color="#A0522D", fillcolor="#CD853F", opacity=0.4)
            fig_side.update_layout(xaxis_title="Globina (mm)", yaxis_title="Višina (mm)", height=400, showlegend=False)
            st.plotly_chart(fig_side, use_container_width=True)

        with tab_zgoraj:
            fig_top = go.Figure()
            fig_top.add_shape(type="rect", x0=0, y0=0, x1=d, y1=g, line_color="#A0522D", fillcolor="#CD853F", opacity=0.7)
            fig_top.add_shape(type="rect", x0=w-d, y0=0, x1=w, y1=g, line_color="#A0522D", fillcolor="#CD853F", opacity=0.7)
            fig_top.update_layout(xaxis_title="Širina (mm)", yaxis_title="Globina (mm)", height=400, showlegend=False)
            st.plotly_chart(fig_top, use_container_width=True)

    st.divider()

    # KROJNI LIST
    if st.button("🧮 Izračunaj krojni list", type="primary"):
        sirina_stropa_poda = w - (2 * d)
        kosi = [
            {"Del": "Stranica", "Količina": 2, "Širina (mm)": g, "Višina (mm)": h},
            {"Del": "Strop / Pod", "Količina": 2, "Širina (mm)": g, "Višina (mm)": sirina_stropa_poda},
            {"Del": "Hrbet", "Količina": 1, "Širina (mm)": sirina_stropa_poda + 8, "Višina (mm)": h + 8},
            {"Del": "Vrata", "Količina": 1 if w <= 600 else 2, "Širina (mm)": (w - 4) if w <= 600 else (w/2 - 3), "Višina (mm)": h - 4}
        ]
        if el["Police"] > 0:
            kosi.append({"Del": "Police", "Količina": el["Police"], "Širina (mm)": g - 38, "Višina (mm)": sirina_stropa_poda - 2})
        st.dataframe(pd.DataFrame(kosi), use_container_width=True)
