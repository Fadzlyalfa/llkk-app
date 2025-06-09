# --- BattleLog.py ---
import streamlit as st
import pandas as pd


def run():
    st.set_page_config(page_title="Battle Log", layout="wide", page_icon="⚔️")
    st.title("⚔️ LLKK Battle Log")

    if "llkk_data" not in st.session_state:
        st.warning("Please upload data in the Home page or enter it in the Data Entry page.")
        return

    df = st.session_state["llkk_data"]

    required_columns = ["Lab", "Parameter", "Level", "CV", "Ratio", "Month"]
    if not all(col in df.columns for col in required_columns):
        st.error("Missing required columns. Required: Level, Cv, Ratio, Parameter, Lab, Month")
        return

    battle_results = []

    for (param, level, month), group in df.groupby(["Parameter", "Level", "Month"]):
        labs = group["Lab"].unique()
        for i in range(len(labs)):
            for j in range(i + 1, len(labs)):
                lab1 = labs[i]
                lab2 = labs[j]

                cv1 = group[group["Lab"] == lab1]["CV"].mean()
                cv2 = group[group["Lab"] == lab2]["CV"].mean()

                if pd.isna(cv1) or pd.isna(cv2):
                    continue

                winner = lab1 if cv1 < cv2 else lab2 if cv2 < cv1 else "Draw"

                delta1 = round(abs(cv2 - cv1) * 2, 2) if winner != "Draw" else 0
                delta2 = -delta1 if winner != "Draw" else 0

                battle_results.append({
                    "Parameter": f"{param}_{level}_{month}",
                    "Lab_1": lab1,
                    "Lab_2": lab2,
                    "CV_1": round(cv1, 2),
                    "CV_2": round(cv2, 2),
                    "Winner": winner,
                    "Δ_Lab_1": delta1 if winner == lab1 else delta2 if winner == lab2 else 0,
                    "Δ_Lab_2": delta2 if winner == lab1 else delta1 if winner == lab2 else 0
                })

    battle_df = pd.DataFrame(battle_results)

    if battle_df.empty:
        st.info("No battles were generated from the data.")
    else:
        st.dataframe(battle_df, use_container_width=True)

    st.markdown(
        """
        <hr style='margin-top: 2rem; margin-bottom: 1rem;'>
        <div style='text-align: center; color: gray;'>
        © 2025 Lab Legend Kingdom Kvalis — Powered by MEQARE
        </div>
        """,
        unsafe_allow_html=True
    )


# --- Champion.py ---
import streamlit as st
import pandas as pd


def run():
    st.set_page_config(page_title="Champion", layout="wide", page_icon="🌟")
    st.title("🏆 LLKK Champion Board")

    if "llkk_data" not in st.session_state:
        st.warning("Please upload or enter data first.")
        return

    df = st.session_state["llkk_data"]

    if not all(col in df.columns for col in ["Lab", "CV"]):
        st.error("Missing required columns. 'Lab' and 'CV' must be present.")
        return

    # Average CV per Lab (lower is better)
    avg_cv = df.groupby("Lab")["CV"].mean().reset_index()
    avg_cv.columns = ["Lab", "Average_CV"]
    avg_cv["Rank"] = avg_cv["Average_CV"].rank(method="min", ascending=True).astype(int)

    # Display
    st.dataframe(avg_cv.sort_values("Rank"), use_container_width=True)

    st.markdown(
        """
        <hr style='margin-top: 2rem; margin-bottom: 1rem;'>
        <div style='text-align: center; color: gray;'>
        © 2025 Lab Legend Kingdom Kvalis — Powered by MEQARE
        </div>
        """,
        unsafe_allow_html=True
    )
