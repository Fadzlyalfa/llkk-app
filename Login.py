# Login.py

import streamlit as st

# Dummy user database
labs_users = {
    "Lab_A": "a123",
    "Lab_B": "b123",
    "Lab_C": "c123"
}

def run_login():
    st.sidebar.title("🔐 Lab Login")

    # Show login form
    username = st.sidebar.selectbox("Select Your Lab", list(labs_users.keys()))
    password = st.sidebar.text_input("Enter Password", type="password")

    if st.sidebar.button("Login"):
        if labs_users.get(username) == password:
            st.session_state["logged_in_lab"] = username
            st.session_state["login_success"] = True
            st.sidebar.success(f"Welcome, {username}!")
        else:
            st.session_state["login_success"] = False
            st.sidebar.error("❌ Incorrect password")

    # If already logged in
    if "logged_in_lab" in st.session_state:
        st.sidebar.markdown(f"✅ Logged in as: `{st.session_state['logged_in_lab']}`")
        if st.sidebar.button("Logout"):
            del st.session_state["logged_in_lab"]
            st.rerun()
