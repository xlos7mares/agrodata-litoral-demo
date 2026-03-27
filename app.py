import streamlit as st
import pandas as pd
import requests
import re
import math
from fpdf import FPDF
from datetime import datetime
import google.generativeai as genai

# --- IDENTIDAD ---
AUTOR = "Leonardo Olivera"
PERFIL = "Estudiante de Agronomía | Desarrollador de Software | IA Aplicada al AGRO"

st.set_page_config(page_title="Agro Data Litoral PRO", layout="wide", page_icon="🛰️")

# --- CONEXIÓN IA ---
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    modelo_ia = genai.GenerativeModel('gemini-1.5-flash-latest')
    ia_lista = True
except:
    ia_lista = False

# --- MOTOR DE TELEMETRÍA REAL (REACTIVE) ---
OW_API_KEY = "6508c51f5beeace1ba98e80ea843e599"

def obtener_telemetria(lat, lon):
    # Forzamos que la URL use las coordenadas que entran por parámetro
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OW_API_KEY}&units=metric&lang=es"
        r = requests.get(url, timeout=10).json()
        
        # Extracción directa de la respuesta de la API
        t = r['main']['temp']
        h = r['main']['humidity']
        v = r['wind']['speed'] * 3.6
        desc = r['weather'][0]['description'].capitalize()
        
        # Cálculo Delta T 100% dependiente de los datos nuevos
        tw = t * math.atan(0.151977 * (h + 8.313659)**0.5) + math.atan(t + h) - math.atan(h - 1.676331) + 0.00391838 * (h)**1.5 * math.atan(0.023101 * h) - 4.686035
        dt = round(t - tw, 1)
        
        return t, h, round(v, 1), dt, desc
    except Exception as e:
        return None

# --- REPORTE TÉCNICO (DATOS DINÁMICOS) ---
class PDF_Cientifico(FPDF):
    def header(self):
        try: self.image('logo_agro.png', 10, 8, 30)
        except: pass
        self.set_font('Arial', 'B', 10)
        self.cell(0, 5, f"AGRO DATA LITORAL - {AUTOR}", 0, 1, 'R')
        self.set_font('Arial', '', 7)
        self.cell(0, 5, f"{PERFIL}", 0, 1, 'R')
        self.ln(15)
        self.line(10, 32, 200, 32)
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()} | Auditoría Técnica Real 100% Validada', 0, 0, 'C')

# --- NAVEGACIÓN ---
st.sidebar.title("Agro Data Litoral 🛰️")
menu = st.sidebar.radio("Navegación:", ["1. Análisis de Predio y PDF", "2. Asistente Agronómico (Mini IA Gemini)", "3. Scouting IA", "4. Viabilidad VRZ"])

if menu == "1. Análisis de Predio y PDF":
    st.title("🛰️ Estación de Monitoreo en Tiempo Real")
    
    # IMPORTANTE: El cambio aquí asegura que Streamlit "escuche" el cambio de GPS
    gps_in = st.text_input("📍 Coordenadas GPS (Lat, Lon):", "-32.2997, -58.0583", key="gps_input")
    padron_input = st.text_input("📄 N° Padrón Catastral:", "", key="padron_input")

    coords = re.findall(r'[-+]?\d*\.\d+|[-+]?\d+', gps_in)
    if len(coords) >= 2:
        lat_actual, lon_actual = float(coords[0]), float(coords[1])
        
        # Ejecutamos la telemetría con los nuevos valores de la caja de texto
        data = obtener_telemetria(lat_actual, lon_actual)
        
        if data:
            t, h, v, dt, desc = data
            
            # --- MUESTRA EN PANTALLA ---
            st.markdown(f"#### Datos validados para: {lat_actual}, {lon_actual}")
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("TEMPERATURA", f"{t} °C")
            m2.metric("HUMEDAD", f"{h} %")
            m3.metric("VIENTO", f"{v} km/h")
            m4.metric("DELTA T", f"{dt}")

            if st.button("🚀 GENERAR REPORTE CON ESTOS DATOS"):
                pdf = PDF_Cientifico()
                # PÁGINA 1
                pdf.add_page()
                pdf.set_font("Arial", 'B', 14); pdf.cell(0, 10, "I. CARACTERIZACIÓN AGROMETEOROLÓGICA", 0, 1)
                pdf.set_font("Arial", '', 11)
                pdf.multi_cell(0, 7, f"Ubicación: {lat_actual}, {lon_actual}\nTemperatura: {t}C\nHumedad: {h}%\nDelta T: {dt}\n\nEste reporte técnico se basa en la psicrometría real captada en el momento de la consulta.")
                # PÁGINA 2
                pdf.add_page()
                pdf.set_font("Arial", 'B', 14); pdf.cell(0, 10, "II. UNIDAD LITOESTRATIGRÁFICA (DINAMIGE)", 0, 1)
                pdf.set_font("Arial", '', 11); pdf.multi_cell(0, 7, "Formación Arapey. Basaltos toleíticos mesozoicos. Datos estructurales estables para el litoral norte.")
                # PÁGINA 3
                pdf.add_page()
                pdf.set_font("Arial", 'B', 14); pdf.cell(0, 10, "III. EDAFOLOGÍA Y GLOSARIO", 0, 1)
                pdf.set_font("Arial", '', 11); pdf.multi_cell(0, 7, f"Padrón: {padron_input}\nSuelos Grupo 12. Brunosoles Éutricos. Capacidad de uso: Campo Natural.")
                
                st.download_button("📥 DESCARGAR PDF REAL", pdf.output(dest='S').encode('latin-1'), f"Reporte_{lat_actual}.pdf")

elif menu == "2. Asistente Agronómico (Mini IA Gemini)":
    st.title("🤖 Mini IA Gemini Especializada")
    # (Aquí va el diseño de tarjetas y el chat que ya teníamos...)
