import streamlit as st
import pandas as pd
from itertools import combinations

st.title("📜 LLKK Battle Log")

# Check for uploaded data in session
if "llkk_data" not in st.session_state:
    st.warning("Please upload data in the Home page first.")
    st.stop()

df = st.session_state.llkk_data

# Prepare battle log
battle_rows = []

# Loop by parameter and level
grouped = df.groupby(["Parameter", "Level"])

for (param, lvl), group in grouped:
    labs = group["Lab"].unique()

    for lab1, lab2 in combinations(labs, 2):
        cv1 = group[group["Lab"] == lab1]["CV"].values
        cv2 = group[group["Lab"] == lab2]["CV"].values

        if len(cv1) == 0 or len(cv2) == 0:
            continue

        cv1 = float(cv1[0])
        cv2 = float(cv2[0])
        winner = lab1 if cv1 < cv2 else lab2

        battle_rows.append({
            "Parameter": f"{param}_{lvl}",
            "Lab_1": lab1,
            "Lab_2": lab2,
            "CV_1": cv1,
            "CV_2": cv2,
            "Winner": winner,
            "Δ_Lab_1": round(cv2 - cv1, 2),
            "Δ_Lab_2": round(cv1 - cv2, 2)
        })

battle_df = pd.DataFrame(battle_rows)

if battle_df.empty:
    st.info("No battles were generated from uploaded data.")
else:
    st.dataframe(battle_df, use_container_width=True)

# Footer
st.markdown(
    "<hr style='margin-top: 2rem; margin-bottom: 1rem;'>"
    "<div style='text-align: center; color: gray;'>"
    "© 2025 Lab Legend Kingdom Kvalis — Powered by MEQARE"
    "</div>",
    unsafe_allow_html=True
)
