def simulate_fadzly_algorithm(df):
    st.subheader("🏁 Fadzly Battle Simulation")

    df["CV (%)"] = pd.to_numeric(df["CV (%)"], errors="coerce")
    df["Ratio"] = pd.to_numeric(df["Ratio"], errors="coerce")
    df = df.dropna(subset=["n (QC)", "Working Days"])

    if "elo_history" not in st.session_state:
        st.session_state["elo_history"] = {}

    ratings = st.session_state["elo_history"].copy()
    scores = {}
    K = 16
    battle_logs = []
    rating_progression = []

    for (param, level, month), group in df.groupby(["Parameter", "Level", "Month"]):
        labs = group.to_dict("records")
        key_prefix = f"{param}_{level}"

        for lab in group["Lab"].unique():
            lab_key = f"{lab}_{key_prefix}"
            if lab_key not in ratings:
                ratings[lab_key] = 1500
            if lab not in scores:
                scores[lab] = 0

        for lab1, lab2 in itertools.combinations(labs, 2):
            labA, labB = lab1["Lab"], lab2["Lab"]
            cvA, cvB = lab1.get("CV (%)"), lab2.get("CV (%)")
            rA, rB = lab1.get("Ratio"), lab2.get("Ratio")

            labA_key = f"{labA}_{key_prefix}"
            labB_key = f"{labB}_{key_prefix}"

            # Penalties
            penalty_A = 10 if pd.isna(cvA) or pd.isna(rA) else 0
            penalty_B = 10 if pd.isna(cvB) or pd.isna(rB) else 0

            # CV scoring
            if pd.isna(cvA) or pd.isna(cvB):
                cv_score_A = cv_score_B = 0.5
            elif abs(cvA - cvB) < 0.1:
                cv_score_A = cv_score_B = 0.5
            elif cvA < cvB:
                cv_score_A, cv_score_B = 1, 0
            else:
                cv_score_A, cv_score_B = 0, 1

            # Bonuses
            bonus_A = 5 if not pd.isna(rA) and rA >= 1.0 else 0
            bonus_B = 5 if not pd.isna(rB) and rB >= 1.0 else 0
            if not pd.isna(cvA) and param in EFLM_TARGETS and cvA <= EFLM_TARGETS[param]:
                bonus_A += 2
            if not pd.isna(cvB) and param in EFLM_TARGETS and cvB <= EFLM_TARGETS[param]:
                bonus_B += 2

            final_A = cv_score_A + bonus_A - penalty_A
            final_B = cv_score_B + bonus_B - penalty_B
            scores[labA] += final_A
            scores[labB] += final_B

            Ra, Rb = ratings[labA_key], ratings[labB_key]
            Ea = 1 / (1 + 10 ** ((Rb - Ra) / 400))
            Eb = 1 / (1 + 10 ** ((Ra - Rb) / 400))
            ratings[labA_key] += K * ((final_A > final_B) - Ea)
            ratings[labB_key] += K * ((final_B > final_A) - Eb)

            battle_logs.append({
                "Lab_A": labA, "Lab_B": labB,
                "Parameter": param, "Level": level, "Month": month,
                "CV_A": cvA, "CV_B": cvB,
                "Ratio_A": rA, "Ratio_B": rB,
                "Score_A": round(final_A, 2),
                "Score_B": round(final_B, 2),
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

    # Aggregate summary by lab
    final_summary = {}
    for lab_key, elo in ratings.items():
        lab, param, level = lab_key.split("_", 2)
        if lab not in final_summary:
            final_summary[lab] = {"Final Elo": 0, "Total Score": scores.get(lab, 0)}
        final_summary[lab]["Final Elo"] += elo

    summary_df = pd.DataFrame([
        {"Lab": lab, **vals} for lab, vals in final_summary.items()
    ]).sort_values(by="Final Elo", ascending=False).reset_index(drop=True)

    summary_df["Medal"] = ""
    if len(summary_df) >= 1: summary_df.loc[0, "Medal"] = "🥇"
    if len(summary_df) >= 2: summary_df.loc[1, "Medal"] = "🥈"
    if len(summary_df) >= 3: summary_df.loc[2, "Medal"] = "🥉"

    st.session_state["elo_history"] = ratings
    st.session_state["elo_progression"] = pd.DataFrame(rating_progression)
    st.session_state["fadzly_battles"] = summary_df

    st.success("✅ Battle simulation completed.")
    st.markdown("### 🏆 Leaderboard")
    st.dataframe(summary_df)
    st.markdown("### 📜 Battle Log")
    st.dataframe(pd.DataFrame(battle_logs))
