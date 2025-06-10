import streamlit as st
import pandas as pd
import numpy as np
import os

DATA_DIR = "data"

def run():
    st.title("📋 LLKK Direct Data Entry")

    if "logged_in_lab" not in st.session_state:
        st.warning("Please log in from the sidebar to access data entry.")
        st.stop()

    lab = st.session_state["logged_in_lab"]

    # Show previously submitted data
    file_path = os.path.join(DATA_DIR, f"submission_{lab}.csv")
    if os.path.exists(file_path):
        st.markdown("### 📂 Previously Submitted Data")
        prev_df = pd.read_csv(file_path)
        st.dataframe(prev_df)

    parameters = sorted([
        "Albumin", "ALT", "AST", "Bilirubin (Total)", "Cholesterol",
        "Creatinine", "Direct Bilirubin", "GGT", "Glucose", "HDL Cholesterol",
        "LDL Cholesterol", "Potassium", "Protein (Total)", "Sodium",
        "Triglycerides", "Urea", "Uric Acid"
    ])
    levels = ["L1", "L2"]
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    num_rows = st.number_input("🔢 How many entries to input?", min_value=1, max_value=50, value=5, step=1)

    st.subheader(f"📝 Enter Data for: :green[{lab}]")

    input_data = []
    for i in range(num_rows):
        cols = st.columns(7)
        parameter = cols[0].selectbox("Parameter", parameters, key=f"param_{i}")
        level = cols[1].selectbox("Level", levels, key=f"level_{i}")
        month = cols[2].selectbox("Month", months, key=f"month_{i}")
        cv = cols[3].number_input("CV (%)", min_value=0.0, max_value=100.0, key=f"cv_{i}")
        n_qc = cols[4].number_input("n (QC)", min_value=0, max_value=100, key=f"n_{i}")
        wd = cols[5].number_input("Working Days", min_value=1, max_value=31, key=f"wd_{i}")
        ratio = round(n_qc / wd, 2) if n_qc > 0 and wd > 0 else 0.0
        cols[6].number_input("Ratio", value=ratio, disabled=True, key=f"ratio_{i}")

        input_data.append({
            "Lab": lab,
            "Parameter": parameter,
            "Level": level,
            "Month": month,
            "CV (%)": cv,
            "n (QC)": n_qc,
            "Working Days": wd,
            "Ratio": ratio
        })

    df = pd.DataFrame(input_data)
    df = df[(df["CV (%)"] > 0) & (df["n (QC)"] > 0) & (df["Working Days"] > 0)]

    st.subheader("📊 Preview of Valid Entries")
    st.dataframe(df)

    # Save lab data to individual file
    if not df.empty:
        os.makedirs(DATA_DIR, exist_ok=True)
        file_path = os.path.join(DATA_DIR, f"submission_{lab}.csv")
        df.to_csv(file_path, index=False)
        st.success(f"✅ Data saved successfully for {lab}!")

    # Export single CSV (optional)
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📅 Download CSV", csv, "llkk_data_entry.csv", "text/csv")

    if st.button("⚔️ Submit to Battle"):
        st.success("🟢 You have entered the battlefield!")
