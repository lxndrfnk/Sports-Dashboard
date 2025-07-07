from garminconnect import Garmin
import pandas as pd
import os
from dotenv import load_dotenv

# .env laden
load_dotenv()

EMAIL = os.getenv("GARMIN_EMAIL")
PASSWORD = os.getenv("GARMIN_PASSWORD")

# Garmin-Session starten
client = Garmin(EMAIL, PASSWORD)
client.login(prompt_mfa=True)

# Aktivitäten holen (z. B. die letzten 50)
activities = client.get_activities(0, 50)

# In DataFrame
df = pd.DataFrame(activities)

# Als CSV speichern
df.to_csv("garmin_activities.csv", index=False)
print("✅ Garmin-Daten gespeichert in garmin_activities.csv")
