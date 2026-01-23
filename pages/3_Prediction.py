import numpy as np
import pandas as pd
import streamlit as st
from pathlib import Path
import plotly.express as px

from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import mean_absolute_error


def render_prediction_page():
    st.header("🔮 Future Reporting Prediction (by Mammal Group)")
    st.caption(
        "This page trains a leakage-safe time-series model to predict *future reporting activity* "
        "for a selected Mammal Group (expected number of records) per Area Code for the next period."
    )

    # -----------------------------
    # PATHS / CONFIG
    # -----------------------------
ROOT = Path(__file__).resolve().parents[1]  # repo root on Heroku is /app

CANDIDATES = [
    ROOT / "data" / "mammal_atlas_cleaned.csv",                 # RECOMMENDED
    ROOT / "pages" / "data" / "mammal_atlas_cleaned.csv",
    ROOT / "jupyter_notebooks" / "outputs" / "mammal_atlas_cleaned.csv",
]


    # -----------------------------
    # DATA LOADING
    # -----------------------------
@st.cache_data
def load_clean_data() -> pd.DataFrame:
    found = None
    for p in CANDIDATES:
        if p.exists():
            found = p
            break

    if found is None:
        st.error(
            "Cleaned dataset not found.\n\nTried:\n- "
            + "\n- ".join(str(p) for p in CANDIDATES)
            + "\n\nFix: commit the cleaned CSV to the repo (recommended path: data/mammal_atlas_cleaned.csv)."
        )
        st.stop()

    df = pd.read_csv(found)
    df.columns = df.columns.str.strip()

    # Visible proof in the deployed app
    st.sidebar.success("Dataset loaded")
    st.sidebar.caption(f"Path: {found}")
    st.sidebar.caption(f"Rows: {len(df):,} | Cols: {df.shape[1]}")
    return df


    # -----------------------------
    # TIME HANDLING
    # -----------------------------
    def add_time_bucket(df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()

        if "Start date" in df.columns:
            dt = pd.to_datetime(df["Start date"], errors="coerce", dayfirst=True)
            if dt.notna().any():
                df["period"] = dt.dt.to_period("M")
                df["period_grain"] = "month"
                return df

        if "Start date year" in df.columns and "Start date month" in df.columns:
            y = pd.to_numeric(df["Start date year"], errors="coerce")
            m = pd.to_numeric(df["Start date month"], errors="coerce")
            dt = pd.to_datetime(dict(year=y, month=m.clip(1, 12), day=1), errors="coerce")
            if dt.notna().any():
                df["period"] = dt.dt.to_period("M")
                df["period_grain"] = "month"
                return df

        if "Start date year" in df.columns:
            y = pd.to_numeric(df["Start date year"], errors="coerce")
            dt = pd.to_datetime(dict(year=y, month=1, day=1), errors="coerce")
            if dt.notna().any():
                df["period"] = dt.dt.to_period("Y")
                df["period_grain"] = "year"
                return df

        st.error(
            "Could not create a time bucket. Expected one of: "
            "'Start date' (preferred) or 'Start date year' (fallback)."
        )
        st.stop()

    # -----------------------------
    # PANEL BUILDING + FEATURES
    # -----------------------------
    @st.cache_data
    def build_panel(df: pd.DataFrame) -> tuple[pd.DataFrame, str]:
        required = {"Area Code", "Mammal Group", "Latitude (WGS84)", "Longitude (WGS84)"}
        missing = required - set(df.columns)
        if missing:
            st.error(f"Missing required columns for forecasting page: {sorted(missing)}")
            st.stop()

        df = add_time_bucket(df)
        grain = df["period_grain"].iloc[0]

        panel = (
            df.dropna(subset=["Area Code", "Mammal Group", "period"])
            .groupby(["Area Code", "Mammal Group", "period"])
            .size()
            .reset_index(name="count")
            .sort_values(["Area Code", "Mammal Group", "period"])
        )

        centroids = (
            df.groupby("Area Code")[["Latitude (WGS84)", "Longitude (WGS84)"]]
            .mean()
            .reset_index()
            .rename(columns={"Latitude (WGS84)": "area_lat", "Longitude (WGS84)": "area_lon"})
        )
        panel = panel.merge(centroids, on="Area Code", how="left")

        if grain == "month":
            panel["year"] = panel["period"].dt.year
            panel["month"] = panel["period"].dt.month
            panel["quarter"] = panel["period"].dt.quarter
        else:
            panel["year"] = panel["period"].dt.year

        g = panel.groupby(["Area Code", "Mammal Group"], group_keys=False)
        panel["lag_1"] = g["count"].shift(1)
        panel["lag_2"] = g["count"].shift(2)
        panel["lag_3"] = g["count"].shift(3)

        panel["roll_3_mean"] = g["count"].shift(1).rolling(3).mean()
        panel["roll_6_mean"] = g["count"].shift(1).rolling(6).mean()
        panel["roll_6_std"] = g["count"].shift(1).rolling(6).std()
        panel["trend_1_2"] = panel["lag_1"] - panel["lag_2"]

        for c in ["lag_1", "lag_2", "lag_3", "roll_3_mean", "roll_6_mean", "roll_6_std", "trend_1_2"]:
            panel[c] = panel[c].fillna(0)

        panel["y_next"] = g["count"].shift(-1)
        return panel, grain

    # -----------------------------
    # MODEL TRAINING / BACKTEST (PER GROUP)
    # -----------------------------
    @st.cache_data
    def train_and_predict_next_for_group(panel: pd.DataFrame, grain: str, mammal_group: str) -> dict:
        group_panel = panel[panel["Mammal Group"] == mammal_group].copy()

        if group_panel.empty:
            return {"status": "empty", "message": "No data available for this group."}

        data = group_panel.dropna(subset=["y_next"]).copy()

        unique_periods = sorted(data["period"].unique())
        if len(unique_periods) < 4:
            return {"status": "too_small", "message": "Not enough time periods to train a forecast model for this group."}

        holdout_periods = unique_periods[-3:] if len(unique_periods) >= 6 else unique_periods[-1:]
        train_df = data[~data["period"].isin(holdout_periods)].copy()
        test_df = data[data["period"].isin(holdout_periods)].copy()

        feats = [
            "area_lat", "area_lon",
            "lag_1", "lag_2", "lag_3",
            "roll_3_mean", "roll_6_mean", "roll_6_std",
            "trend_1_2",
            "year",
        ]
        if grain == "month":
            feats += ["month", "quarter"]

        X_train = train_df[feats].astype(float)
        y_train = train_df["y_next"].astype(float)
        X_test = test_df[feats].astype(float)
        y_test = test_df["y_next"].astype(float)

        model = HistGradientBoostingRegressor(
            loss="squared_error",
            max_depth=6,
            learning_rate=0.08,
            max_iter=300,
            random_state=42
        )
        model.fit(X_train, np.log1p(y_train))

        y_pred_test = np.expm1(model.predict(X_test))
        y_pred_test = np.clip(y_pred_test, 0, None)
        mae = mean_absolute_error(y_test, y_pred_test)

        latest_rows = (
            group_panel.sort_values(["Area Code", "period"])
            .groupby("Area Code", as_index=False)
            .tail(1)
            .copy()
        )
        if latest_rows.empty:
            return {"status": "empty", "message": "No latest rows available for prediction."}

        latest_period = latest_rows["period"].max()
        next_period = (latest_period + 1)

        X_next = latest_rows[feats].astype(float)
        pred_next = np.expm1(model.predict(X_next))
        pred_next = np.clip(pred_next, 0, None)

        preds = latest_rows[["Area Code", "Mammal Group", "area_lat", "area_lon"]].copy()
        preds["latest_period"] = str(latest_period)
        preds["predicted_period"] = str(next_period)
        preds["predicted_count"] = pred_next.round(2)

        last_total = float(group_panel[group_panel["period"] == latest_period]["count"].sum())
        pred_total = float(preds["predicted_count"].sum())
        delta = pred_total - last_total
        pct = (delta / last_total * 100.0) if last_total > 0 else np.nan

        return {
            "status": "ok",
            "preds": preds,
            "mae": float(mae),
            "latest_period": str(latest_period),
            "next_period": str(next_period),
            "last_total": last_total,
            "pred_total": pred_total,
            "delta": float(delta),
            "pct": float(pct) if np.isfinite(pct) else None,
            "holdout_periods": [str(p) for p in holdout_periods],
            "n_train_rows": int(len(train_df)),
            "n_test_rows": int(len(test_df)),
            "n_areas": int(preds["Area Code"].nunique()),
            "n_periods": int(len(unique_periods)),
        }

    # -----------------------------
    # RUN
    # -----------------------------
    df = load_clean_data()
    panel, grain = build_panel(df)

    st.sidebar.header("Model Controls")

    available_groups = sorted(panel["Mammal Group"].dropna().unique().tolist())
    if not available_groups:
        st.error("No Mammal Group values available in the dataset.")
        st.stop()

    selected_group = st.sidebar.selectbox("Select a Mammal Group to predict", available_groups, index=0)

    st.sidebar.divider()
    top_n_table = st.sidebar.slider("Top N areas table", 5, 50, 10, 1)
    min_pred_filter = st.sidebar.slider("Minimum predicted count", 0, 50, 0, 1)
    max_points = st.sidebar.slider("Max points on map", 50, 1000, 300, 50)

    results = train_and_predict_next_for_group(panel, grain, selected_group)

    if results["status"] != "ok":
        st.warning(results.get("message", "Unable to train/predict for this group."))
        st.stop()

    preds = results["preds"].copy()
    preds_view = preds[preds["predicted_count"] >= min_pred_filter].sort_values("predicted_count", ascending=False)
    preds_map = preds_view.head(max_points).copy()

    colA, colB = st.columns([2, 1])

    with colA:
        st.subheader("Model summary (plain-English explanation)")
        st.write(
            f"""
**Selected group:** **{selected_group}**  
**Forecast period:** **{results["next_period"]}** (based on latest observed **{results["latest_period"]}**)  
**Prediction target:** expected number of *reporting records* for **{selected_group}** per Area Code in the next period.  
**Time grain:** **{grain}**  

**Validation check (time holdout)**
- Holdout periods: {", ".join(results["holdout_periods"])}
- MAE: **{results["mae"]:.2f}** records
- Training rows: **{results["n_train_rows"]:,}** | Test rows: **{results["n_test_rows"]:,}**
- Areas predicted: **{results["n_areas"]:,}** | Periods observed: **{results["n_periods"]:,}**
"""
        )

        if results["pct"] is not None:
            direction = "increase" if results["delta"] >= 0 else "decrease"
            st.write(
                f"""
**Overall outlook for {selected_group}:**
- Latest total: **{results["last_total"]:.0f}**
- Predicted total: **{results["pred_total"]:.0f}**
- Expected change: **{results["delta"]:+.0f}** ({results["pct"]:+.1f}%) — overall **{direction}**
"""
            )

        st.info(
            "Important: this predicts *reporting activity* (records submitted), not true animal abundance. "
            "Reporting is influenced by observer effort, accessibility, and engagement."
        )

    with colB:
        st.subheader("Top predicted areas")
        top_df = preds_view.head(top_n_table)[["Area Code", "predicted_count"]].copy()
        top_df["predicted_count"] = top_df["predicted_count"].round(0).astype(int)
        st.dataframe(top_df, use_container_width=True, height=420)

    st.divider()
    st.subheader(f"Predicted map — {selected_group} ({results['next_period']})")

    if preds_map.empty:
        st.warning("No areas to display for the chosen minimum predicted count.")
    else:
        preds_map["predicted_count_int"] = preds_map["predicted_count"].round(0).astype(int)

        fig = px.scatter_mapbox(
            preds_map,
            lat="area_lat",
            lon="area_lon",
            size="predicted_count",
            color="predicted_count",
            color_continuous_scale="Reds",
            hover_name="Area Code",
            hover_data={
                "Mammal Group": True,
                "predicted_count_int": True,
                "predicted_period": True,
                "latest_period": True,
                "area_lat": False,
                "area_lon": False,
            },
            zoom=4,
            center={"lat": 54.5, "lon": -3},
            height=700,
            title=f"Predicted reporting volume per Area Code — {selected_group} — {results['next_period']}",
        )

        fig.update_layout(
            mapbox_style="open-street-map",
            margin={"r": 0, "t": 60, "l": 0, "b": 0},
            coloraxis_colorbar=dict(title="Predicted count"),
        )
        st.plotly_chart(fig, use_container_width=True)

    st.divider()
    st.subheader("Download predictions")
    csv_bytes = preds_view.to_csv(index=False).encode("utf-8")
    st.download_button(
        label=f"Download CSV for {selected_group}",
        data=csv_bytes,
        file_name=f"predicted_reporting_{selected_group}_{results['next_period']}.csv".replace(" ", "_"),
        mime="text/csv",
    )

render_prediction_page()
