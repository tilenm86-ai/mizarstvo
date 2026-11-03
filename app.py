import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.title("🪚 Mizarski Kalkulator: 3D in Krojni List")

if "elements" not in st.session_state:
    st.session_state.elements = [{
        "Naziv": "Omarica 1", 
        "Širina": 800, 
        "Višina": 720, 
        "Globina": 550, 
        "Police": 2, 
        "Debelina": 18
    }]

st.sidebar.header("Nastavitve omarice")
ime = st.sidebar.text_input("Naziv", value="Omarica 1")
debelina = st.sidebar.number_input("Debelina materiala (mm)", value=18)
police = st.sidebar.slider("Število polic", min_value=0, max_value=10, value=2)

sirina = st.sidebar.number_input("Širina (mm)", value=800, step=10)
visina = st.sidebar.number_input("Višina (mm)", value=720, step=10)
globina = st.sidebar.number_input("Globina (mm)", value=550, step=10)

if st.sidebar.button("💾 Shrani omaro"):
    st.session_state.elements = [{
        "Naziv": ime, 
        "Širina": sirina, 
        "Višina": visina, 
        "Globina": globina, 
        "Police": police, 
        "Debelina": debelina
    }]
    st.success("Shranjeno!")

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

with st.expander("🧊 Pokaži 3D predogled omare"):
    fig = go.Figure()
    d = el["Debelina"]
    w = el["Širina"]
    h = el["Višina"]
    g = el["Globina"]
    
    dodaj_kvader(fig, 0, d, 0, g, 0, h, "#A0522D", "Leva stranica")
    dodaj_kvader(fig, w - d, w, 0, g, 0, h, "#CD853F", "Desna stranica")
    dodaj_kvader(fig, d, w - d, 0, g, 0, d, "#DEB887", "Pod")
    dodaj_kvader(fig, d, w - d, 0, g, h - d, h, "#F4A460", "Strop")
    
    fig.update_layout(
        scene={"xaxis_title": "Širina", "yaxis_title": "Globina", "zaxis_title": "Višina"}, 
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)

if st.button("🧮 Izračunaj krojni list", type="primary"):
    d = el["Debelina"]
    w = el["Širina"]
    h = el["Višina"]
    g = el["Globina"]
    
    sirina_stropa_poda = w - (2 * d)
    hrbet_sirina = sirina_stropa_poda + 8
    hrbet_visina = h + 8
    
    kosi = [
        {"Del": "Stranica", "Količina": 2, "Širina (mm)": g, "Višina (mm)": h},
        {"Del": "Strop / Pod", "Količina": 2, "Širina (mm)": g, "Višina (mm)": sirina_stropa_poda},
        {"Del": "Hrbet", "Količina": 1, "Širina (mm)": hrbet_sirina, "Višina (mm)": hrbet_visina}
    ]
    
    if el["Police"] > 0:
        polica_sirina = sirina_stropa_poda - 2
        polica_globina = g - 38
        kosi.append({
            "Del": "Police", 
            "Količina": el["Police"], 
            "Širina (mm)": polica_globina, 
            "Višina (mm)": polica_sirina
        })
        
    df = pd.DataFrame(kosi)
    st.dataframe(df, use_container_width=True)
