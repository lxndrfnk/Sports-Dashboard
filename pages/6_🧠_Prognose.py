import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import ast
import numpy as np

# ---------- Schriftart ----------

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter&display=swap');

        html, body, [class*="css"]  {
            font-family: 'Inter', sans-serif;
        }
    </style>
""", unsafe_allow_html=True)