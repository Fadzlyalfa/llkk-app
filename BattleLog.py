import streamlit as st
import pandas as pd
import itertools
import numpy as np

def run():
    st.title("⚔️ LLKK Battle Log")

    if "llkk_data" not in st.session_state:
        st.warning("Please upload data in the Home page first.")
        return

    df = st.session_state.llkk_data.copy()
    df.columns = df.columns.str.strip().str.title()

    required_cols = {"Lab", "Parameter", "Level", "Cv", "Ratio", "Month"}
    if not required_cols.issubset(df.columns):
        st.error(f"Missing required columns. Required: {', '.join(required_cols)}")
        return

    default_rating = 1000
    k_factor = 16

    # Elo store
    ratings = {lab: default_rating for lab in df["Lab"].unique()}
    battle_log = []

    # Penalty tracking
    penalty_scores = {lab: 0 for lab in df["Lab"].unique()}
    bonus_scores = {lab: 0 for lab in df["Lab"].unique()}

    # Loop over month > parameter > level
    for (month, param, level), group in df.groupby(["Month", "Parameter", "Level"]):
        labs = group["Lab"].unique()
        for lab1, lab2 in itertools.combinations(labs, 2):
            row1 = group[group["Lab"] == lab1]
            row2 = group[group["Lab"] == lab2]

            if row1.empty or row2.empty:
                continue

            cv1, ratio1 = row1["Cv"].values[0], row1["Ratio"].values[0]
            cv2, ratio2 = row2["Cv"].values[0], row2["Ratio"].values[0]

            if pd.isna(cv1) or pd.isna(cv2):
                penalty_scores[lab1] -= 10 if pd.isna(cv1) else 0
                penalty_scores[lab2] -= 10 if pd.isna(cv2) else 0
                continue

            # CV winner
            if abs(cv1 - cv2) < 0.1:
                cv_score = (0.5, 0.5)
            else:
                cv_score = (1, 0) if cv1 < cv2 else (0, 1)

            # Ratio winner
            if pd.isna(ratio1) or pd.isna(ratio2):
                ratio_score = (0.5, 0.5)
            elif abs(ratio1 - 1.0) < abs(ratio2 - 1.0):
                ratio_score = (1, 0)
            elif abs(ratio2 - 1.0) < abs(ratio1 - 1.0):
                ratio_score = (0, 1)
            else:
                ratio_score = (0.5, 0.5)

            # Final score
            final_score1 = (cv_score[0] + ratio_score[0]) / 2
            final_score2 = (cv_score[1] + ratio_score[1]) / 2

            # Elo updates
            r1, r2 = ratings[lab1], ratings[lab2]
            exp1 = 1 / (1 + 10 ** ((r2 - r1) / 400))
            exp2 = 1 / (1 + 10 ** ((r1 - r2) / 400))

            new_r1 = r1 + k_factor * (final_score1 - exp1)
            new_r2 = r2 + k_factor * (final_score2 - exp2)

            ratings[lab1] = round(new_r1, 2)
            ratings[lab2] = round(new_r2, 2)

            battle_log.append({
                "Month": month,
                "Parameter_Level": f"{param}_{level}",
                "Lab_1": lab1,
                "Lab_2": lab2,
                "CV_1": cv1,
                "CV_2": cv2,
                "Ratio_1": ratio1,
                "Ratio_2": ratio2,
                "Score_1": final_score1,
                "Score_2": final_score2,
                "Δ_Lab_1": round(new_r1 - r1, 2),
                "Δ_Lab_2": round(new_r2 - r2, 2),
                "New_Rating_1": new_r1,
                "New_Rating_2": new_r2
            })

    # Apply bonuses (simplified)
    for _, row in df.iterrows():
        lab = row["Lab"]
        if not pd.isna(row["Cv"]) and row["Cv"] <= 2.5:
            bonus_scores[lab] += 2
        if not pd.isna(row["Ratio"]) and row["Ratio"] == 1.0:
            bonus_scores[lab] += 2

    # Final rating table
    result_df = pd.DataFrame([
        {
            "Lab": lab,
            "Final_Elo": ratings[lab],
            "Bonus": bonus_scores[lab],
            "Penalty": penalty_scores[lab],
            "Total_Score": ratings[lab] + bonus_scores[lab] + penalty_scores[lab]
        }
        for lab in ratings
    ])
    result_df.sort_values("Total_Score", ascending=False, inplace=True)

    st.subheader("🧾 Battle Log")
    st.dataframe(pd.DataFrame(battle_log), use_container_width=True)

    st.subheader("🏆 Final Lab Scores")
    st.dataframe(result_df, use_container_width=True)

    st.markdown(
        "<hr style='margin-top: 2rem; margin-bottom: 1rem;'>"
        "<div style='text-align: center; color: gray;'>"
        "© 2025 Lab Legend Kingdom Kvalis — Powered by MEQARE"
        "</div>",
        unsafe_allow_html=True
    )
