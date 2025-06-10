# BattleLog.py

import streamlit as st
import pandas as pd
import numpy as np
import itertools

# --- EFLM Targets ---
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

    df["CV (%)"] = pd.to_numeric(df["CV (%)"], errors="coerce")
    df["Ratio"] = pd.to_numeric(df["Ratio"], errors="coerce")
    df = df.dropna(subset=["n (QC)", "Working Days"])

    ratings = {lab: 1500 for lab in df["Lab"].unique()}
    scores = {lab: 0 for lab in df["Lab"].unique()}
    K = 16
    battle_logs = []

    for (param, level, month), group in df.groupby(["Parameter", "Level", "Month"]):
        labs = group.to_dict("records")
        for lab1, lab2 in itertools.combinations(labs, 2):
            labA, labB = lab1["Lab"], lab2["Lab"]
            cvA, cvB = lab1.get("CV (%)"), lab2.get("CV (%)")
            rA, rB = lab1.get("Ratio"), lab2.get("Ratio")

            # Penalties
            penalty_A = 10 if pd.isna(cvA) or pd.isna(rA) else 0
            penalty_B = 10 if pd.isna(cvB) or pd.isna(rB) else 0

            # CV battle score
            if pd.isna(cvA) or pd.isna(cvB):
                cv_score_A = cv_score_B = 0.5
            elif abs(cvA - cvB) < 0.1:
                cv_score_A, cv_score_B = 0.5, 0.5
            elif cvA < cvB:
                cv_score_A, cv_score_B = 1, 0
            else:
                cv_score_A, cv_score_B = 0, 1

            # Bonuses
            bonus_A = 0
            bonus_B = 0
            if not pd.isna(rA) and rA >= 1.0:
                bonus_A += 5
            if not pd.isna(rB) and rB >= 1.0:
                bonus_B += 5
            if not pd.isna(cvA) and param in EFLM_TARGETS and cvA <= EFLM_TARGETS[param]:
                bonus_A += 2
            if not pd.isna(cvB) and param in EFLM_TARGETS and cvB <= EFLM_TARGETS[param]:
                bonus_B += 2

            final_A = cv_score_A + bonus_A - penalty_A
            final_B = cv_score_B + bonus_B - penalty_B
            scores[labA] += final_A
            scores[labB] += final_B

            # Elo update
            Ra, Rb = ratings[labA], ratings[labB]
            Ea = 1 / (1 + 10 ** ((Rb - Ra) / 400))
            Eb = 1 / (1 + 10 ** ((Ra - Rb) / 400))
            ratings[labA] += K * ((final_A > final_B) - Ea)
            ratings[labB] += K * ((final_B > final_A) - Eb)

            battle_logs.append({
                "Lab_A": labA,
                "Lab_B": labB,
                "Parameter": param,
                "Level": level,
                "Month": month,
                "CV_A": cvA,
                "CV_B": cvB,
                "Ratio_A": rA,
                "Ratio_B": rB,
                "Score_A": round(final_A, 2),
                "Score_B": round(final_B, 2),
                "Updated_Rating_A": round(ratings[labA], 1),
                "Updated_Rating_B": round(ratings[labB], 1)
            })

    rating_df = pd.DataFrame(sorted(ratings.items(), key=lambda x: -x[1]), columns=["Lab", "Final Elo"])
    rating_df["Total Score"] = rating_df["Lab"].map(scores)
    rating_df["Medal"] = ""
    if len(rating_df) >= 1: rating_df.loc[0, "Medal"] = "🥇"
    if len(rating_df) >= 2: rating_df.loc[1, "Medal"] = "🥈"
    if len(rating_df) >= 3: rating_df.loc[2, "Medal"] = "🥉"

    battle_df = pd.DataFrame(battle_logs)

    # Display results
    st.success("✅ Battle simulation completed.")
    st.markdown("### 🏆 Leaderboard")
    st.dataframe(rating_df)
    st.markdown("### 📜 Detailed Battle Log")
    st.dataframe(battle_df)

    # Save to session
    st.session_state["fadzly_battles"] = rating_df


# --- Main Entry Point ---
def run():
    st.title("⚔️ LLKK Battle Log")

    if "logged_in_lab" not in st.session_state:
        st.warning("Please log in to access this page.")
        st.stop()

    role = st.session_state.get("user_role", "lab")

    if "llkk_data" not in st.session_state:
        st.error("🚫 No data found. Please enter data in the Data Entry tab.")
        return

    df = st.session_state["llkk_data"]
    st.markdown("### 📊 Submitted Data")
    st.dataframe(df)

    if role == "admin":
        st.markdown("---")
        st.subheader("🛡️ Admin Control Panel")
        if st.button("🚀 Start Fadzly Battle Simulation"):
            simulate_fadzly_algorithm(df)
    else:
        st.info("🟢 Waiting for Admin to start the battle simulation.")
