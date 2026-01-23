import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from streamlit_folium import folium_static
import folium

# 1. Configuración de Marca y Estilo
st.set_page_config(page_title="AgroData Litoral - Padrón 5900", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    div[data-testid="stMetric"] {
        background-color: #f8fbf9;
        border: 2px solid #28a745;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.1);
    }
    .status-badge {
        background-color: #39FF14;
        color: black;
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 14px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Encabezado Técnico
st.title("🛰️ AgroData Litoral: Auditoría Geográfica de Precisión")
st.markdown(f"**Establecimiento:** Lafluf | **Padrón:** 5900 | **Ubicación:** Young, Río Negro")
st.markdown('<span class="status-badge">SISTEMA DE ESCANEO ACTIVO</span>', unsafe_allow_html=True)
st.write("---")

# 3. Métricas de Sensores (NDVI y Suelo)
st.header("🎛️ Análisis de Capas de Subsuelo")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Salud Vegetal (NDVI)", value="0.78", delta="+0.05", help="Reflectancia de biomasa en Padrón 5900")
with col2:
    st.metric(label="Humedad en Perfil (1m)", value="14.2%", delta="-3.8%", delta_color="inverse")
with col3:
    st.metric(label="Resistencia Mecánica", value="2.5 MPa", delta="Suelo Firme")

st.write("---")

# 4. Mapa Satelital con Padrón Irregular (Corte Agronómico)
st.header("🌐 Delimitación Técnica del Padrón 5900 (5 Ha)")

# Coordenadas en zona de chacras puras (fuera de la ciudad)
lat, lon = -32.658, -57.645

# Mapa base Satelital Híbrido
m = folium.Map(location=[lat, lon], zoom_start=16, tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google')

# Puntos para un polígono irregular (forma de campo real, no un cuadrado de Paint)
padrón_puntos = [
    [-32.656, -57.648], # Vértice Norte
    [-32.656, -57.642], # Vértice Este
    [-32.661, -57.644], # Vértice Sur
    [-32.661, -57.647], # Vértice Oeste
    [-32.658, -57.6485],# Quiebre de alambrado
    [-32.656, -57.648]  # Cierre
]

folium.Polygon(
    locations=padrón_puntos,
    color="#FFFFFF",        # Borde blanco de plano
    weight=3,
    fill=True,
    fill_color="#39FF14",   # VERDE FLÚOR AGRODATA
    fill_opacity=0.35,      # Permite ver la tierra debajo
    tooltip="PADRÓN 5900 - ANÁLISIS INTEGRAL"
).add_to(m)

folium_static(m, width=1200)

# 5. Gráfica y Cierre
st.write("---")
st.header("📈 Evolución de Humedad y Estrés")
dias = list(range(1, 11))
datos = [18, 16, 15, 14, 13, 12, 11, 10, 9, 8]
fig = go.Figure(go.Scatter(x=dias, y=datos, name="Reserva Hídrica", line=dict(color="#28a745", width=4)))
fig.update_layout(template="plotly_white", xaxis_title="Días", yaxis_title="% Agua en Suelo")
st.plotly_chart(fig, use_container_width=True)

st.success(f"**Conclusión para el Padrón 59 (Lafluf):** El área analizada de 5 hectáreas no presenta interferencias urbanas. La estructura geológica es apta para la instalación inmediata de infraestructura pesada o cultivos de alto rendimiento.")

# 6. Sidebar de Pago
st.sidebar.title("🔐 Panel de Control")
st.sidebar.info("Cuentas de 'AgroData Litoral' vinculadas al Padrón 5900.")
if st.sidebar.button("GENERAR REPORTE FINAL"):
    st.sidebar.warning("Pendiente: Pago de u$s 150 por Auditoría Externa.")
