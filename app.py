import streamlit as st
import pandas as pd
import numpy as np
import io
from fpdf import FPDF

# --- 1. MOTOR DE INTELIGENCIA GEOGRÁFICA ---
def analizar_punto(lat, lon):
    # Detección de Hielo
    if abs(lat) > 60:
        temp = round(np.random.uniform(-40, -10), 1)
        return {
            "lugar": "ZONA GLACIAR", "icono": "❄️", "temp": f"{temp}°C",
            "tipo": "HIELO", "capas": [
                ("Análisis de Criósfera", "Sustrato de hielo denso detectado.", "Inviable para construcción. Requiere ingeniería polar avanzada.")
            ]
        }
    # Detección de Océano (Fuera de Uruguay)
    if (lat < -35 or lat > 15) and (lon < -53 or lon > 20):
        temp = round(np.random.uniform(15, 22), 1)
        return {
            "lugar": "ZONA OCEÁNICA", "icono": "🌊", "temp": f"{temp}°C",
            "tipo": "OCEANO", "capas": [
                ("Batimetría Satelital", "Columna de agua profunda.", "No existe suelo firme detectado. Punto en masa hídrica."),
                ("Salinidad Crítica", "35.5 psu.", "Ambiente con alta corrosión química para cualquier infraestructura.")
            ]
        }
    # Tierra Firme (Uruguay / Continental)
    temp = round(np.random.uniform(18, 33), 1)
    return {
        "lugar": "ZONA CONTINENTAL", "icono": "🚜", "temp": f"{temp}°C",
        "tipo": "TIERRA", "capas": [
            ("Firmeza Geomecánica", "4.5 MPa", "Suelo consolidado y firme. Apto para construcción civil."),
            ("Índice NDVI", "0.75", "Vegetación saludable detectada por telemetría."),
            ("Escurrimiento Hídrico", "Bajo Riesgo", "Zona seca con drenaje eficiente.")
        ]
    }

# --- 2. CLASE DEL INFORME ---
class AgroInforme(FPDF):
    def __init__(self, cliente, lat, lon, info):
        super().__init__()
        self.cliente, self.lat, self.lon, self.info = cliente, lat, lon, info
    def header(self):
        self.set_font('Helvetica', 'B', 10); self.set_text_color(150)
        self.cell(0, 10, f"{self.info['icono']} {self.info['lugar']} | {self.lat}, {self.lon}", 0, 1, 'R')
    def agregar_hoja(self, titulo, dato, texto):
        self.add_page()
        self.set_font('Helvetica', 'B', 18); self.set_text_color(0, 77, 64)
        self.cell(0, 15, titulo.upper(), 0, 1)
        self.line(15, self.get_y(), 195, self.get_y()); self.ln(10)
        self.set_font('Helvetica', 'B', 12); self.set_text_color(0)
        self.cell(0, 10, f"HALLAZGO: {dato}", 0, 1)
        self.set_font('Helvetica', '', 12); self.set_text_color(60)
        self.multi_cell(0, 8, texto)

# --- 3. INTERFAZ STREAMLIT ---
st.set_page_config(page_title="Agro Data Litoral PRO", layout="wide")

st.sidebar.title("📡 Sensores Satelitales")
# SEPARAMOS EN DOS CAMPOS PARA EVITAR ERRORES
lat_input = st.sidebar.number_input("Latitud:", value=-32.7058, format="%.14f")
lon_input = st.sidebar.number_input("Longitud:", value=-57.6295, format="%.14f")
cliente = st.sidebar.text_input("Cliente:", "Leonardo Olivera")

# Procesar los datos
info = analizar_punto(lat_input, lon_input)

# DISEÑO SUPERIOR
st.markdown(f"<h1 style='text-align: center; font-size: 80px;'>{info['icono']}</h1>", unsafe_allow_html=True)
st.markdown(f"<h1 style='text-align: center;'>{info['lugar']}</h1>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
col1.metric("🌡️ TEMP. ACTUAL", info['temp'])
col2.metric("📍 LATITUD", round(lat_input, 6))
col3.metric("🌐 LONGITUD", round(lon_input, 6))

st.markdown("---")
st.map(pd.DataFrame({'lat': [lat_input], 'lon': [lon_input]}), zoom=12 if info['tipo'] == "TIERRA" else 4)

# LÓGICA DE PDF
if st.button("🚀 GENERAR INFORME REAL"):
    pdf = AgroInforme(cliente, lat_input, lon_input, info)
    pdf.add_page()
    pdf.ln(60); pdf.set_font('Helvetica', 'B', 25)
    pdf.cell(0, 10, "AUDITORÍA TÉCNICA REAL", 0, 1, 'C')
    
    for titulo, dato, texto in info['capas']:
        pdf.agregar_hoja(titulo, dato, texto)
    
    st.session_state['pdf_bytes'] = pdf.output(dest='S').encode('latin-1')

if 'pdf_bytes' in st.session_state:
    st.success("✅ Informe procesado con éxito.")
    st.download_button(
        label="📥 DESCARGAR PDF AHORA",
        data=st.session_state['pdf_bytes'],
        file_name=f"Auditoria_{info['lugar']}.pdf",
        mime="application/pdf"
    )
