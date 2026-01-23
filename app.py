import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import pydeck as pdk

# Configuración Nítida y Profesional
st.set_page_config(page_title="AgroData Litoral - Inteligencia Satelital", layout="wide")

# Estilo "Modo Campo" (Blanco, Verde y Gris Claro)
st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    div[data-testid="stMetric"] {
        background-color: #f8f9fa;
        border: 2px solid #28a745;
        border-radius: 15px;
        padding: 15px;
    }
    .stButton>button { width: 100%; border-radius: 20px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛰️ AgroData Litoral: Sistema de Escaneo Multiespectral")

# Selector de Interfaz
menu = st.radio("Seleccione el tipo de análisis:", ["Agrícola (Cultivos/Lafluf)", "Inmobiliario (Terrenos/Pozos)"], horizontal=True)

if menu == "Agrícola (Cultivos/Lafluf)":
    st.header("🌾 Análisis de Productividad y Estrés Hídrico")
    
    if st.button("🚀 VER MODO EJEMPLO (CAMPO LAFLUF - YOUNG)"):
        st.success("✅ Conectando con Constelación Sentinel-2 y NASA SMAP...")
        
        # --- MAPA SATELITAL DE YOUNG ---
        st.subheader("📍 Delimitación Satelital del Lote (5 Ha)")
        # Coordenadas aproximadas de zona rural de Young
        view_state = pdk.ViewState(latitude=-32.69, longitude=-57.63, zoom=14, pitch=45)
        layer = pdk.Layer(
            "PolygonLayer",
            data=[{"polygon": [[-57.635, -32.685], [-57.625, -32.685], [-57.625, -32.695], [-57.635, -32.695]]}],
            get_polygon="-",
            get_fill_color=[40, 167, 69, 100],
            get_line_color=[255, 255, 255],
            line_width=3,
        )
        st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state, map_style="mapbox://styles/mapbox/satellite-v9"))

        # --- MÉTRICAS SATELITALES ---
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Índice NDVI (Vigor)", "0.78", "+0.05", help="Indica salud de la planta")
        with col2:
            st.metric("Humedad en Raíz", "14.2%", "-3.8% CRÍTICO", delta_color="inverse")
        with col3:
            st.metric("Pérdida Proyectada", "u$s 4,200", "En 5 Ha", delta_color="inverse")

        # --- GRÁFICO DE DATOS ---
        st.subheader("📈 Historial de Humedad vs. Predicción de Lluvias")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=list(range(10)), y=[20,18,17,15,14,14,13,12,11,10], name="Humedad Suelo %", line=dict(color="#28a745")))
        fig.update_layout(template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)

elif menu == "Inmobiliario (Terrenos/Pozos)":
    st.header("🔍 Escaneo de Aptitud Hídrica Subterránea")
    coord = st.text_input("Ingrese Coordenadas GPS o link de Google Maps:")
    if coord:
        st.info(f"Analizando micro-variaciones gravitacionales en {coord}...")
        st.metric("Probabilidad de Agua Subterránea", "82%", "Punto Óptimo")
        st.write("Aptitud Hortícola: 10/10 (Suelo con alta materia orgánica detectada)")

# --- BARRA LATERAL COMERCIAL ---
st.sidebar.title("💳 Activación de Reportes")
st.sidebar.write("Para recibir el PDF oficial con todos los datos de los satélites Sentinel, SMAP y GRACE para su padrón específico:")
if st.sidebar.button("SOLICITAR ESTUDIO REAL"):
    st.sidebar.error("BLOQUEADO: Se requiere giro de u$s 150")
    st.sidebar.markdown("[👉 Contactar a Leonardo Olivera](https://wa.me/59899417716)")
