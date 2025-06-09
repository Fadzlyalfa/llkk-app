import streamlit as st
import pandas as pd


def run():
    st.title("\U0001F4CB LLKK Direct Data Entry")

    num_rows = st.number_input("How many rows to enter:", min_value=1, max_value=50, value=4, step=1)

    labs = ["Lab_A", "Lab_B", "Lab_C"]
    parameters = ["Glucose", "Creatinine", "Cholesterol"]
    levels = ["L1", "L2"]
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    input_data = []
    for i in range(num_rows):
        cols = st.columns(6)
        lab = cols[0].selectbox(f"Lab {i+1}", labs, key=f"lab_{i}")
        parameter = cols[1].selectbox(f"Parameter {i+1}", parameters, key=f"param_{i}")
        level = cols[2].selectbox(f"Level {i+1}", levels, key=f"lvl_{i}")
        cv = cols[3].number_input(f"CV {i+1}", min_value=0.0, step=0.01, key=f"cv_{i}")
        n = cols[4].number_input(f"n {i+1}", min_value=0, step=1, key=f"n_{i}")
        wd = cols[5].number_input(f"Working Days {i+1}", min_value=1, step=1, key=f"wd_{i}")

        ratio = (n / wd) * 100 if wd > 0 else 0

        month = st.selectbox(f"Month {i+1}", months, key=f"m_{i}")

        input_data.append({
            "Lab": lab,
            "Parameter": parameter,
            "Level": level,
            "CV": round(cv, 2),
            "n": n,
            "Working Days": wd,
            "Ratio": round(ratio, 2),
            "Month": month
        })

    if st.button("Save to LLKK Session"):
        df = pd.DataFrame(input_data)
        st.session_state["llkk_data"] = df
        st.success("Data successfully saved to session.")
        st.dataframe(df, use_container_width=True)
