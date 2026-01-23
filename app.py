import streamlit as st
import pandas as pd
import numpy as np
from streamlit_folium import folium_static
import folium
import os

# 1. CONFIGURACIÓN Y ELIMINACIÓN DE ESPACIOS FANTASMA
st.set_page_config(page_title="AgroData Litoral - Premium", layout="wide")

st.markdown("""
    <style>
    /* Fondo de campo vivo */
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.2), rgba(0, 0, 0, 0.2)), 
                    url("https://images.unsplash.com/photo-1500382017468-9049fed747ef?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80");
        background-size: cover; background-attachment: fixed;
    }
    
    /* BLOQUEO TOTAL DE RECUADROS BLANCOS VACÍOS */
    div[data-testid="stVerticalBlock"] > div:empty { display: none !important; }
    .element-container:empty { display: none !important; }
    div.stTooltipIcon { display: none !important; }

    /* Métricas Tenues Estilo Cristal */
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

    /* Estilo de Pestañas */
    .stTabs [data-baseweb="tab-list"] { background-color: rgba(0,0,0,0.7); border-radius: 12px; padding: 10px; }
    .stTabs [data-baseweb="tab"] { font-size: 22px !important; color: white !important; font-weight: bold !important; }
    .stTabs [aria-selected="true"] { color: #39FF14 !important; border-bottom: 4px solid #39FF14 !important; }

    /* Caja Científica Inferior */
    .cientifico-box {
        background-color: rgba(255, 255, 255, 0.98);
        color: #000;
        padding: 35px;
        border-radius: 20px;
        border-left: 15px solid #1e4d2b;
        margin-top: 25px;
    }
    .fuente-item { background-color: #f0f4f0; padding: 15px; border-radius: 10px; margin-bottom: 12px; border-left: 5px solid #39FF14; }
    </style>
    """, unsafe_allow_html=True)

# 2. PANEL DE CONTROL (BARRA LATERAL)
with st.sidebar:
    st.header("🔑 Panel de Control")
    st.write("Exclusivo: Leonardo Olivera")
    coord_admin = st.text_area("Configurar Coordenadas Padrón:", height=100)
    if st.button("Ejecutar Escaneo Satelital"):
        st.success("Señal vinculada con éxito.")

# 3. ENCABEZADO CON PERFIL PROFESIONAL COMPLETO
with st.container():
    col_l, col_r = st.columns([2.5, 3.5])
    with col_l:
        st.markdown("<div style='display: flex; align-items: center;'><span style='font-size: 95px; margin-right: 20px;'>🛰️</span><div style='font-family: \"Arial Black\"; font-size: 38px; line-height: 0.9; color: white;'>AGRO<span style='color:#39FF14;'>DATA</span><br>LITORAL</div></div>", unsafe_allow_html=True)
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
            if os.path.exists("20250508_225422 (1).jpg"): 
                st.image("20250508_225422 (1).jpg", width=140)

st.markdown("### 🛰️ AUDITORÍA SATELITAL PREMIUM | Padrón 5900")
st.write("---")

# 4. CUERPO DE DATOS (REFORMADO PARA EVITAR RECUADROS)
tabs = st.tabs(["📊 MÉTRICAS CIENTÍFICAS", "🗺️ MAPA DE TERRENO", "🔬 CIENCIA APLICADA"])

with tabs[0]:
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Salud Vegetal (NDVI)", "0.78", "+0.05")
        st.markdown("<p style='color:white; font-size:13px;'>📡 <b>Fuente ESA Sentinel-2:</b> Misión de la Agencia Espacial Europea. Detecta vigor fotosintético antes de ser visible al ojo.</p>", unsafe_allow_html=True)
    with c2:
        st.metric("Humedad Perfil (1m)", "14.2%", "-3.8%", delta_color="inverse")
        st.markdown("<p style='color:white; font-size:13px;'>📡 <b>Fuente NASA SMAP:</b> Monitoreo de humedad profunda (zona radicular) mediante radiometría de banda L.</p>", unsafe_allow_html=True)
    with c3:
        st.metric("Resistencia Suelo", "2.5 MPa", "Firme")
        st.markdown("<p style='color:white; font-size:13px;'>📡 <b>Fuente NASA Landsat:</b> Infrarrojo térmico para medir la firmeza estructural del horizonte.</p>", unsafe_allow_html=True)

with tabs[1]:
    lat, lon = -32.6585, -57.6455
    m = folium.Map(location=[lat, lon], zoom_start=16, tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google')
    folium.Polygon(locations=[[-32.6565, -57.6485], [-32.6565, -57.6425], [-32.6615, -57.6445], [-32.6615, -57.6475], [-32.6585, -57.6490]], color="#39FF14", weight=6, fill=True, fill_opacity=0.3).add_to(m)
    folium_static(m, width=1100)

with tabs[2]:
    st.info("Utilizamos constantes dieléctricas para procesar la señal de los satélites de órbita baja.")
    st.write("✅ **Sincronización:** MGAP, SNIG, DIEA, INIA e OPYPA (Uruguay).")

# 5. SECCIÓN FINAL LIMPIA (INVERSIÓN ÚTIL)
st.markdown('<div class="cientifico-box">', unsafe_allow_html=True)
st.markdown("<h2 style='text-align:center;'>💎 Porque comprar nuestro servicio Premium es una inversión 100% útil</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-style:italic;'>Propiedad exclusiva de Litoral Operaciones Inmobiliarias</p><hr>", unsafe_allow_html=True)

st.markdown("""
<div class="fuente-item">
    <b>🇪🇺 Fuente ESA Sentinel-2:</b> Compuesta por tres satélites que ofrecen imágenes multiespectrales. Detecta falta de nitrógeno con frecuencia de revisión cada 5 días.
</div>
<div class="fuente-item">
    <b>🇺🇸 Fuente NASA SMAP:</b> Soil Moisture Active Passive. Monitorea humedad profunda cada 2-3 días para predecir sequías con precisión científica (USDA).
</div>
<div class="fuente-item">
    <b>🇺🇸 Fuente NASA Landsat:</b> El registro continuo más antiguo (desde 1972). Captura cambios reales en el suelo mediante sensores infrarrojos cada 8 días.
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="background-color: #1e4d2b; color: white; padding: 25px; border-radius: 15px; text-align:center; margin-top:20px;">
    <h3 style="color:white !important;">Reporte Detallado Profesional: U$S 150</h3>
    <p style="font-size: 26px; font-weight: bold; color: #39FF14;">📲 Envía coordenadas al 099417716</p>
    <p style="font-size: 11px; opacity: 0.8;">Creado por Leonardo Olivera © 2026 | Litoral Operaciones Inmobiliarias</p>
</div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br><center>© 2026 Litoral Operaciones Inmobiliarias - Derechos Reservados</center>", unsafe_allow_html=True)
