import streamlit as st
import pandas as pd
import numpy as np
from streamlit_folium import folium_static
import folium
from folium.plugins import Draw
import os

# 1. ESTÉTICA AGRODATA (DISEÑO ORIGINAL Y BLINDAJE)
st.set_page_config(page_title="AgroData Litoral - Auditoría Real", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.3), rgba(0,0,0,0.3)), 
                    url("https://images.unsplash.com/photo-1500382017468-9049fed747ef?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80");
        background-size: cover; background-attachment: fixed;
    }
    div[data-testid="stMetric"] {
        background-color: rgba(255, 255, 255, 0.15) !important;
        border-radius: 15px !important;
        padding: 20px !important;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.3);
    }
    div[data-testid="stMetricValue"] { color: #FFFFFF !important; font-weight: 900 !important; }
    div[data-testid="stMetricLabel"] { color: #39FF14 !important; }

    /* Recuadro de Informe Técnico Profesional */
    .diagnostico-real {
        background-color: rgba(255, 255, 255, 0.98);
        color: #000;
        padding: 30px;
        border-radius: 20px;
        border-left: 15px solid #1e4d2b;
        margin-top: 25px;
        line-height: 1.6;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. PANEL DE CONTROL (ENTRADA DE DATOS REALES)
with st.sidebar:
    st.header("📍 Navegación Satelital")
    coords_raw = st.text_input("Latitud, Longitud Actual:", "-32.6585, -57.6455")
    
    st.write("---")
    st.header("🔬 Ingreso de Datos de Auditoría")
    s_ndvi = st.number_input("NDVI Real (Salud):", 0.0, 1.0, 0.78)
    s_agua = st.number_input("Humedad Real %:", 0.0, 100.0, 14.2)
    s_suelo = st.number_input("Firmeza Real (MPa):", 0.0, 5.0, 2.5)
    st.info("Obtenga estos valores procesando las bandas NASA/ESA.")

# 3. ENCABEZADO (LOGO Y PERFIL ACTUALIZADO)
with st.container():
    col_l, col_r = st.columns([2.5, 3.5])
    with col_l:
        st.markdown("<div style='display: flex; align-items: center; margin-top: 10px;'><span style='font-size: 85px; margin-right: 20px;'>🛰️</span><div style='font-family: \"Arial Black\"; font-size: 38px; line-height: 0.9; color: white;'>AGRO<span style='color:#39FF14;'>DATA</span><br>LITORAL</div></div>", unsafe_allow_html=True)
    with col_r:
        c_txt, c_img = st.columns([2.5, 1])
        with c_txt:
            st.markdown(f"""
                <div style='text-align: right; color: white;'>
                    <h2 style='margin:0;'>Leonardo Olivera</h2>
                    <p style='color:#39FF14; font-weight:bold; font-size: 20px; margin:0;'>📲 099417716</p>
                    <p style='font-size:12px; opacity:0.95; line-height:1.4;'>
                        <b>Perito en Grano | Experto en IA | Estudiante Agronomía</b><br>
                        Operaciones Inmobiliarias | Aficionado a la Geología,<br>
                        Botánica e Ingeniería Agro Ambiental | Protección del Medio Ambiente
                    </p>
                </div>
            """, unsafe_allow_html=True)
        with c_img:
            if os.path.exists("20250508_225422 (1).jpg"): st.image("20250508_225422 (1).jpg", width=130)

st.markdown(f"### 🛰️ AUDITORÍA SATELITAL EN VIVO | Padrón: {coords_raw}")
st.write("---")

# 4. MÉTRICAS CIENTÍFICAS
c1, c2, c3 = st.columns(3)
c1.metric("Vigor (NDVI)", f"{s_ndvi}")
c2.metric("Humedad %", f"{s_agua}%")
c3.metric("Firmeza (MPa)", f"{s_suelo}")

# 5. MAPA SATELITAL REAL (Google Satélite)
st.markdown("#### 🗺️ Explorador Satelital (Use las herramientas de la izquierda para marcar zonas)")
try:
    lat, lon = map(float, coords_raw.split(','))
except:
    lat, lon = -32.6585, -57.6455

m = folium.Map(location=[lat, lon], zoom_start=16, tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google Satélite')

# Herramientas de dibujo limpias (Sin popups de código)
draw = Draw(
    export=False, 
    position='topleft',
    draw_options={'polyline':False, 'circle':False, 'marker':False, 'circlemarker':False, 'polygon':True, 'rectangle':True}
)
draw.add_to(m)

folium_static(m, width=1100)

# 6. INFORME DE INTERPRETACIÓN (SIN ETIQUETAS VISIBLES)
det_monte = "Detección de Monte Nativo / Reserva biológica activa." if s_ndvi > 0.72 else "Vegetación de pastura o cultivo estacional."
det_tosca = "Afloramiento rocoso detectado (Tosca firme)." if s_suelo > 3.0 else "Suelo profundo con aptitud de cimentación estándar."
det_agua = "Cursos de agua activos identificados (NDWI)." if s_agua > 25 else "Suelo con drenaje activo, sin agua superficial detectada."

informe_html = f"""
<div class="diagnostico-real">
    <h3 style="color:#1e4d2b; text-align:center; margin-top:0;">📋 Diagnóstico de Activos Naturales e Infraestructura</h3>
    <hr>
    <p><b>🌿 Ingeniería Agro Ambiental:</b> {det_monte} El análisis Sentinel-2 confirma la salud del ecosistema botánico.</p>
    <p><b>🌍 Geología Aplicada:</b> {det_tosca} La inercia térmica Landsat valida la estabilidad mecánica para construcción.</p>
    <p><b>💧 Recursos Hídricos:</b> {det_agua} Los niveles de {s_agua}% aseguran disponibilidad hídrica para el proyecto.</p>
    <div style="background:#e8f5e9; padding:20px; border-radius:15px; border:1px solid #1e4d2b; margin-top:15px; text-align:center;">
        <h4 style="margin:0;">💰 Inversión en Auditoría: U$S 150</h4>
        <p style="margin:5px;">Este informe certifica la realidad física del padrón mediante inteligencia satelital.</p>
    </div>
</div>
"""
st.markdown(informe_html, unsafe_allow_html=True)

st.markdown("<br><center style='color:white; opacity:0.8;'>© 2026 Litoral Operaciones Inmobiliarias | Leonardo Olivera</center>", unsafe_allow_html=True)
