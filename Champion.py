# Champion.py

import streamlit as st
import pandas as pd

# Page setup
st.set_page_config(page_title="Champion", layout="wide", page_icon="👑")
st.title("👑 LLKK Champion Board")

# Ensure data is available
if "llkk_data" not in st.session_state:
    st.warning("Please enter or upload data from the Home or Data Entry page.")
    st.stop()

df = st.session_state["llkk_data"]

# Check required columns
required_columns = {"Lab", "Parameter", "Level", "CV (%)", "n (QC)", "Working Days", "Month"}
if not required_columns.issubset(df.columns):
    st.error(f"Missing required columns. Required: {', '.join(required_columns)}")
    st.stop()

# Prepare data
df = df.copy()
df = df.dropna(subset=["CV (%)", "n (QC)", "Working Days"])

# Convert columns to numeric
df["CV (%)"] = pd.to_numeric(df["CV (%)"], errors="coerce")
df["n (QC)"] = pd.to_numeric(df["n (QC)"], errors="coerce")
df["Working Days"] = pd.to_numeric(df["Working Days"], errors="coerce")

# 🧠 Fadzly Algorithm: simplified score model
df["score"] = (100 - df["CV (%)"]) * df["n (QC)"].pow(0.5) * (df["Working Days"] / 30)

# 🏆 Leaderboard: total score per lab
lab_scores = df.groupby("Lab")["score"].sum().reset_index()
lab_scores["Rank"] = lab_scores["score"].rank(method="min", ascending=False).astype(int)
lab_scores = lab_scores.sort_values(by="Rank")

# Display leaderboard
st.subheader("🏅 LLKK Total Scores")
st.dataframe(lab_scores, use_container_width=True)

# Footer
st.markdown(
    "<hr style='margin-top: 2rem; margin-bottom: 1rem;'>"
    "<div style='text-align: center; color: gray;'>"
    "© 2025 Lab Legend Kingdom Kvalis — Powered by MEQARE"
    "</div>",
    unsafe_allow_html=True
)
