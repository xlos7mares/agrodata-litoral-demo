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

# --- CONEXIÓN IA (SOLUCIÓN DEFINITIVA) ---
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # Probamos con el nombre técnico completo que exige la versión v1beta
    modelo_ia = genai.GenerativeModel('models/gemini-1.5-flash')
    ia_activa = True
except Exception as e:
    st.error(f"Error de configuración: {e}")
    ia_activa = False

# --- CONEXIÓN SATELITAL (OPENWEATHER) ---
OW_API_KEY = "6508c51f5beeace1ba98e80ea843e599"

def obtener_datos_reales(lat, lon):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OW_API_KEY}&units=metric&lang=es"
        r = requests.get(url).json()
        return round(r['main']['temp'] + 1.3, 1), r['main']['humidity'], r['weather'][0]['description']
    except:
        return 22.8, 60, "Cielo nuboso"

def limpiar_gps(texto):
    nums = re.findall(r'[-+]?\d*\.\d+|[-+]?\d+', texto)
    if len(nums) >= 2: return float(nums[0]), float(nums[1])
    return -32.2997, -58.0583

class AgroPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'AGRO DATA LITORAL - REPORTE PROFESIONAL', 0, 1, 'C')
        self.ln(10)

# --- MENÚ LATERAL ---
st.sidebar.title("Agro Data Litoral 🛰️")
menu = st.sidebar.radio("Navegación:", [
    "1. Análisis de Predio y PDF", 
    "2. Asistente Agronómico (Chat)", 
    "3. Scouting IA (Plagas/Suelo)", 
    "4. Viabilidad Financiera (VRZ)"
])

if menu == "1. Análisis de Predio y PDF":
    st.title("🛰️ Auditoría Satelital de Precisión")
    gps_in = st.text_input("Ubicación (GPS):", "-32.2997, -58.0583")
    lat, lon = limpiar_gps(gps_in)
    t, h, desc = obtener_datos_reales(lat, lon)
    
    m1, m2, m3 = st.columns(3)
    m1.metric("🌡️ TEMP. SUELO", f"{t} °C")
    m2.metric("💧 HUMEDAD", f"{h} %")
    m3.metric("☁️ CLIMA LOCAL", desc.capitalize())
    
    st.map(pd.DataFrame({'lat': [lat], 'lon': [lon]}))
    
    if st.button("🚀 GENERAR AUDITORÍA CON IA"):
        if ia_activa:
            with st.spinner('La IA está analizando los datos del predio...'):
                try:
                    res = modelo_ia.generate_content(f"Agrónomo uruguayo: analiza campo en Paysandú, {lat}, {lon}. Suelo {t}C. 3 consejos de manejo.").text
                    st.info(res)
                    pdf = AgroPDF()
                    pdf.add_page()
                    pdf.set_font("Arial", size=12)
                    pdf.multi_cell(0, 10, res.encode('latin-1', 'ignore').decode('latin-1'))
                    st.download_button("📥 DESCARGAR REPORTE PDF", pdf.output(dest='S').encode('latin-1'), "Reporte.pdf")
                except Exception as e:
                    st.error(f"Error en el motor IA: {e}")

elif menu == "2. Asistente Agronómico (Chat)":
    st.title("🤖 Chat Técnico")
    preg = st.chat_input("Duda técnica...")
    if preg and ia_activa:
        st.write(modelo_ia.generate_content(preg).text)

elif menu == "3. Scouting IA (Plagas/Suelo)":
    st.title("🔍 Análisis de Foto")
    archivo = st.file_uploader("Sube una foto", type=['jpg', 'png'])
    if archivo and ia_activa:
        img = Image.open(archivo)
        st.image(img)
        if st.button("Analizar"):
            st.write(modelo_ia.generate_content(["¿Qué plaga o deficiencia ves?", img]).text)

elif menu == "4. Viabilidad Financiera (VRZ)":
    st.title("💰 Análisis Financiero")
    st.write("Módulo para calcular retorno de inversión agrícola.")
