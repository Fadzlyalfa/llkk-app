import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os
from io import BytesIO

# ───────────────────────────────────────────────────────
# 🔧 Basic Configuration
# ───────────────────────────────────────────────────────
st.set_page_config(layout="wide")
st.title("🧝 LLKK - Lab Legend Kingdom Kvalis")

# ───────────────────────────────────────────────────────
# 📤 Upload Excel File
# ───────────────────────────────────────────────────────
uploaded_file = st.file_uploader("📂 Upload your LLKK Excel file (e.g. March 2025)", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.subheader("📄 Raw Uploaded Data")
    st.dataframe(df)

    # ───────────────────────────────────────────────────
    # 📊 Add Base Elo from Previous Month
    # ───────────────────────────────────────────────────
    df['Base_Elo'] = df['Rank_Feb']

    # ───────────────────────────────────────────────────
    # 🧮 Apply Bonus and Penalty Logic
    # ───────────────────────────────────────────────────
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
    df['Final_Elo'] = df['Base_Elo'] + df['Bonus'] - df['Penalty']

    # ───────────────────────────────────────────────────
    # 🧪 Replace Test Name with Icon using Prefix
    # ───────────────────────────────────────────────────
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
        else:
            return parameter

    df['Parameter_Icon'] = df['Parameter'].apply(get_test_icon)

    st.subheader("🎯 Bonus and Penalty Applied")
    st.dataframe(df[['Lab', 'Parameter_Icon', 'Bonus', 'Penalty', 'Final_Elo']].rename(columns={'Parameter_Icon': 'Test'}))

    # ───────────────────────────────────────────────────
    # ⚔️ Calculate Average Elo by Lab
    # ───────────────────────────────────────────────────
    final_elos = df.groupby('Lab')['Final_Elo'].mean().reset_index()

    st.subheader("⚔️ Elo Battle Summary")
    st.dataframe(final_elos)

    # ───────────────────────────────────────────────────
    # 📊 Plot Elo Scores
    # ───────────────────────────────────────────────────
    st.subheader("📊 Elo Score by Lab")
    fig = px.bar(final_elos, x='Lab', y='Final_Elo', color='Lab', title='Final Elo Scores by Lab')
    st.plotly_chart(fig)

    # ───────────────────────────────────────────────────
    # 🏰 Fantasy Avatars and Scores
    # ───────────────────────────────────────────────────
    st.subheader("🏰 LLKK Fantasy Leaderboard")

    lab_avatars = {
        "Lab_A": os.path.join("lab_a.png"),
        "Lab_B": os.path.join("lab_b.png"),
        "Lab_C": os.path.join("lab_c.png")
    }

    for lab in final_elos['Lab'].unique():
        st.image(lab_avatars.get(lab, ""), width=150)
        score = final_elos[final_elos['Lab'] == lab]['Final_Elo'].values[0]
        st.markdown(f"### 🏅 {lab} — Final Elo: **{score:.2f}**")

    # ───────────────────────────────────────────────────
    # 👑 Champion Announcement (Supports Tie)
    # ───────────────────────────────────────────────────
    st.markdown("## 👑 Champion of the Month")
    max_elo = final_elos['Final_Elo'].max()
    top_labs = final_elos[final_elos['Final_Elo'] == max_elo]

    for _, row in top_labs.iterrows():
        st.image(lab_avatars.get(row['Lab'], ""), width=150)
        st.markdown(f"### 🏆 {row['Lab']} — Final Elo: **{row['Final_Elo']:.2f}**")
        st.success(f"🎉 Congratulations {row['Lab']}! You are crowned this month’s Champion in Kingdom Kvalis.")

    # ───────────────────────────────────────────────────
    # 📥 Download Final Elo Table
    # ───────────────────────────────────────────────────
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
