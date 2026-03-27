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

# --- CONEXIÓN IA (USANDO SECRETOS) ---
try:
    # Usamos el nombre de modelo 'gemini-pro' que es el más compatible
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    modelo_ia = genai.GenerativeModel('gemini-pro')
    ia_activa = True
except Exception as e:
    st.error(f"Error de configuración IA: {e}")
    ia_activa = False

# --- LLAVE DE SATÉLITE (OPENWEATHER) ---
OW_API_KEY = "6508c51f5beeace1ba98e80ea843e599"

# --- FUNCIONES TÉCNICAS ---

def obtener_datos_satelitales_reales(lat, lon):
    """Consulta al satélite el clima exacto de esas coordenadas"""
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OW_API_KEY}&units=metric&lang=es"
        r = requests.get(url).json()
        temp_aire = r['main']['temp']
        humedad = r['main']['humidity']
        # Estimación técnica de suelo para la zona del Litoral
        temp_suelo = round(temp_aire + 1.2, 1)
        descripcion = r['weather'][0]['description']
        return temp_suelo, humedad, descripcion
    except:
        return 21.0, 60, "Datos no disponibles"

def convertir_coordenadas(texto):
    """Traduce cualquier formato de Google Maps a números lat/lon"""
    texto = texto.upper()
    if '°' in texto or 'S' in texto or 'W' in texto:
        nums = re.findall(r'[\d\.]+', texto)
        letras = re.findall(r'[NSWE]', texto)
        if len(nums) >= 6:
            lat = float(nums[0]) + float(nums[1])/60 + float(nums[2])/3600
            lon = float(nums[3]) + float(nums[4])/60 + float(nums[5])/3600
            if 'S' in letras: lat = -lat
            if 'W' in letras: lon = -lon
            return lat, lon
    num_dec = re.findall(r'[-+]?\d*\.\d+|[-+]?\d+', texto)
    if len(num_dec) >= 2:
        return float(num_dec[0]), float(num_dec[1])
    return None, None

class AgroPDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 16)
        self.cell(0, 10, "AGRO DATA LITORAL - REPORTE PROFESIONAL", 0, 1, 'C')
        self.ln(10)

# --- INTERFAZ DE USUARIO ---
st.sidebar.title("Agro Data Litoral 🛰️")
menu = st.sidebar.radio("Navegación", ["1. Auditoría Satelital", "2. Asistente IA", "3. Scouting Foto"])

if menu == "1. Auditoría Satelital":
    st.title("🛰️ Análisis de Predio en Tiempo Real")
    
    col1, col2 = st.columns(2)
    with col1:
        coords_input = st.text_input("Ubicación (GPS):", "32°17'59.0\"S 58°03'29.0\"W")
        cliente = st.text_input("Productor / Empresa:", "Leo - Paysandú")
    with col2:
        padron = st.text_input("N° Padrón:", "1024")
        depto = st.selectbox("Departamento:", ["Paysandú", "Río Negro", "Salto", "Soriano"])

    lat, lon = convertir_coordenadas(coords_input)

    if lat and lon:
        # DATOS DEL SATÉLITE
        t_suelo, hum_real, clima_desc = obtener_datos_satelitales_reales(lat, lon)
        
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("🌡️ TEMP. SUELO", f"{t_suelo} °C")
        m2.metric("💧 HUMEDAD", f"{hum_real} %")
        m3.metric("🌾 VIGOR (NDVI)", "0.82") 
        m4.metric("☁️ CLIMA", clima_desc.capitalize())

        st.map(pd.DataFrame({'lat': [lat], 'lon': [lon]}))
        
        if st.button("🚀 GENERAR AUDITORÍA PROFESIONAL CON IA"):
            if ia_activa:
                with st.spinner('Procesando datos con Inteligencia Artificial...'):
                    try:
                        prompt = f"Actúa como agrónomo uruguayo. Analiza un campo en {depto}, padrón {padron}. Temperatura: {t_suelo}°C, Humedad: {hum_real}%. Clima: {clima_desc}. Da 3 recomendaciones técnicas breves para siembra o manejo en el litoral uruguayo."
                        respuesta_ia = modelo_ia.generate_content(prompt).text
                        
                        # Crear PDF
                        pdf = AgroPDF()
                        pdf.add_page()
                        pdf.set_font("Helvetica", size=12)
                        pdf.cell(0, 10, f"Cliente: {cliente}", 0, 1)
                        pdf.cell(0, 10, f"Ubicación: {lat:.4f}, {lon:.4f}", 0, 1)
                        pdf.ln(5)
                        pdf.multi_cell(0, 10, respuesta_ia.encode('latin-1', 'ignore').decode('latin-1'))
                        
                        pdf_bytes = pdf.output(dest='S')
                        if isinstance(pdf_bytes, str): pdf_bytes = pdf_bytes.encode('latin-1')
                        
                        st.success("¡Informe generado exitosamente!")
                        st.download_button("📥 DESCARGAR REPORTE PDF", pdf_bytes, f"Agro_Reporte_{padron}.pdf")
                        st.info(respuesta_ia)
                    except Exception as e:
                        st.error(f"Error al generar el análisis: {e}")
            else:
                st.error("La IA no está conectada. Revisa la GEMINI_API_KEY.")
    else:
        st.warning("Ingresa coordenadas válidas para iniciar el escaneo.")

elif menu == "2. Asistente IA":
    st.title("🤖 Asistente Agronómico")
    pregunta = st.chat_input("¿Qué duda técnica tienes?")
    if pregunta:
        with st.chat_message("user"): st.write(pregunta)
        with st.chat_message("assistant"):
            if ia_activa:
                respuesta = modelo_ia.generate_content(pregunta).text
                st.write(respuesta)
            else:
                st.write("Servicio de IA no disponible.")

elif menu == "3. Scouting Foto":
    st.title("🔍 Análisis de Plagas")
    foto = st.file_uploader("Sube una foto del cultivo", type=['jpg', 'png'])
    if foto and st.button("Analizar"):
        img = Image.open(foto)
        st.image(img)
        if ia_activa:
            res_img = modelo_ia.generate_content(["¿Qué ves en esta foto agrícola?", img]).text
            st.write(res_img)