import streamlit as st
import pandas as pd
import numpy as np

# Dictionary of EFLM target CVs (%), aligned with LLKK parameters
EFLM_CV = {
    "Albumin": 1.9,
    "ALT": 7.2,
    "AST": 6.4,
    "Bilirubin": 8.6,
    "Cholesterol": 3.6,
    "Creatinine": 4.3,
    "Direct Bilirubin": 14.8,
    "Glucose": 2.9,
    "HDL Cholesterol": 5.1,
    "LDL Cholesterol": 4.1,
    "Potassium": 1.8,
    "Sodium": 0.8,
    "Total Protein": 2.0,
    "Triglyceride": 4.6,
    "Urea": 2.7,
    "Uric Acid": 4.3
}

def run():
    st.title("⚔️ LLKK Battle Log")

    if "logged_in_lab" not in st.session_state:
        st.warning("Please log in from the sidebar to view battle logs.")
        st.stop()

    lab = st.session_state["logged_in_lab"]
    role = st.session_state.get("user_role", "lab")

    if "llkk_data" not in st.session_state:
        st.error("🚫 No data found. Please submit data through the Data Entry tab.")
        return

    df = st.session_state["llkk_data"]

    # Section 1 — Individual Lab View
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

    # Section 2 — Combined Preview
    st.markdown("### 🧩 All Labs Combined (for Battle Preview)")
    st.dataframe(df)

    with st.expander("📊 Overall Summary by Lab"):
        combined_summary = df.groupby("Lab").agg({
            "CV (%)": ["mean", "min", "max"],
            "Ratio": ["mean", "min", "max"]
        }).round(2)
        st.dataframe(combined_summary)

    # Section 3 — Admin Control Panel
    if role == "admin":
        st.markdown("---")
        st.subheader("🛡️ Admin Control Panel")
        if st.button("🛡️ Start Battle"):
            simulate_battles(df)
    else:
        st.info("🟢 You have entered the battlefield. Awaiting admin to start the simulation.")

# Core Simulation Logic (AF = Fadzly Algorithm)
def simulate_battles(df):
    st.subheader("🏁 Battle Results")

    df = df.dropna(subset=["CV (%)", "n (QC)", "Working Days"])
    df["CV (%)"] = pd.to_numeric(df["CV (%)"], errors="coerce")
    df["n (QC)"] = pd.to_numeric(df["n (QC)"], errors="coerce")
    df["Working Days"] = pd.to_numeric(df["Working Days"], errors="coerce")

    # Step 1: Base score
    df["BaseScore"] = (100 - df["CV (%)"]) * df["n (QC)"].pow(0.5) * (df["Working Days"] / 30)

    # Step 2: Bonus
    df["Bonus"] = 0
    df["Bonus"] += np.where(df["Ratio"] >= 1.0, 5, 0)
    df["Bonus"] += df.apply(lambda row: 2 if row["Parameter"] in EFLM_CV and row["CV (%)"] <= EFLM_CV[row["Parameter"]] else 0, axis=1)

    # Step 3: Penalty
    df["Penalty"] = np.where(df[["Ratio", "CV (%)"]].isna().any(axis=1), -10, 0)

    # Step 4: Total Score
    df["TotalScore"] = df["BaseScore"] + df["Bonus"] + df["Penalty"]

    # Step 5: Battle ranking
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
                "CV (%)": row["CV (%)"],
                "Ratio": row["Ratio"],
                "Base": round(row["BaseScore"], 2),
                "Bonus": row["Bonus"],
                "Penalty": row["Penalty"],
                "Total Score": round(row["TotalScore"], 2),
                "Rank": row["Rank"],
                "Medal": row["Medal"]
            })

    if battle_results:
        battle_df = pd.DataFrame(battle_results)
        st.session_state["fadzly_battles"] = battle_df
        st.success("✅ Battle simulation completed using Fadzly Algorithm!")
        st.dataframe(battle_df)
    else:
        st.info("🟢 You have entered the battlefield. Awaiting more labs for match-up.")
