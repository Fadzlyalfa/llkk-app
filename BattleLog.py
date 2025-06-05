import streamlit as st
import pandas as pd

def run():
    st.set_page_config(page_title="Battle Log", layout="wide", page_icon="⚔️")
    st.title("📜 LLKK Battle Log")

    if "llkk_data" not in st.session_state:
        st.warning("Please upload data in the Home page first.")
        st.stop()

    # Placeholder battle logic
    battle_log = pd.DataFrame({
        "Parameter": ["Glu_L1", "Cre_L1"],
        "Lab_1": ["Lab_A", "Lab_B"],
        "Lab_2": ["Lab_B", "Lab_C"],
        "CV_1": [1.2, 1.9],
        "CV_2": [1.4, 2.1],
        "Winner": ["Lab_A", "Lab_B"],
        "Δ_Lab_1": [+8.1, +5.4],
        "Δ_Lab_2": [-8.1, -5.4]
    })

    st.dataframe(battle_log, use_container_width=True)

    st.markdown(
        "<hr style='margin-top: 2rem; margin-bottom: 1rem;'>"
        "<div style='text-align: center; color: gray;'>"
        "© 2025 Lab Legend Kingdom Kvalis — Powered by MEQARE"
        "</div>",
        unsafe_allow_html=True
    )
