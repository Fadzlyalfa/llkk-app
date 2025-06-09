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

    # Number of rows
    num_rows = st.number_input("🔢 How many entries to input?", 
                               min_value=1, max_value=50, value=4, step=1)

    input_data = []
    st.subheader("📝 Enter Your Data")

    for i in range(num_rows):
        cols = st.columns(8)
        lab = cols[0].selectbox(f"Lab {i+1}", labs, key=f"lab_{i}")
        parameter = cols[1].selectbox(f"Parameter {i+1}", parameters, key=f"param_{i}")
        level = cols[2].selectbox(f"Level {i+1}", levels, key=f"level_{i}")
        month = cols[3].selectbox(f"Month {i+1}", months, key=f"month_{i}")
        cv = cols[4].number_input(f"CV {i+1} (%)", min_value=0.0, max_value=100.0, key=f"cv_{i}")
        n_qc = cols[5].number_input(f"n (QC runs) {i+1}", min_value=0, max_value=100, key=f"n_{i}")
        working_days = cols[6].number_input(f"Working Days {i+1}", min_value=1, max_value=31, key=f"wd_{i}")
        
        # Auto-calculate ratio
        ratio = round(n_qc / working_days, 2) if working_days > 0 else 0.0
        cols[7].markdown(f"**Ratio: {ratio}**")

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

    # Output table
    df = pd.DataFrame(input_data)
    st.subheader("📊 Preview of Entered Data")
    st.dataframe(df)

    # Download
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download CSV", csv, "llkk_data_entry.csv", "text/csv")
