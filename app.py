import streamlit as st
import pandas as pd
import numpy as np
import os
import base64
from io import BytesIO
from itertools import combinations

# ──────────────────────────────
# Utility Functions
# ──────────────────────────────
def encode_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def get_lab_avatar_markdown(lab_name):
    if lab_name in lab_avatars:
        return f'<img src="data:image/png;base64,{encode_image(lab_avatars[lab_name])}" width="30"/> {lab_name}'
    return lab_name

def get_test_icon(parameter):
    if parameter.startswith("Glu"):
        return "🩸 Glucose"
    elif parameter.startswith("Cre"):
        return "💧 Creatinine"
    elif parameter.startswith("Chol"):
        return "🥚 Cholesterol"
    elif parameter.startswith("HbA1c"):
        return "🧪 HbA1c"
    elif parameter.startswith("ALT"):
        return "🍷 ALT"
    elif parameter.startswith("AST"):
        return "🔥 AST"
    elif parameter.startswith("Urea"):
        return "🚽 Urea"
    elif parameter.startswith("Alb"):
        return "🎵 Albumin"
    elif parameter.startswith("TP"):
        return "📊 Total Protein"
    elif parameter.startswith("ALP"):
        return "🧱 ALP"
    return parameter

# ──────────────────────────────
# App Config
# ──────────────────────────────
st.set_page_config(layout="wide")
st.image("Header.png", use_container_width=True)

lab_avatars = {
    "Lab_A": os.path.join("lab_a.png"),
    "Lab_B": os.path.join("lab_b.png"),
    "Lab_C": os.path.join("lab_c.png")
}

# ──────────────────────────────
# Upload File
# ──────────────────────────────
uploaded_file = st.file_uploader("📂 Upload LLKK Excel file", type=["xlsx"])

if uploaded_file:
    df_raw = pd.read_excel(uploaded_file)
    df_raw.columns = df_raw.columns.str.strip()

    st.subheader("📄 Raw Uploaded Data")
    st.dataframe(df_raw)

    param_map = {
        "Glucose": "Glu",
        "Creatinine": "Cre",
        "Cholesterol": "Chol",
        "Cholestetol": "Chol",
    }

    df = df_raw.copy()
    df['Lab'] = df['Lab'].str.strip().str.replace(" ", "_")
    df['Parameter_Code'] = df['Parameter'].map(param_map)
    df['Level_Num'] = df['Level'].str.extract(r'(\d)').fillna("1")
    df['Parameter_ID'] = df['Parameter_Code'] + "_L" + df['Level_Num']
    df['CV_Mar'] = df['CV']
    df['Ratio_Mar'] = df['CV']
    df['Rank_Feb'] = 1500

    df_processed = df[['Lab', 'Parameter_ID', 'CV_Mar', 'Ratio_Mar', 'Rank_Feb']].rename(
        columns={'Parameter_ID': 'Parameter'}
    )
    df = df_processed.copy()

    def calculate_bonus_penalty(row):
        if pd.isna(row['CV_Mar']) or pd.isna(row['Ratio_Mar']):
            return 0, 10
        bonus = 0
        if row['CV_Mar'] < 2:
            bonus += 2
        if row['Ratio_Mar'] < 1.5:
            bonus += 1
        return bonus, 0

    df[['Bonus', 'Penalty']] = df.apply(lambda row: pd.Series(calculate_bonus_penalty(row)), axis=1)
    df['Final_Elo'] = df['Rank_Feb'] + df['Bonus'] - df['Penalty']
    df['Parameter_Icon'] = df['Parameter'].apply(get_test_icon)
    df['Lab_Display'] = df['Lab'].apply(get_lab_avatar_markdown)

    st.markdown("### 🎯 Bonus and Penalty Applied", unsafe_allow_html=True)
    st.write(df[['Lab_Display', 'Parameter_Icon', 'Bonus', 'Penalty', 'Final_Elo']]
             .rename(columns={'Lab_Display': 'Lab', 'Parameter_Icon': 'Test'})
             .to_html(escape=False, index=False), unsafe_allow_html=True)

    # ──────────── Battle-Based Elo ─────────────
    base_elo = 1500
    lab_elos = {lab: base_elo for lab in df['Lab'].unique()}
    k_factor = 16
    battle_log = []

    for test_id in df['Parameter'].unique():
        subset = df[df['Parameter'] == test_id]
        labs = subset['Lab'].tolist()

        for lab1, lab2 in combinations(labs, 2):
            cv1 = subset[subset['Lab'] == lab1]['CV_Mar'].values[0]
            cv2 = subset[subset['Lab'] == lab2]['CV_Mar'].values[0]

            if cv1 == cv2:
                outcome = 0.5
            elif cv1 < cv2:
                outcome = 1
            else:
                outcome = 0

            R1 = 10 ** (lab_elos[lab1] / 400)
            R2 = 10 ** (lab_elos[lab2] / 400)
            E1 = R1 / (R1 + R2)
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

    st.subheader("📜 Battle Log")
    st.dataframe(pd.DataFrame(battle_log))

    final_table = pd.DataFrame.from_dict(lab_elos, orient='index', columns=['Final_Elo']).reset_index()
    final_table.rename(columns={'index': 'Lab'}, inplace=True)
    final_table['Lab_Display'] = final_table['Lab'].apply(get_lab_avatar_markdown)

    st.markdown("### ⚔️ Elo Battle Summary", unsafe_allow_html=True)
    st.write(final_table[['Lab_Display', 'Final_Elo']]
             .rename(columns={'Lab_Display': 'Lab'})
             .to_html(escape=False, index=False), unsafe_allow_html=True)

    # ──────────── Champion of the Month ─────────────
    st.markdown("## 👑 Champion of the Month")
    max_elo = final_table['Final_Elo'].max()
    top_labs = final_table[final_table['Final_Elo'] == max_elo]
    for _, row in top_labs.iterrows():
        st.image(lab_avatars.get(row['Lab'], ""), width=150)
        st.markdown(f"### 🏆 {row['Lab']} — Final Elo: **{row['Final_Elo']:.2f}**")
        st.success(f"🎉 Congratulations {row['Lab']}! You are crowned this month’s Champion in Kingdom Kvalis.")

    # ──────────── Download Button ─────────────
    st.subheader("📁 Download Final Elo Table")
    def to_excel(dataframe):
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            dataframe.to_excel(writer, index=False, sheet_name='Final_Elo')
        return output.getvalue()

    excel_data = to_excel(final_table)
    st.download_button("Download Elo Results", data=excel_data, file_name="LLKK_Final_Elo.xlsx")

else:
    st.info("Please upload a valid Excel file to start.")
