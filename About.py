import streamlit as st

st.set_page_config(page_title="About LLKK", layout="wide", page_icon="ℹ️")
st.title("ℹ️ About Lab Legend Kingdom Kvalis")

st.markdown("""
## What is LLKK?

**Lab Legend Kingdom Kvalis (LLKK)** is a gamified Quality Control (QC) evaluation platform developed under the MEQARE initiative.
It uses a modified **Elo rating system** to rank laboratories based on their analytical performance.

Each lab submits monthly QC results, which are then compared in simulated 'battles' where lower Coefficient of Variation (CV) wins.

## Features:
- Monthly CV-based battles between labs
- Elo-based ranking system with bonuses and penalties
- Intuitive dashboards, champion highlights, and exportable results

## Purpose:
To promote continuous improvement, transparency, and engagement in laboratory performance monitoring — turning QC into a competitive and rewarding journey.

## Developed by:
MEQARE, Malaysia's EQA innovation hub.
""", unsafe_allow_html=True)

st.markdown("<hr style='margin-top: 2rem; margin-bottom: 1rem;'>"
            "<div style='text-align: center; color: gray;'>"
            "© 2025 Lab Legend Kingdom Kvalis — Powered by MEQARE"
            "</div>", unsafe_allow_html=True)
