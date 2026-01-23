import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Configuración Nítida
st.set_page_config(page_title="AgroData Litoral - Escaneo de Suelos", layout="wide")

# Estilo Blanco y Verde (Modo Campo)
st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    div[data-testid="stMetric"] {
        background-color: #f1f8f5;
        border: 2px solid #28a745;
        border-radius: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🛰️ AgroData Litoral: Escaneo Satelital de Suelos")

tipo_usuario = st.radio("Seleccione el tipo de análisis:", ["Agrícola (Cultivos)", "Inmobiliario (Compra de Terreno / Pozos)"])

if tipo_usuario == "Inmobiliario (Compra de Terreno / Pozos)":
    st.header("🔍 Análisis de Aptitud y Recursos Hídricos")
    st.write("Ideal para terrenos de 2.000m² en adelante. Detectamos lo que el ojo no ve.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Probabilidad de Veta de Agua", "85%", "ALTA")
        st.write("Anomalía detectada a nivel freático superficial.")
    with col2:
        st.metric("Aptitud Hortícola", "9/10", "Suelo Orgánico")
        st.write("Capacidad de retención de humedad óptima para siembra.")

    st.subheader("🌡️ Mapa de Calor Térmico (Búsqueda de Aguas Profundas)")
    st.info("Detectando variaciones de temperatura en subsuelo para identificación de posibles napas térmicas...")
    # Aquí iría un gráfico de calor simulado
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Soil_moisture_map.png/640px-Soil_moisture_map.png", caption="Ejemplo de Escaneo Satelital de Humedad Subterránea")

    st.success("✅ Terreno apto para perforación de pozo semisurgente.")

# --- EL CIERRE DE VENTA ---
st.sidebar.header("💳 ACTIVAR ESCANEO REAL")
if st.sidebar.button("SOLICITAR ESTUDIO DE TERRENO"):
    st.sidebar.error("BLOQUEADO: Requiere validación de Padrón")
    st.sidebar.write("Giro u$s 150 para reporte de aptitud e informe de aguas subterráneas.")
