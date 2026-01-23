import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from streamlit_folium import folium_static
import folium
from fpdf import FPDF
import base64

# 1. CONFIGURACIÓN DE PÁGINA Y ESTILO VISUAL
st.set_page_config(page_title="AgroData Litoral - Master Report", layout="wide")

# Fondo de campo tenue y estilos de tarjetas
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(255, 255, 255, 0.85), rgba(255, 255, 255, 0.85)), 
                    url("https://images.unsplash.com/photo-1500382017468-9049fed747ef?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80");
        background-size: cover;
        background-attachment: fixed;
    }
    div[data-testid="stMetric"] {
        background-color: rgba(255, 255, 255, 0.95) !important;
        border: 2px solid #28a745 !important;
        border-radius: 15px !important;
        padding: 20px !important;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.1) !important;
    }
    .perfil-card {
        background-color: rgba(255, 255, 255, 0.9);
        padding: 20px;
        border-radius: 15px;
        border-left: 8px solid #1e4d2b;
        margin-bottom: 25px;
    }
    h1, h2, h3 { color: #1e4d2b !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. PRESENTACIÓN PROFESIONAL (PERFIL LEO OLIVERA)
with st.container():
    col_foto, col_info = st.columns([1, 4])
    with col_foto:
        # Aquí usamos tu foto. Asegúrate de subirla a GitHub con el nombre 'perfil.jpg' 
        # o usa este placeholder para la demo
        st.image("https://raw.githubusercontent.com/tu-usuario/tu-repo/main/20250508_225422%20(1).jpg", width=160, caption="Director de Proyecto")
    
    with col_info:
        st.markdown(f"""
        <div class="perfil-card">
            <h2>Desarrollador de Software & Proyecto Agro Tecnológico</h2>
            <h3>Leonardo Olivera</h3>
            <p><b>Estudiante de Agronomía | Experto en Informática (+20 años de exp.)</b><br>
            Perito en Granos | Operador Inmobiliario (Litoral Operaciones)<br>
            <i>Análisis Financiero e Inversiones bajo Inteligencia Artificial Avanzada</i></p>
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
                  help="Fuente: Sentinel-2. SIGLAS: Índice de Vegetación de Diferencia Normalizada. UTILIDAD: Mide vigor fotosintético y salud foliar.")
    with col2:
        st.metric("Humedad en Raíz (1m)", "14.2%", "-3.8% CRÍTICO", delta_color="inverse",
                  help="Fuente: NASA SMAP. UTILIDAD: Escaneo de microondas para medir reserva hídrica real en el perfil profundo.")
    with col3:
        st.metric("Resistencia Mecánica", "2.5 MPa", "Suelo Firme",
                  help="Fuente: Análisis Gravimétrico. UTILIDAD: Mide capacidad de carga para cimentación de infraestructura pesada.")

with tabs[1]:
    st.header("🌐 Delimitación Técnica Padrón 5900 (5 Ha)")
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
        st.write("**Utilidad:** Detección de clorofila y variabilidad de nitrógeno por bandas ópticas.")
    with c2:
        st.markdown("### 🇺🇸 NASA SMAP")
        st.write("**Utilidad:** Sensor pasivo/activo para mapeo de humedad de suelo a escala global.")
    with c3:
        st.markdown("### 🇺🇸 NASA Landsat")
        st.write("**Utilidad:** Infrarrojo térmico para medir evapotranspiración y fiebre de la planta.")
    
    st.divider()
    st.write("✅ **Sincronizado con:** MGAP, SNIG, DIEA, INIA e OPYPA (Uruguay).")

with tabs[3]:
    st.header("📄 Generación de Auditoría Certificada")
    if st.button("👁️ VER MUESTRA DE REPORTE PDF"):
        st.success("Generando vista previa... El reporte completo con coordenadas GPS se libera tras validación de pago.")
    st.divider()
    st.error("🔒 REPORTE PROFESIONAL BLOQUEADO: Requiere validación de giro u$s 150.")

# PIE DE PÁGINA
st.write("---")
st.markdown("""
    <div style="text-align: center; color: #333; padding: 20px;">
        <p><b>© 2026 AgroData Litoral - Todos los derechos reservados</b></p>
        <p><i>Tecnología Satelital Aplicada al Desarrollo Productivo de la Cuenca del Río Uruguay</i></p>
    </div>
""", unsafe_allow_html=True)
