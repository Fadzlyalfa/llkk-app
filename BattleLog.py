import streamlit as st
import pandas as pd
import numpy as np

def run():
    st.title("⚔️ LLKK Battle Log")

    if "logged_in_lab" not in st.session_state:
        st.warning("Please log in from the sidebar to view battle logs.")
        st.stop()

    lab = st.session_state["logged_in_lab"]
    role = st.session_state.get("user_role", "lab")

    if "llkk_data" not in st.session_state:
        st.error("🚫 No data found. Please submit data through the Data Entry tab.")
        return

    df = st.session_state["llkk_data"]

    # Section 1 — Your Own Data
    st.markdown(f"### 🧾 `{lab}` Submission")
    lab_df = df[df["Lab"] == lab]

    if lab_df.empty:
        st.warning(f"⚠️ No data entries found yet for `{lab}`.")
    else:
        st.success(f"✅ Showing battle records for `{lab}`.")
        st.dataframe(lab_df)

        with st.expander("📊 Summary Stats"):
            summary = lab_df.groupby(["Parameter", "Level"]).agg({
                "CV (%)": ["mean", "min", "max"],
                "Ratio": ["mean", "min", "max"]
            }).round(2)
            st.dataframe(summary)

    # Section 2 — All Labs Combined
    st.markdown("### 🧩 All Labs Combined (for Battle Preview)")
    st.dataframe(df)

    with st.expander("📊 Overall Summary by Lab"):
        combined_summary = df.groupby("Lab").agg({
            "CV (%)": ["mean", "min", "max"],
            "Ratio": ["mean", "min", "max"]
        }).round(2)
        st.dataframe(combined_summary)

    # Section 3 — Admin-only Battle Trigger
    if role == "admin":
        st.markdown("---")
        st.subheader("🛡️ Admin Control Panel")
        if st.button("🛡️ Start Battle"):
            simulate_battles(df)
    else:
        st.info("🟢 Awaiting admin to start the battle simulation.")

# 🔁 Battle Simulation Logic (Fadzly Algorithm)
def simulate_battles(df):
    st.subheader("🏁 Battle Results")

    df = df.dropna(subset=["CV (%)", "n (QC)", "Working Days"])
    df["CV (%)"] = pd.to_numeric(df["CV (%)"], errors="coerce")
    df["n (QC)"] = pd.to_numeric(df["n (QC)"], errors="coerce")
    df["Working Days"] = pd.to_numeric(df["Working Days"], errors="coerce")

    df["BaseScore"] = (100 - df["CV (%)"]) * df["n (QC)"].pow(0.5) * (df["Working Days"] / 30)
    df["Bonus"] = df["Ratio"].apply(lambda x: 5 if x >= 1.0 else 0)
    df["Penalty"] = df[["Ratio", "CV (%)"]].isna().any(axis=1).astype(int) * -10
    df["TotalScore"] = df["BaseScore"] + df["Bonus"] + df["Penalty"]

    battle_results = []
    grouped = df.groupby(["Parameter", "Level", "Month"])

    for (param, level, month), group in grouped:
        valid = group.dropna(subset=["TotalScore"])
        if valid["Lab"].nunique() < 2:
            continue

        ranked = valid.sort_values("TotalScore", ascending=False).reset_index(drop=True)
        ranked["Rank"] = ranked["TotalScore"].rank(method="min", ascending=False).astype(int)
        ranked["Medal"] = ranked["Rank"].map({1: "🥇", 2: "🥈", 3: "🥉"})

        for _, row in ranked.iterrows():
            battle_results.append({
                "Lab": row["Lab"],
                "Parameter": param,
                "Level": level,
                "Month": month,
                "Total Score": round(row["TotalScore"], 2),
                "Rank": row["Rank"],
                "Medal": row.get("Medal", "")
            })

    if battle_results:
        battle_df = pd.DataFrame(battle_results)
        st.session_state["fadzly_battles"] = battle_df
        st.success("✅ Battle simulation completed!")
        st.dataframe(battle_df)
    else:
        st.info("🟢 You have entered the battlefield. Awaiting more labs for match-up.")
