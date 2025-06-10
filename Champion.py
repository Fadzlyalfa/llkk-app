import streamlit as st
import pandas as pd
import altair as alt

def run():
    st.title("👑 LLKK Champion Board")

    # Check if results are available
    if "fadzly_battles" not in st.session_state:
        st.warning("⚠️ Battle not simulated yet. Please run the simulation from the Admin tab.")
        return

    df = st.session_state["fadzly_battles"]
    st.subheader("🏅 Final Rankings (Elo + Bonus)")
    st.dataframe(df, use_container_width=True)

    # Champion announcement
    champ_row = df.iloc[0]
    st.markdown(f"""
    <hr>
    <h2 style='text-align: center;'>👑 <span style='color:gold'>{champ_row['Lab']}</span> is the Champion!</h2>
    <h4 style='text-align: center;'>Final Elo: <code>{champ_row['Final Elo']}</code> | Total Score: <code>{champ_row['Total Score']}</code></h4>
    <div style='text-align: center; font-size: 3rem;'>{champ_row['Medal']}</div>
    <hr>
    """, unsafe_allow_html=True)

    # 📈 Elo Progression Chart
    if "elo_progression" in st.session_state:
        st.subheader("📈 Elo Rating Progression")

        prog_df = st.session_state["elo_progression"]
        labs = prog_df["Lab"].unique().tolist()
        parameters = prog_df["Parameter"].unique().tolist()
        levels = prog_df["Level"].unique().tolist()

        col1, col2, col3 = st.columns(3)
        selected_lab = col1.selectbox("Select Lab", labs)
        selected_param = col2.selectbox("Select Parameter", parameters)
        selected_level = col3.selectbox("Select Level", levels)

        filtered = prog_df[
            (prog_df["Lab"] == selected_lab) &
            (prog_df["Parameter"] == selected_param) &
            (prog_df["Level"] == selected_level)
        ].sort_values("Month")

        if not filtered.empty:
            chart = alt.Chart(filtered).mark_line(point=True).encode(
                x="Month:N",
                y="Elo:Q",
                tooltip=["Month", "Elo"]
            ).properties(
                title=f"{selected_lab} — {selected_param} {selected_level} Elo Progression",
                width=700,
                height=400
            )
            st.altair_chart(chart, use_container_width=True)
        else:
            st.info("ℹ️ No rating data available for this combination.")

    # Footer
    st.markdown(
        "<div style='text-align: center; color: gray;'>© 2025 Lab Legend Kingdom Kvalis — Powered by MEQARE</div>",
        unsafe_allow_html=True
    )
