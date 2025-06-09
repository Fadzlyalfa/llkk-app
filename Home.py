import streamlit as st
from PIL import Image

# Set config first
st.set_page_config(page_title="LLKK - Lab Legend Kingdom Kvalis", layout="wide")

# Sidebar navigation
menu = st.sidebar.selectbox(
    "🔍 Navigate LLKK Features",
    ["Home", "Battle Log", "Champion", "Download", "About", "Help", "Data Entry"]
)

# --- Routing ---
if menu == "Home":
    st.success("Use the navigation sidebar to explore LLKK features")
    img = Image.open("Header.png")
    st.image(img, use_container_width=True)

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

elif menu == "Data Entry":
    from DataEntry import run as run_dataentry
    run_dataentry()

# Footer
st.markdown(
    """
    <hr style='margin-top: 2rem; margin-bottom: 1rem;'>
    <div style='text-align: center; color: gray;'>
    © 2025 Lab Legend Kingdom Kvalis — Powered by MEQARE
    </div>
    """,
    unsafe_allow_html=True
)
