# DataEntry.py

import streamlit as st
import pandas as pd
import numpy as np

def run():
    st.title("📋 LLKK Direct Data Entry")

    # Ensure login
    if "logged_in_lab" not in st.session_state:
        st.warning("Please log in from the sidebar to access data entry.")
        st.stop()

    # 🧹 Reset button in sidebar
    st.sidebar.markdown("### 🧹 Data Control")
    if st.sidebar.button("Reset All Data"):
        if "llkk_data" in st.session_state:
            del st.session_state["llkk_data"]
            st.success("✅ All LLKK data has been cleared.")
            st.rerun()

    lab = st.session_state["logged_in_lab"]
    parameters = ["Glucose", "Creatinine", "Cholesterol"]
    levels = ["L1", "L2"]
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    num_rows = st.number_input("🔢 How many entries to input?", 
                               min_value=1, max_value=50, value=5, step=1)

    input_data = []
    st.subheader(f"📝 Enter Data for: :green[{lab}]")

    headers = st.columns(7)
    headers[0].markdown("**Parameter**")
    headers[1].markdown("**Level**")
    headers[2].markdown("**Month**")
    headers[3].markdown("**CV (%)**")
    headers[4].markdown("**n (QC runs)**")
    headers[5].markdown("**Working Days**")
    headers[6].markdown("**Ratio**")

    for i in range(num_rows):
        cols = st.columns(7)
        parameter = cols[0].selectbox("", parameters, key=f"param_{i}")
        level = cols[1].selectbox("", levels, key=f"level_{i}")
        month = cols[2].selectbox("", months, key=f"month_{i}")
        cv = cols[3].number_input("", min_value=0.0, max_value=100.0, key=f"cv_{i}")
        n_qc = cols[4].number_input("", min_value=0, max_value=100, key=f"n_{i}")
        working_days = cols[5].number_input("", min_value=1, max_value=31, key=f"wd_{i}")
        ratio = round(n_qc / working_days, 2) if n_qc > 0 and working_days > 0 else 0.0
        cols[6].number_input("", value=ratio, disabled=True, key=f"ratio_{i}")

        input_data.append({
            "Lab": lab,
            "Parameter": parameter,
            "Level": level,
            "Month": month,
            "CV (%)": cv,
            "n (QC)": n_qc,
            "Working Days": working_days,
            "Ratio": ratio
        })

    df = pd.DataFrame(input_data)
    st.subheader("📊 Preview of Entered Data")
    st.dataframe(df)

    # Deduplication logic
    if "llkk_data" in st.session_state:
        existing = st.session_state["llkk_data"]
        combined = pd.concat([existing, df], ignore_index=True)
        combined = combined.drop_duplicates(subset=["Lab", "Parameter", "Level", "Month", "CV (%)", "n (QC)", "Working Days"])
        st.session_state["llkk_data"] = combined
    else:
        st.session_state["llkk_data"] = df

    # CSV export
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download CSV", csv, "llkk_data_entry.csv", "text/csv")

    # ⚔️ Submit to Battle
    if st.button("⚔️ Submit to Battle"):
        simulate_battles(st.session_state["llkk_data"])

# 🔁 Battle logic with scoring, bonuses, penalties, and medals
def simulate_battles(df):
    st.subheader("🏁 Simulated Battle Results")

    df = df.dropna(subset=["CV (%)", "n (QC)", "Working Days"])
    df["CV (%)"] = pd.to_numeric(df["CV (%)"], errors="coerce")
    df["n (QC)"] = pd.to_numeric(df["n (QC)"], errors="coerce")
    df["Working Days"] = pd.to_numeric(df["Working Days"], errors="coerce")

    df["BaseScore"] = (100 - df["CV (%)"]) * df["n (QC)"].pow(0.5) * (df["Working Days"] / 30)
    df["Bonus"] = df["Ratio"].apply(lambda x: 5 if x >= 1.0 else 0)
    df["Penalty"] = df[["Ratio", "CV (%)"]].isna().any(axis=1).astype(int) * -10
    df["TotalScore"] = df["BaseScore"] + df["Bonus"] + df["Penalty"]

    battle_results = []
    grouped = df.groupby(["Parameter", "Level", "Month"])
    for (param, level, month), group in grouped:
        valid = group.dropna(subset=["TotalScore"])
        if valid["Lab"].nunique() < 2:
            continue
        ranked = valid.sort_values("TotalScore", ascending=False).reset_index(drop=True)
        ranked["Rank"] = ranked["TotalScore"].rank(method="min", ascending=False).astype(int)
        ranked["Medal"] = ranked["Rank"].map({1: "🥇", 2: "🥈", 3: "🥉"})

        for _, row in ranked.iterrows():
            battle_results.append({
                "Lab": row["Lab"],
                "Parameter": param,
                "Level": level,
                "Month": month,
                "Total Score": round(row["TotalScore"], 2),
                "Rank": row["Rank"],
                "Medal": row.get("Medal", "")
            })

    if battle_results:
        battle_df = pd.DataFrame(battle_results)
        st.session_state["fadzly_battles"] = battle_df
        st.success("✅ Battle results submitted and saved!")
        st.dataframe(battle_df)
    else:
        st.warning("⚠️ No valid battles found. Need at least 2 labs per parameter/level/month.")
