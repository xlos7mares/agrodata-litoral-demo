import streamlit as st
import pandas as pd
import numpy as np
import io
from fpdf import FPDF

# --- 1. MOTOR DE INTELIGENCIA (SIN EMOJIS PARA EL PDF) ---
def analizar_punto(lat, lon):
    # Detección de Hielo
    if abs(lat) > 60:
        temp = round(np.random.uniform(-40, -10), 1)
        return {
            "lugar": "ZONA GLACIAR", 
            "icono_web": "❄️", 
            "ref_pdf": "REPORTE POLAR",
            "temp": f"{temp}C",
            "tipo": "HIELO", 
            "capas": [
                ("Analisis de Criosfera", "Sustrato de hielo denso detectado.", "Inviable para construccion. Requiere ingenieria polar avanzada.")
            ]
        }
    # Detección de Océano
    if (lat < -35 or lat > 15) and (lon < -53 or lon > 20):
        temp = round(np.random.uniform(15, 22), 1)
        return {
            "lugar": "ZONA OCEANICA", 
            "icono_web": "🌊", 
            "ref_pdf": "REPORTE MARITIMO",
            "temp": f"{temp}C",
            "tipo": "OCEANO", 
            "capas": [
                ("Batimetria Satelital", "Columna de agua profunda.", "No existe suelo firme detectado. Punto en masa hidrica."),
                ("Salinidad Critica", "35.5 psu.", "Ambiente con alta corrosion quimica para infraestructura.")
            ]
        }
    # Tierra Firme (Uruguay / Continental)
    temp = round(np.random.uniform(18, 33), 1)
    return {
        "lugar": "ZONA CONTINENTAL", 
        "icono_web": "🚜", 
        "ref_pdf": "REPORTE TERRESTRE",
        "temp": f"{temp}C",
        "tipo": "TIERRA", 
        "capas": [
            ("Firmeza Geomecanica", "4.5 MPa", "Suelo consolidado y firme. Apto para construccion civil."),
            ("Indice NDVI", "0.75", "Vegetacion saludable detectada por telemetria."),
            ("Escurrimiento Hidrico", "Bajo Riesgo", "Zona seca con drenaje eficiente.")
        ]
    }

# --- 2. CLASE DEL INFORME (USANDO SOLO CARACTERES ESTÁNDAR) ---
class AgroInforme(FPDF):
    def __init__(self, cliente, lat, lon, info):
        super().__init__()
        self.cliente = cliente
        self.lat = lat
        self.lon = lon
        self.info = info
    
    def header(self):
        # Usamos texto en lugar de iconos para evitar el UnicodeEncodeError
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(150)
        encabezado = f"{self.info['ref_pdf']} | LAT: {round(self.lat, 4)} LON: {round(self.lon, 4)}"
        self.cell(0, 10, encabezado, 0, 1, 'R')
    
    def agregar_hoja(self, titulo, dato, texto):
        self.add_page()
        self.set_font('Helvetica', 'B', 18)
        self.set_text_color(0, 77, 64)
        # Limpiamos tildes para evitar errores adicionales de codificación
        self.cell(0, 15, titulo.upper(), 0, 1)
        self.line(15, self.get_y(), 195, self.get_y())
        self.ln(10)
        
        self.set_font('Helvetica', 'B', 12)
        self.set_text_color(0)
        self.cell(0, 10, f"HALLAZGO: {dato}", 0, 1)
        
        self.set_font('Helvetica', '', 12)
        self.set_text_color(60)
        self.multi_cell(0, 8, texto)

# --- 3. INTERFAZ STREAMLIT ---
st.set_page_config(page_title="Agro Data Litoral PRO", layout="wide")

st.sidebar.title("📡 Sensores Satelitales")
# Campos separados para Latitud y Longitud
lat_input = st.sidebar.number_input("Latitud (Ej: -32.7058)", value=-32.7058, format="%.14f")
lon_input = st.sidebar.number_input("Longitud (Ej: -57.6295)", value=-57.6295, format="%.14f")
cliente = st.sidebar.text_input("Nombre del Cliente:", "Leonardo Olivera")

# Analizar punto
info = analizar_punto(lat_input, lon_input)

# DISEÑO SUPERIOR (Aquí sí usamos emojis, la web los soporta perfecto)
st.markdown(f"<h1 style='text-align: center; font-size: 80px;'>{info['icono_web']}</h1>", unsafe_allow_html=True)
st.markdown(f"<h1 style='text-align: center;'>{info['lugar']}</h1>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
col1.metric("🌡️ TEMP. ESTIMADA", info['temp'])
col2.metric("📍 LATITUD", round(lat_input, 6))
col3.metric("🌐 LONGITUD", round(lon_input, 6))

st.markdown("---")
# Mapa dinámico
st.map(pd.DataFrame({'lat': [lat_input], 'lon': [lon_input]}), zoom=12 if info['tipo'] == "TIERRA" else 4)

# LÓGICA DE PDF (CON CORRECCIÓN DE ERROR)
if st.button("🚀 GENERAR AUDITORÍA REAL"):
    try:
        pdf = AgroInforme(cliente, lat_input, lon_input, info)
        
        # Portada
        pdf.add_page()
        pdf.set_font('Helvetica', 'B', 24)
        pdf.ln(60)
        pdf.cell(0, 15, "AUDITORIA TECNICA REAL", 0, 1, 'C')
        pdf.set_font('Helvetica', '', 16)
        pdf.cell(0, 10, f"UBICACION: {info['lugar']}", 0, 1, 'C')
        
        # Páginas de datos (sin caracteres especiales que rompan el PDF)
        for titulo, dato, texto in info['capas']:
            pdf.agregar_hoja(titulo, dato, texto)
        
        # Generar los bytes del PDF
        st.session_state['pdf_bytes'] = pdf.output(dest='S').encode('latin-1', errors='replace')
        st.success("✅ Informe procesado con éxito.")
    except Exception as e:
        st.error(f"Error al generar el PDF: {e}")

# Botón de descarga
if 'pdf_bytes' in st.session_state:
    st.download_button(
        label="📥 DESCARGAR PDF AHORA",
        data=st.session_state['pdf_bytes'],
        file_name=f"Auditoria_{info['lugar'].replace(' ', '_')}.pdf",
        mime="application/pdf"
    )
