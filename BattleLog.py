# BattleLog.py

import streamlit as st
import pandas as pd

def run():
    st.title("⚔️ LLKK Battle Log")

    # Check if data from DataEntry exists
    if "llkk_data" in st.session_state:
        df = st.session_state["llkk_data"]

        st.success("✅ Data loaded from Data Entry.")
        st.markdown("### 📋 Submitted QC Data")
        st.dataframe(df)

        # Optional stats summary
        st.markdown("### 📊 Summary Statistics")
        with st.expander("View stats by Lab"):
            summary = df.groupby("Lab").agg({
                "CV (%)": ["mean", "min", "max"],
                "Ratio": ["mean", "min", "max"]
            }).round(2)
            st.dataframe(summary)

        st.info("🛠️ Coming soon: Apply Fadzly Algorithm to simulate performance battles.")

    else:
        st.error("🚫 No data found. Please enter data first in the Data Entry tab.")
