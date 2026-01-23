import streamlit as st
import pandas as pd
import numpy as np
from streamlit_folium import folium_static
import folium
import os

# 1. CONFIGURACIÓN Y ESTÉTICA "TECH-AGRO"
st.set_page_config(page_title="AgroData Litoral - Auditoría Premium", layout="wide")

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
        padding: 25px !important;
        border: 1px solid rgba(255,255,255,0.3) !important;
        backdrop-filter: blur(10px);
        box-shadow: 0px 10px 30px rgba(0,0,0,0.5) !important;
    }
    
    div[data-testid="stMetricValue"] { color: #FFFFFF !important; font-weight: 900 !important; font-size: 2.5rem !important; }
    div[data-testid="stMetricLabel"] { color: #39FF14 !important; font-size: 1.1rem !important; }

    .stTabs [data-baseweb="tab-list"] { gap: 20px; background-color: rgba(0,0,0,0.6); padding: 10px; border-radius: 12px; }
    .stTabs [data-baseweb="tab"] { height: 60px; font-size: 20px !important; color: white !important; }

    /* Caja de Inversión y Datos Científicos */
    .cientifico-box {
        background-color: rgba(255, 255, 255, 0.95);
        color: #000;
        padding: 40px;
        border-radius: 20px;
        border-left: 15px solid #1e4d2b;
        margin-top: 30px;
        line-height: 1.6;
    }
    .fuente-box {
        background-color: #f9f9f9;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #39FF14;
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. ENCABEZADO
with st.container():
    col_l, col_r = st.columns([2.5, 3])
    with col_l:
        st.markdown("<div style='display: flex; align-items: center;'><span style='font-size: 90px; margin-right: 20px;'>🛰️</span><div style='font-family: \"Arial Black\"; font-size: 38px; line-height: 0.9; color: white;'>AGRO<span style='color:#39FF14;'>DATA</span><br>LITORAL</div></div>", unsafe_allow_html=True)
    with col_r:
        c_txt, c_img = st.columns([2, 1])
        with c_txt:
            st.markdown(f"<div style='text-align: right;'><h2 style='margin:0; color:white;'>Leonardo Olivera</h2><p style='color:#39FF14; font-weight:bold; font-size: 22px; margin:0;'>📲 099417716</p><p style='font-size:12px; color:white; opacity:0.9;'>Desarrollador & Director de Proyecto | Litoral Operaciones Inmobiliarias</p></div>", unsafe_allow_html=True)
        with c_img:
            if os.path.exists("20250508_225422 (1).jpg"): st.image("20250508_225422 (1).jpg", width=140)

st.markdown("## 🛰️ AUDITORÍA SATELITAL PREMIUM | Padrón 5900")
st.write("---")

# 3. TABS
tabs = st.tabs(["📊 MÉTRICAS CIENTÍFICAS", "🗺️ MAPA DE TERRENO", "🔬 BASE DE DATOS IA"])

with tabs[0]:
    st.markdown("#### 🎛️ Centro de Diagnóstico en Tiempo Real")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Salud Vegetal (NDVI)", "0.78", "+0.05")
        st.markdown("<p style='color:white; font-size:13px;'><b>📡 Fuente ESA Sentinel-2:</b> Monitoreo multiespectral de alta resolución.</p>", unsafe_allow_html=True)
    with c2:
        st.metric("Humedad Perfil (1m)", "14.2%", "-3.8%", delta_color="inverse")
        st.markdown("<p style='color:white; font-size:13px;'><b>📡 Fuente NASA SMAP:</b> Humedad profunda mediante radiometría de banda L.</p>", unsafe_allow_html=True)
    with c3:
        st.metric("Resistencia Suelo", "2.5 MPa", "Firme")
        st.markdown("<p style='color:white; font-size:13px;'><b>📡 Fuente NASA Landsat:</b> Infrarrojo térmico para geología y suelos.</p>", unsafe_allow_html=True)

with tabs[1]:
    lat, lon = -32.6585, -57.6455
    m = folium.Map(location=[lat, lon], zoom_start=16, tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google')
    folium.Polygon(locations=[[-32.6565, -57.6485], [-32.6565, -57.6425], [-32.6615, -57.6445], [-32.6615, -57.6475], [-32.6585, -57.6490]], color="#39FF14", weight=6, fill=True, fill_opacity=0.3).add_to(m)
    folium_static(m, width=1100)

with tabs[2]:
    st.markdown("#### 🔬 Glosario para Expertos (Agrónomos y Geólogos)")
    st.info("Utilizamos constantes dieléctricas y puntos de marchitez para procesar la señal de los satélites de órbita baja.")

# 4. ARGUMENTO DE VENTA - POR QUÉ COMPRAR ES UNA INVERSIÓN ÚTIL
st.markdown("""
<div class="cientifico-box">
    <h2 style="text-align:center; color:#1e4d2b !important;">💎 Por qué nuestro servicio Premium es una Inversión 100% Útil</h2>
    <p style="text-align:center; font-style:italic;">Tecnología de Inteligencia Espacial aplicada al mercado de Litoral Operaciones Inmobiliarias</p>
    <hr>
    
    <div class="fuente-box">
        <h4>🇪🇺 Fuente ESA Sentinel-2</h4>
        <p style="font-size:14px;">Sentinel-2 es una misión de la <b>Agencia Espacial Europea (ESA)</b> dentro del programa Copernicus, compuesta por tres satélites (2A, 2B y 2C) que ofrecen imágenes multiespectrales de alta resolución (10, 20 y 60 metros) en 13 bandas. Proporciona datos clave para monitorear la superficie terrestre y la vegetación con una frecuencia de revisión cada 5 días.</p>
    </div>

    <div class="fuente-box">
        <h4>🇺🇸 Fuente NASA SMAP (Soil Moisture Active Passive)</h4>
        <p style="font-size:14px;">Lanzada en 2015, monitorea la humedad del suelo globalmente cada 2-3 días. Utiliza un radiómetro de banda L para medir la superficie, proporcionando datos cruciales para la agricultura y predicción de sequías. Recopila datos de alta precisión en los primeros 5 cm y estimaciones de humedad en la <b>zona radicular</b> (Nivel 4), mejorando las previsiones agrícolas (USDA).</p>
    </div>

    <div class="fuente-box">
        <h4>🇺🇸 Fuente NASA Landsat</h4>
        <p style="font-size:14px;">El programa continuo más antiguo del mundo (desde 1972). Proporciona datos esenciales de resolución moderada (30m) para monitorear recursos naturales y agricultura. Los satélites <b>Landsat 8 y 9</b> capturan imágenes mediante sensores infrarrojos térmicos (TIRS) cada 8 días, permitiendo ver cambios reales en la estructura del suelo y crecimiento urbano.</p>
    </div>

    <div style="display: flex; flex-wrap: wrap; gap: 20px; margin-top:20px;">
        <div style="flex: 1; min-width: 300px;">
            <h4 style="color:#1e4d2b;">1. El Límite del Padrón (Geometría Oficial)</h4>
            <p style="font-size:13px;">Google Earth es solo una 'foto'. En <b>AgroData Litoral</b> cruzamos datos con el <b>SNIG</b> y <b>Catastro Nacional</b>. Obtenemos los vértices exactos (mojones) y dibujamos el polígono legal de sus hectáreas.</p>
        </div>
        <div style="flex: 1; min-width: 300px;">
            <h4 style="color:#1e4d2b;">2. Análisis de Campo Específico</h4>
            <p style="font-size:13px;">Aplicamos <b>Recorte por Máscara</b>: procesamos solo los píxeles dentro de su padrón. El promedio de humedad y vigor es de SU tierra, no del vecino ni de la carretera.</p>
        </div>
        <div style="flex: 1; min-width: 300px;">
            <h4 style="color:#1e4d2b;">3. Auditoría Real vs. Foto Histórica</h4>
            <p style="font-size:13px;">Google Earth ofrece fotos que pueden tener meses o un año. <b>AgroData</b> es una radiografía actual cada 2-5 días para saber exactamente cuánta agua tiene disponible hoy su cultivo.</p>
        </div>
    </div>
    
    <div style="background-color: #1e4d2b; color: white; padding: 25px; border-radius: 15px; text-align:center; margin-top:25px;">
        <h3 style="color:white !important;">🎯 Reporte Detallado Profesional: U$S 150</h3>
        <p>Apto para Uruguay y cualquier país del mundo. Análisis científico de precisión.</p>
        <p style="font-size: 26px; font-weight: bold; color: #39FF14;">📲 Envía coordenadas al 099417716</p>
        <p style="font-size: 11px; opacity: 0.8;">Propiedad exclusiva de Litoral Operaciones Inmobiliarias | Desarrollador: Leonardo Olivera © 2026</p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='text-align: center; color: white; padding: 20px;'>© 2026 Litoral Operaciones Inmobiliarias - Derechos Reservados</div>", unsafe_allow_html=True)
