import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import ast
import numpy as np
import plotly.graph_objs as go
from datetime import datetime
from datetime import timedelta

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

# ------------------------------
# ---------- Prognose ----------
# ------------------------------

st.title("🧠 Prognose")

# # ---------------------------------------
# # ---------- Daten vorbereiten ----------
# # ---------------------------------------

# df = pd.read_csv("garmin_activities.csv")
# df["startTimeLocal"] = pd.to_datetime(df["startTimeLocal"], errors="coerce")

# if "activityTypeDTO.typeKey" in df.columns:
#     df["typeKey"] = df["activityTypeDTO.typeKey"]
# elif "activityType" in df.columns:
#     df["typeKey"] = df["activityType"].apply(lambda x: ast.literal_eval(x).get("typeKey") if isinstance(x, str) and "{" in x else x)
# else:
#     df["typeKey"] = None

# df = df[
#     (df["typeKey"] == "running") &
#     df["averageHR"].notna() &
#     df["duration"].notna() &
#     df["distance"].notna() &
#     (df["duration"] > 0)
# ].copy()

# df = df.sort_values("startTimeLocal")
# df["distance_km"] = df["distance"] / 1000
# df["duration_h"] = df["duration"] / 3600
# df["speed_kmh"] = df["distance_km"] / df["duration_h"]

# st.write("---")

# fig = px.scatter(
#     df,
#     x="averageHR",
#     y="speed_kmh",
#     trendline="ols",  
#     labels={
#         "averageHR": "Ø Herzfrequenz (bpm)",
#         "speed_kmh": "Ø Geschwindigkeit (km/h)"
#     },
#     title="",  
#     template="plotly_dark",
#     width=1000,
#     height=500
# )

# fig.update_layout(
#     plot_bgcolor="#4b4c4d",
#     paper_bgcolor="#4b4c4d",
#     font=dict(color="white"),
#     margin=dict(l=40, r=20, t=40, b=40),
#     xaxis=dict(
#         title="Ø Herzfrequenz (bpm)",
#         title_standoff=40,
#         color="white",
#         tickcolor="white",
#         linecolor="white",
#         showline=True,
#         showgrid=False,
#         ticks="outside",           
#         ticklen=6,                
#         tickwidth=1,              
#         tickfont=dict(color="white")
#     ),
#     yaxis=dict(
#         title="Ø Geschwindigkeit (km/h)",
#         title_standoff=40,
#         color="white",
#         tickcolor="white",
#         linecolor="white",
#         showline=True,
#         showgrid=False,
#         ticks="outside",
#         ticklen=6,
#         tickwidth=1,
#      tickfont=dict(color="white")
#     )
# )

# fig.update_traces(marker=dict(color="white", size=8, line=dict(width=1)))

# with st.expander("Scatterplot: Zusammenhang zwischen Herzfrequenz und Geschwindigkeit", expanded=False):
#     st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------
# ---------- Scatterplot (neu) ----------
# ---------------------------------------

df_all = pd.read_csv("garmin_activities.csv")
df_all["startTimeLocal"] = pd.to_datetime(df_all["startTimeLocal"], errors="coerce")

if "activityTypeDTO.typeKey" in df_all.columns:
    df_all["typeKey"] = df_all["activityTypeDTO.typeKey"]
elif "activityType" in df_all.columns:
    df_all["typeKey"] = df_all["activityType"].apply(
        lambda x: ast.literal_eval(x).get("typeKey") if isinstance(x, str) and "{" in x else x
    )
else:
    df_all["typeKey"] = None

dfR = (
    df_all[(df_all["typeKey"] == "running")]
         .dropna(subset=["startTimeLocal", "distance", "duration", "averageHR"])
         .copy()
)
dfR = dfR[dfR["duration"] > 0]

cutoff = pd.to_datetime("2025-01-12")
dfR = dfR[dfR["startTimeLocal"] > cutoff]

if dfR.empty:
    st.info("Keine gültigen Laufdaten nach dem 12.01.2025 gefunden.")
else:
    dfR["speed_kmh"] = (dfR["distance"]/1000) / (dfR["duration"]/3600)

    x = dfR["averageHR"].to_numpy()
    y = dfR["speed_kmh"].to_numpy()
    m, b = np.polyfit(x, y, 1)  # y = m*x + b
    x_line = np.linspace(x.min(), x.max(), 100)
    y_line = m * x_line + b

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=dfR["averageHR"], y=dfR["speed_kmh"],
        mode="markers",
        marker=dict(color="white", size=8, line=dict(width=1)),
        hovertemplate="Ø HF: %{x:.0f} bpm<br>Ø Speed: %{y:.2f} km/h<extra></extra>",
        name=""
    ))

    fig.add_trace(go.Scatter(
        x=x_line, y=y_line,
        mode="lines",
        line=dict(color="#ffffff", width=2),
        hoverinfo="skip",
        name=""
    ))

    fig.update_layout(
        plot_bgcolor="#4b4c4d",
        paper_bgcolor="#4b4c4d",
        font=dict(color="white"),
        margin=dict(l=40, r=20, t=20, b=40),
        xaxis=dict(
            title="Ø Herzfrequenz (bpm)",
            title_standoff=40,
            showline=True, linecolor="white",
            tickcolor="white", ticklen=6, tickwidth=1, ticks="outside",
            tickfont=dict(color="white"),
            showgrid=False
        ),
        yaxis=dict(
            title="Ø Geschwindigkeit (km/h)",
            title_standoff=40,
            showline=True, linecolor="white",
            tickcolor="white", ticklen=6, tickwidth=1, ticks="outside",
            tickfont=dict(color="white"),
            showgrid=False
        ),
        showlegend=False
    )

    with st.expander("Scatterplot (neu) anzeigen", expanded=False):
        st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------
# ---------- Korrelationskoeffizient ----------
# ---------------------------------------------

correlation = float(np.corrcoef(dfR["averageHR"], dfR["speed_kmh"])[0, 1])

# ---------------------------
# ---------- Ampel ----------
# ---------------------------
if abs(correlation) >= 0.7:
    color = "#39FF14"   # grün
elif abs(correlation) >= 0.4:
    color = "#FFD700"   # gelb
else:
    color = "#f94144"   # rot

with st.expander("Korrelationskoeffizient (r) anzeigen", expanded=False):
    st.markdown(
        f"""
        <div style='
            display:flex;
            justify-content:center;
            align-items:center;
            height:200px;
            color:white;
            font-family: Arial, sans-serif;
        '>
            <div style='text-align:center;'>
                <div style='font-size:20px; margin-bottom:10px;'>
                    Korrelation zwischen Herzfrequenz & Geschwindigkeit
                </div>
                <div style='font-size:36px; font-weight:bold; color:{color};'>
                    {correlation:.2f}
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.write("---")

# --------------------------------------------------
# ---------- Effizienz-Trend & Projektion ----------
# --------------------------------------------------

st.header("➡️ Effizienz-Trend")

tab1, tab2, tab3 = st.tabs(["Was ist das?", "Formel & Beispiel", "Wie lese ich das?"])

with tab1:
    st.markdown("""  
        Er zeigt, wie gut ich im Verhältnis zu meiner Herzfrequenz (HF) laufe:
        
        ```
        • Hohe Geschwindigkeit bei niedriger HF = effizient  
        • Niedrige Geschwindigkeit bei hoher HF = weniger effizient
        ```
        
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
        • Rote, gestrichelte Linie: Trend
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

# st.write("---")

# -------------------------------------
# ---------- Effizienz-Trend ----------
# -------------------------------------

df_all = pd.read_csv("garmin_activities.csv")
df_all["startTimeLocal"] = pd.to_datetime(df_all["startTimeLocal"], errors="coerce")

if "activityTypeDTO.typeKey" in df_all.columns:
    df_all["typeKey"] = df_all["activityTypeDTO.typeKey"]
elif "activityType" in df_all.columns:
    df_all["typeKey"] = df_all["activityType"].apply(
        lambda x: ast.literal_eval(x).get("typeKey") if isinstance(x, str) and "{" in x else x
    )
else:
    df_all["typeKey"] = None

dfR = (
    df_all[(df_all["typeKey"] == "running")]
         .dropna(subset=["startTimeLocal", "distance", "duration", "averageHR"])
         .copy()
)
dfR = dfR[dfR["duration"] > 0]

cutoff_date = pd.to_datetime("2025-01-12")
dfR = dfR[dfR["startTimeLocal"] > cutoff_date]

if dfR.empty:
    st.info("Keine gültigen Laufdaten nach dem 12.01.2025 gefunden.")
else:
    dfR["speed_kmh"] = (dfR["distance"] / 1000) / (dfR["duration"] / 3600)

    def minmax(s):
        lo, hi = s.min(), s.max()
        return (s - lo) / (hi - lo) if hi > lo else s * 0 + 0.5

    dfR["HR_norm"]    = minmax(dfR["averageHR"])
    dfR["Speed_norm"] = minmax(dfR["speed_kmh"])

    dfR["efficiency"] = dfR["Speed_norm"] - dfR["HR_norm"]

    df_daily = (
        dfR.groupby(dfR["startTimeLocal"].dt.date)["efficiency"]
           .mean()
           .reset_index()
           .rename(columns={"startTimeLocal": "date", "efficiency": "eff_daily"})
    )
    df_daily["date"] = pd.to_datetime(df_daily["date"])
    df_daily = df_daily.sort_values("date")

    if len(df_daily) < 3:
        st.info("Für eine Trendlinie werden mindestens 3 Tage mit Daten benötigt.")
    else:
        x = (df_daily["date"] - df_daily["date"].min()).dt.days.to_numpy()
        y = df_daily["eff_daily"].to_numpy()
        b1, b0 = np.polyfit(x, y, deg=1)

        y_hat = b1 * x + b0

        fig = go.Figure()

        
        fig.add_trace(go.Scatter(
            x=df_daily["date"],
            y=df_daily["eff_daily"],
            mode="lines+markers",
            line=dict(color="white", width=2),
            marker=dict(color="white", size=6),
            name="Effizienz"
        ))

        fig.add_trace(go.Scatter(
            x=df_daily["date"],
            y=y_hat,
            mode="lines",
            line=dict(color="#f94144", width=2, dash="dash"),
            name="Trend"
        ))

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
                zeroline=False,
                range=[-1, 1],
                tickvals=[-1, -0.5, 0, 0.5, 1]
            ),
            showlegend=False
        )

        with st.expander("Effizienz-Trend anzeigen", expanded=False):
            st.plotly_chart(fig, use_container_width=True)

st.write("---")

# -----------------------------
# ---------- Tabelle ----------
# -----------------------------

# if "activityTypeDTO.typeKey" in df_all.columns:
#     df_all["typeKey"] = df_all["activityTypeDTO.typeKey"]
# elif "activityType" in df_all.columns:
#     df_all["typeKey"] = df_all["activityType"].apply(
#         lambda x: ast.literal_eval(x).get("typeKey") if isinstance(x, str) and "{" in x else x
#     )
# else:
#     df_all["typeKey"] = None

# dfR = (
#     df_all[(df_all["typeKey"] == "running")]
#          .dropna(subset=["startTimeLocal", "distance", "duration", "averageHR"])
#          .copy()
# )
# dfR = dfR[dfR["duration"] > 0]

# cutoff = pd.to_datetime("2025-01-12")
# dfR = dfR[dfR["startTimeLocal"] > cutoff]

# if dfR.empty:
#     st.info("Keine gültigen Laufdaten nach dem 12.01.2025 gefunden.")
# else:
#     dfR["speed_kmh"] = (dfR["distance"] / 1000) / (dfR["duration"] / 3600)

#     def minmax(s):
#         lo, hi = s.min(), s.max()
#         return (s - lo) / (hi - lo) if hi > lo else s*0 + 0.5

#     dfR["HR_norm"]    = minmax(dfR["averageHR"])
#     dfR["Speed_norm"] = minmax(dfR["speed_kmh"])

#     dfR["efficiency"] = dfR["Speed_norm"] - dfR["HR_norm"]

#     df_daily = (
#         dfR.groupby(dfR["startTimeLocal"].dt.date)["efficiency"]
#            .mean()
#            .reset_index()
#            .rename(columns={"startTimeLocal": "date", "efficiency": "eff_daily"})
#            .sort_values("date")
#            .reset_index(drop=True)
#     )

#     df_daily["Δ zum Vortag"] = df_daily["eff_daily"].diff()

#     df_show = df_daily.copy()
#     df_show["Datum"] = pd.to_datetime(df_show["date"]).dt.strftime("%d.%m.%Y")
#     df_show["Effizienz"] = df_show["eff_daily"].round(3)
#     df_show["Änderung"] = df_show["Δ zum Vortag"].apply(
#         lambda x: "" if pd.isna(x) else f"{x:+.3f}"
#     )

#     df_show = df_show[["Datum", "Effizienz", "Änderung"]]

#     with st.expander("Änderung der Effizienz je Trainingstag (ab 12.01.2025)", expanded=False):
#         st.dataframe(
#         df_show.style.set_properties(**{'text-align': 'left'}),
#         use_container_width=True,
#         hide_index=True
#     )

#------------------------------------------
# ---------- Verhältnis-Diagramm ----------
#------------------------------------------

st.header("➡️ Verhältnis: Herzfrequenz / Geschwindigkeit")

if "speed_kmh" not in dfR.columns:
    dfR["speed_kmh"] = (dfR["distance"]/1000) / (dfR["duration"]/3600)

dfR["hr_per_speed"] = dfR["averageHR"] / dfR["speed_kmh"]

df_ratio_daily = (
    dfR.groupby(dfR["startTimeLocal"].dt.date)["hr_per_speed"]
        .mean()
        .reset_index()
        .rename(columns={"startTimeLocal": "date", "hr_per_speed": "ratio"})
)
df_ratio_daily["date"] = pd.to_datetime(df_ratio_daily["date"])

df_ratio_daily["ratio_smooth"] = df_ratio_daily["ratio"].rolling(window=10, center=True).mean()

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df_ratio_daily["date"],
    y=df_ratio_daily["ratio"],
    mode="markers+lines",
    line=dict(color="white", width=2),
    marker=dict(color="white", size=6),
    name="Tageswerte"
))

fig.add_trace(go.Scatter(
    x=df_ratio_daily["date"],
    y=df_ratio_daily["ratio_smooth"],
    mode="lines",
    line=dict(color="#f94144", width=2, dash="dash"),
    name="10-Tage Durchschnitt"
))

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
        title="Herzfrequenz pro Geschwindigkeit (bpm pro km/h)",
        title_standoff=40,
        showline=True, linecolor="white",
        tickfont=dict(color="white"),
        ticklen=6, tickwidth=1, tickcolor="white", ticks="outside",
        showgrid=False, gridcolor="white",
        zeroline=False
    ),
    showlegend=True
)

with st.expander("Diagramm anzeigen", expanded=False):
    st.plotly_chart(fig, use_container_width=True)

with st.expander("Erklärung", expanded=False):
    st.markdown("""

    Das Verhältnis zeigt, wie viele Herzschläge ich brauche, um eine bestimmte Geschwindigkeit zu halten.
    Je weniger Schläge pro km/h, desto effizienter bin ich unterwegs.
    Es ist also ein direkter Hinweis auf meine Ausdauerleistung.

    Stell dir vor, du schaust dir nicht jeden einzelnen Trainingstag an, sondern immer einen kleinen Abschnitt, z.B. die letzten 10 Tage.
    Dann bildest du daraus einen Durchschnittswert.
    Das machst du für jeden Abschnitt – so entsteht eine glatte Kurve, die besser zeigt, ob es aufwärts oder abwärts geht.    
    """)

with st.expander("Zukünftige Implementierungen", expanded=False):
    st.markdown("""
        • Automatischer Datenabruf  
        • Exakte Daten, keine Durchschnittswerte
        
    """)

