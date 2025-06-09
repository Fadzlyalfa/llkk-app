import streamlit as st
from PIL import Image

st.set_page_config(page_title="LLKK - Lab Legend Kingdom Kvalis", layout="wide")

# Sidebar navigation
menu = st.sidebar.selectbox(
    "🔍 Navigate LLKK Features",
    ["Home", "Data Entry", "Battle Log", "Champion", "Download", "About", "Help"]
)

# --- ROUTING LOGIC ---
if menu == "Home":
    def run():
        st.success("Use the navigation sidebar to explore LLKK features")
        try:
            img = Image.open("Header.png")
            st.image(img, use_column_width=True)
        except:
            st.warning("Header image not found.")
    run()

elif menu == "Data Entry":
    import pandas as pd
    st.subheader("🧾 LLKK Direct Data Entry")

    # Initialize session state for LLKK data
    if "llkk_data" not in st.session_state:
        st.session_state.llkk_data = pd.DataFrame(columns=["Lab", "Parameter", "Level", "Cv", "Ratio", "Month"])

    # Define options
    labs = ["Lab_A", "Lab_B", "Lab_C", "Lab_D"]
    parameters = ["Glucose", "Creatinine", "Urea", "Cholesterol"]
    levels = ["L1", "L2"]
    months = ["Jan", "Feb", "Mar", "Apr", "May"]

    with st.form("llkk_entry_form"):
        num_rows = st.number_input("How many rows to enter:", min_value=1, max_value=20, value=5)

        entries = []
        for i in range(num_rows):
            cols = st.columns(6)
            row = {
                "Lab": cols[0].selectbox(f"Lab {i+1}", labs, key=f"lab_{i}"),
                "Parameter": cols[1].selectbox(f"Parameter {i+1}", parameters, key=f"param_{i}"),
                "Level": cols[2].selectbox(f"Level {i+1}", levels, key=f"level_{i}"),
                "Cv": cols[3].number_input(f"CV {i+1}", key=f"cv_{i}"),
                "Ratio": cols[4].number_input(f"Ratio {i+1}", key=f"ratio_{i}"),
                "Month": cols[5].selectbox(f"Month {i+1}", months, key=f"month_{i}")
            }
            entries.append(row)

        submitted = st.form_submit_button("✅ Submit to LLKK System")

        if submitted:
            new_data = pd.DataFrame(entries)
            st.session_state.llkk_data = pd.concat([st.session_state.llkk_data, new_data], ignore_index=True)
            st.success("Data submitted successfully!")

    # Show current data
    total_rows = len(st.session_state.llkk_data)
    if total_rows > 0:
        st.subheader(f"📊 Current Submitted Data ({total_rows} rows)")
        st.dataframe(st.session_state.llkk_data, use_container_width=True)
    else:
        st.info("No data submitted yet.")

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
