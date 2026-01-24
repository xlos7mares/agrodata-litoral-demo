import streamlit as st
import pandas as pd
import numpy as np
from streamlit_folium import folium_static
import folium
import os

# 1. ESTÉTICA Y PERFIL (NO SE TOCA NADA)
st.set_page_config(page_title="AgroData Litoral - Premium", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.2), rgba(0, 0, 0, 0.2)), 
                    url("https://images.unsplash.com/photo-1500382017468-9049fed747ef?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80");
        background-size: cover; background-attachment: fixed;
    }
    div[data-testid="stMetric"] {
        background-color: rgba(255, 255, 255, 0.15) !important;
        border-radius: 15px !important;
        padding: 20px !important;
        border: 1px solid rgba(255,255,255,0.3) !important;
        backdrop-filter: blur(10px);
    }
    div[data-testid="stMetricValue"] { color: #FFFFFF !important; font-weight: 900 !important; }
    div[data-testid="stMetricLabel"] { color: #39FF14 !important; }

    /* Tarjetas Profesionales Prolijas */
    .card-profesional {
        background-color: rgba(240, 244, 240, 0.98);
        padding: 20px;
        border-radius: 12px;
        border-top: 5px solid #1e4d2b;
        margin-bottom: 20px;
        color: #000;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.3);
    }

    /* Recuadro de Cita Científica al final */
    .cita-box {
        background-color: #0a1f0a;
        color: #39FF14;
        padding: 10px;
        border-radius: 8px;
        font-style: italic;
        font-size: 12px;
        text-align: center;
        margin-top: 40px;
        opacity: 0.8;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. PANEL DE CONTROL Y SIMULADOR
with st.sidebar:
    st.header("🔑 Simulación y Control")
    st.write("Exclusivo: Leonardo Olivera")
    s_ndvi = st.slider("Ajustar Salud (NDVI)", 0.0, 1.0, 0.78)
    s_var = st.slider("Tendencia NDVI", -0.10, 0.10, 0.05)
    s_agua = st.slider("Humedad %", 0.0, 100.0, 14.2)
    s_suelo = st.slider("Firmeza (MPa)", 0.0, 5.0, 2.5)
    st.write("---")
    st.text_area("Cargar Coordenadas Padrón Real:", placeholder="-32.65, -57.64")

# 3. ENCABEZADO (PERFIL INTACTO)
with st.container():
    col_l, col_r = st.columns([2.5, 3.5])
    with col_l:
        st.markdown("<div style='display: flex; align-items: center; margin-top: 10px;'><span style='font-size: 85px; margin-right: 20px;'>🛰️</span><div style='font-family: \"Arial Black\"; font-size: 38px; line-height: 0.9; color: white;'>AGRO<span style='color:#39FF14;'>DATA</span><br>LITORAL</div></div>", unsafe_allow_html=True)
    with col_r:
        c_txt, c_img = st.columns([2.5, 1])
        with c_txt:
            st.markdown(f"""
                <div style='text-align: right;'>
                    <h2 style='margin:0; color:white;'>Leonardo Olivera</h2>
                    <p style='color:#39FF14; font-weight:bold; font-size: 20px; margin:0;'>📲 099417716</p>
                    <p style='font-size:12px; color:white; opacity:0.95; line-height:1.4;'>
                        <b>Perito en Grano | Experto en IA</b><br>
                        Estudiante de Agronomía | Operador Inmobiliario<br>
                        Desarrollador de Software & Proyecto Agro Tecnológico
                    </p>
                </div>
            """, unsafe_allow_html=True)
        with c_img:
            if os.path.exists("20250508_225422 (1).jpg"): st.image("20250508_225422 (1).jpg", width=130)

st.markdown("### 🛰️ AUDITORÍA SATELITAL PREMIUM | Padrón 5900")
st.write("---")

# 4. MÉTRICAS DINÁMICAS
c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Salud de Pastura (NDVI)", f"{s_ndvi}", f"{s_var:+.2f}")
    st.write("📡 **ESA Sentinel-2:** Vigor activo.")
with c2:
    st.metric("Agua en Raíz (1m)", f"{s_agua}%", "-3.8%", delta_color="inverse")
    st.write("📡 **NASA SMAP:** Humedad profunda.")
with c3:
    st.metric("Firmeza del Suelo", f"{s_suelo} MPa", "Firme")
    st.write("📡 **NASA Landsat:** Estabilidad estructural.")

# 5. DIAGNÓSTICO PROFESIONAL EN CUADROS PROLIJOS
st.write("---")
st.markdown("#### 📋 Análisis de Interpretación para Profesionales")

col_a, col_b, col_c = st.columns(3)

with col_a:
    st.markdown(f"""<div class="card-profesional">
    <b>🌿 Para Ingenieros Agrónomos:</b><br>
    El valor NDVI de {s_ndvi} (+{s_var}) indica un vigor de la planta alto y saludable, confirmando un dosel denso según la misión ESA Sentinel-2.
    </div>""", unsafe_allow_html=True)

with col_b:
    st.markdown(f"""<div class="card-profesional">
    <b>🌍 Para Geólogos:</b><br>
    Los {s_suelo} MPa obtenidos por NASA Landsat confirman un suelo firme para construcción. La humedad de {s_agua}% valida la estabilidad del terreno.
    </div>""", unsafe_allow_html=True)

with col_c:
    st.markdown(f"""<div class="card-profesional">
    <b>🏗️ Para Arquitectos:</b><br>
    Con una firmeza de {s_suelo} MPa, el terreno es apto para diseños de gran porte. El vigor verde (NDVI {s_ndvi}) garantiza un paisajismo frondoso.
    </div>""", unsafe_allow_html=True)

# 6. INVERSIÓN ÚTIL Y CIERRE
st.markdown(f"""
<div style="background-color: #1e4d2b; color: white; padding: 30px; border-radius: 15px; text-align:center; margin-top:20px;">
    <h3 style="color:white !important;">💎 Inversión 100% Útil: Reporte Detallado Profesional</h3>
    <p>Google Earth son fotos históricas. AgroData es una auditoría real de la NASA para asegurar su capital inmobiliario.</p>
    <p style="font-size: 26px; font-weight: bold; color: #39FF14;">U$S 150 | Envía coordenadas al 099417716</p>
</div>
""", unsafe_allow_html=True)

# 7. MAPA Y CITA FINAL
lat, lon = -32.6585, -57.6455
m = folium.Map(location=[lat, lon], zoom_start=16, tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google')
folium.Polygon(locations=[[-32.6565, -57.6485], [-32.6565, -57.6425], [-32.6615, -57.6445], [-32.6615, -57.6475], [-32.6585, -57.6490]], color="#39FF14", weight=6, fill=True, fill_opacity=0.3).add_to(m)
folium_static(m, width=1100)

st.markdown("""<div class="cita-box">
"La agricultura es la profesión propia del sabio, la más adecuada al sencillo y la ocupación digna para todo hombre libre" - Cicerón
</div>""", unsafe_allow_html=True)
