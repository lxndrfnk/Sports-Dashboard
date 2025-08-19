import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import ast
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# --------------------------------
# ---------- Schriftart ----------
# --------------------------------

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=League+Spartan&display=swap');

        html, body, [class*="css"]  {
            font-family: 'League Spartan', sans-serif;
        }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------
# ---------- Textbereich ----------
# ---------------------------------

st.title("🤔 20 Jahre Laufen – und wofür?")

st.write("---")

st.header("➡️ Hypothese")

with st.expander("Meine Effizienz steigt: mehr Geschwindigkeit bei gleicher oder niedrigerer Herzfrequenz.", expanded=False):

    st.markdown("""
                
    Mit meinen Garmin-Daten zeige ich, wie sich Herzfrequenz und Laufgeschwindigkeit im Training entwickeln.
    """)

st.write("---")

st.header("➡️ Analyse")

# ---------------------------------------
# ---------- Daten vorbereiten ----------
# ---------------------------------------

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

# -------------------------------
# ---------- Erwartung ----------
# -------------------------------

def make_scatter_example(r: float, color: str, title: str):
    """
    Erzeugt einen kleinen Demo-Scatter für eine gewünschte Korrelation r.
    """
    rng = np.random.default_rng(42 + int(r*100))
    n = 36
    cov = np.array([[1, r],
                    [r, 1]])
    xy = rng.multivariate_normal(mean=[0, 0], cov=cov, size=n)
    x = xy[:, 0]
    y = xy[:, 1]

    m, b = np.polyfit(x, y, 1)
    x_line = np.linspace(x.min(), x.max(), 50)
    y_line = m * x_line + b

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=x, y=y,
        mode="markers",
        marker=dict(color=color, size=8,
                    line=dict(width=1)),
        hovertemplate="x: %{x:.2f}<br>y: %{y:.2f}<extra></extra>",
        showlegend=False
    ))

    fig.add_trace(go.Scatter(
        x=x_line, y=y_line,
        mode="lines",
        line=dict(color=color, width=2),
        hoverinfo="skip",
        showlegend=False
    ))

    fig.update_layout(
        title=title,
        title_x=0.5,
        plot_bgcolor="#4b4c4d",
        paper_bgcolor="#4b4c4d",
        font=dict(color="white"),
        margin=dict(l=10, r=10, t=30, b=10),
        xaxis=dict(
            showline=True, linecolor="white",
            tickfont=dict(color="white"),
            ticks="outside", tickcolor="white", ticklen=4, tickwidth=1,
            showgrid=False, zeroline=False,
            showticklabels=False
        ),
        yaxis=dict(
            showline=True, linecolor="white",
            tickfont=dict(color="white"),
            ticks="outside", tickcolor="white", ticklen=4, tickwidth=1,
            showgrid=False, zeroline=False,
            showticklabels=False
        ),
        height=260
    )
    return fig

with st.expander("Erwartete Korrelation", expanded=False):
    c1, c2, c3 = st.columns(3)

    fig0  = make_scatter_example(r=0.0,  color="#ffffff", title="r = 0")
    fig05 = make_scatter_example(r=0.5,  color="#ffffff", title="r = 0,5")
    fig09 = make_scatter_example(r=0.9,  color="#ffffff", title="r = 0,9")

    with c1:
        st.plotly_chart(fig0,  use_container_width=True)
    with c2:
        st.plotly_chart(fig05, use_container_width=True)
    with c3:
        st.plotly_chart(fig09, use_container_width=True)

# ---------------------------------
# ---------- Scatterplot ----------
# ---------------------------------

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

# ---------------------------------------------
# ---------- Korrelationskoeffizient ----------
# ---------------------------------------------

correlation = np.corrcoef(df["averageHR"], df["speed_kmh"])[0, 1]

# ---------------------------
# ---------- Ampel ----------
# ---------------------------

if abs(correlation) >= 0.7:
    color = "#39FF14"  
elif abs(correlation) >= 0.4:
    color = "#FFD700"  
else:
    color = "#f94144"  

with st.expander("Korrelationskoeffizient (r) anzeigen", expanded=False):
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

# ----------------------------------------------------
# ---------- Diagramm: Durchschnittliche HF ----------
# ----------------------------------------------------

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
        rangemode="tozero",
        title="Ø Herzfrequenz (bpm)",   
        title_standoff=40,
        showgrid=False,
        showline=True,
        linecolor="white",
        tickcolor="white",
        color="white",
        zeroline=False
    ),
    margin=dict(l=20, r=20, t=20, b=40),
)

fig = go.Figure(layout=layout)

fig.add_trace(go.Scatter(
    x=df["startTimeLocal"],
    y=df["averageHR"],
    mode="lines+markers",
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

# -----------------------------------------------------------------
# ---------- Diagramm: Durchschnittliche Geschwindigkeit ----------
# -----------------------------------------------------------------

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
        rangemode="tozero",
        title="Ø Geschwindigkeit (km/h)",
        title_standoff=40,
        showgrid=False,
        showline=True,
        linecolor="white",
        tickcolor="white",
        ticks="outside",
        ticklen=6,
        tickwidth=1,
        tickfont=dict(color="white"),
        zeroline=False
    ),
    margin=dict(l=20, r=20, t=20, b=40)
)

fig = go.Figure(layout=layout)

fig.add_trace(go.Scatter(
    x=df["startTimeLocal"],
    y=df["speed_kmh"],
    mode="lines+markers",
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

# -------------------------------------------------------------------------------
# ---------- Vergleich: Herzfrequenz & Geschwindigkeit (Originalwerte) ----------
# -------------------------------------------------------------------------------

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
        rangemode="tozero",
        title="Ø Herzfrequenz (bpm)",
        title_standoff=40,
        showgrid=False,
        showline=True,
        linecolor="white",
        tickcolor="white",
        ticks="outside",
        ticklen=6,
        tickwidth=1,
        tickfont=dict(color="white"),
        zeroline=False
    ),
    yaxis2=dict(
        rangemode="tozero",
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
        tickfont=dict(color="white"),
        zeroline=False
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

# ---------------------------------------------------
# ---------- Normalisiertes Liniendiagramm ----------
# ---------------------------------------------------

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
        tickfont=dict(color="white"),
        zeroline=False,
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

highlight_date = pd.to_datetime("2025-05-06")

highlight_rows = df_filtered[df_filtered["startTimeLocal"].dt.date == highlight_date.date()]

if not highlight_rows.empty:
   
    fig.add_trace(go.Scatter(
        x=highlight_rows["startTimeLocal"],
        y=highlight_rows["Speed_norm"],
        mode="markers",
        marker=dict(color="green", size=10, symbol="circle"),
        name="",
        showlegend=False
    ))

    
    fig.add_trace(go.Scatter(
        x=highlight_rows["startTimeLocal"],
        y=highlight_rows["HR_norm"],
        mode="markers",
        marker=dict(color="green", size=10, symbol="circle"),  
        name="",
        showlegend=False
    ))

min_val = 0
max_val = 1

fig.add_shape(
    type="line",
    xref="paper", x0=0, x1=1,
    yref="y", y0=min_val, y1=min_val,
    line=dict(color="white", width=1),
)

fig.add_shape(
    type="line",
    xref="paper", x0=0, x1=1,
    yref="y", y0=max_val, y1=max_val,
    line=dict(color="white", width=1),
)

with st.expander("Normalisiertes Liniendiagramm", expanded=False):
    st.plotly_chart(fig, use_container_width=True)

# ----------------------------------------------------
# ---------- Differenz der Normalisierungen ----------
# ----------------------------------------------------

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
        tickfont=dict(color="white"),
        zeroline=False
    ),
    yaxis=dict(
        title="Differenz (Geschwindigkeit - HF)",
        title_standoff=40,
        showline=True,
        linecolor="white",
        tickcolor="white",
        ticks="outside",
        ticklen=6,
        tickwidth=1,
        tickfont=dict(color="white"),
        range=[-1, 1],
        tickmode="array",      
        tickvals=[-1, 0, 1],          
        zeroline=True,         
        zerolinecolor="white", 
        zerolinewidth=1
    )
)

fig_diff = go.Figure(layout=layout)

fig_diff.add_trace(go.Scatter(
    x=df_filtered["startTimeLocal"],
    y=df_filtered["Differenz"],
    mode="lines+markers",
    line=dict(color="white", width=2, dash="solid"),
    name="Differenz"
))

highlight_date = pd.to_datetime("2025-05-06").date()

mask = df_filtered["startTimeLocal"].dt.date == highlight_date
if mask.any():
    fig_diff.add_trace(go.Scatter(
        x=df_filtered.loc[mask, "startTimeLocal"],
        y=(df_filtered.loc[mask, "Speed_norm"] - df_filtered.loc[mask, "HR_norm"]),
        mode="markers",
        marker=dict(color="green", size=10, symbol="circle"),
        name="06.05.25",
        showlegend=False
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

# ------------------------------
# ---------- Ergebnis ----------
# ------------------------------

st.header("➡️ Ergebnis")

with st.expander("Zusammenfassende Analyse", expanded=False):
    st.markdown("""

    Im Zentrum dieser Untersuchung steht die Frage, ob sich durch mein Lauftraining eine Verbesserung der Ausdauerleistung erkennen lässt – messbar durch den Zusammenhang zwischen Herzfrequenz und Laufgeschwindigkeit.

    Die grundlegende Annahme war: 
    ```
    Mit zunehmender Ausdauer kann ich bei gleicher Geschwindigkeit eine niedrigere Herzfrequenz halten – oder bei höherer Geschwindigkeit die Herzfrequenz auf gleichem Niveau halten bzw. sogar senken.
    ```
    Die Analyse ergibt eine positive Korrelation zwischen durchschnittlicher Herzfrequenz und Geschwindigkeit – ein durchaus plausibles Ergebnis, das sich mit typischem Trainingsverhalten erklären lässt: Intensivere Läufe führen naturgemäß zu einer höheren Geschwindigkeit und gleichzeitig zu einer höheren Herzfrequenz. Das bedeutet: Die Korrelation spiegelt vor allem das Verhältnis zwischen Trainingsintensität und körperlicher Reaktion wider – nicht zwingend den Trainingseffekt.

    Um den Trainingseffekt sichtbar zu machen, wurden weitere Visualisierungen eingesetzt:
    ```
    • Ein normalisiertes Liniendiagramm skaliert beide Größen auf denselben Wertebereich (0–1) und ermöglicht so einen direkten visuellen Vergleich der Trends.
    • Ein Differenzdiagramm stellt die Lücke zwischen der Entwicklung von HF und Geschwindigkeit dar – hier lassen sich Fortschritte durch zunehmende Differenzwerte erkennen.
    ```
    Insgesamt lässt sich aus den Verlaufsdiagrammen eine tendenzielle Verbesserung ablesen: Während die Geschwindigkeit leicht zunimmt, bleibt die Herzfrequenz im Mittel stabil oder sinkt leicht – ein Indiz für wachsende Effizienz im Training.
    """)

st.write("---")

st.header("➡️ Plot Twist")

with st.expander("Hinweis zur Dateninterpretation", expanded=False):
    st.markdown("""

    Ab dem 12. Januar 2025 habe ich von der Herzfrequenzmessung am Handgelenk auf einen Brustgurt umgestellt. Dadurch sind die Messwerte seitdem deutlich präziser und Schwankungen in der Differenzkurve können auch auf diese verbesserte Datenerfassung zurückzuführen sein.

    Dieser Umstand zeigt, dass man bei der Analyse und Interpretation von Trainingsdaten immer den Kontext beachten sollte – Veränderungen in der Ausrüstung, den Messmethoden oder anderen Rahmenbedingungen können die Aussagekraft stark beeinflussen.

    Jetzt bleibt spannend zu sehen, wie sich die Werte in Zukunft entwickeln – und ob mein Training den gewünschten Effekt bringt.
    """)
