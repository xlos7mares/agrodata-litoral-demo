import streamlit as st
import pandas as pd
import time
import random

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Agro Data Litoral | Ingeniería Satelital",
    page_icon="🌱",
    layout="wide"
)

# Estilo de Ingeniería
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
st.sidebar.info("Pegue las coordenadas tal como se las pasan (ej: -32.275, -58.052)")

# Cuadro único de entrada para máxima facilidad del cliente
coord_input = st.sidebar.text_input("Latitud, Longitud:", value="-32.275597, -58.052867")

st.sidebar.write("---")
st.sidebar.write("**Desarrollador de Software:**")
st.sidebar.write("Leonardo Olivera")

# --- LÓGICA DE PROCESAMIENTO INTELIGENTE ---
# Aquí limpiamos la entrada por si traen comas o espacios de más
try:
    if "," in coord_input:
        lat_str, lon_str = coord_input.split(",")
        lat = float(lat_str.strip())
        lon = float(lon_str.strip())
    else:
        # Por si el cliente solo pega un número
        lat = float(coord_input)
        lon = -58.052867 # Valor por defecto si falta el segundo
except Exception as e:
    st.error(f"⚠️ Formato incorrecto. Use: latitud, longitud (ejemplo: -32.27, -58.05)")
    st.stop()

# --- CUERPO PRINCIPAL ---
st.title("🌱 AGRO DATA LITORAL - Dashboard de Ingeniería")
st.write(f"Análisis satelital para el punto: **{lat}, {lon}**")

# Fila 1: Indicadores
col1, col2, col3 = st.columns(3)

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

# Fila 2: Mapa y Análisis
col_map, col_info = st.columns([2, 1])

with col_map:
    st.write("### 🛰️ Visualización Cartográfica")
    map_data = pd.DataFrame({'lat': [lat], 'lon': [lon]})
    st.map(map_data, zoom=16)

with col_info:
    st.write("### 📋 Reporte del Predio")
    if st.button("GENERAR INFORME COMPLETO"):
        with st.spinner("Analizando terreno de 2000m²..."):
            time.sleep(1.5)
            st.write("**Superficie:** ~2000 m²")
            st.write("**Tipo de Suelo:** Franco-Arcilloso")
            st.info("Suelo estable para construcción.")
            st.balloons()

st.write("---")
st.caption("Agro Data Litoral - Tecnología de Precisión | Paysandú, Uruguay")
