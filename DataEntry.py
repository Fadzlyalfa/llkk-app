# DataEntry.py

import streamlit as st
import pandas as pd

def run():
    st.title("📋 LLKK Direct Data Entry")

    # Step 1: Define choices
    labs = ["Lab_A", "Lab_B", "Lab_C"]
    parameters = ["Glucose", "Creatinine", "Cholesterol"]
    levels = ["L1", "L2"]
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    # Step 2: Ask how many rows to enter
    num_rows = st.number_input("🔢 How many entries to input?", 
                               min_value=1, max_value=50, value=4, step=1)

    # Step 3: Data entry loop
    input_data = []
    st.subheader("📝 Enter Your Data")
    for i in range(num_rows):
        cols = st.columns(6)
        lab = cols[0].selectbox(f"Lab {i+1}", labs, key=f"lab_{i}")
        parameter = cols[1].selectbox(f"Parameter {i+1}", parameters, key=f"param_{i}")
        level = cols[2].selectbox(f"Level {i+1}", levels, key=f"level_{i}")
        month = cols[3].selectbox(f"Month {i+1}", months, key=f"month_{i}")
        cv = cols[4].number_input(f"CV {i+1} (%)", min_value=0.0, max_value=100.0, key=f"cv_{i}")
        ratio = cols[5].number_input(f"Ratio {i+1}", min_value=0.0, max_value=10.0, key=f"ratio_{i}")

        input_data.append({
            "Lab": lab,
            "Parameter": parameter,
            "Level": level,
            "Month": month,
            "CV (%)": cv,
            "Ratio": ratio
        })

    # Step 4: Convert to DataFrame and display
    df = pd.DataFrame(input_data)
    st.subheader("📊 Preview of Entered Data")
    st.dataframe(df)

    # Step 5: Optionally save/export
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download CSV", csv, "llkk_data_entry.csv", "text/csv")

