import streamlit as st
import pandas as pd
import ast
import datetime
import matplotlib.pyplot as plt
from datetime import date

# ---------- Schriftart ----------

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=League+Spartan&display=swap');

        html, body, [class*="css"]  {
            font-family: 'League Spartan', sans-serif;
        }
    </style>
""", unsafe_allow_html=True)

# ---------- Einheiten ----------

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

st.title("Meine Wettkämpfe")

st.write("---")

# ---------- Bisherige Wettkämpfe (Triathlon) ----------

st.header("Bisherige Wettkämpfe (Triathlon)")

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

# ---------- Bisherige Wettkämpfe (Läufe) ----------

st.header("Bisherige Wettkämpfe (Läufe)")

my_races = [
    {
        "event": "Venloop",
        "year": 2025,
        "distance_category": "Halbmarathon",
        "finish_time": "01:45:22",
        "finish_delta": "",
    },
    {
        "event": "Venloop",
        "year": 2017,
        "distance_category": "Halbmarathon",
        "finish_time": "01:45:21",
        "finish_delta": "",
    },
    {
        "event": "Venloop",
        "year": 2014,
        "distance_category": "Halbmarathon",
        "finish_time": "01:50:06",
        "finish_delta": "",
    },
    {
        "event": "Venloop",
        "year": 2011,
        "distance_category": "Halbmarathon",
        "finish_time": "01:38:58",
        "finish_delta": "",
    },
    {
        "event": "19. Jungfrau-Marathon",
        "year": 2011,
        "distance_category": "Marathon",
        "finish_time": "06:09:57",
        "finish_delta": "",
    },
    {
        "event": "Töwerland Osterlauf",
        "year": 2022,
        "distance_category": "5 Kilometer",
        "finish_time": "00:22:31",
        "finish_delta": "",
    },
    {
        "event": "14. Korschenbroicher Waldlauf",
        "year": 2018,
        "distance_category": "5 Kilometer",
        "finish_time": "00:21:55",
        "finish_delta": "",
    },
]

distance_categories_running = ["5 Kilometer", "10 Kilometer", "Halbmarathon", "Marathon"]

for category_2 in distance_categories_running:
    races = [r for r in my_races if r["distance_category"] == category_2]

    with st.expander(f"🏁 {category_2}", expanded=False):
        if races:
            for race in races:
                st.write(f"### {race['event']} ({race['year']})")

                cols = st.columns(1)
                cols[0].metric("⏱️ Finish", race["finish_time"], race["finish_delta"])

                if category_2 == "5 Kilometer":
                    run_distance_race_km = 5
                elif category_2 == "10 Kilometer":
                    run_distance_race_km = 10
                elif category_2 == "Halbmarathon":
                    run_distance_race_km = 21.1
                elif category_2 == "Marathon":
                    run_distance_race_km = 42.2

                run_seconds = time_to_seconds(race["finish_time"])

                run_pace = seconds_to_pace(run_seconds / run_distance_race_km) if run_seconds else "--:--"

                pace_cols = st.columns(1)
                pace_cols[0].metric("Ø Run-Pace (min/km)", run_pace)

                st.divider()
        else:
            st.write("Keine Wettkämpfe vorhanden.")

st.write("---")

# ---------- Meine nächsten Wettkämpfe ----------

st.header("Meine nächsten Wettkämpfe")

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
            margin-bottom: 30px;
             background-color: rgba(255, 255, 255, 0.05);
        ">
            <strong>🏁 {race['name']}</strong><br>
            📏 {race['distance']}<br>
            📆 {race['date'].strftime('%d.%m.%Y')}<br>
            ⏳ Noch <strong><span style='color:#39FF14;'>{delta}</span></strong> Tage
        </div>
    """, unsafe_allow_html=True)