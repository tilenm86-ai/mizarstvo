import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.title("🪚 Mizarski Kalkulator: 3D, Krojni List in Tehnične 2D Risbe s Kotami")

if "elements" not in st.session_state:
    st.session_state.elements = [{"Projekt": "Kuhinja", "Naziv": "Omarica 1", "Tip": "Spodnja omarica s policami in vrati", "Širina": 800, "Višina": 720, "Globina": 550, "Police": 2, "Vrata": True, "Debelina": 18, "Nacin_Hrbta": "V utoru: Vsi elementi (stranice, strop, pod)", "Odmik_Utora_Zadaj": 5, "Debelina_Utora": 5, "Globina_Utora": 13, "Zracnost_Visina_Hrbta": 2, "Odmik_Hrbta": 0, "Zracnost_Polic": 2, "Odmik_Police_G": 25, "Izbrani_Robovi_Stranice": ["Sprednji"], "Izbrani_Robovi_StropPod": ["Sprednji"], "ABS_Polica": "Da (1x rob)", "ABS_Vrata": "Vse 4 strani"}]

vrsta_projekta = st.sidebar.selectbox("Izberi prostor", ["Kuhinja", "Dnevna soba", "Spalnica / Garderoba", "Kopalnica"])
st.sidebar.divider()
ime_elementa = st.sidebar.text_input("Naziv elementa", value="Omarica 1")
debelina = st.sidebar.number_input("Debelina materiala (mm)", value=18, step=1)
stevilo_polic = st.sidebar.slider("Število polic", min_value=0, max_value=10, value=2)

c1, c2, c3 = st.sidebar.columns(3)
with c1: sirina = st.sidebar.number_input("Širina", value=800, step=10)
with c2: visina = st.sidebar.number_input("Višina", value=720, step=10)
with c3: globina = st.sidebar.number_input("Globina", value=550, step=10)

if st.sidebar.button("💾 Shrani omaro v projekt"):
    st.session_state.elements = [{"Projekt": vrsta_projekta, "Naziv": ime_elementa, "Tip": "Omarica", "Širina": sirina, "Višina": visina, "Globina": globina, "Police": stevilo_polic, "Vrata": True, "Debelina": debelina, "Nacin_Hrbta": "V utoru: Vsi elementi (stranice, strop, pod)", "Odmik_Utora_Zadaj": 5, "Debelina_Utora": 5, "Globina_Utora": 13, "Zracnost_Visina_Hrbta": 2, "Odmik_Hrbta": 0, "Zracnost_Polic": 2, "Odmik_Police_G": 25, "Izbrani_Robovi_Stranice": ["Sprednji"], "Izbrani_Robovi_StropPod": ["Sprednji"], "ABS_Polica": "Da (1x rob)", "ABS_Vrata": "Vse 4 strani"}]
    st.success("Shranjeno!")

if len(st.session_state.elements) > 0:
    el = st.session_state.elements[0]
    st.write(f"**Element:** {el['Naziv']} | Š: {el['Širina']} mm, V: {el['Višina']} mm, G: {el['Globina']} mm")

    def dodaj_kvader(fig, x_min, x_max, y_min, y_max, z_min, z_max, color, name):
        fig.add_trace(go.Mesh3d(x=[x_min, x_max, x_max, x_min, x_min, x_max, x_max, x_min], y=[y_min, y_min, y_max, y_max, y_min, y_min, y_max, y_max], z=[z_min, z_min, z_min, z_min, z_max, z_max, z_max, z_max], i=[0, 0, 4, 4, 0, 0, 2, 2, 0, 0, 1, 1], j=[1, 2, 5, 6, 1, 5, 3, 7, 3, 7, 2, 6], k=[2, 3, 6, 7, 5, 4, 7, 6, 7, 4, 6, 5], color=color, opacity=0.9, name=name, showscale=False))

    with st.expander("🧊 Pokaži 3D predogled omare"):
        fig = go.Figure()
        d, w, h, g = el["Debelina"], el["Širina"], el["Višina"], el["Globina"]
        dodaj_kvader(fig, 0, d, 0, g, 0, h, "#A0522D", "Leva stranica")
        dodaj_kvader(fig, w - d, w, 0, g, 0, h, "#CD853F", "Desna stranica")
        dodaj_kvader(fig, d, w - d, 0, g, 0, d, "#DEB887", "Pod")
        dodaj_kvader(fig, d, w - d, 0, g, h - d, h, "#F4A460", "Strop")
        fig.update_layout(scene={"xaxis_title": "Širina", "yaxis_title": "Globina", "zaxis_title": "Višina"}, height=500)
        st.plotly_chart(fig, use_container_width=True)

    if st.button("🧮 Izračunaj krojni list", type="primary"):
        kosi = [
            {"Del": "Stranica", "Količina": 2, "Širina": g, "Višina": h},
            {"Del": "Strop / Pod", "Količina": 2, "Širina": g, "Višina": w - (2 * d)},
            {"Del": "Hrbet", "Količina": 1, "Širina": w - (2 * d) + 8, "Višina": h + 8}
        ]
        if el["Police"] > 0:
            kosi.append({"Del": "Police", "Količina": el["Police"], "Širina": g - 38, "Višina": w - (2 * d) - 2})
        st.dataframe(pd.DataFrame(kosi), use_container_width=True)
