import streamlit as st
import pandas as pd

def run():
    st.title("⚔️ LLKK Battle Log")

    required_columns = {"Level", "Cv", "Ratio", "Parameter", "Lab", "Month"}
    if "llkk_data" not in st.session_state:
        st.error("No data found. Please enter data first in Home or Data Entry.")
        return

    df = st.session_state["llkk_data"]
    if not required_columns.issubset(df.columns):
        st.error("Missing required columns. Required: Level, Cv, Ratio, Parameter, Lab, Month")
        return

    # Example placeholder battle logic:
    st.dataframe(df.sort_values(by=["Parameter", "Level"]), use_container_width=True)
