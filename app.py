# app.py
import streamlit as st

st.set_page_config(page_title="UK Animal Tracker", layout="wide")

# -----------------------------
# CENTERED LOGO
# -----------------------------
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image(
        "assets/images/mamalian_tracker.png",
        use_container_width=True
    )

st.title("UK Animal Tracker")

st.markdown(
    """
    **Understanding where mammal reporting activity occurs — and where it may increase next**

    This dashboard explores **UK mammal reporting data** to reveal spatial and temporal
    patterns in mammal observations and to estimate **future reporting activity**
    using data analytics and machine learning.

    Use the **sidebar navigation** to explore:
    - Mammal engagement patterns
    - Spatial and temporal trends
    - Predictive modelling results
    """
)

st.info("Select a page from the sidebar to begin.")
