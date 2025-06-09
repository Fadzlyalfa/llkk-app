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

            # Penalty for missing data
            penalty_A = 0
            penalty_B = 0
            if pd.isna(cvA) or pd.isna(rA):
                penalty_A = 10
            if pd.isna(cvB) or pd.isna(rB):
                penalty_B = 10

            # CV Battle Score
            if pd.isna(cvA) or pd.isna(cvB):
                cv_score_A = cv_score_B = 0.5  # Can't determine winner
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
            if not pd.isna(cvA) and cvA <= EFLM_TARGETS.get(param, 0):
                bonus_A += 2
            if not pd.isna(cvB) and cvB <= EFLM_TARGETS.get(param, 0):
                bonus_B += 2

            # Final Score per lab
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

    # Add medals
    rating_df["Medal"] = ""
    if len(rating_df) >= 1:
        rating_df.loc[0, "Medal"] = "🥇"
    if len(rating_df) >= 2:
        rating_df.loc[1, "Medal"] = "🥈"
    if len(rating_df) >= 3:
        rating_df.loc[2, "Medal"] = "🥉"

    battle_df = pd.DataFrame(battle_logs)

    st.success("✅ Battle simulation completed.")
    st.markdown("### 🏆 Leaderboard")
    st.dataframe(rating_df)
    st.markdown("---")
    st.markdown("### 🔍 Detailed Battle Log")
    st.dataframe(battle_df)

    # Save for use in Champion & Download pages
    st.session_state["fadzly_battles"] = rating_df
