import streamlit as st
import pandas as pd

# Set page configuration
st.set_page_config(page_title="Champion", layout="wide", page_icon="👑")

# Title
st.title("👑 LLKK Champion Board")

# Check for data in session state
if "llkk_data" not in st.session_state:
    st.warning("Please enter or upload data from the Home or Data Entry page.")
    st.stop()

df = st.session_state["llkk_data"]

required_columns = {"Lab", "Parameter", "Level", "CV", "n", "working_days", "Month"}
if not required_columns.issubset(df.columns):
    st.error(f"Missing required columns. Required: {', '.join(required_columns)}")
    st.stop()

# Preprocessing
df = df.copy()
df = df.dropna(subset=["CV", "n", "working_days"])
df["CV"] = pd.to_numeric(df["CV"], errors="coerce")
df["n"] = pd.to_numeric(df["n"], errors="coerce")
df["working_days"] = pd.to_numeric(df["working_days"], errors="coerce")

# Calculate total score using a simplified Elo-inspired Fadzly algorithm
# Score = (100 - CV) * sqrt(n) * (working_days / 30)
df["score"] = (100 - df["CV"]) * df["n"].pow(0.5) * (df["working_days"] / 30)

# Sum score per lab
lab_scores = df.groupby("Lab")["score"].sum().reset_index()
lab_scores["Rank"] = lab_scores["score"].rank(method="min", ascending=False).astype(int)
lab_scores = lab_scores.sort_values(by="Rank")

# Display
st.dataframe(lab_scores, use_container_width=True)

# Footer
st.markdown(
    "<hr style='margin-top: 2rem; margin-bottom: 1rem;'>"
    "<div style='text-align: center; color: gray;'>"
    "© 2025 Lab Legend Kingdom Kvalis — Powered by MEQARE"
    "</div>",
    unsafe_allow_html=True
)
