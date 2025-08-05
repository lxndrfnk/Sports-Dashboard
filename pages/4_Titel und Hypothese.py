import streamlit as st

st.title("Effizienzsteigerung im Ausdauertraining: Eine datenbasierte Untersuchung mittels Herzfrequenz-Pace-Korrelation.")

st.header("Hypothese:")

st.subheader("Mit zunehmender Ausdauer sinkt meine Herzfrequenz bei vergleichbarem Tempo.")

st.write("""
Im Rahmen dieses Projekts werden Daten aus meinem Garmin-Account systematisch ausgewertet, um sportliche Entwicklungen sichtbar zu machen.
Besonderes Augenmerk liegt auf dem Zusammenhang zwischen meiner durchschnittlichen Herzfrequenz und meiner Laufleistung (Pace).
Zur Prüfung werden alle Laufaktivitäten zeitlich gefiltert und anschließend aggregiert.
Die Analyse berechnet wöchentliche Durchschnittswerte für Herzfrequenz und Pace.
Ein Liniendiagramm visualisiert die Entwicklungen beider Kennzahlen im Zeitverlauf.
Zudem wird die Korrelation zwischen Pace und Herzfrequenz über ein rollierendes Fenster analysiert.
So lassen sich Trends, Trainingsfortschritte oder Belastungsspitzen objektiv beurteilen.
Alle Auswertungen basieren auf echten Trainingsdaten.
Ziel ist es, datenbasiert Rückschlüsse auf die Wirksamkeit meines Trainings zu ziehen.
""")
