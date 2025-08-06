import streamlit as st

st.title("Allgemeine Informationen")

# ---------- Schriftart ----------

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter&display=swap');

        html, body, [class*="css"]  {
            font-family: 'Inter', sans-serif;
        }
    </style>
""", unsafe_allow_html=True)

# ---------- Triathlon-Erklärung ----------

st.subheader("Was ist ein Triathlon?")

st.write("""
Triathlon ist eine Ausdauersportart, bestehend aus einem Mehrkampf der Disziplinen Schwimmen, Radfahren und Laufen,
die nacheinander und in genau dieser Reihenfolge zu absolvieren sind.
Die Besonderheit dieses Sports besteht darin, dass eine bestimmte, festgelegte Strecke so schnell wie möglich
zurückzulegen ist, wobei die Uhr auch bei zeitlichen Unterbrechungen wie z. B. den Wechseln zwischen den Disziplinen weiter läuft.
Die Wortschöpfung „Triathlon“ setzt sich aus den griechischen Ausdrücken treis/tria, „drei“, und athlos,
„Wettkampf“ zusammen. Triathlon ist seit dem Jahr 2000 auch eine olympische Disziplin.
""")

st.write("---")

# ---------- Triathlon-Distanzen ----------

st.subheader("Triathlon-Distanzen")

tabs = st.tabs(["Sprintdistanz", "Olympische Distanz", "Mitteldistanz", "Langdistanz"])

with tabs[0]:
    st.write("**Schwimmen**: 0.5 km")
    st.write("**Rad**: 20 km")
    st.write("**Laufen**: 5 km")

with tabs[1]:
    st.write("**Schwimmen**: 1.5 km")
    st.write("**Rad**: 40 km")
    st.write("**Laufen**: 10 km")

with tabs[2]:
    st.write("**Schwimmen**: 1.9 km")
    st.write("**Rad**: 90 km")
    st.write("**Laufen**: 21.1 km (Halbmarathon)")

with tabs[3]:
    st.write("**Schwimmen**: 3.8 km")
    st.write("**Rad**: 180 km")
    st.write("**Laufen**: 42.2 km (Marathon)")
