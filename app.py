import streamlit as st
import pandas as pd

# Naslov aplikacije v brskalniku
st.title("🪚 Mizarski Kalkulator in Krojni List")
st.write("Vnesite mere omare, program pa vam bo izračunal točen krojni list za utorjen hrbet (5 mm).")

# Vnosna polja v stranskem meniju
st.sidebar.header("Nastavitve elementa")
debelina = st.sidebar.number_input("Debelina materiala (mm)", value=18, step=1)
stevilo_polic = st.sidebar.slider("Število polic", min_value=0, max_value=10, value=3)
dodaj_vrata = st.sidebar.checkbox("Dodaj vrata", value=True)

# Glavna vnosna polja za mere
col1, col2, col3 = st.columns(3)
with col1:
    sirina = st.number_input("Širina omare (mm)", value=800, step=10)
with col2:
    visina = st.number_input("Višina omare (mm)", value=2000, step=10)
with col3:
    globina = st.number_input("Globina omare (mm)", value=500, step=10)

# Gumb za izračun
if st.button("Izračunaj krojni list", type="primary"):
    d = debelina
    kosi = []

    # 1. Stranici (polna višina in globina)
    kosi.append({"Del": "Stranica", "Količina": 2, "Širina (mm)": globina, "Dolžina/Višina (mm)": visina})

    # 2. Strop in pod (širina zmanjšana za obe stranici)
    sirina_kosa = sirina - (2 * d)
    kosi.append({"Del": "Strop / Pod", "Količina": 2, "Širina (mm)": globina, "Dolžina/Višina (mm)": sirina_kosa})

    # 3. Hrbtni del (HDF 5 mm v utor)
    sirina_hrbta = sirina - (2 * d) + 10  # z vštetim utorom
    visina_hrbta = visina + 10
    kosi.append({"Del": "Hrbtni del (HDF 5mm - v utor)", "Količina": 1, "Širina (mm)": sirina_hrbta, "Dolžina/Višina (mm)": visina_hrbta})

    # 4. Police (krajše zaradi zraka zadaj in prostora za hrbet)
    if stevilo_polic > 0:
        sirina_police = sirina - (2 * d) - 2  # 1mm zračnosti na vsako stran
        globina_police = globina - 20        # odmik zadaj za zrak/hrbet
        kosi.append({"Del": "Police", "Količina": stevilo_polic, "Širina (mm)": globina_police, "Dolžina/Višina (mm)": sirina_police})

    # 5. Vrata
    if dodaj_vrata:
        visina_vrat = visina - 4
        sirina_vrat = (sirina / 2) - 3 if sirina > 600 else sirina - 4
        strop_kosov_vrat = 2 if sirina > 600 else 1
        kosi.append({"Del": "Vrata", "Količina": strop_kosov_vrat, "Širina (mm)": sirina_vrat, "Dolžina/Višina (mm)": visina_vrat})

    # Izris rezultatov
    st.success("Izračun za utorjen hrbet je končan!")
    st.subheader("Seznam krojnih kosov:")
    
    df = pd.DataFrame(kosi)
    st.dataframe(df, use_container_width=True)
