import streamlit as st
import pandas as pd
from penalty import simulate_fadzly_algorithm  # ✅ Import the new function

def run():
    st.title("🛡️ Admin Control Center")

    if st.session_state.get("user_role") != "admin":
        st.warning("Access denied. This page is for admin only.")
        return

    # View all LLKK data
    if "llkk_data" in st.session_state:
        st.subheader("📋 All Submitted Data")
        st.dataframe(st.session_state["llkk_data"])
    else:
        st.info("No lab data submitted yet.")

    # Trigger Fadzly Algorithm with penalty
    st.subheader("⚔️ Simulate Battles Across All Labs")
    if st.button("🚀 Start Battle Simulation Now"):
        simulate_fadzly_algorithm(st.session_state["llkk_data"])  # ✅ Call from penalty.py
        st.success("✅ Battle simulation complete!")

    # Export CSV of full data
    if "llkk_data" in st.session_state:
        csv = st.session_state["llkk_data"].to_csv(index=False).encode("utf-8")
        st.download_button("📤 Download All Data", csv, "llkk_all_data.csv", "text/csv")

    # Reset all data (danger zone)
    st.subheader("🧨 Danger Zone")
    if st.button("❌ Clear All LLKK Data"):
        del st.session_state["llkk_data"]
        for key in ["fadzly_battles", "elo_history", "elo_progression"]:
            st.session_state.pop(key, None)
        st.success("All LLKK and battle data has been reset.")
