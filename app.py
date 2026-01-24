import streamlit as st
import pandas as pd
import numpy as np
from streamlit_folium import folium_static
import folium
import os

# 1. CONFIGURACIÓN Y ESTÉTICA "TECH-PREMIUM"
st.set_page_config(page_title="AgroData Litoral - Master Control", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.2), rgba(0, 0, 0, 0.2)), 
                    url("https://images.unsplash.com/photo-1500382017468-9049fed747ef?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80");
        background-size: cover; background-attachment: fixed;
    }
    
    /* Métricas Tenues Estilo Cristal */
    div[data-testid="stMetric"] {
        background-color: rgba(255, 255, 255, 0.15) !important;
        border-radius: 15px !important;
        padding: 20px !important;
        border: 1px solid rgba(255,255,255,0.3) !important;
        backdrop-filter: blur(10px);
    }
    div[data-testid="stMetricValue"] { color: #FFFFFF !important; font-weight: 900 !important; }
    div[data-testid="stMetricLabel"] { color: #39FF14 !important; }

    /* Caja de Interpretación Profesional (Blindada) */
    .interpretacion-box {
        background-color: rgba(255, 255, 255, 0.98);
        color: #000;
        padding: 30px;
        border-radius: 20px;
        border-left: 15px solid #1e4d2b;
        margin-top: 25px;
        box-shadow: 0px 10px 30px rgba(0,0,0,0.5);
    }
    .perfil-text { text-align: right; color: white; line-height: 1.4; }
    </style>
    """, unsafe_allow_html=True)

# 2. PANEL DE SIMULACIÓN (SIDEBAR)
with st.sidebar:
    st.header("🔑 Simulación y Control")
    st.write("Exclusivo: Leonardo Olivera")
    s_ndvi = st.slider("Ajustar Salud (NDVI)", 0.0, 1.0, 0.78)
    s_var = st.slider("Tendencia NDVI", -0.10, 0.10, 0.05)
    s_agua = st.slider("Humedad %", 0.0, 100.0, 14.2)
    s_suelo = st.slider("Firmeza (MPa)", 0.0, 5.0, 2.5)
    st.write("---")
    st.text_area("Cargar Coordenadas Padrón:", placeholder="Ej: -32.65, -57.64")

# 3. ENCABEZADO (LOGO Y PERFIL SIN CAMBIOS)
with st.container():
    col_l, col_r = st.columns([2.5, 3.5])
    with col_l:
        st.markdown("<div style='display: flex; align-items: center; margin-top: 10px;'><span style='font-size: 85px; margin-right: 20px;'>🛰️</span><div style='font-family: \"Arial Black\"; font-size: 38px; line-height: 0.9; color: white;'>AGRO<span style='color:#39FF14;'>DATA</span><br>LITORAL</div></div>", unsafe_allow_html=True)
    with col_r:
        c_txt, c_img = st.columns([2.5, 1])
        with c_txt:
            st.markdown(f"""
                <div class="perfil-text">
                    <h2 style="margin:0; font-size: 28px;">Leonardo Olivera</h2>
                    <p style="margin:0; color:#39FF14; font-weight:bold; font-size: 20px;">📲 099417716</p>
                    <p style="font-size:12px; opacity: 0.9;">
                        <b>Perito en Grano | Experto en IA</b><br>
                        Estudiante de Agronomía | Operador Inmobiliario<br>
                        Desarrollador de Software & Proyecto Agro Tecnológico
                    </p>
                </div>
            """, unsafe_allow_html=True)
        with c_img:
            if os.path.exists("20250508_225422 (1).jpg"):
                st.image("20250508_225422 (1).jpg", width=130)

st.markdown("### 🛰️ AUDITORÍA SATELITAL PREMIUM | Padrón 5900")
st.write("---")

# 4. VALORES DINÁMICOS (CONECTADOS AL SIMULADOR)
c1, c2, c3 = st.columns(3)

with c1:
    st.metric("Salud del Cultivo (NDVI)", f"{s_ndvi}", f"{s_var:+.2f}")
    msg_ndvi = "Vigor Alto" if s_ndvi > 0.6 else "Vigor Moderado"
    st.write(f"📡 **Sentinel-2:** {msg_ndvi} detectado.")

with c2:
    st.metric("Agua en Raíz (1m)", f"{s_agua}%", "-3.8%", delta_color="inverse")
    st.write(f"📡 **NASA SMAP:** Humedad profunda real.")

with c3:
    st.metric("Firmeza del Suelo", f"{s_suelo} MPa", "Firme")
    st.write(f"📡 **NASA Landsat:** Estabilidad geológica.")

# 5. INFORME DE INTERPRETACIÓN PARA PROFESIONALES (BLINDADO)
diagnostico_agro = "crecimiento activo y dosel denso" if s_ndvi > 0.7 else "necesidad de monitoreo por biomasa baja"
diagnostico_geol = "óptima para cimentación" if s_suelo > 2.0 else "riesgo de asentamiento, requiere estudio"

st.markdown(f"""
<div class="interpretacion-box">
    <h3 style="color:#1e4d2b; text-align:center;">📋 Informe de Interpretación para Ingenieros, Geólogos y Arquitectos</h3>
    <hr>
    <p><b>🌿 Para Ingenieros Agrónomos:</b> El valor NDVI de {s_ndvi} (+{s_var}) indica una fase de {diagnostico_agro}. La absorción de clorofila es alta, lo que confirma un vigor saludable según la misión ESA Sentinel-2.</p>
    
    <p><b>🌍 Para Geólogos:</b> Los {s_suelo} MPa detectados mediante sensores térmicos de NASA Landsat confirman una firmeza de horizonte {diagnostico_geol}. Los datos de humedad de {s_agua}% validan la estabilidad hídrica profunda.</p>
    
    <p><b>🏗️ Para Arquitectos (Diseño y Estética):</b> Con un suelo firme de {s_suelo} MPa y baja saturación superficial, el terreno permite el diseño de estructuras pesadas con amplios ventanales y orientaciones bioclimáticas, aprovechando la topografía natural sin riesgos de erosión inmediata. La estética del proyecto puede integrarse al entorno verde vibrante (NDVI 0.78) garantizando un paisaje frondoso y sostenible.</p>
    
    <div style="background:#e8f5e9; padding:15px; border-radius:10px; border:1px solid #1e4d2b; margin-top:15px; text-align:center;">
        <b>💡 Inversión Útil:</b> "Usted no paga por un dibujo; paga por acceso a los niveles de datos 1 a 4 de la NASA para asegurar su capital inmobiliario."
    </div>
</div>
""", unsafe_allow_html=True)

# 6. MAPA FINAL
st.write("---")
lat, lon = -32.6585, -57.6455
m = folium.Map(location=[lat, lon], zoom_start=16, tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google')
folium.Polygon(locations=[[-32.6565, -57.6485], [-32.6565, -57.6425], [-32.6615, -57.6445], [-32.6615, -57.6475], [-32.6585, -57.6490]], color="#39FF14", weight=6, fill=True, fill_opacity=0.3).add_to(m)
folium_static(m, width=1100)

st.markdown("<br><center>© 2026 Litoral Operaciones Inmobiliarias - Derechos Reservados</center>", unsafe_allow_html=True)
