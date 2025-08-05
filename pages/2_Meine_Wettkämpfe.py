import streamlit as st
import pandas as pd
import ast
import datetime
import matplotlib.pyplot as plt
from datetime import date

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


st.title("🏅 Meine bisherigen Wettkämpfe")

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

