import streamlit as st

# ---------- Seiteneinstellungen ----------

st.set_page_config(
    page_title="Sports-Dashboard",
    page_icon="🏅",
    layout="wide"
)

# ---------- Import weiterer Module ----------

import pandas as pd
import ast
import datetime
import matplotlib.pyplot as plt
from datetime import date

# ---------- Textblock ----------

import streamlit as st

st.title("🏁 Willkommen in meinem Sports-Dashboard")

st.markdown("""
Dieses interaktive Dashboard visualisiert persönliche Trainings- und Wettkampfdaten aus meinem Garmin-Account mit dem Ziel, sportliche Entwicklungen **datenbasiert sichtbar** zu machen.  
Besonderer Fokus liegt auf der Auswertung meiner **Laufleistungen** in Kombination mit physiologischen Kennzahlen wie der **Herzfrequenz**.

### Was dich erwartet:
- Überblick über absolvierte **Triathlon- und Laufwettkämpfe**  
- **Trainingsauswertung** nach Zeit, Distanz, Tempo und Intensität  
- Entwicklung von **Herzfrequenz & Geschwindigkeit** im Zeitverlauf  
- Analyse des Zusammenhangs zwischen **Belastung & Leistung**

Das Projekt wurde im Rahmen einer Fortbildung zu **Big Data & Künstlicher Intelligenz** entwickelt und kombiniert reale Fitnessdaten mit datenanalytischen Methoden in einer modernen Web-App.
""")


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