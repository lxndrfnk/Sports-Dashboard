# 🏃‍♂️ Sports Dashboard – Analyse meiner Ausdauerentwicklung

Dieses Dashboard visualisiert und analysiert Trainingsdaten aus meinem Garmin-Account, um sportliche Entwicklungen objektiv messbar zu machen. Es wurde vollständig mit [Streamlit](https://streamlit.io/) umgesetzt und ermöglicht datenbasierte Rückschlüsse auf die Wirksamkeit meines Ausdauertrainings.

---

## 🎯 Ziel des Projekts

Mit Hilfe von Herzfrequenz- und Geschwindigkeitsdaten soll erkennbar werden, ob mein Training zu einer besseren Effizienz geführt hat. Eine zentrale Hypothese lautet:

> **Mit zunehmender Ausdauer sinkt meine Herzfrequenz bei vergleichbarer Geschwindigkeit.**

---

## 🧩 Struktur der App

Die App besteht aus mehreren Seiten:

- `ℹ️ Allgemeine Informationen` – Einführung & Beschreibung des Projekts
- `🏅 Meine Wettkämpfe` – Übersicht über vergangene und geplante Laufveranstaltungen
- `📊 Trainingsdaten` – Umfangreiche Diagramme zu Puls, Tempo und Streckenlänge
- `❤️ Meine Trainingsbereiche` – Kategorisierung nach Pulszonen
- `🔬 Analyse` – Korrelation, Differenzverlauf, Normalisierung & Scatterplots
- `🧠 Prognose` – Zukünftige Entwicklung basierend auf aktuellen Trends

---

## 📈 Technische Features

- **Interaktive Diagramme** mit Plotly (inkl. Hover-Funktion)
- **Korrelation zwischen Puls und Geschwindigkeit** als Scatterplot mit Trendlinie
- **Differenzdiagramm** zur Visualisierung der Trainingswirksamkeit
- **Vergleich normalisierter Werte** zur objektiven Fortschrittsbeurteilung
- **Ampel-Metrik zur Interpretation der Korrelation**
- **Automatische Anpassung an neue CSV-Daten**

---

## 🗂️ Verwendete Technologien

- [Streamlit](https://streamlit.io/)
- [Pandas](https://pandas.pydata.org/)
- [Matplotlib](https://matplotlib.org/)
- [Plotly](https://plotly.com/python/)
- [Seaborn](https://seaborn.pydata.org/)

---

## 🚀 Lokale Ausführung

```bash
git clone https://github.com/lxndrfnk/Sports-Dashboard.git
cd Sports-Dashboard
pip install -r requirements.txt
streamlit run Start.py
