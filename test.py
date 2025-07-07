import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Garmin Dashboard", layout="wide")

st.title("📊 Mein persönliches Garmin Dashboard")

# CSV laden
try:
    df = pd.read_csv("garmin_activities.csv")
    st.success("Daten geladen!")

    st.write("**Vorschau:**")
    st.dataframe(df.head())

    # Beispiel-KPI: Anzahl Aktivitäten
    st.metric("Anzahl Aktivitäten", df.shape[0])

    # Beispiel-Plot: Distanz über Zeit
    if 'startTimeLocal' in df.columns:
        df['startTimeLocal'] = pd.to_datetime(df['startTimeLocal'])
        df = df.sort_values('startTimeLocal')
        
        fig, ax = plt.subplots()
        ax.plot(df['startTimeLocal'], df['distance']/1000)
        ax.set_xlabel("Datum")
        ax.set_ylabel("Distanz (km)")
        ax.set_title("Distanz pro Aktivität")
        st.pyplot(fig)

except FileNotFoundError:
    st.error("CSV-Datei nicht gefunden! Bitte zuerst fetch_garmin.py ausführen.")
