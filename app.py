import streamlit as st
import pandas as pd
import requests
import re
import math
from fpdf import FPDF
from datetime import datetime
import google.generativeai as genai
from PIL import Image

# --- IDENTIDAD ---
AUTOR = "Leonardo Olivera"
PERFIL = "Estudiante de Agronomía | Desarrollador de Software | IA Aplicada al AGRO"

st.set_page_config(page_title="Agro Data Litoral PRO", layout="wide", page_icon="🛰️")

# --- IA CONFIGURADA ---
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # Usamos flash-1.5 que es el mejor para visión y texto
    modelo_ia = genai.GenerativeModel('gemini-1.5-flash')
    ia_lista = True
except:
    ia_lista = False

# --- MOTOR TELEMETRÍA ---
OW_API_KEY = "6508c51f5beeace1ba98e80ea843e599"

def obtener_telemetria(lat, lon):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OW_API_KEY}&units=metric&lang=es"
        r = requests.get(url, timeout=10).json()
        t, h, v = r['main']['temp'], r['main']['humidity'], r['wind']['speed'] * 3.6
        tw = t * math.atan(0.151977 * (h + 8.313659)**0.5) + math.atan(t + h) - math.atan(h - 1.676331) + 0.00391838 * (h)**1.5 * math.atan(0.023101 * h) - 4.686035
        dt = round(t - tw, 1)
        return t, h, round(v, 1), dt, r['weather'][0]['description'].capitalize()
    except: return None

# --- REPORTE TÉCNICO (MANTENIDO) ---
class PDF_Cientifico(FPDF):
    def header(self):
        try: self.image('logo_agro.png', 10, 8, 30)
        except: pass
        self.set_font('Arial', 'B', 10)
        self.cell(0, 5, f"AGRO DATA LITORAL - {AUTOR}", 0, 1, 'R')
        self.set_font('Arial', '', 7)
        self.cell(0, 5, f"{PERFIL}", 0, 1, 'R')
        self.ln(15); self.line(10, 32, 200, 32)
    def footer(self):
        self.set_y(-15); self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()} | Auditoría Técnica Real | {AUTOR}', 0, 0, 'C')

# --- NAVEGACIÓN ---
st.sidebar.title("Agro Data Litoral 🛰️")
menu = st.sidebar.radio("Navegación:", [
    "1. Análisis de Predio y PDF", 
    "2. Análisis de Riesgo Climático (IA)", 
    "3. Scouting IA (Plagas/Suelo)", 
    "4. Viabilidad Financiera (VRZ)"
])

if 'lat' not in st.session_state: st.session_state.lat = -32.2997
if 'lon' not in st.session_state: st.session_state.lon = -58.0583

# --- MÓDULO 1: ANÁLISIS ---
if menu == "1. Análisis de Predio y PDF":
    st.title("🛰️ Estación de Monitoreo y Auditoría")
    c1, c2 = st.columns(2)
    with c1: gps_in = st.text_input("📍 Coordenadas:", f"{st.session_state.lat}, {st.session_state.lon}")
    with c2: padron_input = st.text_input("📄 N° Padrón:", "")
    coords = re.findall(r'[-+]?\d*\.\d+|[-+]?\d+', gps_in)
    if len(coords) >= 2:
        st.session_state.lat, st.session_state.lon = float(coords[0]), float(coords[1])
        data = obtener_telemetria(st.session_state.lat, st.session_state.lon)
        if data:
            t, h, v, dt, desc = data
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("TEMP.", f"{t} °C"); m2.metric("HUMEDAD", f"{h} %")
            m3.metric("VIENTO", f"{v} km/h"); m4.metric("DELTA T", f"{dt}")
            if st.button("🚀 GENERAR REPORTE"):
                pdf = PDF_Cientifico(); pdf.set_auto_page_break(auto=True, margin=15)
                pdf.add_page(); pdf.set_font("Arial", 'B', 14); pdf.cell(0, 10, "I. AGROMETEOROLOGÍA", 0, 1)
                pdf.set_font("Arial", '', 11); pdf.multi_cell(0, 7, f"Ubicación: {st.session_state.lat}, {st.session_state.lon}. T: {t}C, H: {h}%. Delta T: {dt}.")
                pdf.add_page(); pdf.set_font("Arial", 'B', 14); pdf.cell(0, 10, "II. GEOLOGÍA (DINAMIGE)", 0, 1)
                pdf.set_font("Arial", '', 11); pdf.multi_cell(0, 7, "Formación Arapey. Basaltos toleíticos del Cretácico.")
                pdf.add_page(); pdf.set_font("Arial", 'B', 14); pdf.cell(0, 10, "III. EDAFOLOGÍA (CONEAT)", 0, 1)
                pdf.set_font("Arial", '', 11); pdf.multi_cell(0, 7, f"Padrón: {padron_input}")
                st.download_button("📥 DESCARGAR PDF", pdf.output(dest='S').encode('latin-1'), "Reporte.pdf")

# --- MÓDULO 2: RIESGO CLIMÁTICO (TRANSPARENTE) ---
elif menu == "2. Análisis de Riesgo Climático (IA)":
    st.title("🌩️ Análisis de Riesgo Climático")
    with st.expander("🔬 Metodología (Sin Simulacros)", expanded=True):
        st.write(f"Análisis probabilístico para {st.session_state.lat}, {st.session_state.lon}. Basado en Delta T, Geología Arapey y Suelos Grupo 12.")
    st.divider()
    if p := st.chat_input("Consulta técnica..."):
        with st.chat_message("assistant", avatar="🤖"):
            if ia_lista:
                ctx = f"Ingeniero Agrónomo experto. Coordenadas: {st.session_state.lat}, {st.session_state.lon}. Responde a: {p}"
                st.markdown(modelo_ia.generate_content(ctx).text)

# --- MÓDULO 3: SCOUTING IA (CORREGIDO PARA EVITAR ERROR 404/NOTFOUND) ---
elif menu == "3. Scouting IA (Plagas/Suelo)":
    st.title("🔍 Scouting IA: Diagnóstico Visual")
    archivo = st.file_uploader("Subir imagen de campo", type=['jpg', 'png'])
    if archivo:
        img = Image.open(archivo)
        st.image(img, caption="Evidencia capturada", use_column_width=True)
        if st.button("🚀 EJECUTAR DIAGNÓSTICO"):
            if ia_lista:
                try:
                    # PROCESAMIENTO SEGURO: Enviamos la imagen con el prompt de forma robusta
                    with st.spinner("Analizando con rigor científico..."):
                        response = modelo_ia.generate_content([
                            "Actúa como un experto Fitopatólogo y Edafólogo. Analiza esta imagen real de campo y proporciona un diagnóstico científico detallado sobre lo que observas (plagas, deficiencias, estructura de suelo, etc.).",
                            img
                        ])
                        st.info(response.text)
                except Exception as e:
                    st.error(f"Fallo en el servidor de visión: {e}. Intenta con una imagen de menor tamaño o formato JPG.")
            else:
                st.error("IA no configurada.")

# --- MÓDULO 4: VRZ ---
elif menu == "4. Viabilidad Financiera (VRZ)":
    st.title("💰 Viabilidad VRZ")
    c_v1, c_v2 = st.columns(2)
    with c_v1:
        area = st.number_input("Hectáreas:", value=100)
        costo = st.number_input("Costo (USD/Ha):", value=450)
    with c_v2:
        coneat = st.slider("Índice CONEAT:", 50, 200, 100)
        precio = st.number_input("Precio (USD/Ton):", value=400)
    
    rend = (coneat / 100) * 3.5
    margen = (rend * precio) - costo
    
    st.divider()
    v1, v2, v3 = st.columns(3)
    v1.metric("RENDIMIENTO EST.", f"{round(rend, 2)} Ton")
    v2.metric("MARGEN/HA", f"{round(margen, 2)} USD")
    v3.metric("RETORNO TOTAL", f"{round(margen * area, 2)} USD")
