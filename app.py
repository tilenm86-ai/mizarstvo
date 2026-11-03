import streamlit as st
import pandas as pd

st.title("🪚 Mizarski Kalkulator: Projektni Vmesnik")
st.write("Dodaj elemente v projekt z natančnimi nastavitvami hrbta v utor (falc), polic in omar.")

# --- 1. KORAK: IZBIRA PROJEKTA ---
st.sidebar.header("📁 Vrsta projekta")
vrsta_projekta = st.sidebar.selectbox("Kaj delamo?", ["Kuhinja", "Garderobna omara", "Kopalniški element", "Pisarniško pohištvo"])

# --- 2. KORAK: OSNOVNI VNOS ELEMENTA ---
st.sidebar.divider()
st.sidebar.header("➕ Dodaj omaro v projekt")
ime_elementa = st.sidebar.text_input("Naziv omare", value="Spodnja omarica 80")

tip_elementa = st.sidebar.selectbox(
    "Konstrukcija omare", 
    ["Omarica s policami in vrati", "Omarica samo s policami (brez vrat)", "Omarica samo z vrati", "Visoka omara / stolp"]
)

debelina = st.sidebar.number_input("Debelina materiala (mm)", value=18, step=1)

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

# --- 3. KORAK: NASTAVITVE TOLERANC IN HRBTA (FALC / UTOR) ---
st.sidebar.subheader("⚙️ Tolerance in hrbet za to omaro")
nacin_hrbta = st.sidebar.selectbox(
    "Vgradnja hrbta", 
    ["Prislonjen zadaj (brez utora)", "V utoru / falcu (stranice in strop/pod)"]
)

globina_utora = 6  # Privzeta globina utora v mm
if "utor" in nacin_hrbta:
    globina_utora = st.sidebar.slider("Globina utora / falca (mm)", min_value=4, max_value=10, value=6)

odmik_hrbta = st.sidebar.slider("Odmik stropa/poda zadaj (mm)", min_value=0, max_value=15, value=5, key="oh_in")
zracnost_polic_sirina = st.sidebar.slider("Zračnost police širina - skupaj (mm)", min_value=0, max_value=10, value=2, key="zp_in")
odmik_police_globina = st.sidebar.slider("Koliko je polica krajša od globine omare (mm)", min_value=10, max_value=50, value=25, key="op_in")

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
        "Odmik_Police_G": odmik_police_globina
    })
    st.sidebar.success(f"Dodano: {ime_elementa}")

# --- GLAVNI ZASLON ---
if "elements" not in st.session_state:
    st.session_state.elements = []

st.subheader(f"📋 Seznam omar za projekt: {vrsta_projekta}")

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
            n_h = el.get('Nacin_Hrbta', 'Prislonjen')
            
            st.write(f"**{i+1}. {naziv_p}** [{tip_p}] — Š: {s_p}, V: {v_p}, G: {g_p} | Police: {pol_p}, Vrata: {vr_p} | (Hrbet: {n_h})")
        with c2:
            if st.button("❌", key=f"del_{i}"):
                st.session_state.elements.pop(i)
                st.rerun()

    if st.button("🗑️ Počisti cel projekt"):
        st.session_state.elements = []
        st.rerun()

    st.divider()

    # --- 4. IZRAČUN ---
    if st.button("🧮 Izračunaj skupni krojni list", type="primary"):
        vsi_kosi = []
        for el in st.session_state.elements:
            d = el.get("Debelina", 18)
            s = el.get("Širina", 800)
            v = el.get("Visina", 720)
            g = el.get("Globina", 550)
            naziv = el.get("Naziv", "Element")
            st_polic = el.get("Police", 0)
            ima_v = el.get("Vrata", False)
            
            nacin_h = el.get("Nacin_Hrbta", "Prislonjen zadaj (brez utora)")
            g_utora = el.get("Globina_Utora", 6)
            oh = el.get("Odmik_Hrbta", 5)
            zp = el.get("Zracnost_Polic", 2)
            opg = el.get("Odmik_Police_G", 25)

            # 1. Stranici (vedno polne)
            vsi_kosi.append({"Omarica": naziv, "Del": "Stranica", "Količina": 2, "Širina (mm)": g, "Dolžina/Višina (mm)": v})
            
            # 2. Strop in pod (krajša zadaj za odmik hrbta)
            sirina_kosa = s - (2 * d)
            globina_stropa_poda = g - oh
            vsi_kosi.append({"Omarica": naziv, "Del": "Strop / Pod", "Količina": 2, "Širina (mm)": globina_stropa_poda, "Dolžina/Višina (mm)": sirina_kosa})
            
            # 3. Hrbtni del (MDF/HDF 5mm) - izračun glede na utor ali prislon
            if "utor" in nacin_h:
                # Če je hrbet v utoru (stranice + strop/pod), mu prištejemo globino utorov
                sirina_hrbta = s - (2 * d) + (2 * g_utora)
                visina_hrbta = v + (2 * g_utora)
            else:
                # Klasičen prislonjen hrbet (med stropom in podom)
                sirina_hrbta = s - (2 * d)
                visina_hrbta = v - (2 * d)
                
            vsi_kosi.append({"Omarica": naziv, "Del": "Hrbtni del (MDF/HDF 5mm v utor/prislon)", "Količina": 1, "Širina (mm)": sirina_hrbta, "Dolžina/Višina (mm)": visina_hrbta})
            
            # 4. Police
            if st_polic > 0:
                sirina_police = sirina_kosa - zp
                globina_police = g - opg
                vsi_kosi.append({"Omarica": naziv, "Del": "Police", "Količina": st_polic, "Širina (mm)": globina_police, "Dolžina/Višina (mm)": sirina_police})
            
            # 5. Vrata
            if ima_v:
                visina_vrat = v - 4
                sirina_vrat = (s / 2) - 3 if s > 600 else s - 4
                strop_kosov = 2 if s > 600 else 1
                vsi_kosi.append({"Omarica": naziv, "Del": "Vrata", "Količina": strop_kosov, "Širina (mm)": sirina_vrat, "Dolžina/Višina (mm)": visina_vrat})

        st.success("Krojni list uspešno izračunan z upoštevanjem utora za hrbet!")
        df_skupaj = pd.DataFrame(vsi_kosi)
        st.dataframe(df_skupaj, use_container_width=True)
else:
    st.info("V projektu še ni omar. Dodajte prvo omaro preko menija na levi.")
