import streamlit as st
import pandas as pd
import ast
import datetime
import matplotlib.pyplot as plt
from datetime import date

# ---------- Schriftart ----------

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=League+Spartan&display=swap');

        html, body, [class*="css"]  {
            font-family: 'League Spartan', sans-serif;
        }
    </style>
""", unsafe_allow_html=True)

st.title("Meine Trainingsbereiche")

st.write("---")

st.subheader("Leistungsdiagnostik 28.08.2024")

tabs = st.tabs(["ReKom", "GA 1", "GA 1/2", "GA 2", "WSA"])

with tabs[0]:
    st.write("**Intensität**: Sehr leicht")
    st.write("**Herzfrequenz**: < 133")
    st.write("**Herzfrequenz %**: 50 - 77 %")
    st.write("**Pace**: > 05:53 min/km")

with tabs[1]:
    st.write("**Intensität**: Leicht")
    st.write("**Herzfrequenz**: 133 - 138")
    st.write("**Herzfrequenz %**: 78 - 80 %")
    st.write("**Pace**:  05:53 - 05:33 min/km")

with tabs[2]:
    st.write("**Intensität**: Moderat")
    st.write("**Herzfrequenz**: 139 - 148")
    st.write("**Herzfrequenz %**: 81 - 86 %")
    st.write("**Pace**: 05:32 - 04:57 min/km")

with tabs[3]:
    st.write("**Intensität**: Schwer")
    st.write("**Herzfrequenz**: 149 - 157")
    st.write("**Herzfrequenz %**: 87 - 91 %")
    st.write("**Pace**: 04:56 - 04:31 min/km")

with tabs[4]:
    st.write("**Intensität**: Sehr schwer")
    st.write("**Herzfrequenz**: > 157")
    st.write("**Herzfrequenz %**: 92 - 100 %")
    st.write("**Pace**: < 04:31 min/km")
    