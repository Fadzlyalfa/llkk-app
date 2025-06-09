# -------------------------- BattleLog.py --------------------------
import streamlit as st
import pandas as pd
import numpy as np

# --- STREAMLIT CONFIG ---
st.set_page_config(page_title="Battle Log", layout="wide", page_icon="⚔️")
st.markdown("## ⚔️ LLKK Battle Log")

# --- CHECK FOR SESSION DATA ---
data = st.session_state.get("llkk_data")
if data is None:
    st.error("No data found. Please upload or enter data via the Home or Data Entry page.")
    st.stop()

required_cols = {"Level", "Cv", "Ratio", "Parameter", "Lab", "Month"}
if not required_cols.issubset(set(data.columns)):
    st.error("Missing required columns. Required: Level, Cv, Ratio, Parameter, Lab, Month")
    st.stop()

# --- FAKE MATCHUPS & FADZLY ALGORITHM ---
battle_log = []
groups = data.groupby(["Parameter", "Level", "Month"])
for key, group in groups:
    labs = group["Lab"].unique()
    for i in range(len(labs)):
        for j in range(i+1, len(labs)):
            lab1 = labs[i]
            lab2 = labs[j]
            row1 = group[group["Lab"] == lab1]
            row2 = group[group["Lab"] == lab2]
            if row1.empty or row2.empty:
                continue

            cv1 = row1["Cv"].values[0]
            cv2 = row2["Cv"].values[0]
            ratio1 = row1["Ratio"].values[0]
            ratio2 = row2["Ratio"].values[0]

            if np.isnan(ratio1) or np.isnan(ratio2):
                bonus1 = bonus2 = 0
            elif ratio1 < 1 and ratio2 >= 1:
                bonus1 = 10
                bonus2 = -10
            elif ratio2 < 1 and ratio1 >= 1:
                bonus1 = -10
                bonus2 = 10
            else:
                bonus1 = bonus2 = 0

            if np.isnan(cv1) or np.isnan(cv2):
                delta1 = -10
                delta2 = -10
                winner = "Missing"
            elif cv1 < cv2:
                delta1 = +10 + bonus1
                delta2 = -10 + bonus2
                winner = lab1
            elif cv2 < cv1:
                delta1 = -10 + bonus1
                delta2 = +10 + bonus2
                winner = lab2
            else:
                delta1 = delta2 = 0
                winner = "Draw"

            battle_log.append({
                "Parameter": key[0],
                "Level": key[1],
                "Month": key[2],
                "Lab_1": lab1,
                "CV_1": cv1,
                "Lab_2": lab2,
                "CV_2": cv2,
                "Winner": winner,
                "Δ_Lab_1": delta1,
                "Δ_Lab_2": delta2
            })

battle_df = pd.DataFrame(battle_log)
if battle_df.empty:
    st.info("No battles were generated from the dataset.")
else:
    st.dataframe(battle_df, use_container_width=True)

# --- FOOTER ---
st.markdown("""
<hr style='margin-top: 2rem; margin-bottom: 1rem;'>
<div style='text-align: center; color: gray;'>
© 2025 Lab Legend Kingdom Kvalis — Powered by MEQARE
</div>""", unsafe_allow_html=True)


# -------------------------- Champion.py --------------------------
import streamlit as st
import pandas as pd

# --- STREAMLIT CONFIG ---
st.set_page_config(page_title="Champion", layout="wide", page_icon="🏆")
st.markdown("## 🏆 LLKK Champion Board")

# --- CHECK FOR SESSION DATA ---
data = st.session_state.get("llkk_data")
if data is None:
    st.error("No data found. Please upload or enter data via the Home or Data Entry page.")
    st.stop()

# --- FAKE RATINGS FOR DISPLAY ---
rating = {}
battles = st.session_state.get("battle_log")
if battles is None:
    st.warning("No battle results found. Visit Battle Log page first.")
    st.stop()

for index, row in battles.iterrows():
    for lab in [row["Lab_1"], row["Lab_2"]]:
        if lab not in rating:
            rating[lab] = 1000
    rating[row["Lab_1"]] += row["Δ_Lab_1"]
    rating[row["Lab_2"]] += row["Δ_Lab_2"]

rank_df = pd.DataFrame([{"Lab": k, "Score": v} for k, v in rating.items()])
rank_df = rank_df.sort_values("Score", ascending=False)
rank_df["Rank"] = range(1, len(rank_df) + 1)

st.dataframe(rank_df, use_container_width=True)

# --- FOOTER ---
st.markdown("""
<hr style='margin-top: 2rem; margin-bottom: 1rem;'>
<div style='text-align: center; color: gray;'>
© 2025 Lab Legend Kingdom Kvalis — Powered by MEQARE
</div>""", unsafe_allow_html=True)
