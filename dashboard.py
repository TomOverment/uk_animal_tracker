import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

@st.cache_data
def load_data():
    return pd.read_csv("inputs/Data resource - National Mammal Atlas Project.csv")

def scatter_plot(df: pd.DataFrame):
    st.subheader("Scatter plot")

    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    if len(numeric_cols) < 2:
        st.info("Need at least 2 numeric columns for a scatter plot.")
        return

    x_col = st.selectbox("X axis", numeric_cols, index=0)
    y_col = st.selectbox("Y axis", numeric_cols, index=1)

    color_options = ["(none)"] + df.columns.tolist()
    color_col = st.selectbox("Color (optional)", color_options, index=0)
    color_col = None if color_col == "(none)" else color_col

    fig = px.scatter(df, x=x_col, y=y_col, color=color_col)
    st.plotly_chart(fig, use_container_width=True)

def stacked_bar(df: pd.DataFrame):
    st.subheader("Stacked bar chart")

    # Choose two categorical columns
    cat_cols = df.select_dtypes(exclude="number").columns.tolist()
    if len(cat_cols) < 2:
        st.info("Need at least 2 non-numeric (categorical) columns for a stacked bar chart.")
        return

    col_a = st.selectbox("Group by (x-axis)", cat_cols, index=0)
    col_b = st.selectbox("Stack by (legend)", cat_cols, index=1)

    ctab = pd.crosstab(df[col_a], df[col_b])

    fig, ax = plt.subplots()
    ctab.plot(kind="bar", stacked=True, ax=ax)
    ax.set_xlabel(col_a)
    ax.set_ylabel("Count")
    ax.set_title(f"Counts of {col_b} within {col_a}")
    st.pyplot(fig)

def parallel_coordinates(df: pd.DataFrame):
    st.subheader("Parallel coordinates")

    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    if len(numeric_cols) < 2:
        st.info("Need numeric columns for a parallel coordinates plot.")
        return

    color_options = ["(none)"] + df.columns.tolist()
    color_col = st.selectbox("Color by (optional)", color_options, index=0)
    color_col = None if color_col == "(none)" else color_col

    dims = st.multiselect(
        "Dimensions (numeric columns)",
        options=numeric_cols,
        default=numeric_cols[:6] if len(numeric_cols) >= 6 else numeric_cols
    )

    if len(dims) < 2:
        st.warning("Select at least 2 dimensions.")
        return

    plot_df = df[dims + ([color_col] if color_col else [])].dropna()

    if color_col and plot_df[color_col].dtype.kind in "biufc":
        fig = px.parallel_coordinates(plot_df, dimensions=dims, color=color_col)
    else:
        fig = px.parallel_coordinates(plot_df, dimensions=dims)

    st.plotly_chart(fig, use_container_width=True)

def dashboard_body():
    st.title("Mammal Dashboard")

    df = load_data()
    st.caption(f"Rows: {len(df):,} | Columns: {df.shape[1]}")
    st.dataframe(df, use_container_width=True)

    st.sidebar.header("Charts")
    chart = st.sidebar.radio(
        "Select a chart",
        ["Scatter", "Stacked bar", "Parallel coordinates"],
        index=0
    )

    if chart == "Scatter":
        scatter_plot(df)
    elif chart == "Stacked bar":
        stacked_bar(df)
    else:
        parallel_coordinates(df)

if __name__ == "__main__":
    dashboard_body()
