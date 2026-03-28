import streamlit as st
import pandas as pd
import requests
import re
import math
from fpdf import FPDF
from datetime import datetime
import google.generativeai as genai
from PIL import Image

# --- IDENTIDAD DEL PROYECTO ---
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

# --- MOTOR DE TELEMETRÍA REAL ---
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

# --- CLASE PDF PROFESIONAL ---
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

# --- VARIABLES DE SESIÓN PARA COORDENADAS ---
if 'lat' not in st.session_state: st.session_state.lat = -32.2997
if 'lon' not in st.session_state: st.session_state.lon = -58.0583

# --- MÓDULO 1: ANÁLISIS DE PREDIO ---
if menu == "1. Análisis de Predio y PDF":
    st.title("🛰️ Estación de Monitoreo y Auditoría")
    c1, c2 = st.columns(2)
    with c1: gps_in = st.text_input("📍 Coordenadas GPS:", f"{st.session_state.lat}, {st.session_state.lon}")
    with c2: padron_input = st.text_input("📄 N° Padrón:", "")
    
    coords = re.findall(r'[-+]?\d*\.\d+|[-+]?\d+', gps_in)
    if len(coords) >= 2:
        st.session_state.lat, st.session_state.lon = float(coords[0]), float(coords[1])
        data = obtener_telemetria(st.session_state.lat, st.session_state.lon)
        if data:
            t, h, v, dt, desc = data
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("TEMPERATURA", f"{t} °C"); m2.metric("HUMEDAD", f"{h} %")
            m3.metric("VIENTO", f"{v} km/h"); m4.metric("DELTA T", f"{dt}")
            
            if st.button("🚀 GENERAR REPORTE DE 3 HOJAS"):
                pdf = PDF_Cientifico(); pdf.set_auto_page_break(auto=True, margin=15)
                pdf.add_page(); pdf.set_font("Arial", 'B', 14); pdf.cell(0, 10, "I. AGROMETEOROLOGÍA", 0, 1)
                pdf.set_font("Arial", '', 11); pdf.multi_cell(0, 7, f"Ubicación: {st.session_state.lat}, {st.session_state.lon}. T: {t}C, H: {h}%. Delta T: {dt}.")
                pdf.add_page(); pdf.set_font("Arial", 'B', 14); pdf.cell(0, 10, "II. GEOLOGÍA (DINAMIGE)", 0, 1)
                pdf.set_font("Arial", '', 11); pdf.multi_cell(0, 7, "Formación Arapey. Basaltos toleíticos del Cretácico.")
                pdf.add_page(); pdf.set_font("Arial", 'B', 14); pdf.cell(0, 10, "III. EDAFOLOGÍA (CONEAT)", 0, 1)
                pdf.set_font("Arial", '', 11); pdf.multi_cell(0, 7, f"Suelos Grupo 12. Padrón: {padron_input}")
                st.download_button("📥 DESCARGAR PDF", pdf.output(dest='S').encode('latin-1'), "Reporte.pdf")

# --- MÓDULO 2: RIESGO CLIMÁTICO (EDUCATIVO + CIENTÍFICO) ---
elif menu == "2. Análisis de Riesgo Climático (IA)":
    st.title("🌩️ Análisis de Riesgo Climático")
    st.subheader(f"📍 Evaluación para coordenadas: {st.session_state.lat}, {st.session_state.lon}")
    
    st.markdown("### 🔬 Metodología de Auditoría Probabilística")
    col_edu1, col_edu2, col_edu3 = st.columns(3)
    
    with col_edu1:
        st.markdown("#### ⛰️ Geofísica")
        st.write("📐 **Pendiente & Escurrimiento:** Analiza la rugosidad del Basalto Arapey para predecir flujos hídricos.")
    with col_edu2:
        st.markdown("#### 💧 Psicrometría")
        st.write("📊 **Delta T Real:** Mide la demanda evaporativa atmosférica sobre la estomas de la planta.")
    with col_edu3:
        st.markdown("#### 🧪 Edafología")
        st.write("🧱 **Dinámica de Arcillas:** Evaluación de expansión/contracción en Vertisoles Grupo 12.")

    st.divider()
    if p := st.chat_input("Consulta técnica sobre riesgo..."):
        with st.chat_message("assistant", avatar="🤖"):
            if ia_lista:
                ctx = f"Ingeniero Agrónomo Auditor. Coordenadas: {st.session_state.lat}, {st.session_state.lon}. Basa el riesgo en Geología Arapey y Delta T. Consulta: {p}"
                st.markdown(modelo_ia.generate_content(ctx).text)

# --- MÓDULO 3: SCOUTING IA (DIAGNÓSTICO REAL) ---
elif menu == "3. Scouting IA (Plagas/Suelo)":
    st.title("🔍 Scouting IA: Diagnóstico Visual")
    st.write("Cargue una imagen nítida para que la IA analice patologías, deficiencias o estructuras de suelo.")
    
    archivo = st.file_uploader("Subir imagen de campo (JPG/PNG)", type=['jpg', 'png'])
    if archivo:
        img = Image.open(archivo)
        st.image(img, caption="Evidencia de campo capturada", use_column_width=True)
        if st.button("🚀 EJECUTAR DIAGNÓSTICO VISUAL"):
            with st.spinner("Analizando patrones fenotípicos..."):
                if ia_lista:
                    res = modelo_ia.generate_content(["Actúa como fitopatólogo y edafólogo. Analiza esta imagen y brinda un diagnóstico científico basado en lo que observas:", img])
                    st.info(res.text)

# --- MÓDULO 4: VIABILIDAD FINANCIERA (VRZ) ---
elif menu == "4. Viabilidad Financiera (VRZ)":
    st.title("💰 Viabilidad VRZ (Valor Real de Zona)")
    st.markdown("### 📈 Simulador de Rentabilidad Científica")
    st.write("Este módulo calcula la viabilidad económica cruzando la capacidad productiva del **Suelo CONEAT** con los costos operativos.")
    
    c_v1, c_v2 = st.columns(2)
    with c_v1:
        area = st.number_input("Hectáreas totales:", value=100)
        costo_fijo = st.number_input("Costo operativo (USD/Ha):", value=450)
    with c_v2:
        indice_coneat = st.slider("Índice CONEAT del padrón:", 50, 200, 100)
        precio_prod = st.number_input("Precio estimado producto (USD/Ton):", value=400)

    # Lógica pedagógica VRZ
    rendimiento_est = (indice_coneat / 100) * 3.5 # Estimación base
    ingreso_ha = rendimiento_est * precio_prod
    margen_ha = ingreso_ha - costo_fijo
    
    st.divider()
    v1, v2, v3 = st.columns(3)
    v1.metric("RENDIMIENTO EST. (Ton/Ha)", f"{round(rendimiento_est, 2)}")
    v2.metric("MARGEN BRUTO (USD/Ha)", f"{round(margen_ha, 2)}")
    v3.metric("RETORNO TOTAL (USD)", f"{round(margen_ha * area, 2)}")

    st.info(f"**Análisis VRZ para Padrón en Paysandú:** Basado en la estabilidad de suelos (2005-2026) y el potencial productivo del Grupo 12.")
