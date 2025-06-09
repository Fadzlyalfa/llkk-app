import streamlit as st
from PIL import Image
from Login import run_login  # Sidebar login

# ✅ Must be the first Streamlit command
st.set_page_config(page_title="LLKK - Lab Legend Kingdom Kvalis", layout="wide")

# 🔐 Run sidebar login
run_login()

# ❗ Stop unless logged in
if "logged_in_lab" not in st.session_state:
    st.warning("Please log in from the sidebar to access LLKK features.")
    st.stop()

# 🧠 Role-based sidebar menu
user_role = st.session_state.get("user_role", "lab")

if user_role == "admin":
    menu_options = ["Home", "Battle Log", "Champion", "Download", "Admin", "About", "Help"]
else:
    menu_options = ["Home", "Data Entry", "Battle Log", "Champion", "Download", "About", "Help"]

# 👑 Navigation
menu = st.sidebar.selectbox("🔍 Navigate LLKK Features", menu_options)

# 🚦 Routing Logic
if menu == "Home":
    st.success("Welcome to LLKK! Use the sidebar to explore features.")
    img = Image.open("Header.png")
    st.image(img, use_container_width=True)

elif menu == "Data Entry":
    from DataEntry import run as run_dataentry
    run_dataentry()

elif menu == "Battle Log":
    from BattleLog import run as run_battlelog
    run_battlelog()

elif menu == "Champion":
    from Champion import run as run_champion
    run_champion()

elif menu == "Download":
    from Download import run as run_download
    run_download()

elif menu == "Admin":
    from Admin import run as run_admin
    run_admin()

elif menu == "About":
    from About import run as run_about
    run_about()

elif menu == "Help":
    from Help import run as run_help
    run_help()
