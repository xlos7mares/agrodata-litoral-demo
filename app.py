import streamlit as st
import folium
from streamlit_folium import st_folium
import numpy as np
import pandas as pd
import requests

# =====================================================================
# 🛰️ CONFIGURACIÓN Y ESTILO (REVISADO PARA CERO ERRORES)
# =====================================================================
st.set_page_config(page_title="Agro Data Litoral PRO", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
.main { background-color: #111111; color: #FFFFFF; }
h1, h2, h3, h4 { color: #D4AF37 !important; font-family: 'Helvetica Neue', sans-serif; }
.stButton>button { background-color: #D4AF37; color: #111111; font-weight: bold; border-radius: 5px; border: none; width: 100%; padding: 10px; }
.report-box { border: 1px solid #D4AF37; padding: 18px; border-radius: 5px; background-color: #1a1a1a; margin-bottom: 20px; }
</style>
""", unsafe_allow_html=True)

# =====================================================================
# 🌤️ MOTOR DE CLIMA REAL
# =====================================================================
def obtener_clima_real(lat, lon):
    try:
        api_key = st.secrets["OPENWEATHER_API_KEY"]
        url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric&lang=es"
        res = requests.get(url
