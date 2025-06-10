import streamlit as st
import pandas as pd

# ✅ This must be the first Streamlit command
st.set_page_config(page_title="Champion", layout="wide", page_icon="👑")

st.title("👑 LLKK Champion Board")

# Check if results exist
if "fadzly_battles" not in st.session_state:
    st.warning("⚠️ Battle not simulated yet. Please run the simulation from the Admin tab.")
    st.stop()

# Load results
df = st.session_state["fadzly_battles"]

# Display table
st.subheader("🏅 Final Rankings (Elo + Bonus)")
st.dataframe(df, use_container_width=True)

# Show Champion details
champ_row = df.iloc[0]
st.markdown(f"""
<hr>
<h2 style='text-align: center;'>👑 <span style='color:gold'>{champ_row['Lab']}</span> is the Champion!</h2>
<h4 style='text-align: center;'>Final Elo: <code>{champ_row['Final Elo']}</code> | Total Score: <code>{champ_row['Total Score']}</code></h4>
<div style='text-align: center; font-size: 3rem;'>{champ_row['Medal']}</div>
<hr>
""", unsafe_allow_html=True)

# Footer
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "© 2025 Lab Legend Kingdom Kvalis — Powered by MEQARE"
    "</div>",
    unsafe_allow_html=True
)
