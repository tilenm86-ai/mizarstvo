import streamlit as st
import pandas as pd

st.title("🪚 Mizarski Kalkulator: Projektni Vmesnik")
st.write("Izberi vrsto projekta, nastavi tolerance in dodajaj elemente.")

# --- 1. KORAK: IZBIRA PROJEKTA ---
st.sidebar.header("📁 Vrsta projekta")
vrsta_projekta = st.sidebar.selectbox("Kaj delamo?", ["Kuhinja", "Garderobna omara", "Kopalniški element", "Pisarniško pohištvo"])

# --- 2. KORAK: NASTAVITVE TOLERANC ---
st.sidebar.header("⚙️ Nastavitve toleranc (mm)")
odmik_hrbta = st.sidebar.slider("Odmik stropa/poda zadaj za hrbet", min_value=0, max_value=15, value=5)
zracnost_polic_sirina = st.sidebar.slider("Zračnost police širina (skupaj)", min_value=0, max_value=5, value=2)
odmik_police_globina = st.sidebar.slider("Odmik police od zadaj", min_value=10, max_value=50, value=20)

# --- 3. KORAK: DODAJANJE ELEMENTA ---
st.sidebar.divider()
st.sidebar.header("➕ Dodaj element v projekt")
ime_elementa = st.sidebar.text_input("Naziv elementa", value="Spodnja omarica 80")

# Izbira podtipa glede na to, kaj element vsebuje
tip_elementa = st.sidebar.selectbox(
    "Konstrukcija elementa", 
    ["Omarica s policami in vrati", "Omarica samo s policami (brez vrat)", "Omarica samo z vrati", "Visoka omara / stolp"]
)

debelina = st.sidebar.number_input("Debelina materiala (mm)", value=18, step=1)

# Dinamično prilagajanje glede na izbran tip
ima_police = "s policami" in tip_elementa
ima_vrata = "z vrati" in tip_elementa

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

if st.sidebar.button("💾 Shrani element v projekt"):
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
        "Odmik_Hrbta": odmik_hrbta,
        "Zracnost_Polic": zracnost_polic_sirina,
        "Odmik_Police_G": odmik_police_globina
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
            tip_p = el.get('Tip', 'Omarica')
            s_p = el.get('Širina', 0)
            v_p = el.get('Višina', 0)
            g_p = el.get('Globina', 0)
            pol_p = el.get('Police', 0)
            vr_p = 'Da' if el.get('Vrata', False) else 'Ne'
            
            st.write(f"**{i+1}. {naziv_p}** [{tip_p}] — Š: {s_p} mm, V: {v_p} mm, G: {g_p} mm | Police: {pol_p}, Vrata: {vr_p}")
        with c2:
            if st.button("❌", key=f"del_{i}"):
                st.session_state.elements.pop(i)
                st.rerun()

    if st.button("🗑️ Počisti cel projekt"):
        st.session_state.elements = []
        st.rerun()

    st.divider()

    if st.button("🧮 Izračunaj skupni krojni list", type="primary"):
        vsi_kosi = []
        for el in st.session_state.elements:
            d = el.get("Debelina", 18)
            s = el.get("Širina", 800)
            v = el.get("Višina", 720)
            g = el.get("Globina", 550)
            oh = el.get("Odmik_Hrbta", 5)
            zp = el.get("Zracnost_Polic", 2)
            opg = el.get("Odmik_Police_G", 20)
            naziv = el.get("Naziv", "Element")
            st_polic = el.get("Police", 0)
            ima_v = el.get("Vrata", False)

            # 1. Stranici (vedno polne)
            vsi_kosi.append({"Element": naziv, "Del": "Stranica", "Količina": 2, "Širina (mm)": g, "Dolžina/Višina (mm)": v})
            
            # 2. Strop in pod (krajša zadaj za odmik hrbta)
            sirina_kosa = s - (2 * d)
            globina_stropa_poda = g - oh
            vsi_kosi.append({"Element": naziv, "Del": "Strop / Pod", "Količina": 2, "Širina (mm)": globina_stropa_poda, "Dolžina/Višina (mm)": sirina_kosa})
            
            # 3. Hrbtni del (MDF/HDF 5mm)
            sirina_hrbta = s - (2 * d)
            visina_hrbta = v - (2 * d)
            vsi_kosi.append({"Element": naziv, "Del": "Hrbtni del (MDF/HDF 5mm)", "Količina": 1, "Širina (mm)": sirina_hrbta, "Dolžina/Višina (mm)": visina_hrbta})
            
            # 4. Police (samo če jih element ima)
            if st_polic > 0:
                sirina_police = sirina_kosa - zp
                globina_police = g - opg
                vsi_kosi.append({"Element": naziv, "Del": "Police", "Količina": st_polic, "Širina (mm)": globina_police, "Dolžina/Višina (mm)": sirina_police})
            
            # 5. Vrata (samo če jih element ima)
            if ima_v:
                visina_vrat = v - 4
                sirina_vrat = (s / 2) - 3 if s > 600 else s - 4
                strop_kosov = 2 if s > 600 else 1
                vsi_kosi.append({"Element": naziv, "Del": "Vrata", "Količina": strop_kosov, "Širina (mm)": sirina_vrat, "Dolžina/Višina (mm)": visina_vrat})

        st.success("Krojni list uspešno izračunan glede na izbrane tipe elementov!")
        df_skupaj = pd.DataFrame(vsi_kosi)
        st.dataframe(df_skupaj, use_container_width=True)
else:
    st.info("V projektu še ni elementov. Izberite nastavitve v meniju levo in dodajte prvi kos.")
