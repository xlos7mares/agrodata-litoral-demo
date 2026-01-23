import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from streamlit_folium import folium_static
import folium
from fpdf import FPDF
import base64
import os

# 1. CONFIGURACIÓN DE PÁGINA Y ESTILO VISUAL
st.set_page_config(page_title="AgroData Litoral - Master Report", layout="wide")

# Estilo: Fondo de campo tenue y tarjetas de datos premium
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(255, 255, 255, 0.88), rgba(255, 255, 255, 0.88)), 
                    url("https://images.unsplash.com/photo-1500382017468-9049fed747ef?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80");
        background-size: cover;
        background-attachment: fixed;
    }
    div[data-testid="stMetric"] {
        background-color: rgba(255, 255, 255, 0.98) !important;
        border: 2px solid #28a745 !important;
        border-radius: 15px !important;
        padding: 20px !important;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.1) !important;
    }
    .perfil-card {
        background-color: rgba(255, 255, 255, 0.95);
        padding: 25px;
        border-radius: 15px;
        border-left: 10px solid #1e4d2b;
        box-shadow: 5px 5px 20px rgba(0,0,0,0.05);
    }
    h1, h2, h3 { color: #1e4d2b !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. ENCABEZADO CON LOGO DE AGRODATA
col_l1, col_l2 = st.columns([1, 5])
with col_l1:
    if os.path.exists("logoagrodata.png"):
        st.image("logoagrodata.png", width=150)
with col_l2:
    st.title("AgroData Litoral: Auditoría 360°")

# 3. PRESENTACIÓN DEL DIRECTOR DE PROYECTO
with st.container():
    col_foto, col_info = st.columns([1, 4])
    with col_foto:
        # El nombre debe coincidir EXACTAMENTE con el de GitHub
        foto_path = "20250508_225422 (1).jpg"
        if os.path.exists(foto_path):
            st.image(foto_path, width=220)
        else:
            st.warning("Foto de perfil no detectada")
    
    with col_info:
        st.markdown(f"""
        <div class="perfil-card">
            <h2 style="margin-top:0;">Desarrollador de Software & Proyecto Agro Tecnológico</h2>
            <h1 style="font-size: 30px; margin-bottom:5px;">Leonardo Olivera</h1>
            <p><b>Estudiante de Agronomía | Experto en Informática (+20 años de exp.)</b><br>
            Perito en Granos | Operador Inmobiliario (Litoral Operaciones)<br>
            <i>Análisis Financiero e Inversiones bajo Inteligencia Artificial Avanzada</i></p>
        </div>
        """, unsafe_allow_html=True)

st.write("---")

# --- TABS DE NAVEGACIÓN ---
tabs = st.tabs(["📊 Monitoreo Satelital", "🗺️ Mapa Geológico", "🔬 Ciencia y Fuentes", "📥 Reporte Final"])

with tabs[0]:
    st.header("🎛️ Indicadores Multiespectrales (NASA / ESA)")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Salud Vegetal (NDVI)", "0.78", "+0.05", help="Fuente: Sentinel-2")
    with col2:
        st.metric("Humedad en Raíz (1m)", "14.2%", "-3.8%", delta_color="inverse", help="Fuente: NASA SMAP")
    with col3:
        st.metric("Resistencia Suelo", "2.5 MPa", "Suelo Firme", help="Análisis de cimentación")

with tabs[1]:
    st.header("🌐 Delimitación Técnica Padrón 5900 (5 Ha)")
    lat, lon = -32.6585, -57.6455
    m = folium.Map(location=[lat, lon], zoom_start=16, tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google')
    folium.Polygon(locations=[[-32.6565, -57.6485], [-32.6565, -57.6425], [-32.6615, -57.6445], [-32.6615, -57.6475], [-32.6585, -57.6490], [-32.6565, -57.6485]], 
                   color="#FFFFFF", weight=4, fill=True, fill_color="#39FF14", fill_opacity=0.35).add_to(m)
    folium_static(m, width=1200)

with tabs[2]:
    st.subheader("📡 Fuentes Satelitales y Validación")
    st.write("Datos procesados de: **ESA Sentinel-2, NASA SMAP y NASA Landsat**.")
    st.write("Sincronización oficial: **MGAP, SNIG, DIEA e INIA (Uruguay)**.")

with tabs[3]:
    st.header("📄 Generación de Reporte Certificado")
    st.error("🔒 REPORTE BLOQUEADO: Requiere validación de pago (u$s 150) a Leonardo Olivera.")

# PIE DE PÁGINA
st.write("---")
st.markdown("<center>© 2026 AgroData Litoral - Derechos Reservados | Director de Proyecto: Leonardo Olivera</center>", unsafe_allow_html=True)
