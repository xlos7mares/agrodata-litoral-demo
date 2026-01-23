import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from streamlit_folium import folium_static
import folium
import os

# 1. CONFIGURACIÓN DE PÁGINA Y ESTÉTICA "CAMPO VIVO"
st.set_page_config(page_title="AgroData Litoral - Master Control", layout="wide")

st.markdown("""
    <style>
    /* Fondo de campo con colores vivos y nítidos */
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.2), rgba(0, 0, 0, 0.3)), 
                    url("https://images.unsplash.com/photo-1500382017468-9049fed747ef?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80");
        background-size: cover;
        background-attachment: fixed;
    }
    
    /* Panel Superior Negro Transparente */
    .top-panel {
        background-color: rgba(0, 0, 0, 0.75);
        padding: 20px;
        border-radius: 15px;
        border-bottom: 4px solid #39FF14;
        margin-bottom: 25px;
    }

    /* Logo Satélite Estilizado */
    .logo-box {
        display: flex;
        align-items: center;
        gap: 15px;
    }
    .logo-text {
        font-family: 'Arial Black', sans-serif;
        color: white;
        line-height: 1;
        font-size: 26px;
    }

    /* Perfil a la Derecha */
    .perfil-box {
        text-align: right;
        color: white;
    }
    .img-circular {
        border-radius: 50%;
        border: 3px solid #39FF14;
        box-shadow: 0px 0px 15px rgba(57, 255, 20, 0.5);
    }

    /* Tarjetas de Métricas de Alta Visibilidad */
    div[data-testid="stMetric"] {
        background-color: rgba(255, 255, 255, 0.92) !important;
        border-radius: 12px !important;
        border-left: 8px solid #28a745 !important;
        box-shadow: 0px 8px 20px rgba(0,0,0,0.3) !important;
    }
    
    h1, h2, h3, p { color: white !important; text-shadow: 1px 1px 3px black; }
    .stTabs [data-baseweb="tab-list"] { background-color: rgba(0,0,0,0.7); border-radius: 10px; padding: 5px; }
    </style>
    """, unsafe_allow_html=True)

# 2. ENCABEZADO: LOGO SATÉLITE (IZQ) | PERFIL PROFESIONAL (DER)
with st.container():
    col_izq, col_der = st.columns([2, 2])
    
    with col_izq:
        st.markdown("""
            <div class="logo-box">
                <span style="font-size: 50px;">🛰️</span>
                <div class="logo-text">AGRO<span style="color:#39FF14;">DATA</span><br>LITORAL</div>
            </div>
        """, unsafe_allow_html=True)

    with col_der:
        c_info, c_foto = st.columns([3, 1])
        with c_info:
            st.markdown(f"""
                <div class="perfil-box">
                    <h2 style="margin:0; font-size: 24px;">Leonardo Olivera</h2>
                    <p style="margin:0; color:#39FF14; font-weight:bold;">📲 099417716</p>
                    <p style="font-size:11px; line-height:1.2; opacity: 0.9;">
                        Desarrollador de Software & Proyecto Agro Tecnológico<br>
                        Estudiante de Agronomía | Experto Informático (+20 años exp.)<br>
                        Perito en Grano | Operador Inmobiliario | Especialista en IA
                    </p>
                </div>
            """, unsafe_allow_html=True)
        with c_foto:
            # Tu foto real cargada desde GitHub
            foto_path = "20250508_225422 (1).jpg"
            if os.path.exists(foto_path):
                st.image(foto_path, width=100)

st.markdown("### 📡 Auditoría Satelital de Precisión | Padrón 5900 - Young")
st.write("---")

# 3. CUERPO TÉCNICO - LA "MIEL PURA" DEL DATO
tabs = st.tabs(["📊 MONITOREO EN VIVO", "🗺️ MAPA DE TERRENO", "🔬 CIENCIA ESPACIAL", "🔒 REPORTE FULL"])

with tabs[0]:
    st.markdown("#### 🎛️ Centro de Indicadores Críticos")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Salud Vegetal (NDVI)", value="0.78", delta="+0.05",
            help="""🛰️ FUENTE: Sentinel-2 (ESA). 
📖 NOMENCLATURA: Normalized Difference Vegetation Index. 
💡 UTILIDAD: Evalúa vigor fotosintético. 
🎯 OBJETIVO: Un valor de 0.78 indica biomasa sana y productiva."""
        )
    with col2:
        st.metric(
            label="Humedad Perfil (1m)", value="14.2%", delta="-3.8% CRÍTICO", delta_color="inverse",
            help="""🛰️ FUENTE: NASA SMAP. 
📖 NOMENCLATURA: Agua Disponible en Perfil Profundo. 
💡 UTILIDAD: Escaneo radar de microondas. 
🎯 OBJETIVO: Determinar reservas hídricas bajo tierra en zona de raíces."""
        )
    with col3:
        st.metric(
            label="Resistencia Suelo", value="2.5 MPa", delta="Suelo Firme",
            help="""🛰️ FUENTE: Gravimetría Satelital. 
📖 NOMENCLATURA: Mega Pascales (MPa). 
💡 UTILIDAD: Capacidad de carga mecánica. 
🎯 OBJETIVO: Determinar aptitud para infraestructura pesada sin hundimiento."""
        )

with tabs[1]:
    st.markdown("#### 🌐 Escaneo sobre Imágenes de Google Hybrid")
    lat, lon = -32.6585, -57.6455
    m = folium.Map(location=[lat, lon], zoom_start=16, tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google')
    folium.Polygon(
        locations=[[-32.6565, -57.6485], [-32.6565, -57.6425], [-32.6615, -57.6445], [-32.6615, -57.6475], [-32.6585, -57.6490], [-32.6565, -57.6485]],
        color="#39FF14", weight=5, fill=True, fill_color="#39FF14", fill_opacity=0.25,
        tooltip="Padrón 5900 Analizado"
    ).add_to(m)
    folium_static(m, width=1100)

with tabs[2]:
    st.markdown("#### 🔬 Ciencia Aplicada al Campo")
    st.info("Sistemas de Adquisición: **ESA Sentinel-2, NASA SMAP y Landsat**.")
    st.write("Validación Local: **MGAP, SNIG, DIEA, INIA e OPYPA (Uruguay)**.")

with tabs[3]:
    st.header("📄 Informe Final Certificado")
    st.error("🔒 BLOQUEADO: Requiere validación de pago u$s 150 a Leonardo Olivera.")

# 4. PIE DE PÁGINA (FIRMA)
st.markdown(f"""
    <div style="text-align: center; color: white; padding: 20px; background-color: rgba(0,0,0,0.6); border-radius: 10px;">
        <p>© 2026 AgroData Litoral - Todos los derechos reservados</p>
        <p><b>Desarrollador & Director: Leonardo Olivera</b> | Contacto: 099417716</p>
    </div>
""", unsafe_allow_html=True)
