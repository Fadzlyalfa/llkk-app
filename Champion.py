import streamlit as st
import pandas as pd

def run():
    st.set_page_config(page_title="LLKK Champion", layout="wide", page_icon="🏆")
    st.title("🏆 LLKK Champion Board")

    if "llkk_data" not in st.session_state:
        st.warning("Please upload data in the Home page first.")
        return

    # Ratings must be computed in BattleLog first
    if "final_scores" not in st.session_state:
        st.error("Please view the Battle Log first to initialize scores.")
        return

    results = st.session_state["final_scores"]
    results = results.sort_values("Total_Score", ascending=False).reset_index(drop=True)

    # Add rank & medal
    medals = ["🥇", "🥈", "🥉"]
    results["Rank"] = results.index + 1
    results["Medal"] = results["Rank"].apply(lambda x: medals[x-1] if x <= 3 else "")

    # Optional avatars — replace with your actual avatar image mapping
    avatar_map = {
        "Lab_A": "🧪",
        "Lab_B": "🔬",
        "Lab_C": "💉",
        "Lab_D": "⚗️",
        "Lab_E": "🧬"
    }
    results["Avatar"] = results["Lab"].map(avatar_map).fillna("🏷️")

    # Display
    for i, row in results.iterrows():
        with st.container():
            st.markdown(f"""
                <div style="background-color:#f0f2f6;padding:1rem;border-radius:1rem;margin-bottom:1rem;">
                    <h3>{row["Medal"]} {row["Avatar"]} <b>{row["Lab"]}</b></h3>
                    <ul>
                        <li><b>Rank:</b> {row["Rank"]}</li>
                        <li><b>Final Elo:</b> {row["Final_Elo"]}</li>
                        <li><b>Bonus:</b> {row["Bonus"]}</li>
                        <li><b>Penalty:</b> {row["Penalty"]}</li>
                        <li><b>Total Score:</b> <span style="color:green;"><b>{row["Total_Score"]}</b></span></li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)

    st.markdown(
        "<hr style='margin-top: 2rem; margin-bottom: 1rem;'>"
        "<div style='text-align: center; color: gray;'>"
        "🏰 LLKK — Lab Legend Kingdom Kvalis | Champions of Quality"
        "</div>",
        unsafe_allow_html=True
    )
