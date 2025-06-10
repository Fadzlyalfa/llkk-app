# Download.py

import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Download", layout="wide", page_icon="📁")
st.title("📥 Download Final Elo Table")

if "fadzly_battles" not in st.session_state:
    st.warning("⚠️ No battle results found. Please run the simulation first from the Admin tab.")
    st.stop()

data = st.session_state["fadzly_battles"]

# Preview in app
st.subheader("📊 Preview of Final Rankings")
st.dataframe(data, use_container_width=True)

# Excel conversion
def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='LLKK_Final_Elo')
    return output.getvalue()

excel_data = to_excel(data)
csv_data = data.to_csv(index=False).encode("utf-8")

# Download buttons
st.download_button("📥 Download Excel File", data=excel_data, file_name="LLKK_Final_Elo.xlsx")
st.download_button("📥 Download CSV File", data=csv_data, file_name="LLKK_Final_Elo.csv", mime="text/csv")

# Footer
st.markdown("<hr style='margin-top: 2rem; margin-bottom: 1rem;'>"
            "<div style='text-align: center; color: gray;'>"
            "© 2025 Lab Legend Kingdom Kvalis — Powered by MEQARE"
            "</div>", unsafe_allow_html=True)
