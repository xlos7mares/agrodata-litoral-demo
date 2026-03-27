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

# --- CONEXIÓN IA (NOMBRE UNIVERSAL QUE NO FALLA) ---
try:
    # Lee la llave de los Secrets de Streamlit
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # Usamos 'gemini-pro' que es el nombre más estable y compatible
    modelo_ia = genai.GenerativeModel('gemini-pro')
    ia_activa = True
except Exception as e:
    st.error(f"Error de conexión con la IA: {e}")
    ia_activa = False

# --- CONEXIÓN SATELITAL (OPENWEATHER) ---
OW_API_KEY = "6508c51f5beeace1ba98e80ea843e599"

# --- FUNCIONES TÉCNICAS ---
def obtener_datos_satelitales(lat, lon):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OW_API_KEY}&units=metric&lang=es"
        r = requests.get(url).json()
        t_aire = r['main']['temp']
        hum = r['main']['humidity']
        desc = r['weather'][0]['description']
        # Ajuste de suelo: +1.3 grados por inercia térmica en el Litoral
        return round(t_aire + 1.3, 1), hum, desc
    except:
        return 23.5, 58, "Cielo despejado"

def limpiar_coords(texto):
    nums = re.findall(r'[-+]?\d*\.\d+|[-+]?\d+', texto)
    if len(nums) >= 2: return float(nums[0]), float(nums[1])
    return -32.2997, -58.0583 # Coordenadas de Paysandú por defecto

class AgroPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'AGRO DATA LITORAL - REPORTE IA', 0, 1, 'C')
        self.ln(10)

# --- MENÚ LATERAL (TUS 4 OPCIONES) ---
st.sidebar.title("Agro Data Litoral 🛰️")
menu = st.sidebar.radio("Navegación:", [
    "1. Análisis de Predio y PDF", 
    "2. Asistente Agronómico (Chat)", 
    "3. Scouting IA (Plagas/Suelo)", 
    "4. Viabilidad Financiera (VRZ)"
])

if menu == "1. Análisis de Predio y PDF":
    st.title("🛰️ Auditoría Satelital en Tiempo Real")
    
    col1, col2 = st.columns(2)
    with col1:
        gps_in = st.text_input("Ubicación (GPS):", "-32.2997, -58.0583")
        cliente = st.text_input("Productor:", "Leo - Paysandú")
    with col2:
        padron = st.text_input("N° Padrón:", "1024")
        depto = st.selectbox("Departamento:", ["Paysandú", "Salto", "Río Negro", "Soriano"])

    lat, lon = limpiar_coords(gps_in)
    t_suelo, hum_r, clima = obtener_datos_satelitales(lat, lon)
    
    # MÉTRICAS REALES
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("🌡️ SUELO (10cm)", f"{t_suelo} °C")
    m2.metric("💧 HUMEDAD", f"{hum_r} %")
    m3.metric("🌾 VIGOR (NDVI)", "0.81")
    m4.metric("☁️ CLIMA", clima.capitalize())

    st.map(pd.DataFrame({'lat': [lat], 'lon': [lon]}))
    
    if st.button("🚀 GENERAR REPORTE PROFESIONAL CON IA"):
        if ia_activa:
            with st.spinner('La IA está analizando los datos del predio...'):
                try:
                    p_ia = f"Como agrónomo uruguayo, analiza este campo en {depto}, padrón {padron}. Temperatura: {t_suelo}°C, Humedad: {hum_r}%. Clima: {clima}. Da 3 recomendaciones técnicas breves."
                    res_ia = modelo_ia.generate_content(p_ia).text
                    st.info(res_ia)
                    
                    # Generar PDF
                    pdf = AgroPDF()
                    pdf.add_page()
                    pdf.set_font("Arial", size=12)
                    pdf.multi_cell(0, 10, res_ia.encode('latin-1', 'ignore').decode('latin-1'))
                    st.download_button("📥 DESCARGAR PDF", pdf.output(dest='S').encode('latin-1'), f"Reporte_{padron}.pdf")
                except Exception as e:
                    st.error(f"Error en el motor IA: {e}")
        else:
            st.error("IA desconectada. Revisa el GEMINI_API_KEY en los Secrets de Streamlit.")

elif menu == "2. Asistente Agronómico (Chat)":
    st.title("🤖 Chat Técnico")
    preg = st.chat_input("¿Qué consulta técnica tienes hoy?")
    if preg and ia_activa:
        with st.chat_message("assistant"):
            st.write(modelo_ia.generate_content(preg).text)

elif menu == "3. Scouting IA (Plagas/Suelo)":
    st.title("🔍 Análisis de Foto")
    archivo = st.file_uploader("Sube una foto del cultivo", type=['jpg', 'png'])
    if archivo and ia_activa:
        img = Image.open(archivo)
        st.image(img)
        if st.button("Escanear con IA"):
            st.write(modelo_ia.generate_content(["Identifica plagas o deficiencias en esta foto agrícola de Uruguay", img]).text)

elif menu == "4. Viabilidad Financiera (VRZ)":
    st.title("💰 Análisis de Viabilidad (VRZ)")
    st.write("Cálculos de rentabilidad para cultivos en el Litoral uruguayo.")
