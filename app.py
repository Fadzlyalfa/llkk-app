# LLKK App — Battle-Based Elo System (Stage 1)

import streamlit as st
import pandas as pd
import numpy as np
import os
import base64
from io import BytesIO
from itertools import combinations

# ────────────────
# Config & Images
# ────────────────
st.set_page_config(layout="wide")
st.title("⚔️ LLKK Battle Arena — Parameter-Level Elo Showdown")

lab_avatars = {
    "Lab_A": os.path.join("lab_a.png"),
    "Lab_B": os.path.join("lab_b.png"),
    "Lab_C": os.path.join("lab_c.png")
}

def encode_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def get_avatar_html(lab):
    if lab in lab_avatars:
        return f"<img src='data:image/png;base64,{encode_image(lab_avatars[lab])}' width='30'/> {lab}"
    return lab

# ────────────────
# Upload Excel File
# ────────────────
file = st.file_uploader("📂 Upload CV dataset", type=["xlsx"])

if file:
    df = pd.read_excel(file)
    df.columns = df.columns.str.strip()
    df['Lab'] = df['Lab'].str.strip().str.replace(" ", "_")

    # Construct Parameter_ID (e.g., Glu_L1)
    param_map = {"Glucose": "Glu", "Creatinine": "Cre", "Cholesterol": "Chol", "Cholestetol": "Chol"}
    df['Parameter_Code'] = df['Parameter'].map(param_map)
    df['Level_Num'] = df['Level'].str.extract(r'(\d)').fillna("1")
    df['Parameter_ID'] = df['Parameter_Code'] + "_L" + df['Level_Num']
    df = df[['Lab', 'Parameter_ID', 'CV']]

    # Initialize Elo
    base_elo = 1500
    lab_elos = {lab: base_elo for lab in df['Lab'].unique()}
    k_factor = 16

    battle_log = []

    for test_id in df['Parameter_ID'].unique():
        subset = df[df['Parameter_ID'] == test_id]
        labs = subset['Lab'].tolist()

        for lab1, lab2 in combinations(labs, 2):
            cv1 = subset[subset['Lab'] == lab1]['CV'].values[0]
            cv2 = subset[subset['Lab'] == lab2]['CV'].values[0]

            # Determine winner
            if cv1 == cv2:
                outcome = 0.5
            elif cv1 < cv2:
                outcome = 1  # lab1 wins
            else:
                outcome = 0  # lab2 wins

            R1 = 10 ** (lab_elos[lab1] / 400)
            R2 = 10 ** (lab_elos[lab2] / 400)
            E1 = R1 / (R1 + R2)
            E2 = R2 / (R1 + R2)

            # Update Elo
            delta1 = k_factor * (outcome - E1)
            delta2 = -delta1
            lab_elos[lab1] += delta1
            lab_elos[lab2] += delta2

            battle_log.append({
                "Parameter": test_id,
                "Lab_1": lab1,
                "CV_1": cv1,
                "Lab_2": lab2,
                "CV_2": cv2,
                "Winner": lab1 if outcome == 1 else (lab2 if outcome == 0 else "Draw"),
                "Δ_Lab_1": round(delta1, 2),
                "Δ_Lab_2": round(delta2, 2)
            })

    # ────────────────
    # Display Results
    # ────────────────
    st.subheader("📜 Battle Log")
    st.dataframe(pd.DataFrame(battle_log))

    st.subheader("🏁 Final Elo Scores")
    final_table = pd.DataFrame.from_dict(lab_elos, orient='index', columns=['Final_Elo']).reset_index()
    final_table.rename(columns={'index': 'Lab'}, inplace=True)
    final_table['Avatar'] = final_table['Lab'].apply(get_avatar_html)
    st.write(final_table[['Avatar', 'Final_Elo']].to_html(escape=False, index=False), unsafe_allow_html=True)

else:
    st.info("Please upload your LLKK Excel file.")
