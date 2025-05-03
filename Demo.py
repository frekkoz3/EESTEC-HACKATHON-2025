import streamlit as st
import time
import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


#--------------------------------------------------------------------------------
def calulate_SoC(Q_vec, delta_t, const_i, t_cycle):
    Soc = 1 + (const_i * t_cycle)/(Q_vec[0]*36000)

    for i in range(1, len(Q_vec) - 2):
        Soc = Soc + (const_i * t_cycle)/(Q_vec[i-1]*36000)
        print(Soc)
    
    actual_SoC = Soc + (const_i * delta_t)/(Q_vec[-1]*36000)

    return actual_SoC
#--------------------------------------------------------------------------------


# Inizializzazione session state
if 'soc' not in st.session_state:
    st.session_state.soc = 100
if 'soh' not in st.session_state:
    st.session_state.soh = 100
if 'charging_profile' not in st.session_state:
    st.session_state.charging_profile = 'Standard'


def update_SoC(csv_file):
    df = pd.read_csv(csv_file)


    voltages_history = df["Voltage"]
    voltages = []
    for voltage_h in voltages_history[:1]:
        voltage_h_no_chars = voltage_h.replace("[", "")
        voltage_h_no_chars = voltage_h_no_chars.replace("]", "")
        voltage = np.array([float(v.strip()) for v in voltage_h_no_chars.split()])
        voltages.append(voltage)

    avg_cycle_time = 0
    for serie in voltages:
        avg_cycle_time += len(serie)

    avg_cycle_time = avg_cycle_time / len(voltages)
    Q_vec = df["discharge_capacities"].to_list()
    my_SoC = calulate_SoC(Q_vec, 100000, -1, avg_cycle_time)


    st.session_state.soc = round(my_SoC*100, 2)

def update_SoH(SoH=100):
    st.session_state.soh = SoH


# Titolo
st.title("Monitoraggio Stato Batteria")

# Stato per controllare la visualizzazione
if "show_uploader" not in st.session_state:
    st.session_state.show_uploader = False

# Pulsante che attiva l'uploader
if st.button("📁 Carica dati batteria"):
    st.session_state.show_uploader = True

# Se il pulsante è stato premuto, mostra il file uploader
if st.session_state.show_uploader:
    uploaded_file = st.file_uploader("Seleziona un file", type=["csv", "txt", "json"])
    
    if uploaded_file is not None:
        update_SoC(uploaded_file)
        update_SoH(0.989 * 100)
        # Qui puoi chiamare le tue funzioni: update_SoC(data), ecc.
        st.success("Dati caricati con successo!")
        st.session_state.show_uploader = False

# Colonne affiancate
col1, col2 = st.columns(2)

with col1:
    # Indicatore SoC (barra + numero)
    soc = int(st.session_state.soc)
    st.subheader("State of Charge (SoC) :")
    st.subheader(f"🔋 {st.session_state.soc:.1f} %")
    st.progress(soc)

with col2:
    # Indicatore SoH (numero colorato)
    soh_color = "green" if st.session_state.soh > 80 else "orange" if st.session_state.soh > 60 else "red"
    st.subheader("State of Health (SoH)")
    st.markdown(
        f"""
        <div style='text-align:center;'>
            <div style='color:{soh_color}; font-size:24px;'>❤️ {st.session_state.soh:.1f}%</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# Spazio extra
st.markdown("<br><br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 6, 1])

with col2:
    # Titolo centrato
    st.markdown(
        "<h3 style='text-align:center;'>Seleziona il profilo di carica:</h3>",
        unsafe_allow_html=True
    )

    # Radio centrato con un po’ di CSS
    st.markdown("""
        <style>
        [data-testid="stRadio"] > div {
            display: flex;
            justify-content: center;
        }
        </style>
    """, unsafe_allow_html=True)
    profile = st.radio("", ["Quick", "Balanced", "Long Life"])
    st.session_state.charging_profile = profile

    # Messaggio e lista centrati
    if profile == "Quick":
        st.markdown("⚡ **Ricarica veloce selezionata**: priorità alla velocità, possibile stress sulla batteria.", unsafe_allow_html=True)
        st.markdown(
            """
            <div style='text-align:center;'>
              <ul style='display:inline-block; text-align:left;'>
                <li>Charge at 0.59 A for 15 minutes</li>
                <li>Charge at 2 A until 4.2V</li>
                <li>Hold at 4.2V until C/100</li>
              </ul>
            </div>
            """,
            unsafe_allow_html=True
        )
    elif profile == "Balanced":
        st.markdown("🔋 **Profilo bilanciato selezionato**: compromesso tra velocità e durata.", unsafe_allow_html=True)
        st.markdown(
            """
            <div style='text-align:center;'>
              <ul style='display:inline-block; text-align:left;'>
                <li>Charge at 0.5 A for 30 minutes</li>
                <li>Rest 30 minutes</li>
                <li>Charge at 2 A until 4.2V</li>
                <li>Hold at 4.2V until C/100</li>
              </ul>
            </div>
            """,
            unsafe_allow_html=True
        )
    elif profile == "Long Life":
        st.markdown("🌱 **Lunga durata selezionata**: priorità alla salute della batteria nel lungo termine.", unsafe_allow_html=True)
        st.markdown(
            """
            <div style='text-align:center;'>
              <ul style='display:inline-block; text-align:left;'>
                <li>Charge at 0.5 A for 15 minutes</li>
                <li>Charge at 1 A for 15 minutes</li>
                <li>Charge at 1.5 A until 4.2V</li>
                <li>Hold at 4.2V until C/20</li>
              </ul>
            </div>
            """,
            unsafe_allow_html=True
        )
# # Scelta profilo di carica
# st.subheader("Seleziona il profilo di carica:")
# profile = st.radio(
#     ["Quick", "Balanced", "Long Life"]
# )
# st.session_state.charging_profile = profile

# if profile == "Quick":
#     st.markdown("⚡ **Ricarica veloce selezionata**: priorità alla velocità, possibile stress sulla batteria.")
#     st.markdown(
#     """
#     - Charge at 0.59 A for 15 minutes
#     - Charge at 2 A until 4.2V
#     - Hold at 4.2V until C/100
#     """
#     )
# elif profile == "Balanced":
#     st.markdown("🔋 **Profilo bilanciato selezionato**: compromesso tra velocità e durata.")
#     st.markdown(
#     """
#     - Charge at 0.5 A for 30 minutes
#     - Rest 30 minutes
#     - Charge at 2 A until 4.2V
#     - Hold at 4.2V until C/100
#     """
#     )
# elif profile == "Long Life":
#     st.markdown("🌱 **Lunga durata selezionata**: priorità alla salute della batteria nel lungo termine.")
#     st.markdown(
#     """
#     - Charge at 0.5 A for 15 minutes
#     - Charge at 1 A for 15 minutes
#     - Charge at 1.5 A until 4.2V
#     - Hold at 4.2V until C/20
#     """
#     )

st.markdown("""
<style>
    .stDivider {
        background-color: #ff4b4b;
        height: 2px;
    }
</style>
""", unsafe_allow_html=True)
