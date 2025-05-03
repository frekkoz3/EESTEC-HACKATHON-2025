import streamlit as st

# Configurazione della pagina
st.set_page_config(page_title="Monitoraggio Stato Batteria", layout="centered")

# Titolo
st.title("Monitoraggio Stato Batteria")

# Creazione di due colonne per SoC e SoH
col1, col2 = st.columns(2)

# State of Charge (SoC)
with col1:
    st.subheader("State of Charge (SoC)")
    st.metric(label="", value="32%")

# State of Health (SoH)
with col2:
    st.subheader("State of Health (SoH)")
    st.metric(label="", value="70%")

# Selettore del profilo di carica
st.subheader("Seleziona il profilo di carica:")
profile = st.radio(
    "",
    options=["Lenta", "Standard", "Veloce"],
    index=1,  # Seleziona "Standard" di default
    label_visibility="collapsed"
)

# Stile aggiuntivo per migliorare l'aspetto
st.markdown("""
<style>
    .stMetric {
        text-align: center;
    }
    .stMetric label {
        font-size: 1.2rem;
    }
    .stMetric value {
        font-size: 2.5rem;
    }
    .stRadio > div {
        flex-direction: row;
        gap: 2rem;
    }
</style>
""", unsafe_allow_html=True)