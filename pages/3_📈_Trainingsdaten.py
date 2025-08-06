import streamlit as st
import pandas as pd
import ast
import datetime
import matplotlib.pyplot as plt
from datetime import date
from matplotlib.patches import FancyBboxPatch
import plotly.graph_objects as go

# ---------- Schriftart ----------

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=League+Spartan&display=swap');

        html, body, [class*="css"]  {
            font-family: 'League Spartan', sans-serif;
        }
    </style>
""", unsafe_allow_html=True)

# ---------- Garmin Daten laden ----------

df = pd.read_csv("garmin_activities.csv")

if "activityTypeDTO.typeKey" in df.columns:
    activity_col = "activityTypeDTO.typeKey"
    df["typeKey"] = df[activity_col]
elif "activityType" in df.columns:
    first = df["activityType"].iloc[0]
    if isinstance(first, str) and "{" in first:
        def get_typekey(val):
            try:
                return ast.literal_eval(val).get("typeKey")
            except:
                return None
        df["typeKey"] = df["activityType"].apply(get_typekey)
    else:
        df["typeKey"] = df["activityType"]
else:
    st.error("Keine passende Spalte für Aktivitätstyp gefunden.")
    st.stop()

triathlon_types = ["running", "cycling", "lap_swimming"]
df_tri = df[df["typeKey"].isin(triathlon_types)]

def time_to_seconds(timestr):
    if "--" in timestr or timestr.strip() == "":
        return None
    h, m, s = map(int, timestr.split(":"))
    return h * 3600 + m * 60 + s

def seconds_to_pace(seconds_per_unit):
    if seconds_per_unit is None:
        return "--:--"
    m = int(seconds_per_unit // 60)
    s = int(seconds_per_unit % 60)
    return f"{m:02d}:{s:02d}"

# ---------- Trainingsdaten ----------

st.title("Trainingsdaten")

st.markdown("---")

df_tri["startTimeLocal"] = pd.to_datetime(df_tri["startTimeLocal"])

min_date = df_tri["startTimeLocal"].min().date()
max_date = df_tri["startTimeLocal"].max().date()

col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input(
        "Start",
        value=min_date,
        min_value=min_date,
        max_value=max_date,
        format="DD.MM.YYYY"
    )
with col2:
    end_date = st.date_input(
        "Ende",
        value=max_date,
        min_value=min_date,
        max_value=max_date,
        format="DD.MM.YYYY"
    )

df_filtered = df_tri[
    (df_tri["startTimeLocal"].dt.date >= start_date) &
    (df_tri["startTimeLocal"].dt.date <= end_date)
]
swim_count = df_filtered[df_filtered["typeKey"] == "lap_swimming"].shape[0]
bike_count = df_filtered[df_filtered["typeKey"] == "cycling"].shape[0]
run_count  = df_filtered[df_filtered["typeKey"] == "running"].shape[0]

swim_distance_km = df_filtered[df_filtered["typeKey"] == "lap_swimming"]["distance"].sum() / 1000
bike_distance_km = df_filtered[df_filtered["typeKey"] == "cycling"]["distance"].sum() / 1000
run_distance_km  = df_filtered[df_filtered["typeKey"] == "running"]["distance"].sum() / 1000

from datetime import timedelta

def format_seconds(seconds):
    if not seconds or seconds == 0:
        return "00:00:00"
    seconds = int(seconds)
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{hours:02}:{minutes:02}:{secs:02}"

swim_duration_sec = df_filtered[df_filtered["typeKey"] == "lap_swimming"]["duration"].sum()
bike_duration_sec = df_filtered[df_filtered["typeKey"] == "cycling"]["duration"].sum()
run_duration_sec  = df_filtered[df_filtered["typeKey"] == "running"]["duration"].sum()

swim_duration_str = format_seconds(swim_duration_sec)
bike_duration_str = format_seconds(bike_duration_sec)
run_duration_str  = format_seconds(run_duration_sec)

st.markdown("""
    <style>
    .metric-card {
        border: 2px solid #ffffff33;
        border-radius: 0px;
        padding: 20px;
        text-align: center;
        font-family: 'Arial', sans-serif;
        box-shadow: 2px 2px 12px rgba(0,0,0,0.3);
        margin-bottom: 10px;
        color: white;
    }
    .metric-swim { border-color: #0077b6; }
    .metric-bike { border-color: #43aa8b; }
    .metric-run  { border-color: #f94144; }
    .metric-card h3 { margin: 0; font-size: 20px; }
    .metric-card p  { margin: 5px 0 0 0; font-size: 28px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

cols = st.columns(3)
with cols[0]:
    st.markdown(f"""
        <div class="metric-card metric-swim">
            <h3>🏊 Swim Sessions</h3>
            <p>{swim_count}</p>
        </div>
    """, unsafe_allow_html=True)
with cols[1]:
    st.markdown(f"""
        <div class="metric-card metric-bike">
            <h3>🚴 Bike Sessions</h3>
            <p>{bike_count}</p>
        </div>
    """, unsafe_allow_html=True)
with cols[2]:
    st.markdown(f"""
        <div class="metric-card metric-run">
            <h3>🏃 Run Sessions</h3>
            <p>{run_count}</p>
        </div>
    """, unsafe_allow_html=True)

cols_dist = st.columns(3)
with cols_dist[0]:
    st.markdown(f"""
        <div class="metric-card metric-swim">
            <h3>📐 Gesamtdistanz</h3>
            <p>{swim_distance_km:.1f} km</p>
        </div>
    """, unsafe_allow_html=True)
with cols_dist[1]:
    st.markdown(f"""
        <div class="metric-card metric-bike">
            <h3>📐 Gesamtdistanz</h3>
            <p>{bike_distance_km:.0f} km</p>
        </div>
    """, unsafe_allow_html=True)
with cols_dist[2]:
    st.markdown(f"""
        <div class="metric-card metric-run">
            <h3>📐 Gesamtdistanz</h3>
            <p>{run_distance_km:.0f} km</p>
        </div>
    """, unsafe_allow_html=True)

cols_time = st.columns(3)
with cols_time[0]:
    st.markdown(f"""
        <div class="metric-card metric-swim">
            <h3>⌛ Gesamtzeit</h3>
            <p>{swim_duration_str}</p>
        </div>
    """, unsafe_allow_html=True)
with cols_time[1]:
    st.markdown(f"""
        <div class="metric-card metric-bike">
            <h3>⌛ Gesamtzeit</h3>
            <p>{bike_duration_str}</p>
        </div>
    """, unsafe_allow_html=True)
with cols_time[2]:
    st.markdown(f"""
        <div class="metric-card metric-run">
            <h3>⌛ Gesamtzeit</h3>
            <p>{run_duration_str}</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ---------- Kilometer pro Jahr und Monat ----------

df["startTimeLocal"] = pd.to_datetime(df["startTimeLocal"], errors="coerce")

if "activityTypeDTO.typeKey" in df.columns:
    df["typeKey"] = df["activityTypeDTO.typeKey"]
elif "activityType" in df.columns:
    import ast
    df["typeKey"] = df["activityType"].apply(lambda x: ast.literal_eval(x).get("typeKey") if isinstance(x, str) and "{" in x else x)
else:
    df["typeKey"] = None

df = df[df["typeKey"].isin(["running"])]
df = df.dropna(subset=["startTimeLocal", "distance"])

df["distance_km"] = df["distance"] / 1000
df["year"] = df["startTimeLocal"].dt.year
df["month"] = df["startTimeLocal"].dt.to_period("M").astype(str)
df["week"] = df["startTimeLocal"].dt.to_period("W").astype(str)

by_year = df.groupby("year")["distance_km"].sum()
by_month = df.groupby("month")["distance_km"].sum()
by_week = df.groupby("week")["distance_km"].sum()

# ---------- Diagramm: Kilometer pro Jahr ----------

st.header("🏃 Kilometer pro Jahr")

fig = go.Figure()

fig.add_trace(go.Bar(
    x=by_year.index.astype(str),
    y=by_year.values,
    marker_color="white",
    text=[f"{int(val)}" for val in by_year.values],
    textposition='inside',
    insidetextanchor='middle',
    width=0.4
))

fig.update_layout(
    plot_bgcolor="#4b4c4d",
    paper_bgcolor="#4b4c4d",
    font=dict(color="white"),
    margin=dict(l=40, r=20, t=30, b=40),
    xaxis=dict(
        showline=True,
        linecolor="white",
        tickfont=dict(color="white"),
        ticklen=6,
        tickwidth=1,
        tickcolor="white",
        ticks="outside",
        tickmode="array",
         tickvals=[str(year) for year in by_year.index]
    ),
    yaxis=dict(
        showline=True,
        showticklabels=True,  
        ticklen=6,
        tickwidth=1,
        tickcolor="white",
        tickfont=dict(color="white"),
        showgrid=True,
        gridcolor="white",
        tickformat=".0f"
    ),
    showlegend=False
)

fig.update_xaxes(linecolor="white")
fig.update_yaxes(linecolor="white")

with st.expander("Diagramm anzeigen", expanded=False):
    st.plotly_chart(fig, use_container_width=True)

# ---------- Diagramm: Kilometer pro Monat ----------

ddf = pd.read_csv("garmin_activities.csv")
df["startTimeLocal"] = pd.to_datetime(df["startTimeLocal"], errors="coerce")

if "activityTypeDTO.typeKey" in df.columns:
    df["typeKey"] = df["activityTypeDTO.typeKey"]
elif "activityType" in df.columns:
    import ast
    df["typeKey"] = df["activityType"].apply(lambda x: ast.literal_eval(x).get("typeKey") if isinstance(x, str) and "{" in x else x)
else:
    df["typeKey"] = None

df = df[df["typeKey"] == "running"]

df["month_dt"] = df["startTimeLocal"].dt.to_period("M").dt.to_timestamp()
by_month = df.groupby("month_dt")["distance"].sum() / 1000  
by_month = by_month.sort_index()
by_month_last12 = by_month.tail(12)


month_labels = by_month_last12.index.strftime("%m") 
month_names = {
    '01': 'Jan.', '02': 'Feb.', '03': 'Mär.', '04': 'Apr.', '05': 'Mai', '06': 'Jun.',
    '07': 'Jul.', '08': 'Aug.', '09': 'Sep.', '10': 'Okt.', '11': 'Nov.', '12': 'Dez.'
}
month_labels = [month_names[m] for m in month_labels]

st.header("🏃 Kilometer pro Monat (letzte 12 Monate)")

fig, ax = plt.subplots(figsize=(10, 4))
fig.patch.set_facecolor('#4b4c4d')   
ax.set_facecolor('#4b4c4d')

bars = ax.bar(
    month_labels,
    by_month_last12.values,
    color="#ffffff"
)

ax.tick_params(colors="white")
ax.set_xlabel("")
ax.set_ylabel("")
ax.set_yticks([])

for spine in ax.spines.values():
    spine.set_visible(True)
    spine.set_edgecolor("#f94144")
    spine.set_linewidth(2)

for bar in bars:
    height = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        height / 2,
        f"{height:.0f}",
        ha='center', va='center',
        color='black',
        fontsize=10
    )

st.pyplot(fig)
