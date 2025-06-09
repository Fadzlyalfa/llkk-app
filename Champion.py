import streamlit as st
import pandas as pd

def run():
    st.title("🏆 LLKK Champion Board")

    if "llkk_data" not in st.session_state:
        st.warning("Please upload data in the Home page first.")
        return

    df = st.session_state.llkk_data.copy()

    # Standardize column names
    df.columns = df.columns.str.strip().str.title()

    if not {"Lab", "Parameter", "Level", "Cv"}.issubset(df.columns):
        st.error("Missing required columns in uploaded data.")
        return

    # Calculate average CV per Lab
    df["Param_Level"] = df["Parameter"] + "_" + df["Level"]
    avg_cv = df.groupby("Lab")["Cv"].mean().reset_index()
    avg_cv.columns = ["Lab", "Average_CV"]
    avg_cv["Rank"] = avg_cv["Average_CV"].rank(method="min", ascending=True).astype(int)
    champion_df = avg_cv.sort_values(by="Average_CV")

    st.dataframe(champion_df, use_container_width=True)

    st.markdown(
        "<hr style='margin-top: 2rem; margin-bottom: 1rem;'>"
        "<div style='text-align: center; color: gray;'>"
        "© 2025 Lab Legend Kingdom Kvalis — Powered by MEQARE"
        "</div>",
        unsafe_allow_html=True
    )
