import plotly.express as px
from pathlib import Path
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Mammals Dashboard", layout="wide")
st.title("UK Mammal Engagement Dashboard")

# -----------------------------
# PATHS / CONFIG
# -----------------------------
ROOT = Path(__file__).resolve().parents[1]
CLEAN_PATH = ROOT / "jupyter_notebooks" / "outputs" / "mammal_atlas_cleaned.csv"
TOP_AREAS = 300

# -----------------------------
# DATA LOADING
# -----------------------------
@st.cache_data
def load_clean_data() -> pd.DataFrame:
    if not CLEAN_PATH.exists():
        st.error(f"Cleaned dataset not found at: {CLEAN_PATH}")
        st.stop()
    df = pd.read_csv(CLEAN_PATH)
    df.columns = df.columns.str.strip()
    return df


@st.cache_data
def build_plot_df(df: pd.DataFrame) -> pd.DataFrame:
    area_group_counts = (
        df.groupby(["Area Code", "Mammal Group"])
        .size()
        .reset_index(name="group_count")
    )

    area_totals = (
        df.groupby("Area Code")
        .size()
        .reset_index(name="area_total")
    )

    top_group_per_area = (
        area_group_counts
        .sort_values(["Area Code", "group_count"], ascending=[True, False])
        .groupby("Area Code", as_index=False)
        .first()
    )

    top_group_per_area = top_group_per_area.merge(area_totals, on="Area Code")
    top_group_per_area["top_share"] = top_group_per_area["group_count"] / top_group_per_area["area_total"]

    centroids = (
        df.groupby("Area Code")[["Latitude (WGS84)", "Longitude (WGS84)"]]
        .mean()
        .reset_index()
        .rename(columns={"Latitude (WGS84)": "area_lat", "Longitude (WGS84)": "area_lon"})
    )

    return top_group_per_area.merge(centroids, on="Area Code")


@st.cache_data
def build_top5_commonnames_per_area(df: pd.DataFrame, top_n: int = 5) -> pd.DataFrame:
    """
    Returns a DataFrame: Area Code -> hover string listing top N Common names with counts.
    Requires columns: 'Area Code' and 'Common name'.
    """
    if "Common name" not in df.columns:
        return pd.DataFrame({"Area Code": [], "Top 5 species": []})

    tmp = (
        df.dropna(subset=["Area Code", "Common name"])
        .groupby(["Area Code", "Common name"])
        .size()
        .reset_index(name="count")
        .sort_values(["Area Code", "count"], ascending=[True, False])
    )

    tmp["rank"] = tmp.groupby("Area Code")["count"].rank(method="first", ascending=False)
    tmp = tmp[tmp["rank"] <= top_n]

    hover_df = (
        tmp.groupby("Area Code")
        .apply(lambda g: "<br>".join([f"{r['Common name']}: {int(r['count']):,}" for _, r in g.iterrows()]))
        .reset_index(name="Top 5 species")
    )

    return hover_df


# -----------------------------
# CHARTS
# -----------------------------
def group_pie_chart(df: pd.DataFrame, top_n: int = 5):
    """
    Pie chart of Mammal Groups.
    Hover shows top N Common names within each group (if 'Common name' exists).
    """
    if "Mammal Group" not in df.columns:
        st.error("Missing required column: 'Mammal Group'")
        return

    group_counts = (
        df["Mammal Group"]
        .value_counts()
        .rename_axis("Mammal Group")
        .reset_index(name="Record Count")
    )

    # Default hover text
    group_counts["Top Common names"] = "Top common names unavailable"

    # Add top common names if available
    if "Common name" in df.columns:
        top_species = (
            df.dropna(subset=["Mammal Group", "Common name"])
            .groupby(["Mammal Group", "Common name"])
            .size()
            .reset_index(name="count")
            .sort_values(["Mammal Group", "count"], ascending=[True, False])
        )

        top_species["rank"] = top_species.groupby("Mammal Group")["count"].rank(method="first", ascending=False)
        top_species = top_species[top_species["rank"] <= top_n]

        hover_map = (
            top_species.groupby("Mammal Group")
            .apply(lambda g: "<br>".join([f"{r['Common name']}: {int(r['count']):,}" for _, r in g.iterrows()]))
            .to_dict()
        )

        group_counts["Top Common names"] = group_counts["Mammal Group"].map(hover_map).fillna("No common-name data")

    fig = px.pie(
        group_counts,
        values="Record Count",
        names="Mammal Group",
        title="Mammal Groups (Record Share)"
    )

    fig.update_traces(
        textposition="inside",
        textinfo="percent+label",
        hovertemplate=(
            "<b>%{label}</b><br>"
            "Records: %{value:,}<br>"
            "Share: %{percent}<br><br>"
            "<b>Top Common names</b><br>%{customdata[0]}"
            "<extra></extra>"
        ),
        customdata=group_counts[["Top Common names"]].values
    )

    st.plotly_chart(fig, use_container_width=True)


# -----------------------------
# PAGES
# -----------------------------
def page_overview(df: pd.DataFrame):
    st.subheader("Dataset Overview")
    st.caption(f"Rows: {len(df):,} | Columns: {df.shape[1]}")
    st.dataframe(df.head(200), use_container_width=True)

    if "Start date year" in df.columns:
        year_counts = df["Start date year"].value_counts().sort_index().reset_index()
        year_counts.columns = ["Year", "Records"]
        fig = px.line(year_counts, x="Year", y="Records", title="Records by Year (Cleaned Data)")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Column 'Start date year' not found in the cleaned dataset.")


def page_map(df: pd.DataFrame):
    st.subheader("Dominant Mammal Group Map")

    required = {"Area Code", "Mammal Group", "Latitude (WGS84)", "Longitude (WGS84)"}
    missing = required - set(df.columns)
    if missing:
        st.error(f"Missing required columns for map: {sorted(missing)}")
        return

    plot_df = build_plot_df(df)

    # --- ADD: Top 5 Common names per area for hover ---
    top5_df = build_top5_commonnames_per_area(df, top_n=5)
    plot_df = plot_df.merge(top5_df, on="Area Code", how="left")
    plot_df["Top 5 species"] = plot_df["Top 5 species"].fillna("No common-name data")

    plot_df_top = plot_df.sort_values("area_total", ascending=False).head(TOP_AREAS)

    fig = px.scatter_mapbox(
        plot_df_top,
        lat="area_lat",
        lon="area_lon",
        size="area_total",
        color="Mammal Group",
        hover_name="Area Code",  # shows as the header line in hover
        zoom=4,
        center={"lat": 54.5, "lon": -3},
        height=650,
        title=f"Dominant Mammal Group per Area Code — Top {TOP_AREAS} Areas",
    )

    # Custom hover panel (includes Top 5 species)
    fig.update_traces(
        customdata=plot_df_top[["Mammal Group", "group_count", "area_total", "top_share", "Top 5 species"]].values,
        hovertemplate=(
            "<b>Area:</b> %{hovertext}<br>"
            "<b>Dominant group:</b> %{customdata[0]}<br>"
            "<b>Dominant group records:</b> %{customdata[1]:,}<br>"
            "<b>Total records (area):</b> %{customdata[2]:,}<br>"
            "<b>Dominant share:</b> %{customdata[3]:.1%}<br><br>"
            "<b>Top 5 species (Common name)</b><br>%{customdata[4]}"
            "<extra></extra>"
        )
    )

    fig.update_layout(mapbox_style="open-street-map", margin={"r": 0, "t": 50, "l": 0, "b": 0})
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Circle size represents observation record volume (reporting activity), not population size.")


def page_groups(df: pd.DataFrame):
    st.subheader("Group Breakdown")
    group_pie_chart(df, top_n=5)


# -----------------------------
# APP ENTRYPOINT
# -----------------------------
def main():
    df = load_clean_data()

    st.sidebar.header("Navigation")
    page = st.sidebar.radio("Go to", ["Overview", "Map", "Groups"], index=0)

    if page == "Overview":
        page_overview(df)
    elif page == "Map":
        page_map(df)
    else:
        page_groups(df)


if __name__ == "__main__":
    main()

