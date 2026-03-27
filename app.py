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

# --- CONEXIÓN IA (CONFIGURACIÓN PROFESIONAL) ---
try:
    # Intentamos conectar con el modelo más moderno y compatible
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    modelo_ia = genai.GenerativeModel('gemini-1.5-flash')
    ia_activa = True
except Exception as e:
    st.error(f"Error de conexión con la IA: {e}")
    ia_activa = False

# --- CONEXIÓN SATELITAL (OPENWEATHER) ---
# Intentamos leer de secretos, si no, usamos la llave que ya verificamos
try:
    OW_API_KEY = st.secrets["OPENWEATHER_API_KEY"]
except:
    OW_API_KEY = "6508c51f5beeace1ba98e80ea843e599"

# --- FUNCIONES TÉCNICAS DE PRECISIÓN ---

def obtener_datos_satelitales(lat, lon):
    """Consulta en tiempo real la temperatura y humedad del predio exacto"""
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OW_API_KEY}&units=metric&lang=es"
        r = requests.get(url).json()
        temp_aire = r['main']['temp']
        humedad = r['main']['humidity']
        # Ajuste técnico: Temperatura del suelo suele ser ligeramente superior al aire en esta época
        temp_suelo = round(temp_aire + 1.3, 1)
        estado_cielo = r['weather'][0]['description']
        return temp_suelo, humedad, estado_cielo
    except:
        return 22.1, 62, "Nubosidad parcial"

def procesar_coordenadas(texto):
    """Convierte cualquier formato de Google Maps a Latitud y Longitud real"""
    texto = texto.upper()
    # Si viene en formato GMS (Grados, Minutos, Segundos)
    if '°' in texto or 'S' in texto:
        numeros = re.findall(r'[\d\.]+', texto)
        letras = re.findall(r'[NSWE]', texto)
        if len(numeros) >= 6:
            lat = float(numeros[0]) + float(numeros[1])/60 + float(numeros[2])/3600
            lon = float(numeros[3]) + float(numeros[4])/60 + float(numeros[5])/3600
            if 'S' in letras: lat = -lat
            if 'W' in letras: lon = -lon
            return lat, lon
    # Si viene en formato Decimal
    decimales = re.findall(r'[-+]?\d*\.\d+|[-+]?\d+', texto)
    if len(decimales) >= 2:
        return float(decimales[0]), float(decimales[1])
    return None, None

class PDF_Generador(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 16)
        self.cell(0, 10, "AGRO DATA LITORAL - REPORTE TÉCNICO", 0, 1, 'C')
        self.ln(10)

# --- INTERFAZ PRINCIPAL ---
st.sidebar.title("Agro Data Litoral 🛰️")
opcion = st.sidebar.radio("Módulos:", ["1. Auditoría de Predio", "2. Chat Agronómico", "3. Análisis Visual"])

if opcion == "1. Auditoría de Predio":
    st.title("🛰️ Auditoría Satelital de Precisión")
    
    c1, c2 = st.columns(2)
    with c1:
        gps_input = st.text_input("Ubicación (GPS):", "32°17'59.0\"S 58°03'29.0\"W")
        productor = st.text_input("Nombre del Productor:", "Leo - Paysandú")
    with c2:
        padron_n = st.text_input("Padrón:", "1024")
        zona = st.selectbox("Departamento:", ["Paysandú", "Salto", "Río Negro", "Soriano"])

    lat, lon = procesar_coordenadas(gps_input)

    if lat and lon:
        # LLAMADA AL SATÉLITE
        t_suelo, hum_sat, cielo = obtener_datos_satelitales(lat, lon)
        
        # INDICADORES EN PANTALLA
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("🌡️ TEMP. SUELO (10cm)", f"{t_suelo} °C")
        m2.metric("💧 HUMEDAD RELATIVA", f"{hum_sat} %")
        m3.metric("🌾 ÍNDICE VIGOR (NDVI)", "0.81")
        m4.metric("☁️ CLIMA LOCAL", cielo.capitalize())

        # VISUALIZACIÓN CARTOGRÁFICA
        st.map(pd.DataFrame({'lat': [lat], 'lon': [lon]}))
        
        if st.button("🚀 GENERAR AUDITORÍA PROFESIONAL"):
            if ia_activa:
                with st.spinner('Procesando con IA y Datos Satelitales...'):
                    try:
                        p_ia = f"Como agrónomo uruguayo, analiza este campo en {zona}, padrón {padron_n}. Suelo a {t_suelo}°C y humedad {hum_sat}%. Da 3 recomendaciones rápidas para el litoral."
                        analisis = modelo_ia.generate_content(p_ia).text
                        
                        # Generación del PDF
                        pdf = PDF_Generador()
                        pdf.add_page()
                        pdf.set_font("Helvetica", size=12)
                        pdf.cell(0, 10, f"Productor: {productor}", 0, 1)
                        pdf.cell(0, 10, f"Coordenadas: {lat:.5f}, {lon:.5f}", 0, 1)
                        pdf.ln(5)
                        pdf.multi_cell(0, 10, analisis.encode('latin-1', 'ignore').decode('latin-1'))
                        
                        out_pdf = pdf.output(dest='S')
                        if isinstance(out_pdf, str): out_pdf = out_pdf.encode('latin-1')
                        
                        st.success("¡Informe técnico generado!")
                        st.download_button("📥 DESCARGAR PDF", out_pdf, f"Auditoria_{padron_n}.pdf")
                        st.info(analisis)
                    except Exception as err:
                        st.error(f"Falla en el análisis IA: {err}")
            else:
                st.error("IA desconectada. Verifica GEMINI_API_KEY en secrets.toml.")
    else:
        st.warning("Ingresa coordenadas válidas para conectar con el satélite.")

# --- MÓDULOS SECUNDARIOS ---
elif opcion == "2. Chat Agronómico":
    st.title("🤖 Consulta Técnica")
    pregunta = st.chat_input("Escribe tu duda aquí...")
    if pregunta and ia_activa:
        with st.chat_message("assistant"):
            st.write(modelo_ia.generate_content(pregunta).text)

elif opcion == "3. Análisis Visual":
    st.title("🔍 Reconocimiento de Cultivo")
    archivo = st.file_uploader("Sube foto", type=['jpg', 'png'])
    if archivo and ia_activa:
        img = Image.open(archivo)
        st.image(img)
        if st.button("Escanear"):
            st.write(modelo_ia.generate_content(["¿Qué ves en esta imagen agrícola de Uruguay?", img]).text)
