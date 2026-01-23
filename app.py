import streamlit as st
import pandas as pd
import numpy as np
from streamlit_folium import folium_static
import folium
import os

# 1. CONFIGURACIÓN Y ESTÉTICA "CAMPO VIVO"
st.set_page_config(page_title="AgroData Litoral - Master Control", layout="wide")

st.markdown("""
    <style>
    /* Fondo de campo vivo con saturación y nitidez */
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.1), rgba(0, 0, 0, 0.2)), 
                    url("https://images.unsplash.com/photo-1500382017468-9049fed747ef?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80");
        background-size: cover;
        background-attachment: fixed;
    }
    
    /* Contenedor Superior Negro para legibilidad */
    .header-container {
        background-color: rgba(0, 0, 0, 0.7);
        padding: 30px;
        border-radius: 15px;
        border-bottom: 5px solid #39FF14;
        margin-bottom: 20px;
        color: white;
    }

    /* Logo Satélite GRANDE */
    .logo-text {
        font-family: 'Arial Black', sans-serif;
        font-size: 38px;
        line-height: 0.9;
        color: white;
    }
    .satellite-icon {
        font-size: 70px; /* Tamaño aumentado */
        margin-right: 15px;
    }

    /* Perfil Alineado a la Derecha */
    .perfil-info {
        text-align: right;
        padding-right: 20px;
    }
    .perfil-foto {
        border-radius: 15px;
        border: 4px solid #39FF14;
        box-shadow: 0px 0px 20px rgba(57, 255, 20, 0.4);
    }

    /* Métricas: Texto NEGRO sobre fondo BLANCO para lectura perfecta */
    div[data-testid="stMetric"] {
        background-color: rgba(255, 255, 255, 0.95) !important;
        border-radius: 15px !important;
        padding: 20px !important;
        border-left: 10px solid #28a745 !important;
        box-shadow: 0px 8px 25px rgba(0,0,0,0.4) !important;
    }
    div[data-testid="stMetricLabel"], div[data-testid="stMetricValue"] {
        color: #000000 !important; /* Texto Negro */
    }

    h1, h2, h3 { color: white !important; text-shadow: 2px 2px 5px black; }
    .stTabs [data-baseweb="tab-list"] { background-color: rgba(0,0,0,0.8); border-radius: 10px; padding: 5px; }
    </style>
    """, unsafe_allow_html=True)

# 2. ENCABEZADO: LOGO XL (IZQ) | PERFIL ALINEADO (DER)
with st.container():
    col_izq, col_der = st.columns([2.5, 2.5])
    
    with col_izq:
        st.markdown("""
            <div style="display: flex; align-items: center;">
                <span class="satellite-icon">🛰️</span>
                <div class="logo-text">AGRO<span style="color:#39FF14;">DATA</span><br>LITORAL</div>
            </div>
        """, unsafe_allow_html=True)

    with col_der:
        c_text, c_img = st.columns([2, 1])
        with c_text:
            st.markdown(f"""
                <div class="perfil-info">
                    <h2 style="margin:0; font-size: 28px;">Leonardo Olivera</h2>
                    <p style="margin:0; color:#39FF14; font-weight:bold; font-size: 20px;">📲 099417716</p>
                    <p style="font-size:12px; line-height:1.3; opacity: 0.9;">
                        Desarrollador de Software & Proyecto Agro Tecnológico<br>
                        Estudiante de Agronomía | Experto Informático (+20 años exp.)<br>
                        Perito en Grano | Operador Inmobiliario | Especialista en IA
                    </p>
                </div>
            """, unsafe_allow_html=True)
        with c_img:
            foto_path = "20250508_225422 (1).jpg"
            if os.path.exists(foto_path):
                st.image(foto_path, width=130)

st.markdown("### 🛰️ Auditoría Sateeno | Padrón 5900 - Young")
st.write("---")

# 3. CUERPO TÉCNICO (LA "MIEL PURA")
tabs = st.tabs(["📊 MONITOREO EN VIVO", "🗺️ CAPA DE TERRENO", "🔬 CIENCIA ESPACIAL", "🔒 REPORTE FULL"])

with tabs[0]:
    st.markdown("#### 🎛️ Centro de Indicadores Críticos")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Salud Vegetal (NDVI)", value="0.78", delta="+0.05",
            help="FUENTES: Sentinel-2 (ESA). Mide el vigor fotosintético y biomasa activa."
        )
    with col2:
        st.metric(
            label="Humedad Perfil (1m)", value="14.2%", delta="-3.8% CRÍTICO", delta_color="inverse",
            help="FUENTES: NASA SMAP. Escaneo de microondas para reservas hídricas profundas."
        )
    with col3:
        st.metric(
            label="Resistencia Suelo", value="2.5 MPa", delta="Suelo Firme",
            help="FUENTES: NASA Landsat. Capacidad de carga mecánica para infraestructura."
        )

with tabs[1]:
    st.markdown("#### 🌐 Delimitación y Escaneo sobre Google Hybrid")
    lat, lon = -32.6585, -57.6455
    m = folium.Map(location=[lat, lon], zoom_start=16, tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google')
    folium.Polygon(
        locations=[[-32.6565, -57.6485], [-32.6565, -57.6425], [-32.6615, -57.6445], [-32.6615, -57.6475], [-32.6585, -57.6490], [-32.6565, -57.6485]],
        color="#39FF14", weight=5, fill=True, fill_color="#39FF14", fill_opacity=0.25
    ).add_to(m)
    folium_static(m, width=1100)

with tabs[2]:
    st.markdown("#### 🔬 Ciencia Satelital Aplicada")
    st.info("Sincronización total con: **MGAP, SNIG, DIEA, INIA e OPYPA (Uruguay)**.")

with tabs[3]:
    st.header("📄 Informe Certificado")
    st.error("🔒 BLOQUEADO: Requiere validación de pago u$s 150 a Leonardo Olivera.")

# 4. PIE DE PÁGINA
st.markdown("""
    <div style="text-align: center; color: white; padding: 30px; background-color: rgba(0,0,0,0.7); border-radius: 10px;">
        <p>© 2026 AgroData Litoral - Todos los derechos reservados</p>
        <p><b>Director de Proyecto: Leonardo Olivera</b> | Contacto: 099417716</p>
    </div>
""", unsafe_allow_html=True)
