import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import ast
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ---------- Schriftart ----------

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter&display=swap');

        html, body, [class*="css"]  {
            font-family: 'Inter', sans-serif;
        }
    </style>
""", unsafe_allow_html=True)

# ---------- Textbereich ----------

st.title("📈 Effizienzsteigerung im Ausdauertraining: Eine datenbasierte Untersuchung mittels Herzfrequenz-Geschwindigkeits-Beziehung.")

st.write("---")

st.header("➡️ Hypothese")

with st.expander("Mit zunehmender Ausdauer sinkt meine Herzfrequenz bei vergleichbarer Geschwindigkeit.", expanded=False):

    st.markdown("""
                
    Im Rahmen dieses Projekts werden Trainingsdaten aus meinem Garmin-Account systematisch ausgewertet, um sportliche Entwicklungen nachvollziehbar darzustellen. 
    Der Schwerpunkt liegt auf dem Zusammenhang zwischen meiner durchschnittlichen Herzfrequenz und meiner Laufgeschwindigkeit (km/h). 
    Neben Einzelverläufen beider Kennzahlen im Zeitverlauf werden diese zusätzlich normiert dargestellt, um Veränderungen visuell vergleichbar zu machen. 
    Ein separates Differenzdiagramm zeigt die Abweichung zwischen Herzfrequenz und Geschwindigkeit und ermöglicht Rückschlüsse auf Effizienzsteigerungen. 
    Ergänzend quantifiziert ein Scatterplot mit Regressionslinie die Korrelation zwischen beiden Größen. 
    Alle Auswertungen basieren auf echten Laufdaten. Ziel ist es, trainingsbedingte Entwicklungen datenbasiert sichtbar zu machen und die Wirksamkeit meines Ausdauertrainings zu bewerten.
    """)

st.write("---")

st.header("➡️ Analyse")

# ---------- Daten vorbereiten ----------

df = pd.read_csv("garmin_activities.csv")
df["startTimeLocal"] = pd.to_datetime(df["startTimeLocal"], errors="coerce")

if "activityTypeDTO.typeKey" in df.columns:
    df["typeKey"] = df["activityTypeDTO.typeKey"]
elif "activityType" in df.columns:
    df["typeKey"] = df["activityType"].apply(lambda x: ast.literal_eval(x).get("typeKey") if isinstance(x, str) and "{" in x else x)
else:
    df["typeKey"] = None

df = df[
    (df["typeKey"] == "running") &
    df["averageHR"].notna() &
    df["duration"].notna() &
    df["distance"].notna() &
    (df["duration"] > 0)
].copy()

df = df.sort_values("startTimeLocal")
df["distance_km"] = df["distance"] / 1000
df["duration_h"] = df["duration"] / 3600
df["speed_kmh"] = df["distance_km"] / df["duration_h"]

# ---------- Scatterplot ----------

fig = px.scatter(
    df,
    x="averageHR",
    y="speed_kmh",
    trendline="ols",  
    labels={
        "averageHR": "Ø Herzfrequenz (bpm)",
        "speed_kmh": "Ø Geschwindigkeit (km/h)"
    },
    title="",  
    template="plotly_dark",
    width=1000,
    height=500
)

fig.update_layout(
    plot_bgcolor="#4b4c4d",
    paper_bgcolor="#4b4c4d",
    font=dict(color="white"),
    margin=dict(l=40, r=20, t=40, b=40),
    xaxis=dict(
        title="Ø Herzfrequenz (bpm)",
        title_standoff=40,
        color="white",
        tickcolor="white",
        linecolor="white",
        showline=True,
        showgrid=False,
        ticks="outside",           
        ticklen=6,                
        tickwidth=1,              
        tickfont=dict(color="white")
    ),
    yaxis=dict(
        title="Ø Geschwindigkeit (km/h)",
        title_standoff=40,
        color="white",
        tickcolor="white",
        linecolor="white",
        showline=True,
        showgrid=False,
        ticks="outside",
        ticklen=6,
        tickwidth=1,
     tickfont=dict(color="white")
    )
)

fig.update_traces(marker=dict(color="white", size=8, line=dict(width=1)))

with st.expander("Scatterplot: Zusammenhang zwischen Herzfrequenz und Geschwindigkeit", expanded=False):
    st.plotly_chart(fig, use_container_width=True)

# ---------- Korrelationskoeffizient ----------

correlation = np.corrcoef(df["averageHR"], df["speed_kmh"])[0, 1]

# ---------- Ampel ----------

if abs(correlation) >= 0.7:
    color = "#39FF14"  
elif abs(correlation) >= 0.4:
    color = "#FFD700"  
else:
    color = "#f94144"  

with st.expander("Korrelationskoeffizient anzeigen", expanded=False):
    st.markdown(
        f"""
        <div style='
            display: flex;
            justify-content: center;
            align-items: center;
            height: 200px;
            color: white;
            font-family: Arial, sans-serif;
        '>
            <div style='text-align: center;'>
                <div style='font-size: 20px; margin-bottom: 10px;'>
                    Korrelation zwischen Herzfrequenz & Geschwindigkeit
                </div>
                <div style='font-size: 36px; font-weight: bold; color: {color};'>
                    {correlation:.2f}
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ---------- Diagramm: Durchschnittliche HF ----------

avg_hr = df["averageHR"].mean()

layout = go.Layout(
    plot_bgcolor="#4b4c4d",
    paper_bgcolor="#4b4c4d",
    font=dict(color="white"),
    xaxis=dict(
        title="",       
        title_standoff=40,                 
        showgrid=False,
        showline=True,
        linecolor="white",
        tickcolor="white",
        color="white"
    ),
    yaxis=dict(
        title="Ø Herzfrequenz (bpm)",   
        title_standoff=40,
        showgrid=False,
        showline=True,
        linecolor="white",
        tickcolor="white",
        color="white"
    ),
    margin=dict(l=20, r=20, t=20, b=40),
)

fig = go.Figure(layout=layout)

fig.add_trace(go.Scatter(
    x=df["startTimeLocal"],
    y=df["averageHR"],
    mode="lines",
    line=dict(color="white", width=2),
    name="Ø HF"
))

fig.add_trace(go.Scatter(
    x=df["startTimeLocal"],
    y=[avg_hr] * len(df),
    mode="lines",
    line=dict(color="lightgray", width=1, dash="dash"),
    name="Durchschnitt"
))

with st.expander("Durchschnittliche Herzfrequenz", expanded=False):
    st.plotly_chart(fig, use_container_width=True)

# ---------- Diagramm: Durchschnittliche Geschwindigkeit

df["speed_kmh"] = (df["distance"] / 1000) / (df["duration"] / 3600)
avg_speed = df["speed_kmh"].mean()

layout = go.Layout(
    plot_bgcolor="#4b4c4d",
    paper_bgcolor="#4b4c4d",
    font=dict(color="white"),
    xaxis=dict(
        title="",
        title_standoff=40,
        showgrid=False,
        showline=True,
        linecolor="white",
        tickcolor="white",
        ticks="outside",
        ticklen=6,
        tickwidth=1,
        tickfont=dict(color="white")
    ),
    yaxis=dict(
        title="Ø Geschwindigkeit (km/h)",
        title_standoff=40,
        showgrid=False,
        showline=True,
        linecolor="white",
        tickcolor="white",
        ticks="outside",
        ticklen=6,
        tickwidth=1,
        tickfont=dict(color="white")
    ),
    margin=dict(l=20, r=20, t=20, b=40)
)

fig = go.Figure(layout=layout)

fig.add_trace(go.Scatter(
    x=df["startTimeLocal"],
    y=df["speed_kmh"],
    mode="lines",
    line=dict(color="white", width=2, dash="dot"),
    name="Ø Geschwindigkeit"
))

fig.add_trace(go.Scatter(
    x=df["startTimeLocal"],
    y=[avg_speed] * len(df),
    mode="lines",
    line=dict(color="lightgray", width=1, dash="dash"),
    name="Durchschnitt"
))

with st.expander("Durchschnittliche Geschwindigkeit", expanded=False):
    st.plotly_chart(fig, use_container_width=True)

# ---------- Vergleich: Herzfrequenz & Geschwindigkeit (Originalwerte) ----------

df["speed_kmh"] = (df["distance"] / 1000) / (df["duration"] / 3600)

avg_hr = df["averageHR"].mean()
avg_speed = df["speed_kmh"].mean()

layout = go.Layout(
    plot_bgcolor="#4b4c4d",
    paper_bgcolor="#4b4c4d",
    font=dict(color="white"),
    margin=dict(l=20, r=20, t=20, b=40),
    xaxis=dict(
        title="",
        title_standoff=40,
        showgrid=False,
        showline=True,
        linecolor="white",
        tickcolor="white",
        ticks="outside",
        ticklen=6,
        tickwidth=1,
        tickfont=dict(color="white")
    ),
    yaxis=dict(
        title="Ø Herzfrequenz (bpm)",
        title_standoff=40,
        showgrid=False,
        showline=True,
        linecolor="white",
        tickcolor="white",
        ticks="outside",
        ticklen=6,
        tickwidth=1,
        tickfont=dict(color="white")
    ),
    yaxis2=dict(
        title="Ø Geschwindigkeit (km/h)",
        title_standoff=40,
        overlaying="y",
        side="right",
        showgrid=False,
        showline=True,
        linecolor="white",
        tickcolor="white",
        ticks="outside",
        ticklen=6,
        tickwidth=1,
        tickfont=dict(color="white")
    )
)

fig = go.Figure(layout=layout)

fig.add_trace(go.Scatter(
    x=df["startTimeLocal"],
    y=df["averageHR"],
    mode="lines",
    name="Ø Herzfrequenz",
    line=dict(color="white", width=2),
    yaxis="y"
))

fig.add_trace(go.Scatter(
    x=df["startTimeLocal"],
    y=df["speed_kmh"],
    mode="lines",
    name="Ø Geschwindigkeit",
    line=dict(color="lightgray", width=2, dash="dot"),
    yaxis="y2"
))

# Durchschnittslinie HF
# fig.add_trace(go.Scatter(
#     x=df["startTimeLocal"],
#     y=[avg_hr] * len(df),
#     mode="lines",
#     line=dict(color="white", width=1, dash="dash"),
#     name="HF-Durchschnitt",
#     showlegend=False,
#     yaxis="y"
# ))

# Durchschnittslinie Geschwindigkeit
# fig.add_trace(go.Scatter(
#     x=df["startTimeLocal"],
#     y=[avg_speed] * len(df),
#     mode="lines",
#     line=dict(color="lightgray", width=1, dash="dash"),
#     name="Speed-Durchschnitt",
#     showlegend=False,
#     yaxis="y2"
# ))

with st.expander("Vergleich: Herzfrequenz & Geschwindigkeit (Originalwerte)", expanded=False):
    st.plotly_chart(fig, use_container_width=True)

# ---------- Normalisiertes Liniendiagramm ----------

df_filtered = df[["startTimeLocal", "averageHR", "speed_kmh"]].dropna()

df_filtered["HR_norm"] = (
    (df_filtered["averageHR"] - df_filtered["averageHR"].min()) /
    (df_filtered["averageHR"].max() - df_filtered["averageHR"].min())
)

df_filtered["Speed_norm"] = (
    (df_filtered["speed_kmh"] - df_filtered["speed_kmh"].min()) /
    (df_filtered["speed_kmh"].max() - df_filtered["speed_kmh"].min())
)

layout = go.Layout(
    plot_bgcolor="#4b4c4d",
    paper_bgcolor="#4b4c4d",
    font=dict(color="white"),
    margin=dict(l=20, r=20, t=20, b=40),
    xaxis=dict(
        title="",
        title_standoff=40,
        showgrid=False,
        showline=True,
        linecolor="white",
        tickcolor="white",
        ticks="outside",
        ticklen=6,
        tickwidth=1,
        tickfont=dict(color="white")
    ),
    yaxis=dict(
        title="Normalisierte Werte (0–1)",
        title_standoff=40,
        showgrid=False,
        showline=True,
        linecolor="white",
        tickcolor="white",
        ticks="outside",
        ticklen=6,
        tickwidth=1,
        tickfont=dict(color="white")
    )
)

fig = go.Figure(layout=layout)

fig.add_trace(go.Scatter(
    x=df_filtered["startTimeLocal"],
    y=df_filtered["HR_norm"],
    mode="lines",
    name="Ø Herzfrequenz",
    line=dict(color="white", width=2)
))

fig.add_trace(go.Scatter(
    x=df_filtered["startTimeLocal"],
    y=df_filtered["Speed_norm"],
    mode="lines",
    name="Ø Geschwindigkeit",
    line=dict(color="lightgray", width=2, dash="dot")
))

with st.expander("Normalisiertes Liniendiagramm", expanded=False):
    st.plotly_chart(fig, use_container_width=True)

# ---------- Differenz der Normalisierungen ----------

df_filtered["Differenz"] = df_filtered["Speed_norm"] - df_filtered["HR_norm"]

layout = go.Layout(
    plot_bgcolor="#4b4c4d",
    paper_bgcolor="#4b4c4d",
    font=dict(color="white"),
    margin=dict(l=20, r=20, t=20, b=40),
    xaxis=dict(
        title="",
        title_standoff=40,
        showgrid=False,
        showline=True,
        linecolor="white",
        tickcolor="white",
        ticks="outside",
        ticklen=6,
        tickwidth=1,
        tickfont=dict(color="white")
    ),
    yaxis=dict(
        title="Differenz (Geschwindigkeit - HF)",
        title_standoff=40,
        showgrid=False,
        showline=True,
        linecolor="white",
        tickcolor="white",
        ticks="outside",
        ticklen=6,
        tickwidth=1,
        tickfont=dict(color="white")
    )
)

fig_diff = go.Figure(layout=layout)

fig_diff.add_trace(go.Scatter(
    x=df_filtered["startTimeLocal"],
    y=df_filtered["Differenz"],
    mode="lines",
    line=dict(color="white", width=2, dash="solid"),
    name="Differenz"
))

# fig_diff.add_trace(go.Scatter(
#     x=df_filtered["startTimeLocal"],
#     y=[df_filtered["Differenz"].mean()] * len(df_filtered),
#     mode="lines",
#     line=dict(color="lightgray", width=1, dash="dash"),
#     name="Durchschnitt"
# ))

with st.expander("Differenz der Normalisierungen", expanded=False):
    st.plotly_chart(fig_diff, use_container_width=True)

st.write("---")

# ---------- Ergebnis ----------

st.header("➡️ Ergebnis")

with st.expander("Zusammenfassende Analyse der Herzfrequenz-Geschwindigkeits-Beziehung", expanded=False):
    st.markdown("""

    Im Zentrum dieser Untersuchung steht die Frage, ob sich durch mein Lauftraining eine Verbesserung der Ausdauerleistung erkennen lässt – messbar durch den Zusammenhang zwischen Herzfrequenz und Laufgeschwindigkeit. Zur Beantwortung wurden ausschließlich Laufaktivitäten aus meinem Garmin-Profil herangezogen und systematisch analysiert.

    Die grundlegende Annahme war: **Wenn sich meine Ausdauer verbessert, sollte ich bei gleicher oder höherer Geschwindigkeit mit einer niedrigeren Herzfrequenz laufen können.** Erwartet hätte man in diesem Fall eine **negative Korrelation** zwischen den beiden Größen.

    Die tatsächliche Analyse ergibt jedoch eine **positive Korrelation von +0.4** zwischen durchschnittlicher Herzfrequenz und Geschwindigkeit – ein durchaus plausibles Ergebnis, das sich mit typischem Trainingsverhalten erklären lässt: Intensivere Läufe führen naturgemäß zu einer höheren Geschwindigkeit und gleichzeitig zu einer höheren Herzfrequenz. Das bedeutet: **Die Korrelation spiegelt vor allem das Verhältnis zwischen Trainingsintensität und körperlicher Reaktion wider – nicht zwingend den Trainingseffekt.**

    Um den **Trainingseffekt** dennoch sichtbar zu machen, wurden weitere Visualisierungen eingesetzt:
    - Ein **Liniendiagramm mit Zeitverlauf** zeigt getrennt die Entwicklung der durchschnittlichen Geschwindigkeit und Herzfrequenz über die letzten Monate.
    - Ein **normalisiertes Liniendiagramm** skaliert beide Größen auf denselben Wertebereich (0–1) und ermöglicht so einen direkten visuellen Vergleich der Trends.
    - Ein **Differenzdiagramm** stellt die Lücke zwischen der Entwicklung von HF und Geschwindigkeit dar – hier lassen sich Fortschritte durch abnehmende Differenzwerte oder eine Verlagerung der Kurve erkennen.

    Insgesamt lässt sich aus den Verlaufsdiagrammen eine **tendenzielle Verbesserung** ablesen: Während die Geschwindigkeit leicht zunimmt, bleibt die Herzfrequenz im Mittel stabil oder sinkt leicht – ein Indiz für wachsende Effizienz im Training.

    Die Korrelation selbst gibt daher **keinen direkten Hinweis auf eine Verbesserung**, sondern beschreibt nur die gleichzeitige Entwicklung zweier Werte pro Lauf. Erst die **Verlaufskurven und Differenzwerte** ermöglichen eine Bewertung der Frage, ob mein Training Wirkung zeigt.
    """)

st.write("---")

st.header("➡️ Plot Twist")