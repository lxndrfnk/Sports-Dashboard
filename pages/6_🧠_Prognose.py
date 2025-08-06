import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import ast
import numpy as np
import plotly.graph_objs as go
from datetime import datetime

# ---------- Schriftart ----------

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=League+Spartan&display=swap');

        html, body, [class*="css"]  {
            font-family: 'League Spartan', sans-serif;
        }
    </style>
""", unsafe_allow_html=True)

# ---------- Prognose ----------

st.title("🧠 Prognose")

# ---------- Daten laden ----------

df = pd.read_csv("garmin_activities.csv")
df["startTimeLocal"] = pd.to_datetime(df["startTimeLocal"], errors="coerce")
df = df[df["startTimeLocal"] > "2025-01-12"]

if "activityTypeDTO.typeKey" in df.columns:
    df["typeKey"] = df["activityTypeDTO.typeKey"]
elif "activityType" in df.columns:
    import ast
    df["typeKey"] = df["activityType"].apply(
        lambda x: ast.literal_eval(x).get("typeKey") if isinstance(x, str) and "{" in x else x
    )
else:
    df["typeKey"] = None

df = df[df["typeKey"] == "running"]
df = df.dropna(subset=["startTimeLocal", "distance", "duration"])
df = df[df["distance"] > 0]
df = df[df["duration"] > 0]

df["speed_kmh"] = (df["distance"] / 1000) / (df["duration"] / 3600)

df = df[df["distance"] >= 4000]

df = df.sort_values("startTimeLocal")

# ---------- Prognose per Linearer Regression ----------

x = np.arange(len(df))  
y = df["speed_kmh"].values

# Lineare Regression mit numpy
slope, intercept = np.polyfit(x, y, 1)
predicted = slope * x + intercept
future_index = len(x)
future_speed = slope * future_index + intercept

# Zielgeschwindigkeit berechnen
ziel_min_pro_km = 4
ziel_speed = 60 / ziel_min_pro_km  # = 15 km/h

# ---------- Diagramm ----------
layout = go.Layout(
    plot_bgcolor="#4b4c4d",
    paper_bgcolor="#4b4c4d",
    font=dict(color="white"),
    xaxis=dict(
        title=dict(
            text="",
            font=dict(color="white")
        ),
        tickfont=dict(color="white"),
        tickcolor="white",
        linecolor="white",
        showline=True
    ),
    yaxis=dict(
        title=dict(
            text="Geschwindigkeit (km/h)",
            font=dict(color="white")
        ),
        title_standoff=40,
        tickfont=dict(color="white"),
        tickcolor="white",
        linecolor="white",
        showline=True
    ),
    margin=dict(l=40, r=20, t=30, b=40),
)

fig = go.Figure(layout=layout)

# Originale Trainingsdaten
fig.add_trace(go.Scatter(
    x=df["startTimeLocal"],
    y=df["speed_kmh"],
    mode="lines",
    name="Ø Geschwindigkeit",
    line=dict(color="white", width=2),
    marker=dict(color="white")
))

# Lineare Trendlinie
fig.add_trace(go.Scatter(
    x=df["startTimeLocal"],
    y=predicted,
    mode="lines",
    name="Trend",
    line=dict(color="red", dash="dot", width=2)
))

# Zielgeschwindigkeit als horizontale Linie
fig.add_trace(go.Scatter(
    x=[df["startTimeLocal"].iloc[0], df["startTimeLocal"].iloc[-1]],
    y=[ziel_speed, ziel_speed],
    mode="lines",
    name="Ziel (15 km/h)",
    line=dict(color="green", dash="dash", width=2)
))

# Prognosepunkt hinzufügen
fig.add_trace(go.Scatter(
    x=[df["startTimeLocal"].iloc[-1] + pd.Timedelta(days=14)],
    y=[future_speed],
    mode="markers+text",
    name="Prognose",
    marker=dict(color="orange", size=10),
    text=[f"{future_speed:.1f} km/h"],
    textposition="top center"
))

st.plotly_chart(fig, use_container_width=True)

# ---------- Bewertung ----------
# if future_speed >= ziel_speed:
#     st.success(f"Du bist auf Kurs! Prognose: **{future_speed:.2f} km/h** ✅")
# else:
#     st.info(f"Prognose: **{future_speed:.2f} km/h** – Ziel: **15.00 km/h** ❗")

print(df.tail())  # oder df[["startTimeLocal", "speed_kmh"]].tail()

