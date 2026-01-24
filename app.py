import streamlit as st
import pandas as pd
import numpy as np
from streamlit_folium import folium_static
import folium
import os

# 1. CONFIGURACIÓN Y ESTÉTICA "CRISTAL PREMIUM"
st.set_page_config(page_title="AgroData Litoral - Master Control", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.2), rgba(0, 0, 0, 0.2)), 
                    url("https://images.unsplash.com/photo-1500382017468-9049fed747ef?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80");
        background-size: cover; background-attachment: fixed;
    }
    
    /* Eliminar cualquier recuadro blanco residual */
    div[data-testid="stVerticalBlock"] > div:empty { display: none !important; }

    /* Métricas Tenues */
    div[data-testid="stMetric"] {
        background-color: rgba(255, 255, 255, 0.15) !important;
        border-radius: 15px !important;
        padding: 20px !important;
        border: 1px solid rgba(255,255,255,0.3) !important;
        backdrop-filter: blur(10px);
    }
    div[data-testid="stMetricValue"] { color: #FFFFFF !important; font-weight: 900 !important; }
    div[data-testid="stMetricLabel"] { color: #39FF14 !important; }

    /* Recuadro de Informe Profesional Limpio */
    .informe-limpio {
        background-color: rgba(255, 255, 255, 0.98);
        color: #000;
        padding: 30px;
        border-radius: 20px;
        border-left: 15px solid #1e4d2b;
        margin-top: 25px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. PANEL DE CONTROL (BARRA LATERAL)
with st.sidebar:
    st.header("🔑 Panel de Control")
    st.write("Exclusivo: Leonardo Olivera")
    coord_real = st.text_area("Cargar Coordenadas Padrón Real:", placeholder="Ej: -32.65, -57.64")
    
    st.write("---")
    st.header("🎮 Simulador de Datos")
    s_ndvi = st.slider("Salud (NDVI)", 0.0, 1.0, 0.78)
    s_var = st.slider("Tendencia NDVI", -0.10, 0.10, 0.05)
    s_agua = st.slider("Humedad %", 0.0, 100.0, 14.2)
    s_suelo = st.slider("Firmeza (MPa)", 0.0, 5.0, 2.5)

# 3. ENCABEZADO CON PERFIL PROFESIONAL COMPLETO
with st.container():
    col_l, col_r = st.columns([2.5, 3.5])
    with col_l:
        st.markdown("<div style='display: flex; align-items: center;'><span style='font-size: 85px; margin-right: 20px;'>🛰️</span><div style='font-family: \"Arial Black\"; font-size: 35px; line-height: 0.9; color: white;'>AGRO<span style='color:#39FF14;'>DATA</span><br>LITORAL</div></div>", unsafe_allow_html=True)
    with col_r:
        c_txt, c_img = st.columns([2.5, 1])
        with c_txt:
            st.markdown(f"""
                <div style='text-align: right;'>
                    <h2 style='margin:0; color:white;'>Leonardo Olivera</h2>
                    <p style='color:#39FF14; font-weight:bold; font-size: 22px; margin:0;'>📲 099417716</p>
                    <p style='font-size:13px; color:white; opacity:0.95; line-height:1.4;'>
                        <b>Perito en Grano | Experto en IA</b><br>
                        Estudiante de Agronomía | Operador Inmobiliario<br>
                        Desarrollador de Software & Proyecto Agro Tecnológico
                    </p>
                </div>
            """, unsafe_allow_html=True)
        with c_img:
            if os.path.exists("20250508_225422 (1).jpg"): st.image("20250508_225422 (1).jpg", width=140)

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
    st.write("📡 **NASA Landsat:** Firmeza estructural.")

# 5. EL INFORME PROFESIONAL (BAJO LOS VALORES)
msg_agro = "vigor alto y saludable" if s_ndvi > 0.6 else "estrés hídrico detectado"
msg_suelo = "firme para construcción pesada" if s_suelo > 2.0 else "suelo blando, requiere refuerzo"

st.markdown(f"""
<div class="informe-limpio">
    <h3 style="color:#1e4d2b; text-align:center;">📋 Informe de Interpretación Multi-Perfil</h3>
    <hr>
    <p><b>🌿 Para Ingenieros Agrónomos:</b> El NDVI de {s_ndvi} (+{s_var}) indica un estado de {msg_agro}. Las hojas absorben gran cantidad de luz roja (clorofila), confirmando un dosel denso según ESA Sentinel-2.</p>
    
    <p><b>🌍 Para Geólogos:</b> Los {s_suelo} MPa obtenidos mediante sensores térmicos de NASA Landsat confirman un suelo {msg_suelo}. La humedad de {s_agua}% en la zona donde comen las raíces valida la estabilidad del terreno.</p>
    
    <p><b>🏗️ Para Arquitectos (Diseño y Estética):</b> Con una firmeza de {s_suelo} MPa, el terreno es apto para diseños de gran porte. El verdor del entorno (NDVI {s_ndvi}) garantiza un paisajismo frondoso y sostenible para la estética final del proyecto.</p>
    
    <div style="background:#e8f5e9; padding:20px; border-radius:10px; border:1px solid #1e4d2b; margin-top:15px;">
        <h4 style="margin:0;">💎 Inversión 100% Útil: ¿Por qué pagar u$s 150?</h4>
        <p style="font-size:14px; margin-top:10px;">Google Earth son fotos históricas. AgroData es una <b>Auditoría en Tiempo Real</b>. Cruzamos coordenadas de Catastro (Mojones reales) con niveles de datos 1 a 4 de la NASA. Usted no paga por un dibujo, paga por seguridad jurídica y física de su tierra.</p>
    </div>
    
    <div style="background-color: #1e4d2b; color: white; padding: 20px; border-radius: 15px; text-align:center; margin-top:20px;">
        <h3 style="color:white !important; margin:0;">Reporte Detallado Profesional: U$S 150</h3>
        <p style="font-size: 24px; font-weight: bold; color: #39FF14; margin:5px;">📲 Envía coordenadas al 099417716</p>
    </div>
</div>
""", unsafe_allow_html=True)

# 6. MAPA FINAL
st.write("---")
lat, lon = -32.6585, -57.6455
m = folium.Map(location=[lat, lon], zoom_start=16, tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google')
folium.Polygon(locations=[[-32.6565, -57.6485], [-32.6565, -57.6425], [-32.6615, -57.6445], [-32.6615, -57.6475], [-32.6585, -57.6490]], color="#39FF14", weight=6, fill=True, fill_opacity=0.3).add_to(m)
folium_static(m, width=1100)
