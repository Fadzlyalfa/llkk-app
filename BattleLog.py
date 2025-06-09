# BattleLog.py

import streamlit as st
import pandas as pd
import numpy as np
import itertools

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

    df = st.session_state["llkk_data"].copy()

    # Show current lab data
    st.markdown(f"### 📎 `{lab}` Submission")
    lab_df = df[df["Lab"] == lab]
    st.dataframe(lab_df)

    # Show all data
    st.markdown("### 🧹 All Labs Combined")
    st.dataframe(df)

    if role == "admin":
        st.markdown("---")
        st.subheader("🛡️ Admin Control Panel")
        if st.button("🛡️ Start Battle Simulation"):
            simulate_fadzly_algorithm(df)
    else:
        st.info("🟢 Awaiting admin to start the battle.")

# --- EFLM Targets (hardcoded as per user doc) ---
EFLM_TARGETS = {
    "Albumin": 2.1,
    "ALT": 6.0,
    "ALP": 5.4,
    "AST": 5.3,
    "Bilirubin": 8.6,
    "Cholesterol": 2.9,
    "CK": 4.5,
    "Creatinine": 3.4,
    "GGT": 7.7,
    "Glucose": 2.9,
    "HDL Cholesterol": 4.0,
    "LDH": 4.9,
    "Potassium": 1.8,
    "Sodium": 0.9,
    "Total Protein": 2.0,
    "Urea": 3.9,
    "Uric Acid": 3.3
}

def simulate_fadzly_algorithm(df):
    st.subheader("🏁 Fadzly Battle Simulation")

    df = df.dropna(subset=["CV (%)", "Ratio", "n (QC)", "Working Days"])
    df["CV (%)"] = pd.to_numeric(df["CV (%)"], errors="coerce")
    df["Ratio"] = pd.to_numeric(df["Ratio"], errors="coerce")

    # Initialize rating dictionary
    ratings = {lab: 1500 for lab in df["Lab"].unique()}
    K = 16

    battle_logs = []

    for (param, level, month), group in df.groupby(["Parameter", "Level", "Month"]):
        labs = group.to_dict("records")
        for lab1, lab2 in itertools.combinations(labs, 2):
            labA = lab1["Lab"]
            labB = lab2["Lab"]
            cvA, cvB = lab1["CV (%)"], lab2["CV (%)"]
            rA, rB = lab1["Ratio"], lab2["Ratio"]

            # --- CV Scoring ---
            if abs(cvA - cvB) < 0.1:
                cv_score_A, cv_score_B = 0.5, 0.5
            elif cvA < cvB:
                cv_score_A, cv_score_B = 1, 0
            else:
                cv_score_A, cv_score_B = 0, 1

            # --- Ratio Scoring ---
            if abs(rA - rB) < 0.05:
                ratio_score_A, ratio_score_B = 0.5, 0.5
            else:
                closer_to_1 = lambda x: abs(x - 1)
                if closer_to_1(rA) < closer_to_1(rB):
                    ratio_score_A, ratio_score_B = 1, 0
                else:
                    ratio_score_A, ratio_score_B = 0, 1

            final_A = (cv_score_A + ratio_score_A) / 2
            final_B = (cv_score_B + ratio_score_B) / 2

            # --- Elo Update ---
            Ra, Rb = ratings[labA], ratings[labB]
            Ea = 1 / (1 + 10 ** ((Rb - Ra) / 400))
            Eb = 1 / (1 + 10 ** ((Ra - Rb) / 400))
            ratings[labA] += K * (final_A - Ea)
            ratings[labB] += K * (final_B - Eb)

            # --- Log ---
            battle_logs.append({
                "Lab_A": labA,
                "Lab_B": labB,
                "Parameter": param,
                "Level": level,
                "Month": month,
                "Score_A": round(final_A, 2),
                "Score_B": round(final_B, 2),
                "Updated_Rating_A": round(ratings[labA], 1),
                "Updated_Rating_B": round(ratings[labB], 1)
            })

    battle_df = pd.DataFrame(battle_logs)
    rating_df = pd.DataFrame(sorted(ratings.items(), key=lambda x: -x[1]), columns=["Lab", "Final Rating"])

    st.success("✅ Battle simulation completed with Elo updates.")
    st.dataframe(rating_df)
    st.markdown("---")
    st.markdown("#### 🔹 Detailed Battle Log")
    st.dataframe(battle_df)

    st.session_state["fadzly_battles"] = rating_df
