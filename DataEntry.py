# DataEntry.py

import streamlit as st
import pandas as pd
import numpy as np

def run():
    st.title("📋 LLKK Direct Data Entry")

    if "logged_in_lab" not in st.session_state:
        st.warning("Please log in from the sidebar to access data entry.")
        st.stop()

    # 🧹 Reset button in sidebar
    st.sidebar.markdown("### 🧹 Data Control")
    if st.sidebar.button("Reset All Data"):
        if "llkk_data" in st.session_state:
            del st.session_state["llkk_data"]
            st.success("✅ All LLKK data has been cleared.")
            st.rerun()

    lab = st.session_state["logged_in_lab"]
    
    # ✅ Updated parameter list (17 items, alphabetically sorted)
    parameters = [
        "Albumin",
        "Alanine Transaminase (ALT)",
        "Alkaline Phosphatase (ALP)",
        "Aspartate Transaminase (AST)",
        "Chloride (Cl⁻)",
        "Cholesterol",
        "Creatinine",
        "Direct Bilirubin",
        "Glucose",
        "HDL Cholesterol",
        "Potassium (K⁺)",
        "Sodium (Na⁺)",
        "Total Bilirubin",
        "Total Protein",
        "Triglycerides",
        "Urea",
        "Uric Acid"
    ]

    levels = ["L1", "L2"]
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    num_rows = st.number_input("🔢 How many entries to input?", 
                               min_value=1, max_value=50, value=5, step=1)

    input_data = []
    st.subheader(f"📝 Enter Data for: :green[{lab}]")

    headers = st.columns(7)
    headers[0].markdown("**Parameter**")
    headers[1].markdown("**Level**")
    headers[2].markdown("**Month**")
    headers[3].markdown("**CV (%)**")
    headers[4].markdown("**n (QC runs)**")
    headers[5].markdown("**Working Days**")
    headers[6].markdown("**Ratio**")

    for i in range(num_rows):
        cols = st.columns(7)
        parameter = cols[0].selectbox("", parameters, key=f"param_{i}")
        level = cols[1].selectbox("", levels, key=f"level_{i}")
        month = cols[2].selectbox("", months, key=f"month_{i}")
        cv = cols[3].number_input("", min_value=0.0, max_value=100.0, key=f"cv_{i}")
        n_qc = cols[4].number_input("", min_value=0, max_value=100, key=f"n_{i}")
        working_days = cols[5].number_input("", min_value=1, max_value=31, key=f"wd_{i}")
        ratio = round(n_qc / working_days, 2) if n_qc > 0 and working_days > 0 else 0.0
        cols[6].number_input("", value=ratio, disabled=True, key=f"ratio_{i}")

        input_data.append({
            "Lab": lab,
            "Parameter": parameter,
            "Level": level,
            "Month": month,
            "CV (%)": cv,
            "n (QC)": n_qc,
            "Working Days": working_days,
            "Ratio": ratio
        })

    df = pd.DataFrame(input_data)
    st.subheader("📊 Preview of Entered Data")
    st.dataframe(df)

    # Merge & deduplicate
    if "llkk_data" in st.session_state:
        existing = st.session_state["llkk_data"]
        combined = pd.concat([existing, df], ignore_index=True)
        combined = combined.drop_duplicates(subset=["Lab", "Parameter", "Level", "Month", "CV (%)", "n (QC)", "Working Days"])
        st.session_state["llkk_data"] = combined
    else:
        st.session_state["llkk_data"] = df

    # Export CSV
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download CSV", csv, "llkk_data_entry.csv", "text/csv")

    # ✅ Confirm Entry into Battlefield (no simulation)
    if st.button("⚔️ Submit to Battle"):
        st.success("🟢 You have entered the battlefield!")
