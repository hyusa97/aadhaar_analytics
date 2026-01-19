import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os

# ---------------- Page config ----------------
st.set_page_config(
    page_title="Aadhaar State Map & Anomalies",
    layout="wide"
)

st.title("Aadhaar State-Level Overview")

# ---------------- Load base data ----------------
@st.cache_data
def load_base_data():
    return pd.read_csv(
        r"C:\Users\hp\workspace\aadhaar_analytics\data\processed\state_monthly.csv"
    )

# ---------------- Load anomaly data ----------------
@st.cache_data
def load_anomaly_data():
    return pd.read_csv(
        r"C:\Users\hp\workspace\aadhaar_analytics\data\processed\state_monthly_anomalies.csv"
    )

df = load_base_data()
df_anom = load_anomaly_data()

# ---------------- State name normalization ----------------
STATE_NAME_MAP = {
    "Andaman & Nicobar": "Andaman and Nicobar Islands",
    "Dadra & Nagar Haveli": "Dadra and Nagar Haveli and Daman and Diu",
    "Jammu & Kashmir": "Jammu and Kashmir",
    "NCT of Delhi": "Delhi"
}

df["state_geo"] = df["state"].replace(STATE_NAME_MAP)

# ---------------- Sidebar filters ----------------
st.sidebar.header("Filters")

metric_cols = [c for c in df.columns if c not in ["state", "state_geo", "year", "month"]]

metric = st.sidebar.selectbox("Metric", metric_cols)
year = st.sidebar.selectbox("Year", sorted(df["year"].unique()))

month_options = ["All"] + sorted(df["month"].unique())
month = st.sidebar.selectbox("Month", month_options)

# ---------------- Filter base data ----------------
if month == "All":
    df_f = df[df["year"] == year]
else:
    df_f = df[
        (df["year"] == year) &
        (df["month"] == month)
    ]

# ---------------- Load GeoJSON ----------------
with open("app/geo/india_states.geojson", "r", encoding="utf-8") as f:
    india_geojson = json.load(f)

if df_f.empty:
    st.error("No data after filtering.")
    st.stop()

# ---------------- Choropleth map ----------------
fig = px.choropleth(
    df_f,
    geojson=india_geojson,
    locations="state_geo",
    featureidkey="properties.NAME_1",
    color=metric,
    color_continuous_scale="Viridis",
    title=f"{metric} | {year}" if month == "All" else f"{metric} | {month}-{year}"
)

fig.update_geos(
    fitbounds="locations",
    visible=False
)

fig.update_layout(
    margin=dict(l=0, r=0, t=40, b=0)
)

st.plotly_chart(fig, use_container_width=True)

# =========================================================
# ================== PHASE 4: ANOMALIES ===================
# =========================================================

st.markdown("## 🚨 Detected Anomalies ")

# ---------------- Filter anomaly data ----------------
if month == "All":
    anom_f = df_anom[
        (df_anom["year"] == year) &
        (df_anom["anomaly_flag"] != "NORMAL")
    ]
else:
    anom_f = df_anom[
        (df_anom["year"] == year) &
        (df_anom["month"] == month) &
        (df_anom["anomaly_flag"] != "NORMAL")
    ]

if anom_f.empty:
    st.info("No anomalies detected for the selected period.")
else:
    st.dataframe(
        anom_f[
            [
                "state",
                "month",
                metric,
                "mom_change",
                "mom_pct_change",
                "anomaly_flag"
            ]
        ].sort_values("mom_pct_change", ascending=False),
        use_container_width=True
    )
# =========================================================
# ================== TRENDS & GRAPHS ======================
# =========================================================

st.markdown("## 📈 Trends & Temporal Patterns")

# ---------------- State selector for trend ----------------
state_for_trend = st.selectbox(
    "Select State for Trend Analysis",
    sorted(df["state"].unique())
)

# ---------------- Prepare time column ----------------
df["date"] = pd.to_datetime(
    df["year"].astype(str) + "-" + df["month"].astype(str) + "-01"
)

df_anom["date"] = pd.to_datetime(
    df_anom["year"].astype(str) + "-" + df_anom["month"].astype(str) + "-01"
)

# ---------------- Filter data ----------------
trend_df = df[df["state"] == state_for_trend]
trend_anom = df_anom[
    (df_anom["state"] == state_for_trend) &
    (df_anom["anomaly_flag"] != "NORMAL")
]

# ---------------- Line trend ----------------
fig_trend = px.line(
    trend_df,
    x="date",
    y=metric,
    title=f"{metric} Trend | {state_for_trend}",
    markers=True
)

# ---------------- Overlay anomalies ----------------
if not trend_anom.empty:
    fig_trend.add_scatter(
        x=trend_anom["date"],
        y=trend_anom[metric],
        mode="markers",
        marker=dict(
            size=12,
            symbol="x",
            color="red"   
        ),
        name="Anomaly"
    )


fig_trend.update_layout(
    xaxis_title="Time",
    yaxis_title=metric,
    margin=dict(l=20, r=20, t=50, b=20)
)

st.plotly_chart(fig_trend, use_container_width=True)
