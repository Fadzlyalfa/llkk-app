# DataEntry.py

import streamlit as st
import pandas as pd

def run():
    st.title("📋 LLKK Direct Data Entry")

    # Ensure login
    if "logged_in_lab" not in st.session_state:
        st.warning("Please log in from the sidebar to access data entry.")
        st.stop()

    # Get logged-in lab
    lab = st.session_state["logged_in_lab"]

    # Choices
    parameters = ["Glucose", "Creatinine", "Cholesterol"]
    levels = ["L1", "L2"]
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    # Number of entries
    num_rows = st.number_input("🔢 How many entries to input?", 
                               min_value=1, max_value=50, value=4, step=1)

    input_data = []
    st.subheader(f"📝 Enter Data for: `{lab}`")

    # Column headers
    headers = st.columns(8)
    headers[0].markdown("**Parameter**")
    headers[1].markdown("**Level**")
    headers[2].markdown("**Month**")
    headers[3].markdown("**CV (%)**")
    headers[4].markdown("**n (QC runs)**")
    headers[5].markdown("**Working Days**")
    headers[6].markdown("**Ratio**")
    headers[7].markdown("")

    for i in range(num_rows):
        cols = st.columns(8)
        parameter = cols[0].selectbox("", parameters, key=f"param_{i}")
        level = cols[1].selectbox("", levels, key=f"level_{i}")
        month = cols[2].selectbox("", months, key=f"month_{i}")
        cv = cols[3].number_input("", min_value=0.0, max_value=100.0, key=f"cv_{i}")
        n_qc = cols[4].number_input("", min_value=0, max_value=100, key=f"n_{i}")
        working_days = cols[5].number_input("", min_value=1, max_value=31, key=f"wd_{i}")
        
        ratio = round(n_qc / working_days, 2) if working_days > 0 else 0.0
        cols[6].markdown(f"**{ratio}**")

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

    # Convert to DataFrame
    df = pd.DataFrame(input_data)
    st.subheader("📊 Preview of Entered Data")
    st.dataframe(df)

    # Save to session state (append if previous data exists)
    if "llkk_data" in st.session_state:
        st.session_state["llkk_data"] = pd.concat([st.session_state["llkk_data"], df], ignore_index=True)
    else:
        st.session_state["llkk_data"] = df

    # Download option
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download CSV", csv, "llkk_data_entry.csv", "text/csv")
