import streamlit as st
import pandas as pd
from PIL import Image

# Set Streamlit config (must be first)
st.set_page_config(page_title="LLKK - Lab Legend Kingdom Kvalis", layout="wide")

# Sidebar menu
menu = st.sidebar.selectbox(
    "🔍 Navigate LLKK Features",
    ["Home", "Battle Log", "Champion", "Download", "About", "Help"]
)

# --- ROUTER ---
if menu == "Home":
    def run():
        # Display image header
        st.image("Header.png", use_column_width=True)

        st.header("📤 Upload Your LLKK Excel Data")
        st.caption("Upload `.xlsx` file")

        uploaded_file = st.file_uploader(
            "Drag and drop file here",
            type=["xlsx"],
            label_visibility="collapsed"
        )

        if uploaded_file:
            try:
                df = pd.read_excel(uploaded_file)

                # Standardize column names
                df.columns = df.columns.str.strip().str.title()

                # Store in session_state for global access
                st.session_state.llkk_data = df

                st.success("✅ File uploaded successfully!")
                st.markdown("### 👁️ Uploaded Preview")
                st.dataframe(df, use_container_width=True)

            except Exception as e:
                st.error(f"❌ Error reading file: {e}")

        # Footer
        st.markdown(
            "<hr style='margin-top: 2rem; margin-bottom: 1rem;'>"
            "<div style='text-align: center; color: gray;'>"
            "© 2025 Lab Legend Kingdom Kvalis — Powered by MEQARE"
            "</div>",
            unsafe_allow_html=True
        )

    run()

elif menu == "Battle Log":
    from BattleLog import run as run_battlelog
    run_battlelog()

elif menu == "Champion":
    from Champion import run as run_champion
    run_champion()

elif menu == "Download":
    from Download import run as run_download
    run_download()

elif menu == "About":
    from About import run as run_about
    run_about()

elif menu == "Help":
    from Help import run as run_help
    run_help()
