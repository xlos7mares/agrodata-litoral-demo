import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from streamlit_folium import folium_static
import folium
import os

# 1. CONFIGURACIÓN DE PÁGINA Y ESTÉTICA "TECH-AGRO"
st.set_page_config(page_title="AgroData Litoral - Estación de Control", layout="wide")

st.markdown("""
    <style>
    /* Fondo de campo tenue */
    .stApp {
        background: linear-gradient(rgba(255, 255, 255, 0.85), rgba(255, 255, 255, 0.85)), 
                    url("https://images.unsplash.com/photo-1500382017468-9049fed747ef?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80");
        background-size: cover;
        background-attachment: fixed;
    }
    
    /* Logotipo AgroData Litoral con Satélite */
    .logo-container {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 10px;
    }
    .logo-text {
        font-family: 'Arial Black', sans-serif;
        font-size: 28px;
        line-height: 1;
        color: #1e4d2b;
    }
    .satellite-icon {
        font-size: 40px;
    }

    /* Tarjeta de Perfil a la Derecha */
    .perfil-derecha {
        text-align: right;
        padding: 10px;
        border-right: 5px solid #28a745;
        padding-right: 20px;
    }
    .img-circular {
        border-radius: 50%;
        border: 4px solid #28a745;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
    }

    /* Estilo de Métricas */
    div[data-testid="stMetric"] {
        background-color: rgba(255, 255, 255, 0.95) !important;
        border-radius: 15px !important;
        border: 1px solid #ddd !important;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.1) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. ENCABEZADO DISTRIBUIDO (LOGO IZQ | PERFIL DER)
col_izq, col_der = st.columns([2, 2])

with col_izq:
    st.markdown("""
        <div class="logo-container">
            <span class="satellite-icon">🛰️</span>
            <div class="logo-text">AGRO<br><span style="color:#28a745;">DATA</span><br><span style="font-size:18px; color:#555;">LITORAL</span></div>
        </div>
    """, unsafe_allow_html=True)

with col_der:
    c_info, c_foto = st.columns([3, 1])
    with c_info:
        st.markdown(f"""
            <div class="perfil-derecha">
                <h3 style="margin:0; color:#1e4d2b !important;">Leonardo Olivera</h3>
                <p style="margin:0; color:#28a745; font-weight:bold;">📲 099417716</p>
                <p style="font-size:11px; color:#333; line-height:1.2;">
                    Desarrollador de Software & Proyecto Agro Tecnológico<br>
                    Estudiante de Agronomía | Experto Informático (+20 años exp.)<br>
                    Perito en Grano | Operador Inmobiliario | Especialista en IA
                </p>
            </div>
        """, unsafe_allow_html=True)
    with c_foto:
        foto_path = "20250508_225422 (1).jpg"
        if os.path.exists(foto_path):
            st.image(foto_path, width=100)

st.markdown("### 🛰️ Auditoría 360° | Padrón Rural 5900 - Young")
st.write("---")

# 3. CUERPO TÉCNICO CON TODA LA NOMENCLATURA
tabs = st.tabs(["📊 MONITOREO SATELITAL", "🗺️ MAPA GEOLÓGICO", "🔬 CIENCIA ESPACIAL", "🔒 ACCESO REPORTE"])

with tabs[0]:
    st.subheader("🎛️ Centro de Indicadores Críticos")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Salud Vegetal (NDVI)", value="0.78", delta="+0.05",
            help="""🛰️ FUENTE: Sentinel-2 (ESA).
📖 NOMENCLATURA: Normalized Difference Vegetation Index.
💡 UTILIDAD: Mide el vigor fotosintético.
🎯 OBJETIVO: Evaluar salud foliar. Un 0.78 indica biomasa activa y productiva."""
        )
    with col2:
        st.metric(
            label="Humedad Perfil (1m)", value="14.2%", delta="-3.8% CRÍTICO", delta_color="inverse",
            help="""🛰️ FUENTE: NASA SMAP.
📖 NOMENCLATURA: Agua Disponible en Perfil Profundo.
💡 UTILIDAD: Escaneo por radar de microondas.
🎯 OBJETIVO: Determinar reservas hídricas subterráneas en zona de raíces."""
        )
    with col3:
        st.metric(
            label="Resistencia Suelo", value="2.5 MPa", delta="Suelo Firme",
            help="""🛰️ FUENTE: Gravimetría Infrarroja.
📖 NOMENCLATURA: Mega Pascales (Medida de Presión).
💡 UTILIDAD: Mide compactación y firmeza del horizonte.
🎯 OBJETIVO: Determinar aptitud para infraestructura pesada (galpones/silos)."""
        )

with tabs[1]:
    st.subheader("🌐 Escaneo Satelital de Precisión")
    lat, lon = -32.6585, -57.6455
    m = folium.Map(location=[lat, lon], zoom_start=16, tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google')
    folium.Polygon(
        locations=[[-32.6565, -57.6485], [-32.6565, -57.6425], [-32.6615, -57.6445], [-32.6615, -57.6475], [-32.6585, -57.6490], [-32.6565, -57.6485]],
        color="#28a745", weight=4, fill=True, fill_color="#39FF14", fill_opacity=0.3,
        tooltip="Análisis de Padrón 5900"
    ).add_to(m)
    folium_static(m, width=1100)

with tabs[2]:
    st.subheader("🔬 Arquitectura de Datos")
    st.write("Sistemas Integrados: **ESA Sentinel-2, NASA SMAP, NASA Landsat**.")
    st.write("Validación Institucional: **MGAP, SNIG, DIEA, INIA e OPYPA**.")

with tabs[3]:
    st.header("📄 Descarga de Auditoría Certificada")
    st.error("🔒 BLOQUEADO: Requiere validación de pago u$s 150.")

# 4. PIE DE PÁGINA PROFESIONAL
st.markdown(f"""
    <div style="text-align: center; color: #555; padding: 20px;">
        <p>© 2026 AgroData Litoral - Todos los derechos reservados</p>
        <p><b>Desarrollador de Software & Director de Proyecto: Leonardo Olivera</b> | Contacto: 099417716</p>
    </div>
""", unsafe_allow_html=True)
