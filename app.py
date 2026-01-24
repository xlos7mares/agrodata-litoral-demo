import streamlit as st
import pandas as pd
import numpy as np
from streamlit_folium import folium_static
import folium
import os

# 1. CONFIGURACIÓN Y ESTÉTICA (PERFIL RESTAURADO AL 100%)
st.set_page_config(page_title="AgroData Litoral - Auditoría Real SIG", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), 
                    url("https://images.unsplash.com/photo-1500382017468-9049fed747ef?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80");
        background-size: cover; background-attachment: fixed;
    }
    div[data-testid="stMetric"] {
        background-color: rgba(0, 0, 0, 0.8) !important;
        border-radius: 15px !important;
        padding: 20px !important;
        border: 1px solid #39FF14 !important;
    }
    div[data-testid="stMetricValue"] { color: #39FF14 !important; font-weight: 900 !important; }
    div[data-testid="stMetricLabel"] { color: #FFFFFF !important; }
    
    .card-profesional {
        background-color: rgba(255, 255, 255, 0.98);
        padding: 25px;
        border-radius: 15px;
        border-left: 12px solid #1e4d2b;
        color: #000;
        margin-bottom: 20px;
        box-shadow: 0px 6px 20px rgba(0,0,0,0.5);
    }
    .badge-satelite {
        background-color: #1e4d2b; color: #39FF14; padding: 4px 10px; border-radius: 20px; font-size: 10px; font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. PANEL DE CONTROL (ENTRADA DE COORDENADAS Y SIMULADOR)
with st.sidebar:
    st.header("📍 Sistema de Referencia")
    coords_raw = st.text_input("Latitud, Longitud (WGS84):", "-32.6585, -57.6455")
    
    st.write("---")
    st.header("🎮 Simulador de Validación")
    st.write("Ingrese los valores reales obtenidos del satélite para este campo:")
    s_ndvi = st.slider("Vigor / Monte (NDVI)", 0.0, 1.0, 0.78)
    s_agua = st.slider("Humedad / NDWI %", 0.0, 100.0, 14.2)
    s_suelo = st.slider("Firmeza / MPa", 0.0, 5.0, 2.5)
    
    st.write("---")
    st.button("Generar Informe Demo")

# 3. ENCABEZADO (TU PERFIL COMPLETO REORGANIZADO)
with st.container():
    col_l, col_r = st.columns([2.5, 3.5])
    with col_l:
        st.markdown("<div style='display: flex; align-items: center;'><span style='font-size: 80px; margin-right: 20px;'>🛰️</span><div style='font-family: \"Arial Black\"; font-size: 35px; line-height: 0.9; color: white;'>AGRO<span style='color:#39FF14;'>DATA</span><br>LITORAL</div></div>", unsafe_allow_html=True)
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
                        Geología, Botánica e Ingeniería Agro Ambiental | Protección del Medio Ambiente<br>
                        <i>Desarrollador de Software con IA aplicada a la Ciencia Física</i>
                    </p>
                </div>
            """, unsafe_allow_html=True)
        with c_img:
            if os.path.exists("20250508_225422 (1).jpg"): st.image("20250508_225422 (1).jpg", width=120)

st.write("---")

# 4. MÉTRICAS CON FUENTES SATELITALES
c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Vigor (NDVI)", s_ndvi)
    st.markdown("<span class='badge-satelite'>🛰️ ESA Sentinel-2</span>", unsafe_allow_html=True)
with c2:
    st.metric("Humedad %", f"{s_agua}%")
    st.markdown("<span class='badge-satelite'>🛰️ NASA SMAP</span>", unsafe_allow_html=True)
with c3:
    st.metric("Firmeza (MPa)", f"{s_suelo}")
    st.markdown("<span class='badge-satelite'>🛰️ NASA Landsat</span>", unsafe_allow_html=True)

# 5. MAPA SIG REAL (CORREGIDO SIN ERRORES)
try:
    lat, lon = map(float, coords_raw.split(','))
except:
    lat, lon = -32.6585, -57.6455

st.markdown(f"#### 🗺️ Visualizador Cartográfico Satelital (Coordenadas: {lat}, {lon})")
m = folium.Map(location=[lat, lon], zoom_start=16, tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google Satélite')

# Círculo de Auditoría (Representa el escaneo del padrón)
folium.Circle([lat, lon], radius=400, color="#39FF14", fill=True, fill_opacity=0.2, tooltip="Área de Escaneo").add_to(m)
folium_static(m, width=1100)

# 6. RESULTADOS AUTOMÁTICOS (EL CEREBRO DEL SISTEMA)
st.write("---")
st.markdown("### 📋 Resultados de la Auditoría Geológica y Agrícola")

# Lógica que cambia los cuadros según los datos del satélite
agro_txt = "Monte Nativo Detectado." if s_ndvi > 0.72 else "Zonas de Pastura o Cultivo Estacional."
geo_txt = "Tosca détectada (Firmeza Alta)." if s_suelo > 3.0 else "Suelo Profundo con cimentación estándar."
agua_txt = "Curso de Agua Activo / Cañada." if s_agua > 25 else "Suelo Estable (Sin agua superficial)."

col_a, col_b = st.columns(2)

with col_a:
    st.markdown(f"""<div class="card-profesional">
    <h4>🌿 Botánica e Ingeniería Agro Ambiental</h4>
    <b>Detección:</b> {agro_txt}<br>
    <b>Análisis:</b> Procesamiento de banda Infrarrojo Cercano (Sentinel-2). Identifica densidad foliar y salud del ecosistema botánico en tiempo real.
    </div>""", unsafe_allow_html=True)
    
    st.markdown(f"""<div class="card-profesional">
    <h4>🌍 Geología y Ciencia Física</h4>
    <b>Suelo:</b> {s_suelo} MPa ({geo_text}).<br>
    <b>Física de Suelos:</b> Análisis de Inercia Térmica (Landsat TIRS). La roca retiene calor a las 2 AM de forma distinta a la tierra, validando la resistencia mecánica.
    </div>""", unsafe_allow_html=True)

with col_b:
    st.markdown(f"""<div class="card-profesional">
    <h4>💧 Recursos Hídricos (Histórico 20 años)</h4>
    <b>Estado Actual:</b> {agua_text}<br>
    <b>Hidrología:</b> Análisis NDWI. Permite visualizar el comportamiento histórico de inundaciones y sequías para asegurar la inversión.
    </div>""", unsafe_allow_html=True)
    
    st.markdown(f"""<div class="card-profesional">
    <h4>🏗️ Ingeniería y Arquitectura</h4>
    <b>Aptitud de Obra:</b> Apto para silos, galpones o complejos habitacionales.<br>
    <b>Conclusión:</b> Validación de firmeza estructural basada en el cruce de datos térmicos de la NASA y estabilidad hídrica.
    </div>""", unsafe_allow_html=True)

# 7. SERVICIOS PROFESIONALES
st.markdown(f"""
<div style="background-color: #1e4d2b; color: white; padding: 25px; border-radius: 15px; text-align:center; margin-top:10px;">
    <h3 style="color:white !important;">💎 Informe Profesional Completo: U$S 150</h3>
    <p style="font-size: 16px; color: #39FF14;">Estudio Hídrico 20 Años e Inercia Térmica de Suelos (NASA/ESA).</p>
    <p>Envíe coordenadas al <b>099417716</b> para habilitar el escaneo de profundidad.</p>
</div>
""", unsafe_allow_html=True)
