import streamlit as st
from garminconnect import Garmin
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

# Variante: Nutze Umgebungsvariablen für deine Zugangsdaten (empfohlen!)
EMAIL = os.getenv("GARMIN_EMAIL")
PASSWORD = os.getenv("GARMIN_PASSWORD")

# Oder: Direkt eintragen (NICHT empfohlen!)
# EMAIL = "deine@email.com"
# PASSWORD = "deinpasswort"

# Garmin-Session starten
client = Garmin(EMAIL, PASSWORD, mfa=TRUE)
client.login()

# Beispiel: Hole die letzten 20 Aktivitäten
activities = client.get_activities(0, 20)  # (start, limit)

# In Pandas-DataFrame umwandeln
df = pd.DataFrame(activities)

print(df.head())

# Speichere als CSV
df.to_csv("garmin_activities.csv", index=False)
print("Daten gespeichert in garmin_activities.csv")