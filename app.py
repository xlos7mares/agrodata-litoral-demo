import streamlit as st
import pandas as pd
import numpy as np
from streamlit_folium import folium_static
import folium
from folium.plugins import Draw
import os

# 1. CONFIGURACIÓN Y ESTÉTICA (CON CONTRASTE MEJORADO)
st.set_page_config(page_title="AgroData Litoral - Auditoría Real", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), 
                    url("https://images.unsplash.com/photo-1500382017468-9049fed747ef?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80");
        background-size: cover; background-attachment: fixed;
    }
    /* Métricas con fondo oscuro para máxima visibilidad */
    div[data-testid="stMetric"] {
        background-color: rgba(0, 0, 0, 0.7) !important;
        border-radius: 15px !important;
        padding: 20px !important;
        border: 1px solid #39FF14 !important;
    }
    div[data-testid="stMetricValue"] { color: #39FF14 !important; font-weight: 900 !important; }
    div[data-testid="stMetricLabel"] { color: #FFFFFF !important; }

    /* Tarjetas Profesionales Prolijas */
    .card-profesional {
        background-color: rgba(255, 255, 255, 0.98);
        padding: 20px;
        border-radius: 12px;
        border-top: 5px solid #1e4d2b;
        color: #000;
        margin-bottom: 20px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.5);
    }
    .badge-satelite {
        background-color: #1e4d2b;
        color: #39FF14;
        padding: 5px 10px;
        border-radius: 20px;
        font-size: 10px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. PANEL DE CONTROL (SLIDERS Y COORDENADAS)
with st.sidebar:
    st.header("📍 Ubicación Real")
    coords_raw = st.text_input("Latitud, Longitud:", "-32.6585, -57.6455")
    
    st.write("---")
    st.header("🎮 Simulador Satelital")
    st.write("Ajuste para demostrar variaciones técnicas:")
    s_ndvi = st.slider("Salud / Monte (NDVI)", 0.0, 1.0, 0.78)
    s_agua = st.slider("Humedad / NDWI %", 0.0, 100.0, 14.2)
    s_suelo = st.slider("Firmeza / MPa", 0.0, 5.0, 2.5)
    
    st.write("---")
    if st.button("📥 Descargar Informe DEMO"):
        st.success("Generando vista previa del informe...")

# 3. ENCABEZADO (PERFIL DE ÉLITE REORGANIZADO)
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
                    <p style='color:#39FF14; font-weight:bold; font-size: 18px; margin:0;'>📲 099417716</p>
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

# 4. MÉTRICAS CON DATOS DE ACTUALIZACIÓN SATELITAL
c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Vigor Vegetal (NDVI)", s_ndvi)
    st.markdown("<span class='badge-satelite'>🛰️ ESA Sentinel-2: Cada 5 días</span>", unsafe_allow_html=True)
with c2:
    st.metric("Humedad Profunda %", f"{s_agua}%")
    st.markdown("<span class='badge-satelite'>🛰️ NASA SMAP: Cada 3 días</span>", unsafe_allow_html=True)
with c3:
    st.metric("Resistencia (MPa)", f"{s_suelo}")
    st.markdown("<span class='badge-satelite'>🛰️ NASA Landsat: Cada 8 días</span>", unsafe_allow_html=True)

# 5. MAPA SATELITAL REAL (SIN ERRORES)
try:
    lat, lon = map(float, coords_raw.split(','))
except:
    lat, lon = -32.6585, -57.6455

st.markdown("#### 🗺️ Explorador Satelital en Tiempo Real (Google Satélite)")
m = folium.Map(location=[lat, lon], zoom_start=16, tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google')
Draw(export=False, show_geometryonclick=False).add_to(m)
folium_static(m, width=1100)

# 6. CUADROS PROFESIONALES CON LÓGICA TÉCNICA
st.write("---")
col_a, col_b, col_c = st.columns(3)

with col_a:
    st.markdown(f"""<div class="card-profesional">
    <h4>🌿 Agronomía e IA</h4>
    <b>Detección:</b> {'Monte Nativo / Reserva' if s_ndvi > 0.72 else 'Pastura Estacional'}.<br>
    <b>Info Técnica:</b> Análisis de biomasa activa para cría o plantación. Identificación de vegetación perenne protegida.
    </div>""", unsafe_allow_html=True)

with col_b:
    st.markdown(f"""<div class="card-profesional">
    <h4>🌍 Geología y Física</h4>
    <b>Firmeza:</b> {s_suelo} MPa ({'Tosca détectada' if s_suelo > 3.0 else 'Suelo profundo'}).<br>
    <b>Ingeniería:</b> Apto para cimentación de silos, galpones o viviendas de gran porte.
    </div>""", unsafe_allow_html=True)

with col_c:
    st.markdown(f"""<div class="card-profesional">
    <h4>🏗️ Arq. y Medio Ambiente</h4>
    <b>Recurso:</b> {'Agua superficial activa' if s_agua > 25 else 'Suelo seco / estable'}.<br>
    <b>Diseño:</b> Integración paisajística basada en micro-arroyos y protección ambiental.
    </div>""", unsafe_allow_html=True)

# 7. SERVICIOS PROFESIONALES
st.markdown(f"""
<div style="background-color: #1e4d2b; color: white; padding: 30px; border-radius: 15px; text-align:center; margin-top:20px;">
    <h2 style="color:white !important;">💼 Informe Profesional Completo: U$S 150</h2>
    <p style="font-size: 18px; color: #39FF14;">Incluye Estudio Hídrico Histórico (20 años) e Inercia Térmica de Suelos.</p>
    <p>Envíe coordenadas al <b>099417716</b> para habilitar el escaneo de profundidad.</p>
</div>
""", unsafe_allow_html=True)
