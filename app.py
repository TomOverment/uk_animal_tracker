import streamlit as st
from pathlib import Path

from app_pages.prediction_page import render_prediction_page

st.set_page_config(page_title="UK Animal Tracker", layout="wide")

# Resolve logo path robustly (works locally + on Heroku)
ROOT = Path(__file__).resolve().parent
LOGO_PATH = ROOT / "assets" / "images" / "mamalian_tracker.png"

st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Prediction"], index=0)

if page == "Home":
    # Centered logo (above title)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if LOGO_PATH.exists():
            st.image(str(LOGO_PATH), use_container_width=True)
        else:
            st.warning(f"Logo not found at: {LOGO_PATH}")

    st.title("🐾 Mammalian Location Predictor")

    st.markdown(
        """
        **Understanding where mammal reporting activity occurs — and where it may increase next**

        This dashboard explores **UK mammal reporting data** to reveal spatial and temporal
        patterns in mammal observations and to estimate **future reporting activity**
        using data analytics and machine learning.
        """
    )

    st.info("Select a page from the sidebar to begin.")

else:
    render_prediction_page()
