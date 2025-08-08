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

st.write("---")

# ---------- Effizienz-Trend & Projektion ----------

st.header("➡️ Effizienz-Trend")

st.write("""
    Der Effizienz-Trend beschreibt, wie sich das Verhältnis zwischen meiner Laufgeschwindigkeit und meiner Herzfrequenz im Zeitverlauf entwickelt.  
    Dazu werden beide Werte zunächst auf eine vergleichbare Skala (0–1) normalisiert und anschließend die Differenz berechnet:  
    
    > **Effizienz = normalisierte Geschwindigkeit – normalisierte Herzfrequenz**  
    
    Positive Werte bedeuten, dass ich im Verhältnis zu meiner Herzfrequenz schneller gelaufen bin – ein Zeichen für gesteigerte Ausdauer und ökonomischere Belastung.  
    Negative Werte deuten dagegen auf eine geringere Effizienz hin.  
    
    **Berechnung des Trends:**  
    Für die Trendlinie werden die einzelnen Effizienzwerte gegen das Datum aufgetragen. Anschließend wird eine lineare Regression durchgeführt, um den Verlauf zu glätten und eine Richtung anzuzeigen.  
    So lässt sich abschätzen, ob meine Trainingsentwicklung über die Zeit eher positiv oder negativ verläuft.  
    """)

# Daten frisch laden (damit keine alten Filter stören)
df_all = pd.read_csv("garmin_activities.csv")
df_all["startTimeLocal"] = pd.to_datetime(df_all["startTimeLocal"], errors="coerce")

# typeKey robust bestimmen
if "activityTypeDTO.typeKey" in df_all.columns:
    df_all["typeKey"] = df_all["activityTypeDTO.typeKey"]
elif "activityType" in df_all.columns:
    import ast
    df_all["typeKey"] = df_all["activityType"].apply(
        lambda x: ast.literal_eval(x).get("typeKey") if isinstance(x, str) and "{" in x else x
    )
else:
    df_all["typeKey"] = None

# Nur Läufe, nur nach 12.01.2025, nur valide
cutoff = pd.Timestamp("2025-01-12")
dfR = (
    df_all[(df_all["typeKey"] == "running")]
          .dropna(subset=["startTimeLocal","distance","duration","averageHR"])
)
dfR = dfR[dfR["startTimeLocal"] > cutoff].copy()
dfR = dfR[dfR["duration"] > 0]
dfR["speed_kmh"] = (dfR["distance"]/1000) / (dfR["duration"]/3600)

if dfR.empty:
    st.info("Keine Laufdaten nach 12.01.2025 gefunden.")
else:
    # Min-Max-Normalisierung (nur auf Nach-Cutoff-Daten)
    def minmax(s):
        lo, hi = s.min(), s.max()
        return (s - lo) / (hi - lo) if hi > lo else s*0 + 0.5
    dfR["HR_norm"]    = minmax(dfR["averageHR"])
    dfR["Speed_norm"] = minmax(dfR["speed_kmh"])

    # Effizienz = Speed_norm - HR_norm
    dfR["efficiency"] = dfR["Speed_norm"] - dfR["HR_norm"]

    # Wöchentlichen Mittelwert bilden
    w = (dfR
        .set_index("startTimeLocal")
        .resample("W-MON")["efficiency"]
        .mean()
        .dropna()
        .sort_index()
    )

    if len(w) < 3:
        st.info("Für eine Projektion werden mind. 3 Wochen mit Daten benötigt.")
    else:
        import numpy as np
        # Index für Regression (0..n-1)
        x = np.arange(len(w))
        y = w.values
        # lineare Trendlinie
        b1, b0 = np.polyfit(x, y, deg=1)  # y ≈ b1*x + b0

        # Forecast für die nächsten 8 Wochen
        steps = 8
        x_future = np.arange(len(w), len(w)+steps)
        y_future = b1*x_future + b0

        # Plot
        import plotly.graph_objects as go
        fig_trend = go.Figure()

        fig_trend.add_trace(go.Scatter(
            x=w.index, y=w.values,
            mode="lines+markers",
            line=dict(color="white", width=2),
            marker=dict(color="white", size=6),
            name="Effizienz (wöchentlich)"
        ))

        fig_trend.add_trace(go.Scatter(
            x=pd.date_range(w.index[-1] + pd.Timedelta(days=7), periods=steps, freq="W-MON"),
            y=y_future,
            mode="lines",
            line=dict(color="lightgray", width=2, dash="dash"),
            name="Projektion (8 Wochen)"
        ))

        fig_trend.update_layout(
            plot_bgcolor="#4b4c4d",
            paper_bgcolor="#4b4c4d",
            font=dict(color="white"),
            margin=dict(l=40, r=20, t=30, b=40),
            xaxis=dict(
                title="",
                showline=True, linecolor="white",
                tickfont=dict(color="white"),
                ticklen=6, tickwidth=1, tickcolor="white", ticks="outside"
            ),
            yaxis=dict(
                title="Effizienz (norm. Speed − norm. HF)",
                title_standoff=40,
                showline=True, linecolor="white",
                tickfont=dict(color="white"),
                ticklen=6, tickwidth=1, tickcolor="white", ticks="outside",
                showgrid=True, gridcolor="white",
                zeroline=False
            ),
            showlegend=False
        )

        with st.expander("Diagramm anzeigen", expanded=False):
            st.plotly_chart(fig_trend, use_container_width=True)
