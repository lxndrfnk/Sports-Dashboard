from garminconnect import Garmin
import pandas as pd

EMAIL = "hi@alexanderfink.com"
PASSWORD = "DataPlus_2025"

client = Garmin(EMAIL, PASSWORD)
client.login()

all_activities = []
batch_size = 100
start = 0

while True:
    activities = client.get_activities(start, batch_size)
    if not activities:
        break
    all_activities.extend(activities)
    start += batch_size

df = pd.DataFrame(all_activities)

columns_to_keep = [
    "startTimeLocal",
    "activityType",
    "activityTypeDTO.typeKey",
    "distance",
    "duration",
    "averageSpeed",
    "averageHR",
    "calories"
]

columns_available = [col for col in columns_to_keep if col in df.columns]
df = df[columns_available]

df.to_csv("garmin_activities.csv", index=False)
print("✅ Reduzierte CSV gespeichert!")
