import streamlit as st
import pandas as pd
import itertools

def run():
    st.title("📜 LLKK Battle Log")

    if "llkk_data" not in st.session_state:
        st.warning("Please upload data in the Home page first.")
        return

    df = st.session_state.llkk_data.copy()

    # Standardize column names just in case
    df.columns = df.columns.str.strip().str.title()

    required_cols = {"Lab", "Parameter", "Level", "Cv"}
    if not required_cols.issubset(df.columns):
        st.error("Missing required columns in uploaded data. Required: Lab, Parameter, Level, CV")
        return

    # Prepare battle results
    battles = []

    for (param, level), group in df.groupby(["Parameter", "Level"]):
        labs = group["Lab"].unique()
        if len(labs) < 2:
            continue

        for lab1, lab2 in itertools.combinations(labs, 2):
            cv1 = group[group["Lab"] == lab1]["Cv"].values[0]
            cv2 = group[group["Lab"] == lab2]["Cv"].values[0]

            if pd.isna(cv1) or pd.isna(cv2):
                continue

            winner = lab1 if cv1 < cv2 else lab2
            delta = round(abs(cv1 - cv2) * 10, 1)

            battles.append({
                "Parameter": f"{param}_{level}",
                "Lab_1": lab1,
                "Lab_2": lab2,
                "CV_1": cv1,
                "CV_2": cv2,
                "Winner": winner,
                "Δ_Lab_1": +delta if winner == lab1 else -delta,
                "Δ_Lab_2": -delta if winner == lab1 else +delta
            })

    if battles:
        battle_df = pd.DataFrame(battles)
        st.dataframe(battle_df, use_container_width=True)
    else:
        st.info("No valid lab comparisons could be generated.")

    st.markdown(
        "<hr style='margin-top: 2rem; margin-bottom: 1rem;'>"
        "<div style='text-align: center; color: gray;'>"
        "© 2025 Lab Legend Kingdom Kvalis — Powered by MEQARE"
        "</div>",
        unsafe_allow_html=True
    )
