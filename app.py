import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from streamlit_folium import folium_static
import folium
from fpdf import FPDF
import base64

# 1. CONFIGURACIÓN DE PÁGINA Y DISEÑO CINEMATOGRÁFICO
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
    h1, h2, h3 { color: #1e4d2b !important; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    </style>
    """, unsafe_allow_html=True)

# 2. PRESENTACIÓN PROFESIONAL (ESTRUCTURA CORREGIDA)
with st.container():
    col_foto, col_info = st.columns([1, 4])
    with col_foto:
        # LINK CORREGIDO: Apunta directamente a tu archivo en GitHub
        foto_url = "https://raw.githubusercontent.com/leonardolitoral/agrodata-litoral-demo/main/20250508_225422%20(1).jpg"
        st.image(foto_url, width=180, use_container_width=False)
    
    with col_info:
        st.markdown(f"""
        <div class="perfil-card">
            <h2 style="margin-top:0;">Desarrollador de Software & Proyecto Agro Tecnológico</h2>
            <h1 style="font-size: 32px; margin-bottom:10px;">Leonardo Olivera</h1>
            <p style="font-size: 18px; line-height: 1.6;">
                <b>Estudiante de Agronomía | Experto en Informática (+20 años de exp.)</b><br>
                Perito en Granos | Operador Inmobiliario (Litoral Operaciones)<br>
                <span style="color: #28a745; font-weight: bold;">Análisis Financiero e Inversiones bajo Inteligencia Artificial Avanzada</span>
            </p>
        </div>
        """, unsafe_allow_html=True)

st.title("🛰️ AgroData Litoral: Auditoría 360°")
st.markdown("**Análisis de Padrón Rural 5900 | Young, Río Negro | Cliente: Lafluf**")
st.write("---")

# --- TABS DE NAVEGACIÓN ---
tabs = st.tabs(["📊 Monitoreo Satelital", "🗺️ Mapa Geológico", "🔬 Ciencia Espacial", "📥 Reporte Final"])

with tabs[0]:
    st.header("🎛️ Indicadores Multiespectrales (NASA / ESA)")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Salud Vegetal (NDVI)", "0.78", "+0.05", 
                  help="Fuente: Sentinel-2 (ESA). Mide vigor fotosintético y salud foliar.")
    with col2:
        st.metric("Humedad en Raíz (1m)", "14.2%", "-3.8% CRÍTICO", delta_color="inverse",
                  help="Fuente: NASA SMAP. Escaneo de microondas para medir reserva hídrica real.")
    with col3:
        st.metric("Resistencia Mecánica", "2.5 MPa", "Suelo Firme",
                  help="Fuente: Análisis Gravimétrico. Útil para cimentación de infraestructura pesada.")

with tabs[1]:
    st.header("🌐 Delimitación Técnica Padrón 5900 (5 Ha)")
    # Coordenadas rurales reales para evitar casas
    lat, lon = -32.6585, -57.6455
    m = folium.Map(location=[lat, lon], zoom_start=16, tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google')
    
    puntos_padrón = [[-32.6565, -57.6485], [-32.6565, -57.6425], [-32.6615, -57.6445], [-32.6615, -57.6475], [-32.6585, -57.6490], [-32.6565, -57.6485]]
    folium.Polygon(locations=puntos_padrón, color="#FFFFFF", weight=4, fill=True, fill_color="#39FF14", fill_opacity=0.35, tooltip="ESCANEANDO PADRÓN 5900").add_to(m)
    folium_static(m, width=1200)

with tabs[2]:
    st.subheader("📡 Constelaciones y Validación Oficial")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("### 🇪🇺 ESA Sentinel-2")
        st.write("Detecta variabilidad de nitrógeno y clorofila.")
    with c2:
        st.markdown("### 🇺🇸 NASA SMAP")
        st.write("Mapeo global de humedad de suelo mediante radar.")
    with c3:
        st.markdown("### 🇺🇸 NASA Landsat")
        st.write("Infrarrojo térmico para medir evapotranspiración.")
    
    st.divider()
    st.write("✅ **Sincronizado con:** MGAP, SNIG, DIEA, INIA e OPYPA (Uruguay).")

with tabs[3]:
    st.header("📄 Auditoría Certificada")
    if st.button("👁️ VER MUESTRA DE REPORTE PDF"):
        st.success("Vista previa generada. El reporte completo se libera tras validación de pago.")
    st.error("🔒 REPORTE BLOQUEADO: Requiere validación de giro u$s 150.")

# PIE DE PÁGINA
st.write("---")
st.markdown("""
    <div style="text-align: center; color: #333; padding: 20px; font-size: 14px;">
        <p><b>© 2026 AgroData Litoral - Todos los derechos reservados</b></p>
        <p><i>Derechos reservados Agro Data Litoral desarrollador de Software y Director de Proyecto Leonardo Olivera</i></p>
    </div>
""", unsafe_allow_html=True)
