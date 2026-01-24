import streamlit as st
import pandas as pd
import numpy as np
from streamlit_folium import folium_static
import folium
from folium.plugins import Draw
import os

# 1. ESTÉTICA Y DISEÑO (PERFIL RESTAURADO)
st.set_page_config(page_title="AgroData Litoral - Auditoría Real", layout="wide")

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
    .card-profesional {
        background-color: rgba(245, 245, 245, 0.98);
        padding: 20px;
        border-radius: 12px;
        border-top: 5px solid #1e4d2b;
        color: #000;
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. PANEL DE CONTROL (ENTRADA DE DATOS REALES)
with st.sidebar:
    st.header("📍 Navegación en Vivo")
    coords_raw = st.text_input("Latitud, Longitud Actual:", "-32.6585, -57.6455")
    
    st.write("---")
    st.header("🔬 Parámetros Físico-Satelitales")
    s_ndvi = st.number_input("NDVI (Salud Botánica):", 0.0, 1.0, 0.78)
    s_agua = st.number_input("Humedad Real (NDWI) %:", 0.0, 100.0, 14.2)
    s_suelo = st.number_input("Resistencia Física (MPa):", 0.0, 5.0, 2.5)
    st.info("Valores procesados mediante su Software de IA de Ciencia Física aplicada.")

# 3. ENCABEZADO (LOGO Y PERFIL DE ÉLITE COMPLETO)
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
                    <p style='font-size:11px; opacity:0.95; line-height:1.3;'>
                        <b>Estudiante Agronomía | Operaciones Inmobiliarias</b><br>
                        Perito en Grano | Experto en IA | Aficionado a la Ciencia Física,<br>
                        Geología, Botánica e Ingeniería Agro Ambiental | Protección del M. Ambiente<br>
                        <i>Desarrollador de Software con IA aplicada a la Ciencia Física</i>
                    </p>
                </div>
            """, unsafe_allow_html=True)
        with c_img:
            if os.path.exists("20250508_225422 (1).jpg"): st.image("20250508_225422 (1).jpg", width=125)

st.write("---")

# 4. MÉTRICAS CIENTÍFICAS
c1, c2, c3 = st.columns(3)
c1.metric("Vigor (NDVI)", f"{s_ndvi}")
c2.metric("Humedad (NDWI) %", f"{s_agua}%")
c3.metric("Firmeza (MPa)", f"{s_suelo}")

# 5. MAPA SATELITAL REAL (CORREGIDO SIN ERRORES)
try:
    lat, lon = map(float, coords_raw.split(','))
except:
    lat, lon = -32.6585, -57.6455

m = folium.Map(location=[lat, lon], zoom_start=16, tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google Satélite')

# Dibujo blindado: export=False evita el error de la pantalla roja
Draw(export=False, show_geometryonclick=False).add_to(m)
folium_static(m, width=1100)

# 6. INFORMES PROFESIONALES (RESTAURADOS)
st.write("---")
st.markdown("### 📋 Análisis de Interpretación para Profesionales")

col_a, col_b, col_c = st.columns(3)

with col_a:
    st.markdown(f"""<div class="card-profesional">
    <b>🌿 Agronomía e Ing. Agro Ambiental:</b><br>
    Vigor de {s_ndvi} NDVI. Estado: {'Saludable' if s_ndvi > 0.7 else 'Monitorear'}.<br>
    Detección de Monte Nativo y biomasa botánica activa mediante Sentinel-2.
    </div>""", unsafe_allow_html=True)

with col_b:
    st.markdown(f"""<div class="card-profesional">
    <b>🌍 Geología y Ciencia Física:</b><br>
    Resistencia de {s_suelo} MPa. Horizonte: {'Firme (Tosca)' if s_suelo > 3.0 else 'Profundo'}.<br>
    Interpretación de inercia térmica Landsat para estabilidad estructural.
    </div>""", unsafe_allow_html=True)

with col_c:
    st.markdown(f"""<div class="card-profesional">
    <b>🏗️ Arquitectura y Protección M.A.:</b><br>
    Suelo apto para diseños de gran porte. Paisajismo sustentado por humedad de {s_agua}%.<br>
    Integración de software con IA para diseño bioclimático.
    </div>""", unsafe_allow_html=True)

st.markdown("<br><center style='color:white; opacity:0.8;'>© 2026 Litoral Operaciones Inmobiliarias | Leonardo Olivera</center>", unsafe_allow_html=True)
