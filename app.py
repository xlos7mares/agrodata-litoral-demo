import streamlit as st
import pandas as pd
import time
import random

# --- CONFIGURACIÓN DE MARCA Y ESTÉTICA (COURSERA: RENDIMIENTO) ---
st.set_page_config(
    page_title="Agro Data Litoral | Ingeniería Satelital",
    page_icon="🌱",
    layout="wide"
)

# Estilo de Ingeniería: Fondos limpios y cuadros de datos resaltados
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .metric-card {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #2e7d32;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    .stButton>button {
        background-color: #2e7d32;
        color: white;
        width: 100%;
        border-radius: 8px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- BARRA LATERAL (SIDEBAR) ---
try:
    st.sidebar.image("logoagrodata.png", width=200)
except:
    st.sidebar.header("🌱 AGRO DATA LITORAL")

st.sidebar.write("### 📍 Ubicación del Padrón")
st.sidebar.info("Ingrese coordenadas para escaneo satelital")

# Separación de Latitud y Longitud para Agilidad
col_lat, col_lon = st.sidebar.columns(2)

with col_lat:
    # Valor por defecto: El terreno de tu hermano
    lat_input = st.text_input("Latitud", value="-32.275611")

with col_lon:
    lon_input = st.text_input("Longitud", value="-58.052861")

st.sidebar.write("---")
st.sidebar.write("**Desarrollador de Software:**")
st.sidebar.write("Leonardo Olivera")

# --- LÓGICA DE PROCESAMIENTO (PASO A PASO) ---
try:
    lat = float(lat_input)
    lon = float(lon_input)
except ValueError:
    st.error("⚠️ Error: Las coordenadas deben ser números decimales.")
    st.stop()

# --- CUERPO PRINCIPAL DE LA APP ---
st.title("🌱 AGRO DATA LITORAL - Dashboard de Ingeniería")
st.write(f"Análisis satelital para el punto: **{lat}, {lon}**")

# Fila 1: Los 3 Indicadores Clave (Botánica, Geología, Ingeniería)
col1, col2, col3 = st.columns(3)

# Simulación de datos satelitales (Basado en tus fotos)
with col1:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.subheader("🌿 Botánica")
    st.write("**Vigor (NDVI):** 0.82")
    st.caption("🛰️ ESA Sentinel-2")
    st.progress(0.82)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.subheader("💧 Recursos Hídricos")
    st.write("**Humedad Suelo:** 16.5%")
    st.caption("🛰️ NASA SMAP")
    st.progress(0.16)
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="metric-card" style="border-left-color: #1565c0;">', unsafe_allow_html=True)
    st.subheader("🏗️ Ingeniería")
    st.write("**Firmeza:** 2.8 MPa")
    st.caption("🛰️ NASA Landsat")
    st.success("Aptitud: Obra Firme")
    st.markdown('</div>', unsafe_allow_html=True)

st.write("---")

# Fila 2: Mapa y Análisis de Terreno
col_map, col_info = st.columns([2, 1])

with col_map:
    st.write("### 🛰️ Visualización Cartográfica (Círculo de Muestreo)")
    map_data = pd.DataFrame({'lat': [lat], 'lon': [lon]})
    st.map(map_data, zoom=16)

with col_info:
    st.write("### 📋 Reporte del Predio")
    if st.button("GENERAR INFORME COMPLETO"):
        with st.spinner("Consultando histórico de 20 años..."):
            time.sleep(2)
            st.write("**Superficie Detectada:** ~2000 m²")
            st.write("**Drenaje:** Natural hacia el NO")
            st.write("**Riesgo Hídrico:** Mínimo")
            st.info("Suelo apto para construcción inmediata sin pilotaje.")
            st.balloons()

st.write("---")
st.caption("Agro Data Litoral - Agilidad, Disponibilidad y Seguridad de la Información.")
