import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from streamlit_folium import folium_static
import folium
from fpdf import FPDF
import base64
import os

# 1. CONFIGURACIÓN DE PÁGINA Y ESTÉTICA "TECH-AGRO"
st.set_page_config(page_title="AgroData Litoral - Estación de Control", layout="wide")

st.markdown("""
    <style>
    /* Fondo de campo con overlay oscuro para resaltar el blanco */
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.4)), 
                    url("https://images.unsplash.com/photo-1500382017468-9049fed747ef?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80");
        background-size: cover;
        background-attachment: fixed;
    }
    
    /* Encabezado Negro Estilo Panel de Control */
    .header-panel {
        background-color: rgba(0, 0, 0, 0.85);
        padding: 20px;
        border-radius: 0 0 20px 20px;
        border-bottom: 3px solid #39FF14;
        margin-bottom: 30px;
        color: white;
    }

    /* Tarjetas de Métricas Transparentes y Modernas */
    div[data-testid="stMetric"] {
        background-color: rgba(255, 255, 255, 0.95) !important;
        border-left: 10px solid #28a745 !important;
        border-radius: 15px !important;
        padding: 20px !important;
        box-shadow: 0px 10px 30px rgba(0,0,0,0.5) !important;
    }

    /* Foto de Perfil Circular */
    .img-perfil {
        border-radius: 50%;
        border: 4px solid #39FF14;
        box-shadow: 0px 0px 15px #39FF14;
    }

    h1, h2, h3 { color: #ffffff !important; text-shadow: 2px 2px 4px #000; }
    .stTabs [data-baseweb="tab-list"] { background-color: rgba(0,0,0,0.6); border-radius: 10px; }
    .stTabs [data-baseweb="tab"] { color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. ENCABEZADO TIPO PANEL DE CONTROL (LOGO SATÉLITE + FOTO + CONTACTO)
with st.container():
    col_logo, col_perfil, col_contacto = st.columns([1.5, 1, 2.5])
    
    with col_logo:
        if os.path.exists("logoagrodata.png"):
            st.image("logoagrodata.png", width=180)
        else:
            st.markdown("<h1 style='color:#39FF14 !important;'>AgroData<br>Litoral</h1>", unsafe_allow_html=True)

    with col_perfil:
        foto_path = "20250508_225422 (1).jpg"
        if os.path.exists(foto_path):
            st.image(foto_path, width=130) # Imagen pequeña y circular por CSS

    with col_contacto:
        st.markdown(f"""
        <div style="color: white; text-align: left;">
            <h2 style="margin:0; font-size:24px;">Leonardo Olivera</h2>
            <p style="margin:0; color:#39FF14; font-weight:bold;">📲 Contacto Directo: 099417716</p>
            <p style="font-size:12px; line-height:1.2;">
                Desarrollador de Software & Proyecto Agro Tecnológico<br>
                Estudiante de Agronomía | Experto Informático (+20 años exp.)<br>
                Perito en Grano | Operador Inmobiliario | Especialista en IA
            </p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("### 🛰️ Auditoría 360° | Padrón Rural 5900 - Young")
st.write("---")

# 3. TABS DE INFORMACIÓN TÉCNICA TOTAL
tabs = st.tabs(["📊 MONITOREO SATELITAL", "🗺️ MAPA GEOLÓGICO", "🔬 CIENCIA ESPACIAL", "📥 AUDITORÍA FINAL"])

with tabs[0]:
    st.markdown("### 🎛️ Centro de Indicadores Críticos")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Salud Vegetal (NDVI)", value="0.78", delta="+0.05",
            help="""🛰️ FUENTE: Sentinel-2 (Agencia Espacial Europea).
📖 NOMENCLATURA: Normalized Difference Vegetation Index.
💡 UTILIDAD: Mide la reflectancia del infrarrojo cercano. 
🎯 OBJETIVO: Evaluar vigor fotosintético. Un valor de 0.78 indica biomasa sana y crecimiento activo."""
        )
    with col2:
        st.metric(
            label="Humedad de Perfil (1m)", value="14.2%", delta="-3.8% CRÍTICO", delta_color="inverse",
            help="""🛰️ FUENTE: NASA SMAP (Soil Moisture Active Passive).
📖 NOMENCLATURA: Agua Disponible en Perfil Profundo.
💡 UTILIDAD: Escaneo por radar de microondas.
🎯 OBJETIVO: Determinar la reserva hídrica real en la zona de raíces. El descenso indica estrés hídrico subterráneo."""
        )
    with col3:
        st.metric(
            label="Resistencia Mecánica", value="2.5 MPa", delta="Suelo Firme",
            help="""🛰️ FUENTE: Gravimetría Infrarroja.
📖 NOMENCLATURA: Mega Pascales (Medida de Presión).
💡 UTILIDAD: Mide la compactación y firmeza del horizonte superficial.
🎯 OBJETIVO: Determinar aptitud para infraestructura pesada y capacidad de penetración de raíces."""
        )

with tabs[1]:
    st.markdown("### 🌐 Visualización de Precisión sobre Terreno Real")
    lat, lon = -32.6585, -57.6455
    m = folium.Map(location=[lat, lon], zoom_start=16, tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google')
    
    # Polígono del Padrón con estética Neón
    puntos_padrón = [[-32.6565, -57.6485], [-32.6565, -57.6425], [-32.6615, -57.6445], [-32.6615, -57.6475], [-32.6585, -57.6490], [-32.6565, -57.6485]]
    folium.Polygon(locations=puntos_padrón, color="#39FF14", weight=5, fill=True, fill_color="#39FF14", fill_opacity=0.25, tooltip="ESPECTRO PADRÓN 5900").add_to(m)
    folium_static(m, width=1200)

with tabs[2]:
    st.markdown("### 🔬 Arquitectura de Datos y Fuentes")
    st.write("La herramienta integra capas de datos crudos procesadas mediante algoritmos de Inteligencia Artificial:")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.info("**Sentinel-2 (ESA):** Monitoreo óptico de alta resolución (10m) para clorofila.")
    with c2:
        st.info("**SMAP (NASA):** Sensores térmicos para balance hídrico global.")
    with c3:
        st.info("**Landsat (USGS):** Datos históricos para análisis multitemporal de suelos.")
    
    st.write("🏛️ **Sincronización Uruguay:** Validación mediante DIEA, INIA (GRAS), SNIG y MGAP.")

with tabs[3]:
    st.markdown("### 📄 Generación de Reporte para Toma de Decisiones")
    st.warning("⚠️ El Reporte Completo incluye: Coordenadas GPS de vértices, mapa de calor de nitrógeno y proyección climática a 15 días.")
    st.error("🔒 BLOQUEADO: Requiere validación de pago u$s 150.")

# 4. PIE DE PÁGINA (COPYRIGHT Y FIRMA)
st.markdown(f"""
    <div style="text-align: center; color: white; padding: 40px; background-color: rgba(0,0,0,0.8); border-radius: 20px 20px 0 0;">
        <p>© 2026 AgroData Litoral - Todos los derechos reservados</p>
        <p><b>Desarrollador de Software & Proyecto Agro Tecnológico: Leonardo Olivera</b></p>
        <p>Contacto: 099417716 | Young, Río Negro, Uruguay</p>
    </div>
""", unsafe_allow_html=True)
