# Login.py

import streamlit as st

# User database with roles
labs_users = {
    "admin": {"password": "admin123", "role": "admin"},
    "Lab_A": {"password": "a123", "role": "lab"},
    "Lab_B": {"password": "b123", "role": "lab"},
    "Lab_C": {"password": "c123", "role": "lab"}
}

def run_login():
    st.sidebar.title("🔐 Lab Login")

    # Form inputs
    username = st.sidebar.selectbox("Select Your Lab", list(labs_users.keys()))
    password = st.sidebar.text_input("Enter Password", type="password")

    if st.sidebar.button("Login"):
        user = labs_users.get(username)
        if user and user["password"] == password:
            st.session_state["logged_in_lab"] = username
            st.session_state["user_role"] = user["role"]
            st.session_state["login_success"] = True
            st.sidebar.success(f"Welcome, {username}!")
        else:
            st.session_state["login_success"] = False
            st.sidebar.error("❌ Incorrect password")

    # Show login state if logged in
    if "logged_in_lab" in st.session_state:
        st.sidebar.markdown(f"✅ Logged in as: `{st.session_state['logged_in_lab']}`")
        st.sidebar.markdown(f"🧩 Role: `{st.session_state['user_role']}`")
        if st.sidebar.button("Logout"):
            for key in ["logged_in_lab", "user_role", "login_success"]:
                st.session_state.pop(key, None)
            st.rerun()
