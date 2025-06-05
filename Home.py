import streamlit as st
from PIL import Image
import pandas as pd

# Configure page
st.set_page_config(page_title="LLKK - Lab Legend Kingdom Kvalis", layout="wide")

# Sidebar navigation
menu = st.sidebar.selectbox(
    "🔍 Navigate LLKK Features",
    ["Home", "Battle Log", "Champion", "Download", "About", "Help"]
)

# --- ROUTING LOGIC ---
if menu == "Home":
    def run():
        st.success("Use the navigation sidebar to explore LLKK features")

        # Header Image
        img = Image.open("Header.png")
        st.image(img, use_container_width=True)

        # File uploader
        st.markdown("### 📤 Upload Your LLKK Excel Data")
        uploaded_file = st.file_uploader("Upload .xlsx file", type=["xlsx"])
        
        if uploaded_file is not None:
            try:
                df = pd.read_excel(uploaded_file)
                st.session_state["llkk_data"] = df  # Save to session state
                st.success("✅ File uploaded successfully!")

                # Preview
                st.markdown("### 👁️ Uploaded Preview")
                st.dataframe(df, use_container_width=True)

            except Exception as e:
                st.error(f"Error reading file: {e}")

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
