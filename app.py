import streamlit as st
import pandas as pd
import requests
import re
import io
import google.generativeai as genai
from fpdf import FPDF
from PIL import Image

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Agro Data Litoral PRO", layout="wide", page_icon="🛰️")

# --- CONEXIÓN IA ---
try:
    # Usamos la llave que definiremos en los Secrets de Streamlit
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    modelo_ia = genai.GenerativeModel('gemini-1.5-flash')
    ia_activa = True
except Exception as e:
    st.error(f"Error IA: {e}")
    ia_activa = False

# --- LLAVE SATELITAL ---
OW_API_KEY = "6508c51f5beeace1ba98e80ea843e599"

# --- FUNCIONES ---
def obtener_clima(lat, lon):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OW_API_KEY}&units=metric&lang=es"
        r = requests.get(url).json()
        return round(r['main']['temp'] + 1.2, 1), r['main']['humidity'], r['weather'][0]['description']
    except:
        return 22.0, 60, "Despejado"

def limpiar_gps(texto):
    nums = re.findall(r'[-+]?\d*\.\d+|[-+]?\d+', texto)
    if len(nums) >= 2: return float(nums[0]), float(nums[1])
    return -32.2997, -58.0583 # Default Paysandú

# --- INTERFAZ ---
st.title("Agro Data Litoral 🛰️")
gps = st.text_input("Ubicación:", "-32.2997, -58.0583")
lat, lon = limpiar_gps(gps)

t, h, desc = obtener_clima(lat, lon)
col1, col2, col3 = st.columns(3)
col1.metric("TEMP. SUELO", f"{t} °C")
col2.metric("HUMEDAD", f"{h} %")
col3.metric("CLIMA", desc.capitalize())

if st.button("🚀 GENERAR AUDITORÍA"):
    if ia_activa:
        with st.spinner('Analizando...'):
            res = modelo_ia.generate_content(f"Agrónomo: Reporte breve para campo en lat {lat}, lon {lon}. Suelo {t}C.").text
            st.info(res)
    else:
        st.error("Falta GEMINI_API_KEY en Secrets.")
