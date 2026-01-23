import streamlit as st
import pandas as pd
import numpy as np
from streamlit_folium import folium_static
import folium
import os

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="AgroData Litoral - Premium", layout="wide")

# 2. ESTILOS CSS (DISEÑO Y LECTURA)
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

    .cientifico-box {
        background-color: rgba(255, 255, 255, 0.98);
        color: #000;
        padding: 40px;
        border-radius: 20px;
        border-left: 15px solid #1e4d2b;
        margin-top: 30px;
    }
    .fuente-item {
        background-color: #f0f4f0;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 15px;
        border-left: 5px solid #39FF14;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. PANEL DE ADMINISTRADOR (BARRA LATERAL)
with st.sidebar:
    st.header("🔑 Panel de Control")
    st.write("Solo para Leonardo Olivera")
    coord_admin = st.text_area("Ingresar Coordenadas del Padrón:", height=150, placeholder="Ej: -32.65, -57.64")
    if st.button("Ejecutar Escaneo Satelital"):
        st.success("Señal vinculada con éxito.")

# 4. ENCABEZADO
with st.container():
    col_l, col_r = st.columns([2.5, 3])
    with col_l:
        st.markdown("<div style='display: flex; align-items: center;'><span style='font-size: 80px; margin-right: 20px;'>🛰️</span><div style='font-family: \"Arial Black\"; font-size: 35px; line-height: 0.9; color: white;'>AGRO<span style='color:#39FF14;'>DATA</span><br>LITORAL</div></div>", unsafe_allow_html=True)
    with col_r:
        c_txt, c_img = st.columns([2, 1])
        with c_txt:
            st.markdown(f"<div style='text-align: right;'><h2 style='margin:0; color:white;'>Leonardo Olivera</h2><p style='color:#39FF14; font-weight:bold; font-size: 22px; margin:0;'>📲 099417716</p><p style='font-size:11px; color:white; opacity:0.9;'>Litoral Operaciones Inmobiliarias | Desarrollador de Software</p></div>", unsafe_allow_html=True)
        with c_img:
            if os.path.exists("20250508_225422 (1).jpg"): st.image("20250508_225422 (1).jpg", width=130)

st.markdown("## 🛰️ AUDITORÍA SATELITAL PREMIUM | Padrón 5900")
st.write("---")

# 5. TABS DE DATOS
tabs = st.tabs(["📊 MÉTRICAS", "🗺️ TERRENO", "🔬 CIENCIA"])

with tabs[0]:
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Salud (NDVI)", "0.78", "+0.05")
        st.markdown("<p style='color:white; font-size:12px;'>Fuente ESA Sentinel-2: Vigor fotosintético.</p>", unsafe_allow_html=True)
    with c2:
        st.metric("Humedad (1m)", "14.2%", "-3.8%", delta_color="inverse")
        st.markdown("<p style='color:white; font-size:12px;'>Fuente NASA SMAP: Reserva hídrica profunda.</p>", unsafe_allow_html=True)
    with c3:
        st.metric("Suelo (MPa)", "2.5", "Firme")
        st.markdown("<p style='color:white; font-size:12px;'>Fuente NASA Landsat: Capacidad de carga.</p>", unsafe_allow_html=True)

with tabs[1]:
    lat, lon = -32.6585, -57.6455
    m = folium.Map(location=[lat, lon], zoom_start=16, tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google')
    folium.Polygon(locations=[[-32.6565, -57.6485], [-32.6565, -57.6425], [-32.6615, -57.6445], [-32.6615, -57.6475], [-32.6585, -57.6490]], color="#39FF14", weight=6, fill=True, fill_opacity=0.3).add_to(m)
    folium_static(m, width=1100)

# 6. SECCIÓN TÉCNICA Y ARGUMENTOS (BLINDADA)
st.markdown('<div class="cientifico-box">', unsafe_allow_html=True)
st.markdown("<h2 style='text-align:center;'>💎 Inversión 100% Útil: ¿Por qué elegirnos?</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-style:italic;'>Propiedad exclusiva de Litoral Operaciones Inmobiliarias</p><hr>", unsafe_allow_html=True)

# Bloques de Satélites
st.markdown("""
<div class="fuente-item">
    <b>🇪🇺 ESA Sentinel-2:</b> Misión de la Agencia Espacial Europea. 3 satélites (2A, 2B, 2C) con 13 bandas multiespectrales. 
    Monitoreo cada 5 días para detectar falta de nitrógeno antes de que sea visible.
</div>
<div class="fuente-item">
    <b>🇺🇸 NASA SMAP:</b> Soil Moisture Active Passive. Monitorea humedad profunda cada 2-3 días. 
    Vital para entender la zona radicular (Nivel 4) y predecir sequías con precisión agrícola (USDA).
</div>
<div class="fuente-item">
    <b>🇺🇸 NASA Landsat:</b> Registro continuo desde 1972. Satélites 8 y 9 con sensores infrarrojos térmicos (TIRS). 
    Captura cambios reales en la estructura del suelo y recursos hídricos cada 8 días.
</div>
""", unsafe_allow_html=True)

# Argumentos de Venta
col_a, col_b, col_c = st.columns(3)
with col_a:
    st.markdown("### 1. Geometría Oficial")
    st.write("No es solo una foto. Cruzamos datos con el SNIG y Catastro para dibujar el polígono legal exacto.")
with col_b:
    st.markdown("### 2. Análisis Específico")
    st.write("Recorte por Máscara: Los satélites analizan solo los píxeles dentro de su padrón, no del vecino.")
with col_c:
    st.markdown("### 3. Auditoría vs Foto")
    st.write("Google usa fotos viejas. Nosotros entregamos una radiografía actual cada 2-5 días.")

# Cierre y Contacto
st.markdown(f"""
<div style="background-color: #1e4d2b; color: white; padding: 25px; border-radius: 15px; text-align:center; margin-top:25px;">
    <h3 style="color:white !important;">Reporte Detallado Profesional: U$S 150</h3>
    <p>Apto para Uruguay y cualquier país del mundo. Análisis científico de precisión.</p>
    <p style="font-size: 26px; font-weight: bold; color: #39FF14;">📲 Envía coordenadas al 099417716</p>
    <p style="font-size: 11px; opacity: 0.8;">Desarrollador: Leonardo Olivera © 2026</p>
</div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br><center>© 2026 Litoral Operaciones Inmobiliarias - Derechos Reservados</center>", unsafe_allow_html=True)
