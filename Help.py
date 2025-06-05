import streamlit as st

st.set_page_config(page_title="Help", layout="wide", page_icon="❓")
st.title("❓ How to Use LLKK")

st.markdown("""
### Step-by-Step Guide

1. **Go to the Home page**
   - Upload your monthly QC Excel file.
   - Make sure your columns include: Lab, Parameter, Level, CV.

2. **View Battle Log**
   - Shows detailed matchups between labs for each parameter.
   - Uses CV values to determine winners.

3. **Check Champion**
   - See who won the month based on highest final Elo rating.
   - Bonus/penalty logic is automatically applied.

4. **Download Results**
   - Export the final Elo ranking table in Excel format.

5. **Read About Page**
   - Understand the philosophy and structure behind LLKK.

### Notes
- Missing data will be penalized by -10 points per field.
- Only valid data contributes to ranking.
- Streamlit session resets on page reload. Re-upload if needed.

Still need help? Contact MEQARE support.
""", unsafe_allow_html=True)

st.markdown("<hr style='margin-top: 2rem; margin-bottom: 1rem;'>"
            "<div style='text-align: center; color: gray;'>"
            "© 2025 Lab Legend Kingdom Kvalis — Powered by MEQARE"
            "</div>", unsafe_allow_html=True)
