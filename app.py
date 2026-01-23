import streamlit as st
from pathlib import Path

st.set_page_config(page_title="UK Animal Tracker", layout="wide")

ROOT = Path(__file__).resolve().parent
LOGO_PATH = ROOT / "assets" / "images" / "mamalian_tracker.png"

# Centered logo
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

st.info("Use the left sidebar to open the Prediction page.")
