import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Download", layout="wide", page_icon="📁")
st.title("📥 Download Final Elo Table")

if "llkk_data" not in st.session_state:
    st.warning("Please upload data in the Home page first.")
    st.stop()

# Dummy final Elo table (replace with actual results)
data = pd.DataFrame({
    "Lab": ["Lab_A", "Lab_B", "Lab_C"],
    "Final_Elo": [1524, 1490, 1486]
})

@st.cache_data

def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Final_Elo')
    return output.getvalue()

st.dataframe(data, use_container_width=True)
excel_data = to_excel(data)
st.download_button("📥 Download Excel File", data=excel_data, file_name="LLKK_Final_Elo.xlsx")

st.markdown(
    "<hr style='margin-top: 2rem; margin-bottom: 1rem;'>"
    "<div style='text-align: center; color: gray;'>"
    "© 2025 Lab Legend Kingdom Kvalis — Powered by MEQARE"
    "</div>",
    unsafe_allow_html=True
)
