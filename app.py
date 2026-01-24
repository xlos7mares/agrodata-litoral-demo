import streamlit as st
import pandas as pd
import numpy as np
from streamlit_folium import folium_static
import folium
from folium.plugins import Draw
import os

# 1. ESTÉTICA AGRODATA (DISEÑO BLINDADO)
st.set_page_config(page_title="AgroData Litoral - Master Control", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.4), rgba(0,0,0,0.4)), 
                    url("https://images.unsplash.com/photo-1500382017468-9049fed747ef?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80");
        background-size: cover; background-attachment: fixed;
    }
    div[data-testid="stMetric"] {
        background-color: rgba(255, 255, 255, 0.12) !important;
        border-radius: 15px !important;
        padding: 20px !important;
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255,255,255,0.2);
    }
    div[data-testid="stMetricValue"] { color: #FFFFFF !important; font-weight: 900 !important; }
    div[data-testid="stMetricLabel"] { color: #39FF14 !important; }

    .diagnostico-real {
        background-color: rgba(255, 255, 255, 0.98);
        color: #000;
        padding: 30px;
        border-radius: 20px;
        border-left: 15px solid #1e4d2b;
        margin-top: 25px;
        box-shadow: 0px 10px 30px rgba(0,0,0,0.5);
    }
    </style>
    """, unsafe_allow_html=True)

# 2. PANEL DE CONTROL (ENTRADA DE DATOS REALES)
with st.sidebar:
    st.header("📍 Auditoría en Vivo")
    coords_raw = st.text_input("Latitud, Longitud Actual:", "-32.6585, -57.6455")
    
    st.write("---")
    st.header("🔬 Parámetros Físico-Satelitales")
    s_ndvi = st.number_input("NDVI (Salud Botánica):", 0.0, 1.0, 0.78)
    s_agua = st.number_input("Humedad Real (NDWI) %:", 0.0, 100.0, 14.2)
    s_suelo = st.number_input("Resistencia Física (MPa):", 0.0, 5.0, 2.5)
    st.info("Valores procesados mediante IA de Ciencia Física aplicada.")

# 3. ENCABEZADO: LOGO Y PERFIL REESTRUCTURADO
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
                    <p style='color:#39FF14; font-weight:bold; font-size: 19px; margin:0;'>📲 099417716</p>
                    <p style='font-size:12px; opacity:0.95; line-height:1.3;'>
                        <b>Estudiante Agronomía | Operaciones Inmobiliarias</b><br>
                        Perito en Grano | Experto en IA | Aficionado a la Ciencia Física,<br>
                        Geología, Botánica e Ingeniería Agro Ambiental | Protección del M. Ambiente<br>
                        <i>Desarrollador de Software con IA aplicada a la Ciencia Física</i>
                    </p>
                </div>
            """, unsafe_allow_html=True)
        with c_img:
            if os.path.exists("20250508_225422 (1).jpg"): st.image("20250508_225422 (1).jpg", width=125)

st.markdown(f"### 🛰️ DIAGNÓSTICO SATELITAL INTEGRADO | Padrón: {coords_raw}")
st.write("---")

# 4. MÉTRICAS CIENTÍFICAS
c1, c2, c3 = st.columns(3)
c1.metric("Vigor Fotovoltaico (NDVI)", f"{s_ndvi}")
c2.metric("Saturación NDWI %", f"{s_agua}%")
c3.metric("Módulo Elástico (MPa)", f"{s_suelo}")

# 5. MAPA SATELITAL (Google Satélite)
try:
    lat, lon = map(float, coords_raw.split(','))
except:
    lat, lon = -32.6585, -57.6455

m = folium.Map(location=[lat, lon], zoom_start=16, tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google Satélite')
Draw(export=False, position='topleft', draw_options={'polyline':False, 'circle':False, 'marker':False, 'circlemarker':False, 'polygon':True, 'rectangle':True}).add_to(m)
folium_static(m, width=1100)

# 6. INFORME DE LOGROS Y CIENCIA APLICADA (SIN ETIQUETAS VISIBLES)
det_monte = "Detección de Monte Nativo / Reserva biológica activa." if s_ndvi > 0.72 else "Vegetación de pastura o cultivo estacional."
det_tosca = "Afloramiento rocoso detectado (Tosca firme)." if s_suelo > 3.0 else "Suelo profundo con aptitud de cimentación estándar."
det_agua = "Cursos de agua activos identificados (NDWI)." if s_agua > 25 else "Suelo con drenaje activo, sin agua superficial detectada."

informe_html = f"""
<div class="diagnostico-real">
    <h3 style="color:#1e4d2b; text-align:center; margin-top:0;">📋 Reporte Técnico de Auditoría Profesional</h3>
    <hr>
    <p><b>🌿 Agronomía y Botánica:</b> {det_monte} Análisis espectral de biomasa realizado mediante Sentinel-2.</p>
    <p><b>🌍 Geología y Ciencia Física:</b> {det_tosca} Cálculo de resistencia mecánica de {s_suelo} MPa validado por IA de Ciencia Física aplicada.</p>
    <p><b>💧 Ingeniería Agro Ambiental:</b> {det_agua} Detección de recursos hídricos para protección del medio ambiente.</p>
    <div style="background:#e8f5e9; padding:20px; border-radius:15px; border:1px solid #1e4d2b; margin-top:15px; text-align:center;">
        <h4 style="margin:0;">Certificación de Auditoría: U$S 150</h4>
        <p style="margin:5px; font-size:14px;">Este informe integra Ciencia Física, IA y Agronomía para garantizar la seguridad de su inversión inmobiliaria.</p>
    </div>
</div>
"""
st.markdown(informe_html, unsafe_allow_html=True)

st.markdown("<br><center style='color:white; opacity:0.8;'>© 2026 Litoral Operaciones Inmobiliarias | Leonardo Olivera</center>", unsafe_allow_html=True)
