import streamlit as st
import pandas as pd
import os
import base64
from io import BytesIO

st.set_page_config(page_title="LLKK Dashboard", layout="wide", page_icon="🧝")
st.image("Header.png", use_container_width=True)

st.sidebar.success("Use the navigation sidebar to explore LLKK features")

# Upload Section
st.header("📂 Upload QC Data")
uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file:
    df_raw = pd.read_excel(uploaded_file)
    st.subheader("📄 Uploaded Preview")
    st.dataframe(df_raw)

    # Save to session state for use in other pages
    st.session_state["llkk_data"] = df_raw

# Footer
st.markdown(
    "<hr style='margin-top: 2rem; margin-bottom: 1rem;'>"
    "<div style='text-align: center; color: gray;'>"
    "© 2025 Lab Legend Kingdom Kvalis — Powered by MEQARE"
    "</div>",
    unsafe_allow_html=True
)
