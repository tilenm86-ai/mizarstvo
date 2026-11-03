import streamlit as st
import pandas as pd

st.title("🪚 Mizarski Kalkulator: Celotna Kuhinja / Več Omar")
st.write("Dodajajte posamezne omarice v projekt. Aplikacija vam bo na koncu izračunala skupni krojni list za celotno naročilo.")

# Inicializacija seznama elementov v spominu
if "elements" not in st.session_state:
    st.session_state.elements = []

# Vnos v stranskem meniju za dodajanje nove omare
st.sidebar.header("➕ Dodaj omaro v projekt")
ime_elementa = st.sidebar.text_input("Naziv omare", value="Spodnja omarica 80")
tip_elementa = st.sidebar.selectbox("Tip", ["Spodnja omarica", "Viseča omarica", "Visoka omara"])

debelina = st.sidebar.number_input("Debelina materiala (mm)", value=18, step=1)
stevilo_polic = st.sidebar.slider("Število polic", min_value=0, max_value=10, value=1)
dodaj_vrata = st.sidebar.checkbox("Dodaj vrata", value=True)

col1, col2, col3 = st.sidebar.columns(3)
with col1:
    sirina = st.number_input("Širina (mm)", value=800, step=10)
with col2:
    visina = st.number_input("Višina (mm)", value=720, step=10)
with col3:
    globina = st.number_input("Globina (mm)", value=550, step=10)

if st.sidebar.button("💾 Shrani omaro v projekt"):
    st.session_state.elements.append({
        "Naziv": ime_elementa,
        "Tip": tip_elementa,
        "Širina": sirina,
        "Višina": visina,
        "Globina": globina,
        "Police": stevilo_polic,
        "Vrata": dodaj_vrata,
        "Debelina": debelina
    })
    st.sidebar.success(f"Dodano: {ime_elementa}")

# Prikaz trenutnih elementov v projektu
st.subheader("📋 Seznam omar v tem projektu")
if len(st.session_state.elements) > 0:
    for i, el in enumerate(st.session_state.elements):
        c1, c2 = st.columns([5, 1])
        with c1:
            st.write(f"**{i+1}. {el['Naziv']}** ({el['Tip']}) — Š: {el['Širina']} mm, V: {el['Višina']} mm, G: {el['Globina']} mm | Police: {el['Police']}, Vrata: {'Da' if el['Vrata'] else 'Ne'}")
        with c2:
            if st.button("❌", key=f"del_{i}"):
                st.session_state.elements.pop(i)
                st.rerun()

    if st.button("🗑️ Počisti cel projekt"):
        st.session_state.elements = []
        st.rerun()

    st.divider()

    # Gumb za skupni izračun
    if st.button("🧮 Izračunaj skupni krojni list za celo kuhinjo", type="primary"):
        vsi_kosi = []
        for el in st.session_state.elements:
            d = el["Debelina"]
            s = el["Širina"]
            v = el["Višina"]
            g = el["Globina"]
            naziv = el["Naziv"]

            # 1. Stranici
            vsi_kosi.append({"Omarica": naziv, "Del": "Stranica", "Količina": 2, "Širina (mm)": g, "Dolžina/Višina (mm)": v})
            
            # 2. Strop in pod
            sirina_kosa = s - (2 * d)
            vsi_kosi.append({"Omarica": naziv, "Del": "Strop / Pod", "Količina": 2, "Širina (mm)": g, "Dolžina/Višina (mm)": sirina_kosa})
            
            # 3. Hrbtni del (HDF 5mm v utor)
            vsi_kosi.append({"Omarica": naziv, "Del": "Hrbtni del (HDF 5mm - v utor)", "Količina": 1, "Širina (mm)": s - (2 * d) + 10, "Dolžina/Višina (mm)": v + 10})
            
            # 4. Police
            if el["Police"] > 0:
                vsi_kosi.append({"Omarica": naziv, "Del": "Police", "Količina": el["Police"], "Širina (mm)": g - 20, "Dolžina/Višina (mm)": s - (2 * d) - 2})
            
            # 5. Vrata
            if el["Vrata"]:
                visina_vrat = v - 4
                sirina_vrat = (s / 2) - 3 if s > 600 else s - 4
                strop_kosov = 2 if s > 600 else 1
                vsi_kosi.append({"Omarica": naziv, "Del": "Vrata", "Količina": strop_kosov, "Širina (mm)": sirina_vrat, "Dolžina/Višina (mm)": visina_vrat})

        st.success("Skupni krojni list uspešno izračunan!")
        df_skupaj = pd.DataFrame(vsi_kosi)
        st.dataframe(df_skupaj, use_container_width=True)
else:
    st.info("V projektu še ni omar. Uporabite nastavitve levo/zgoraj, da dodate prvo omaro.")
