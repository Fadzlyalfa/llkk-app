import streamlit as st
import pandas as pd
import numpy as np
import itertools
import os
from pathlib import Path
import glob

# --- EFLM Targets ---
EFLM_TARGETS = {
    "Albumin": 2.1, "ALT": 6.0, "ALP": 5.4, "AST": 5.3, "Bilirubin": 8.6,
    "Cholesterol": 2.9, "CK": 4.5, "Creatinine": 3.4, "GGT": 7.7, "Glucose": 2.9,
    "HDL Cholesterol": 4.0, "LDL Cholesterol": 4.9, "Potassium": 1.8, "Sodium": 0.9,
    "Total Protein": 2.0, "Urea": 3.9, "Uric Acid": 3.3
}

def simulate_fadzly_algorithm(df):
    st.subheader("\U0001F3C1 Fadzly Battle Simulation")

    df["CV (%)"] = pd.to_numeric(df["CV (%)"], errors="coerce")
    df["Ratio"] = pd.to_numeric(df["Ratio"], errors="coerce")
    df = df.dropna(subset=["n (QC)", "Working Days"])

    if "elo_history" not in st.session_state:
        st.session_state["elo_history"] = {}

    ratings = st.session_state["elo_history"].copy()
    param_level_scores = {}
    K = 16
    battle_logs = []
    rating_progression = []

    # 🧩 Penalize missing submissions
    all_labs = df["Lab"].unique().tolist()
    all_params = df["Parameter"].unique().tolist()
    all_levels = df["Level"].unique().tolist()
    all_months = df["Month"].unique().tolist()

    expected_combinations = list(itertools.product(all_labs, all_params, all_levels, all_months))
    actual_submissions = set(tuple(row) for row in df[["Lab", "Parameter", "Level", "Month"]].drop_duplicates().to_numpy())

    for lab, param, level, month in expected_combinations:
        if (lab, param, level, month) not in actual_submissions:
            key = f"{lab}_{param}_{level}"
            if key not in ratings:
                ratings[key] = 1500
            if key not in param_level_scores:
                param_level_scores[key] = 0
            ratings[key] -= 10
            param_level_scores[key] += ratings[key]

    # ⚔️ Battle loop
    for (param, level, month), group in df.groupby(["Parameter", "Level", "Month"]):
        labs = group.to_dict("records")
        key_prefix = f"{param}_{level}"

        for lab in group["Lab"].unique():
            lab_key = f"{lab}_{key_prefix}"
            if lab_key not in ratings:
                ratings[lab_key] = 1500
            if lab_key not in param_level_scores:
                param_level_scores[lab_key] = 0

        for lab1, lab2 in itertools.combinations(labs, 2):
            labA, labB = lab1["Lab"], lab2["Lab"]
            cvA, cvB = lab1.get("CV (%)"), lab2.get("CV (%)")
            rA, rB = lab1.get("Ratio"), lab2.get("Ratio")

            labA_key = f"{labA}_{key_prefix}"
            labB_key = f"{labB}_{key_prefix}"

            penalty_A = 10 if pd.isna(cvA) or pd.isna(rA) else 0
            penalty_B = 10 if pd.isna(cvB) or pd.isna(rB) else 0

            if pd.isna(cvA) or pd.isna(cvB):
                cv_score_A = cv_score_B = 0.5
            elif abs(cvA - cvB) < 0.1:
                cv_score_A = cv_score_B = 0.5
            elif cvA < cvB:
                cv_score_A, cv_score_B = 1, 0
            else:
                cv_score_A, cv_score_B = 0, 1

            bonus_A = 5 if not pd.isna(rA) and rA >= 1.0 else 0
            bonus_B = 5 if not pd.isna(rB) and rB >= 1.0 else 0
            if not pd.isna(cvA) and param in EFLM_TARGETS and cvA <= EFLM_TARGETS[param]:
                bonus_A += 2
            if not pd.isna(cvB) and param in EFLM_TARGETS and cvB <= EFLM_TARGETS[param]:
                bonus_B += 2

            Ra, Rb = ratings[labA_key], ratings[labB_key]
            Ea = 1 / (1 + 10 ** ((Rb - Ra) / 400))
            Eb = 1 / (1 + 10 ** ((Ra - Rb) / 400))

            ratings[labA_key] += K * ((cv_score_A > cv_score_B) - Ea)
            ratings[labB_key] += K * ((cv_score_B > cv_score_A) - Eb)

            ratings[labA_key] += bonus_A - penalty_A
            ratings[labB_key] += bonus_B - penalty_B

            param_level_scores[labA_key] += ratings[labA_key]
            param_level_scores[labB_key] += ratings[labB_key]

            battle_logs.append({
                "Lab_A": labA, "Lab_B": labB,
                "Parameter": param, "Level": level, "Month": month,
                "CV_A": cvA, "CV_B": cvB,
                "Ratio_A": rA, "Ratio_B": rB,
                "Bonus_A": bonus_A, "Penalty_A": penalty_A,
                "Bonus_B": bonus_B, "Penalty_B": penalty_B,
                "Updated_Rating_A": round(ratings[labA_key], 1),
                "Updated_Rating_B": round(ratings[labB_key], 1)
            })

        for lab in group["Lab"].unique():
            lab_key = f"{lab}_{key_prefix}"
            rating_progression.append({
                "Lab": lab,
                "Parameter": param,
                "Level": level,
                "Month": month,
                "Elo": round(ratings[lab_key], 2)
            })

    lab_elos = {}
    lab_counts = {}

    for key, elo in ratings.items():
        parts = key.split("_")
        lab = "_".join(parts[:-2])
        lab_elos[lab] = lab_elos.get(lab, 0) + elo
        lab_counts[lab] = lab_counts.get(lab, 0) + 1

    summary_df = pd.DataFrame([{
        "Lab": lab,
        "Final Elo": round(lab_elos[lab] / lab_counts[lab], 2),
        "Total Score": round(sum([v for k, v in ratings.items() if k.startswith(lab)]), 2)
    } for lab in lab_elos]).sort_values(by="Final Elo", ascending=False).reset_index(drop=True)

    summary_df["Medal"] = ""
    if len(summary_df) >= 1: summary_df.loc[0, "Medal"] = "\U0001F947"
    if len(summary_df) >= 2: summary_df.loc[1, "Medal"] = "\U0001F948"
    if len(summary_df) >= 3: summary_df.loc[2, "Medal"] = "\U0001F949"

    st.session_state["elo_history"] = ratings
    st.session_state["elo_progression"] = pd.DataFrame(rating_progression)
    st.session_state["fadzly_battles"] = summary_df

    Path("data").mkdir(exist_ok=True)
    pd.DataFrame.from_dict(ratings, orient="index", columns=["elo"]).to_csv("data/elo_history.csv")
    st.session_state["elo_progression"].to_csv("data/elo_progression.csv", index=False)

    st.success("✅ Battle simulation completed.")
    st.markdown("### Leaderboard")
    st.dataframe(summary_df)
    st.markdown("### Battle Log")
    st.dataframe(pd.DataFrame(battle_logs))

def run():
    st.title("⚔️ LLKK Battle Log")

    if "logged_in_lab" not in st.session_state:
        st.warning("Please log in to access this page.")
        st.stop()

    role = st.session_state.get("user_role", "lab")

    dataframes = []
    for file in glob.glob("data/submission_*.csv"):
        dataframes.append(pd.read_csv(file))

    if dataframes:
        df = pd.concat(dataframes, ignore_index=True)
        st.session_state["llkk_data"] = df
    else:
        df = pd.DataFrame()

    if df.empty:
        st.error("🚫 No data found. Please enter data in the Data Entry tab.")
        return

    st.markdown("### Submitted Data")
    st.dataframe(df)

    if "elo_history" not in st.session_state and os.path.exists("data/elo_history.csv"):
        hist_df = pd.read_csv("data/elo_history.csv")
        st.session_state["elo_history"] = dict(zip(hist_df["Unnamed: 0"], hist_df["elo"]))

    if "elo_progression" not in st.session_state and os.path.exists("data/elo_progression.csv"):
        st.session_state["elo_progression"] = pd.read_csv("data/elo_progression.csv")

    if role == "admin":
        st.markdown("---")
        st.subheader("🛡️ Admin Control Panel")
        if st.button("🚀 Start Fadzly Battle Simulation"):
            simulate_fadzly_algorithm(df)

        st.markdown("### Danger Zone")
        if st.button("❌ Clear All Elo History"):
            for key in ["elo_history", "elo_progression", "fadzly_battles"]:
                st.session_state.pop(key, None)
            for file in ["data/elo_history.csv", "data/elo_progression.csv"]:
                if os.path.exists(file):
                    os.remove(file)
            st.success("✅ All historical data cleared.")
            st.rerun()
    else:
        st.info("🟢 Waiting for Admin to start the battle simulation.")
