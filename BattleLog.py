# BattleLog.py

import streamlit as st
import pandas as pd

def run():
    st.title("⚔️ LLKK Battle Log")

    # Ensure user is logged in
    if "logged_in_lab" not in st.session_state:
        st.warning("Please log in from the sidebar to view battle logs.")
        st.stop()

    lab = st.session_state["logged_in_lab"]

    # Ensure data is available
    if "llkk_data" not in st.session_state:
        st.error("🚫 No data found. Please submit data through the Data Entry tab.")
        return

    df = st.session_state["llkk_data"]

    # ================================
    # 🔍 1. Logged-in Lab View
    # ================================
    st.markdown(f"### 🧾 `{lab}` Submission")
    lab_df = df[df["Lab"] == lab]

    if lab_df.empty:
        st.warning(f"⚠️ No data entries found yet for `{lab}`.")
    else:
        st.success(f"✅ Showing battle records for `{lab}`.")
        st.dataframe(lab_df)

        with st.expander("📊 Summary Stats"):
            summary = lab_df.groupby(["Parameter", "Level"]).agg({
                "CV (%)": ["mean", "min", "max"],
                "Ratio": ["mean", "min", "max"]
            }).round(2)
            st.dataframe(summary)

    # ================================
    # 🧩 2. All Labs Combined Preview
    # ================================
    st.markdown("### 🧩 All Labs Combined (for Battle Preview)")
    st.dataframe(df)

    # Optional combined summary
    with st.expander("📊 Overall Summary by Lab"):
        combined_summary = df.groupby("Lab").agg({
            "CV (%)": ["mean", "min", "max"],
            "Ratio": ["mean", "min", "max"]
        }).round(2)
        st.dataframe(combined_summary)

    st.info("💡 You're ready to apply the Fadzly Algorithm for full multi-lab battle simulation.")
