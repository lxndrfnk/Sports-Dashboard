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

st.title("📈 Trainingsdaten")

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
        border-radius: 20px;
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
    width=0.2
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
        tickformat=".0f",
        zeroline=False,
        zerolinecolor="white"
    ),
    showlegend=False
)

fig.update_xaxes(linecolor="white")
fig.update_yaxes(linecolor="white")

with st.expander("Diagramm anzeigen", expanded=False):
    st.plotly_chart(fig, use_container_width=True)

# ---------- Diagramm: Kilometer pro Monat ----------

df["startTimeLocal"] = pd.to_datetime(df["startTimeLocal"], errors="coerce")

if "activityTypeDTO.typeKey" in df.columns:
    df["typeKey"] = df["activityTypeDTO.typeKey"]
elif "activityType" in df.columns:
    df["typeKey"] = df["activityType"].apply(
        lambda x: ast.literal_eval(x).get("typeKey") if isinstance(x, str) and "{" in x else x
    )

df_runs = df[df["typeKey"] == "running"].dropna(subset=["startTimeLocal", "distance"]).copy()

df_runs["month_dt"] = df_runs["startTimeLocal"].dt.to_period("M").dt.to_timestamp()
by_month = (df_runs.groupby("month_dt")["distance"].sum() / 1000).sort_index()


by_month_last12 = by_month.tail(12)

month_nums = by_month_last12.index.strftime("%m")
month_map = {
    "01": "Jan.", "02": "Feb.", "03": "Mär.", "04": "Apr.", "05": "Mai", "06": "Jun.",
    "07": "Jul.", "08": "Aug.", "09": "Sep.", "10": "Okt.", "11": "Nov.", "12": "Dez."
}
month_labels = [month_map[m] for m in month_nums]

st.header("🏃 Kilometer pro Monat (letzte 12 Monate)")

fig_m = go.Figure()

fig_m.add_trace(go.Bar(
    x=month_labels,
    y=by_month_last12.values,
    marker_color="white",
    text=[f"{int(round(v))}" for v in by_month_last12.values],  
    textposition="inside",
    insidetextanchor="middle",
    width=0.4
))

fig_m.update_layout(
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
        tickvals=month_labels
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
        tickformat=".0f",
        zeroline=False
    ),
    showlegend=False
)

fig_m.update_xaxes(linecolor="white")
fig_m.update_yaxes(linecolor="white")

with st.expander("Diagramm anzeigen", expanded=False):
    st.plotly_chart(fig_m, use_container_width=True)

# ---------- Diagramm: Kilometer pro Jahr (Rad) ----------

import ast

st.header("🚴 Kilometer pro Jahr")

# Frisch laden, damit kein vorheriger Filter (z. B. running) stört
df_all = pd.read_csv("garmin_activities.csv")
df_all["startTimeLocal"] = pd.to_datetime(df_all["startTimeLocal"], errors="coerce")

# typeKey zuverlässig ermitteln
if "activityTypeDTO.typeKey" in df_all.columns:
    df_all["typeKey"] = df_all["activityTypeDTO.typeKey"]
elif "activityType" in df_all.columns:
    df_all["typeKey"] = df_all["activityType"].apply(
        lambda x: ast.literal_eval(x).get("typeKey") if isinstance(x, str) and "{" in x else x
    )
else:
    df_all["typeKey"] = None

# Radfahren filtern (ggf. weitere Varianten ergänzen)
bike_keys = ["cycling"]  # bei Bedarf: "mountain_biking", "virtual_ride", ...
df_bike = df_all[df_all["typeKey"].isin(bike_keys)].dropna(subset=["startTimeLocal", "distance"]).copy()

if df_bike.empty:
    types = ", ".join(sorted(map(str, df_all["typeKey"].dropna().unique())))
    st.info(f"Keine Radfahr-Daten gefunden. Verfügbare Typen in der CSV: {types}")
else:
    # km pro Jahr
    by_year_bike = (df_bike.groupby(df_bike["startTimeLocal"].dt.year)["distance"].sum() / 1000).sort_index()

    fig_bike_year = go.Figure()
    fig_bike_year.add_trace(go.Bar(
        x=by_year_bike.index.astype(str),
        y=by_year_bike.values,
        marker_color="white",
        text=[f"{int(round(v))}" for v in by_year_bike.values],
        textposition='inside',
        insidetextanchor='middle',
        width=0.2
    ))

    fig_bike_year.update_layout(
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
            tickvals=[str(year) for year in by_year_bike.index]
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
            tickformat=".0f",
            zeroline=False
        ),
        showlegend=False
    )

    fig_bike_year.update_xaxes(linecolor="white")
    fig_bike_year.update_yaxes(linecolor="white")

    with st.expander("Diagramm anzeigen", expanded=False):
        st.plotly_chart(fig_bike_year, use_container_width=True)

# ---------- Diagramm: Kilometer pro Monat (Rad, letzte 12 Monate) ----------

st.header("🚴 Kilometer pro Monat (letzte 12 Monate)")

if df_bike.empty:
    st.info("Keine Radfahr-Daten für die Monatsansicht gefunden.")
else:
    bike_month = (
        df_bike
        .assign(month_dt=df_bike["startTimeLocal"].dt.to_period("M"))
        .groupby("month_dt")["distance"].sum()
        .div(1000)
        .sort_index()
    )

    last_month = df_bike["startTimeLocal"].max().to_period("M")
    months_range = pd.period_range(last_month - 11, last_month, freq="M")
    bike_month_12 = (
        bike_month.reindex(months_range, fill_value=0.0)
        .astype(float)
    )

    month_map = {
        1: "Jan.", 2: "Feb.", 3: "Mär.", 4: "Apr.", 5: "Mai", 6: "Jun.",
        7: "Jul.", 8: "Aug.", 9: "Sep.", 10: "Okt.", 11: "Nov.", 12: "Dez."
    }
    x_labels = [month_map[p.month] for p in bike_month_12.index]

    fig_bike_month = go.Figure()
    fig_bike_month.add_trace(go.Bar(
        x=x_labels,                               
        y=bike_month_12.values,
        marker_color="white",
        text=[f"{int(round(v))}" for v in bike_month_12.values],
        textposition="inside",
        insidetextanchor="middle",
        width=0.4                                   
    ))

    fig_bike_month.update_layout(
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
            tickvals=x_labels                        
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
            tickformat=".0f",
            zeroline=False
        ),
        showlegend=False
    )

    fig_bike_month.update_xaxes(linecolor="white")
    fig_bike_month.update_yaxes(linecolor="white")

    with st.expander("Diagramm anzeigen", expanded=False):
        st.plotly_chart(fig_bike_month, use_container_width=True)

