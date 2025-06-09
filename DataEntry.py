# DataEntry.py

import streamlit as st
import pandas as pd

def run():
    st.title("📋 LLKK Direct Data Entry")

    # Choices
    labs = ["Lab_A", "Lab_B", "Lab_C"]
    parameters = ["Glucose", "Creatinine", "Cholesterol"]
    levels = ["L1", "L2"]
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    # Number of entries
    num_rows = st.number_input("🔢 How many entries to input?", 
                               min_value=1, max_value=50, value=4, step=1)

    input_data = []
    st.subheader("📝 Enter Your Data")

    # 🧾 Column headers (only once)
    headers = st.columns(8)
    headers[0].markdown("**Lab**")
    headers[1].markdown("**Parameter**")
    headers[2].markdown("**Level**")
    headers[3].markdown("**Month**")
    headers[4].markdown("**CV (%)**")
    headers[5].markdown("**n (QC runs)**")
    headers[6].markdown("**Working Days**")
    headers[7].markdown("**Ratio**")

    for i in range(num_rows):
        cols = st.columns(8)
        lab = cols[0].selectbox("", labs, key=f"lab_{i}")
        parameter = cols[1].selectbox("", parameters, key=f"param_{i}")
        level = cols[2].selectbox("", levels, key=f"level_{i}")
        month = cols[3].selectbox("", months, key=f"month_{i}")
        cv = cols[4].number_input("", min_value=0.0, max_value=100.0, key=f"cv_{i}")
        n_qc = cols[5].number_input("", min_value=0, max_value=100, key=f"n_{i}")
        working_days = cols[6].number_input("", min_value=1, max_value=31, key=f"wd_{i}")
        
        # Auto calculate ratio
        ratio = round(n_qc / working_days, 2) if working_days > 0 else 0.0
        cols[7].markdown(f"**{ratio}**")

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

    # Preview table
    df = pd.DataFrame(input_data)
    st.subheader("📊 Preview of Entered Data")
    st.dataframe(df)

    # Download as CSV
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download CSV", csv, "llkk_data_entry.csv", "text/csv")
