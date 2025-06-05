import streamlit as st
import pandas as pd
import numpy as np
import os
import base64
from io import BytesIO

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
st.title("🧝 LLKK - Lab Legend Kingdom Kvalis")

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
    st.subheader("📄 Raw Uploaded Data")
    st.dataframe(df_raw)

    # Map parameters
    param_map = {
        "Glucose": "Glu",
        "Creatinine": "Cre",
        "Cholesterol": "Chol",
        "Cholestetol": "Chol",  # typo fix
    }

    df = df_raw.copy()
    df['Parameter_Code'] = df['Parameter'].map(param_map)
    df['Level_Num'] = df['Level'].str.extract(r'(\d)').fillna("1")
    df['Parameter_ID'] = df['Parameter_Code'] + "_L" + df['Level_Num']
    df['CV_Mar'] = df['CV']
    df['Ratio_Mar'] = df['CV']
    df['Rank_Feb'] = 1500

    # Prepare processed dataframe
    df_processed = df[['Lab', 'Parameter_ID', 'CV_Mar', 'Ratio_Mar', 'Rank_Feb']].rename(
        columns={'Parameter_ID': 'Parameter'}
    )

    df = df_processed.copy()

    # ──────────────────────────────
    # Bonus & Penalty
    # ──────────────────────────────
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

    # ──────────────────────────────
    # Display Tables
    # ──────────────────────────────
    st.markdown("### 🎯 Bonus and Penalty Applied", unsafe_allow_html=True)
    st.write(df[['Lab_Display', 'Parameter_Icon', 'Bonus', 'Penalty', 'Final_Elo']]
             .rename(columns={'Lab_Display': 'Lab', 'Parameter_Icon': 'Test'})
             .to_html(escape=False, index=False), unsafe_allow_html=True)

    final_elos = df.groupby('Lab')['Final_Elo'].mean().reset_index()
    final_elos['Lab_Display'] = final_elos['Lab'].apply(get_lab_avatar_markdown)

    st.markdown("### ⚔️ Elo Battle Summary", unsafe_allow_html=True)
    st.write(final_elos[['Lab_Display', 'Final_Elo']]
             .rename(columns={'Lab_Display': 'Lab'})
             .to_html(escape=False, index=False), unsafe_allow_html=True)

    # ──────────────────────────────
    # Avatar Cards with Medals
    # ──────────────────────────────
    st.subheader("🏆 Legend Ranking View")
    ranked_labs = final_elos.sort_values(by='Final_Elo', ascending=False).reset_index(drop=True)
    medals = ["🥇", "🥈", "🥉"]

    for idx, row in ranked_labs.iterrows():
        lab = row['Lab']
        elo = row['Final_Elo']
        medal = medals[idx] if idx < len(medals) else "🏅"
        st.markdown(f"""
            <div style='border: 2px solid #ccc; border-radius: 12px; padding: 10px 16px; margin: 10px 0; display: flex; align-items: center; background-color: #f9f9f9;'>
                <img src='data:image/png;base64,{encode_image(lab_avatars[lab])}' width='60' style='margin-right: 16px; border-radius: 8px;'/>
                <div>
                    <div style='font-size: 20px; font-weight: bold;'>{medal} {lab}</div>
                    <div style='font-size: 16px;'>Final Elo: <b>{elo:.2f}</b></div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # ──────────────────────────────
    # Champion Display
    # ──────────────────────────────
    st.markdown("## 👑 Champion of the Month")
    max_elo = final_elos['Final_Elo'].max()
    top_labs = final_elos[final_elos['Final_Elo'] == max_elo]
    for _, row in top_labs.iterrows():
        st.image(lab_avatars.get(row['Lab'], ""), width=150)
        st.markdown(f"### 🏆 {row['Lab']} — Final Elo: **{row['Final_Elo']:.2f}**")
        st.success(f"🎉 Congratulations {row['Lab']}! You are crowned this month’s Champion in Kingdom Kvalis.")

    # ──────────────────────────────
    # Download
    # ──────────────────────────────
    st.subheader("📁 Download Final Elo Table")
    def to_excel(dataframe):
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            dataframe.to_excel(writer, index=False, sheet_name='Final_Elo')
        return output.getvalue()

    excel_data = to_excel(final_elos)
    st.download_button("Download Elo Results", data=excel_data, file_name="LLKK_Final_Elo.xlsx")

else:
    st.info("Please upload a valid Excel file to start.")
