import streamlit as st
import pandas as pd

st.set_page_config(page_title="Champion", layout="wide", page_icon="👑")
st.title("👑 Champion of the Month")

if "llkk_data" not in st.session_state:
    st.warning("Please upload data in the Home page first.")
    st.stop()

# Placeholder logic for champion display (replace with actual logic)
st.image("lab_a.png", width=150)
st.markdown("### 🏆 Lab_A — Final Elo: **1524.1**")
st.success("🎉 Congratulations Lab_A! You are crowned this month’s Champion in Kingdom Kvalis.")

st.markdown(
    "<hr style='margin-top: 2rem; margin-bottom: 1rem;'>"
    "<div style='text-align: center; color: gray;'>"
    "© 2025 Lab Legend Kingdom Kvalis — Powered by MEQARE"
    "</div>",
    unsafe_allow_html=True
)
