import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os
from io import BytesIO

st.set_page_config(layout="wide")
st.title("🧝 LLKK - Lab Legend Kingdom Kvalis")

# File uploader
uploaded_file = st.file_uploader("📂 Upload your LLKK Excel file (e.g. March 2025)", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.subheader("📄 Raw Uploaded Data")
    st.dataframe(df)

    # Add Base_Elo from Rank_Feb
    df['Base_Elo'] = df['Rank_Feb']

    # Apply bonus and penalty
    def calculate_bonus_penalty(row):
        if pd.isna(row['CV_Mar']) or pd.isna(row['Ratio_Mar']):
            return 0, 10
        bonus = 0
        penalty = 0
        if row['CV_Mar'] < 2:
            bonus += 2
        if row['Ratio_Mar'] < 1.5:
            bonus += 1
        return bonus, penalty

    df[['Bonus', 'Penalty']] = df.apply(lambda row: pd.Series(calculate_bonus_penalty(row)), axis=1)
    df['Final_Elo'] = df['Base_Elo'] + df['Bonus'] - df['Penalty']

    st.subheader("🎯 Bonus and Penalty Applied")
    st.dataframe(df[['Lab', 'Parameter', 'Bonus', 'Penalty', 'Final_Elo']])

    # Calculate Elo battle summary
    def calculate_elo(df):
        grouped = df.groupby(['Lab'])['Final_Elo'].mean().reset_index()
        return grouped

    final_elos = calculate_elo(df)

    st.subheader("⚔️ Elo Battle Summary")
    st.dataframe(final_elos)

    # Plot Elo Ratings
    st.subheader("📊 Elo Score by Lab")
    fig = px.bar(final_elos, x='Lab', y='Final_Elo', color='Lab', title='Final Elo Scores by Lab')
    st.plotly_chart(fig)

    # Avatar display
    st.subheader("🏰 LLKK Fantasy Leaderboard")

    lab_avatars = {
        "Lab_A": os.path.join("lab_a.png"),
        "Lab_B": os.path.join("lab_b.png"),
        "Lab_C": os.path.join("lab_c.png")
    }

    for lab in final_elos['Lab'].unique():
        st.image(lab_avatars[lab], width=150)
        score = final_elos[final_elos['Lab'] == lab]['Final_Elo'].values[0]
        st.markdown(f"### 🏅 {lab} — Final Elo: **{score:.2f}**")

    # Champion announcement
    top_lab = final_elos.sort_values(by='Final_Elo', ascending=False).iloc[0]
    st.markdown("## 👑 Champion of the Month")
    st.image(lab_avatars[top_lab['Lab']], width=150)
    st.markdown(f"### 🏆 {top_lab['Lab']} — Final Elo: **{top_lab['Final_Elo']:.2f}**")
    st.success(f"🎉 Congratulations {top_lab['Lab']}! You are crowned this month’s Champion in Kingdom Kvalis.")

    # Download final Elo results
    st.subheader("📁 Download Final Elo Table")
    def to_excel(df):
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Final_Elo')
        processed_data = output.getvalue()
        return processed_data

    excel_data = to_excel(final_elos)
    st.download_button("Download Elo Results", data=excel_data, file_name="LLKK_Final_Elo.xlsx")

else:
    st.info("Please upload a valid Excel file to start.")
