import streamlit as st
import folium
from streamlit_folium import st_folium
import numpy as np
import pandas as pd
import requests

# =====================================================================
# 🛰️ CONFIGURACIÓN DE LA PÁGINA E IDENTIDAD VISUAL EXECUTIVE GOLD
# =====================================================================
st.set_page_config(
    page_title="Agro Data Litoral PRO",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estética premium: fondo oscuro y acentos dorados institucionales
st.markdown("""
<style>
.main { background-color: #111111; color: #FFFFFF; }
h1, h2, h3, h4 { color: #D4AF37 !important; font-family: 'Helvetica Neue', sans-serif; }
.stButton>button {
    background-color: #D4AF37;
    color: #111111;
    font-weight: bold;
    border-radius: 5px;
    border: none;
    width: 100%;
    padding: 10px;
    transition: 0.3s;
}
.stButton>button:hover { background-color: #AA8515; color: #FFFFFF; }
div[data-testid="stMetricValue"] { color: #D4AF37 !important; font-weight: bold; }
.report-box {
    border: 1px solid #D4AF37;
    padding: 18px;
    border-radius: 5px;
    background-color: #1a1a1a;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)
