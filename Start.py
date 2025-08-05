import streamlit as st

# ---------- Seiteneinstellungen ----------

st.set_page_config(
    page_title="Triathlon-Dashboard",
    page_icon="🏅",
    layout="wide"
)

# ---------- Import weiterer Module ----------

import pandas as pd
import ast
import datetime
import matplotlib.pyplot as plt
from datetime import date

# ---------- Garmin Daten laden ----------

df = pd.read_csv("garmin_activities.csv")

# Prüfe Spalte

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

# Nur Triathlon-Disziplinen

triathlon_types = ["running", "cycling", "lap_swimming"]
df_tri = df[df["typeKey"].isin(triathlon_types)]

# ---------- Hilfsfunktionen ----------

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

# ---------- Sidebar Farblegende ----------

with st.sidebar:
    st.markdown("""
    <style>
    .color-square {
    display: inline-block;
    width: 18px;
    height: 18px;
    border: 2px solid;
    border-radius: 3px;
    background-color: black;
    margin-right: 10px;
    }
    .legend-item {
    display: flex;
    align-items: center;
    margin-bottom: 8px;
    }
    .legend-text {
    font-size: 24px;
    font-weight: 500;
    color: white;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="legend-item">
    <span class="color-square" style="border-color:#0077b6;"></span>
    <span class="legend-text">Swim</span>
    </div>
    <div class="legend-item">
    <span class="color-square" style="border-color:#43aa8b;"></span>
    <span class="legend-text">Bike</span>
    </div>
    <div class="legend-item">
    <span class="color-square" style="border-color:#f94144;"></span>
    <span class="legend-text">Run</span>
    </div>
    """, unsafe_allow_html=True)


    st.markdown("---")
    st.subheader("Meine nächsten Wettkämpfe")

    races = [
        {"name": "28. Willicher Triathlon", "date": date(2025, 9, 7), "distance": "Sprintdistanz"},
        {"name": "Venloop", "date": date(2026, 3, 29), "distance": "Halbmarathon"}
    ]

    today = date.today()

    for race in races:
        delta = (race["date"] - today).days

        st.markdown(f"""
            <div style="
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 10px;
                padding: 10px;
                margin-bottom: 10px;
                background-color: rgba(255, 255, 255, 0.05);
            ">
                <strong>🏁 {race['name']}</strong><br>
                📏 {race['distance']}<br>
                📆 {race['date'].strftime('%d.%m.%Y')}<br>
                ⏳ Noch <strong><span style='color:#39FF14;'>{delta}</span></strong> Tage
            </div>
        """, unsafe_allow_html=True)

# ---------- Titel ----------

st.title("Triathlon-Dashboard")

# ---------- Triathlon-Erklärung ----------

st.write("""
Triathlon ist eine Ausdauersportart, bestehend aus einem Mehrkampf der Disziplinen Schwimmen, Radfahren und Laufen,
die nacheinander und in der Regel in genau dieser Reihenfolge zu absolvieren sind.
Die Besonderheit dieses Sports besteht darin, dass eine bestimmte, festgelegte Strecke so schnell wie möglich
zurückzulegen ist, wobei die Uhr auch bei zeitlichen Unterbrechungen wie z. B. den Wechseln zwischen den Disziplinen weiter läuft.
Die Wortschöpfung „Triathlon“ setzt sich aus den griechischen Ausdrücken τρεῖς/τρία bzw. treis/tria, „drei“, und ἆθλος bzw. athlos,
„Wettkampf“ zusammen. Triathlon ist seit dem Jahr 2000 auch eine olympische Disziplin.
""")

st.write("---")

# ---------- Triathlon-Distanzen ----------

st.subheader("⬇️ Triathlon-Distanzen ⬇️")

tabs = st.tabs(["Sprintdistanz", "Olympische Distanz", "Mitteldistanz", "Langdistanz"])

with tabs[0]:
    st.write("**Schwimmen**: 0.5 km")
    st.write("**Rad**: 20 km")
    st.write("**Laufen**: 5 km")

with tabs[1]:
    st.write("**Schwimmen**: 1.5 km")
    st.write("**Rad**: 40 km")
    st.write("**Laufen**: 10 km")

with tabs[2]:
    st.write("**Schwimmen**: 1.9 km")
    st.write("**Rad**: 90 km")
    st.write("**Laufen**: 21.1 km (Halbmarathon)")

with tabs[3]:
    st.write("**Schwimmen**: 3.8 km")
    st.write("**Rad**: 180 km")
    st.write("**Laufen**: 42.2 km (Marathon)")

st.write("---")

# ---------- Bisherige Wettkämpfe ----------

st.subheader("🏅 Meine bisherigen Wettkämpfe 🏅")

my_races = [
    {
        "event": "28. Willicher Triathlon",
        "year": 2025,
        "distance_category": "Sprintdistanz",
        "swim_time": "--:--:--",
        "swim_delta": "",
        "bike_time": "--:--:--",
        "bike_delta": "",
        "run_time": "--:--:--",
        "run_delta": "",
        "finish_time": "--:--:--",
        "finish_delta": ""
    },
    {
        "event": "27. Willicher Triathlon",
        "year": 2024,
        "distance_category": "Sprintdistanz",
        "swim_time": "00:11:06",
        "swim_delta": "+ 00:00:57",
        "bike_time": "00:35:19",
        "bike_delta": "+ 00:02:48",
        "run_time": "00:23:44",
        "run_delta": "- 00:01:03",
        "finish_time": "01:15:44",
        "finish_delta": "+ 00:03:09"
    },
    {
        "event": "26. Willicher Triathlon",
        "year": 2023,
        "distance_category": "Sprintdistanz",
        "swim_time": "00:12:03",
        "swim_delta": "",
        "bike_time": "00:38:07",
        "bike_delta": "",
        "run_time": "00:22:41",
        "run_delta": "",
        "finish_time": "01:18:53",
        "finish_delta": ""
    },
]

distance_categories = ["Sprintdistanz", "Olympische Distanz", "Mitteldistanz", "Langdistanz"]

for category in distance_categories:
    races = [r for r in my_races if r["distance_category"] == category]

    with st.expander(f"🏁 {category}", expanded=False):
        if races:
            for race in races:
                st.write(f"### {race['event']} ({race['year']})")

                cols = st.columns(4)
                cols[0].metric("🏊 Swim", race["swim_time"], race["swim_delta"])
                cols[1].metric("🚴 Bike", race["bike_time"], race["bike_delta"])
                cols[2].metric("🏃 Run", race["run_time"], race["run_delta"])
                cols[3].metric("⏱️ Finish", race["finish_time"], race["finish_delta"])

                if category == "Sprintdistanz":
                    swim_distance_race_m = 500
                    bike_distance_race_km = 20
                    run_distance_race_km = 5
                elif category == "Olympische Distanz":
                    swim_distance_race_m = 1500
                    bike_distance_race_km = 40
                    run_distance_race_km = 10
                elif category == "Mitteldistanz":
                    swim_distance_race_m = 1900
                    bike_distance_race_km = 90
                    run_distance_race_km = 21.1
                elif category == "Langdistanz":
                    swim_distance_race_m = 3800
                    bike_distance_race_km = 180
                    run_distance_race_km = 42.2

                swim_seconds = time_to_seconds(race["swim_time"])
                bike_seconds = time_to_seconds(race["bike_time"])
                run_seconds = time_to_seconds(race["run_time"])

                swim_pace = seconds_to_pace(swim_seconds / (swim_distance_race_m / 100)) if swim_seconds else "--:--"
                bike_speed = bike_distance_race_km / (bike_seconds / 3600) if bike_seconds else "--"
                bike_speed_str = f"{bike_speed:.1f}" if bike_speed != "--" else "--"
                run_pace = seconds_to_pace(run_seconds / run_distance_race_km) if run_seconds else "--:--"

                pace_cols = st.columns(4)
                pace_cols[0].metric("Ø Swim-Pace (min/100 m)", swim_pace)
                pace_cols[1].metric("Ø Bike-Speed (km/h)", bike_speed_str)
                pace_cols[2].metric("Ø Run-Pace (min/km)", run_pace)
                pace_cols[3].write("")

                st.divider()
        else:
            st.write("Keine Wettkämpfe vorhanden.")

st.write("---")

# ---------- Trainingsdaten ----------

st.subheader("📈 Trainingsdaten 📈")

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

swim_duration_h = df_filtered[df_filtered["typeKey"] == "lap_swimming"]["duration"].sum() / 3600
bike_duration_h = df_filtered[df_filtered["typeKey"] == "cycling"]["duration"].sum() / 3600
run_duration_h  = df_filtered[df_filtered["typeKey"] == "running"]["duration"].sum() / 3600

st.markdown("""
    <style>
    .metric-card {
        border: 2px solid #ffffff33;
        border-radius: 15px;
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
            <p>{swim_duration_h:.1f} h</p>
        </div>
    """, unsafe_allow_html=True)
with cols_time[1]:
    st.markdown(f"""
        <div class="metric-card metric-bike">
            <h3>⌛ Gesamtzeit</h3>
            <p>{bike_duration_h:.1f} h</p>
        </div>
    """, unsafe_allow_html=True)
with cols_time[2]:
    st.markdown(f"""
        <div class="metric-card metric-run">
            <h3>⌛ Gesamtzeit</h3>
            <p>{run_duration_h:.1f} h</p>
        </div>
    """, unsafe_allow_html=True)

