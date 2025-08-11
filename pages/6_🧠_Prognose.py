import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import ast
import numpy as np
import plotly.graph_objs as go
from datetime import datetime
from datetime import timedelta

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

st.write("---")

# ---------- Effizienz-Trend & Projektion ----------

st.header("➡️ Effizienz-Trend")

tab1, tab2, tab3 = st.tabs(["Was ist das?", "Formel & Beispiel", "Wie lese ich das?"])

with tab1:
    st.markdown("""  
        Er zeigt, wie gut ich im Verhältnis zu meiner Herzfrequenz (HF) laufe:
        
        ```
        • Hohe Geschwindigkeit bei niedriger HF = effizient  
        • Niedrige Geschwindigkeit bei hoher HF = weniger effizient
        ```
                
        Dafür rechne ich beide Größen (Geschwindigkeit, HF) auf eine gemeinsame Skala um.  
        So sind sie vergleichbar. Danach bilde ich die Differenz.
        
        """)

with tab2:
    st.markdown("""
        <u>Formel:</u>
        ```
        Effizienz = Normalisierte Geschwindigkeit − Normalisierte Herzfrequenz
        ```
                
        <u>Beispielrechnung:</u>
        ```        
        • Normalisierte Geschwindigkeit = 0.82
        • Normalisierte Herzfrequenz = 0.70 
        • Effizienz = 0.82 − 0.70 = 0.12
        ```
                
        <u>Bedeutung der Skala:</u>
        ```
        • Werte > 0: effizient  
        • Werte ≈ 0: neutral  
        • Werte < 0: nicht effizient
        ```
        """
        ,unsafe_allow_html=True        
        )

with tab3:
    st.markdown("""
        ```
        • Weiße Linie: Tageswerte (durchschnittliche Effizienz pro Tag)  
        • Rote, gestrichelte Linie: Trend/Prognose (glättet Schwankungen und zeigt die Richtung)
        ```
        
        <u>Interpretation:</u>
        ```
        • Trend steigt → Effizienz verbessert sich  
        • Trend flach → stabil  
        • Trend fällt → Effizienz nimmt ab
        ```
        """
        ,unsafe_allow_html=True       
        )

st.write("---")

# ---------- Diagramm ----------

# --- Daten laden ---
df_all = pd.read_csv("garmin_activities.csv")
df_all["startTimeLocal"] = pd.to_datetime(df_all["startTimeLocal"], errors="coerce")

# typeKey robust bestimmen
if "activityTypeDTO.typeKey" in df_all.columns:
    df_all["typeKey"] = df_all["activityTypeDTO.typeKey"]
elif "activityType" in df_all.columns:
    df_all["typeKey"] = df_all["activityType"].apply(
        lambda x: ast.literal_eval(x).get("typeKey") if isinstance(x, str) and "{" in x else x
    )
else:
    df_all["typeKey"] = None

# --- Nur Läufe, valide Daten ---
dfR = (
    df_all[(df_all["typeKey"] == "running")]
         .dropna(subset=["startTimeLocal", "distance", "duration", "averageHR"])
         .copy()
)
dfR = dfR[dfR["duration"] > 0]

# --- Filter ab 12.01.2025 ---
cutoff_date = pd.to_datetime("2025-01-12")
dfR = dfR[dfR["startTimeLocal"] > cutoff_date]

if dfR.empty:
    st.info("Keine gültigen Laufdaten nach dem 12.01.2025 gefunden.")
else:
    # Geschwindigkeit (km/h)
    dfR["speed_kmh"] = (dfR["distance"] / 1000) / (dfR["duration"] / 3600)

    # Min-Max-Normalisierung (auf den gefilterten Daten)
    def minmax(s):
        lo, hi = s.min(), s.max()
        return (s - lo) / (hi - lo) if hi > lo else s * 0 + 0.5

    dfR["HR_norm"]    = minmax(dfR["averageHR"])
    dfR["Speed_norm"] = minmax(dfR["speed_kmh"])

    # Effizienz = norm. Speed − norm. HF
    dfR["efficiency"] = dfR["Speed_norm"] - dfR["HR_norm"]

    # Tagesmittel NUR für Trainingstage (keine Lücken auffüllen)
    df_daily = (
        dfR.groupby(dfR["startTimeLocal"].dt.date)["efficiency"]
           .mean()
           .reset_index()
           .rename(columns={"startTimeLocal": "date", "efficiency": "eff_daily"})
    )
    df_daily["date"] = pd.to_datetime(df_daily["date"])
    df_daily = df_daily.sort_values("date")

    if len(df_daily) < 3:
        st.info("Für eine Trendlinie werden mindestens 3 unterschiedliche Trainingstage benötigt.")
    else:
        # Regression NUR über Trainingstage
        x_days = (df_daily["date"] - df_daily["date"].min()).dt.days.to_numpy()
        y_vals = df_daily["eff_daily"].to_numpy()
        slope, intercept = np.polyfit(x_days, y_vals, deg=1)

        # Trendwerte ausschließlich auf den vorhandenen Trainingstagen
        y_trend_on_training_days = slope * x_days + intercept

        # Plot
        fig = go.Figure()

        # 1) Tageswerte (weiß)
        fig.add_trace(go.Scatter(
            x=df_daily["date"],
            y=df_daily["eff_daily"],
            mode="lines+markers",
            line=dict(color="white", width=2),
            marker=dict(color="white", size=6),
            name="Effizienz (Trainingstage)"
        ))

        # 2) Trend NUR auf Trainingstagen (rot gestrichelt)
        fig.add_trace(go.Scatter(
            x=df_daily["date"],
            y=y_trend_on_training_days,
            mode="lines",
            line=dict(color="#f94144", width=2, dash="dash"),
            name="Trend (Trainingstage)"
        ))

        # Gestrichelte 0-Linie (über gesamte Breite)
        fig.add_shape(
            type="line",
            xref="paper", x0=0, x1=1,
            yref="y",     y0=0, y1=0,
            line=dict(color="white", width=1, dash="dash")
        )

        fig.update_layout(
            plot_bgcolor="#4b4c4d",
            paper_bgcolor="#4b4c4d",
            font=dict(color="white"),
            margin=dict(l=40, r=20, t=30, b=40),
            xaxis=dict(
                title="",
                showline=True, linecolor="white",
                tickfont=dict(color="white"),
                ticklen=6, tickwidth=1, tickcolor="white", ticks="outside",
                showgrid=False
            ),
            yaxis=dict(
                title="Effizienz (norm. Geschwindigkeit − norm. HF)",
                title_standoff=40,
                showline=True, linecolor="white",
                tickfont=dict(color="white"),
                ticklen=6, tickwidth=1, tickcolor="white", ticks="outside",
                showgrid=True, gridcolor="white",
                range=[-1, 1],
                tickvals=[-1, -0.5, 0, 0.5, 1],
                zeroline=False
            ),
            showlegend=False
        )

        with st.expander("Effizienz-Trend (tageweise, nur Trainingstage) anzeigen", expanded=False):
            st.plotly_chart(fig, use_container_width=True)
