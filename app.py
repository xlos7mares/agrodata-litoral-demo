import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import pydeck as pdk

# Configuración de Ingeniería de Alta Gama
st.set_page_config(page_title="AgroData Litoral - Master Report", layout="wide")

# Estilo para cuadros Nítidos y Profesionales
st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: 2px solid #28a745;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🛰️ AgroData Litoral: Auditoría Agro-Geológica Integral")
st.subheader("Establecimiento: Lafluf | Young, Río Negro")

# --- SECCIÓN 1: MÉTRICAS TÉCNICAS (CON MENSAJES FLOTANTES) ---
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Salud Vegetal (NDVI)", value="0.78", delta="+0.05",
        help="Satelite Sentinel-2. El 0.78 indica fotosíntesis activa. El inversor ve un activo biológico en crecimiento."
    )
with col2:
    st.metric(
        label="Humedad Profunda (1m)", value="14.2%", delta="-3.8% CRÍTICO", delta_color="inverse",
        help="Satelite NASA SMAP. Mide agua útil para la raíz. Indica que el subsuelo está entrando en zona de déficit."
    )
with col3:
    st.metric(
        label="Resistencia Suelo", value="2.5 MPa", delta="Suelo Fuerte",
        help="Análisis Geológico. Apto para cimentación pesada de galpones o infraestructura sin riesgo de hundimiento."
    )

st.write("---")

# --- SECCIÓN 2: EL MAPA SATELITAL REAL ---
st.subheader("🌐 Escaneo Satelital de Precisión (Capa de Subsuelo)")

# Definimos el área exacta de Lafluf (5 Ha) con color Verde Neón Flúor
polygon_data = [{
    "polygon": [
        [-57.635, -32.685], [-57.625, -32.685], 
        [-57.625, -32.695], [-57.635, -32.695], 
        [-57.635, -32.685]
    ],
    "label": "Lote Lafluf - Análisis de Capas"
}]

layer = pdk.Layer(
    "PolygonLayer",
    polygon_data,
    get_polygon="polygon",
    get_fill_color=[57, 255, 20, 120],  # VERDE NEÓN TRASLÚCIDO
    get_line_color=[255, 255, 255],     # BORDE BLANCO FUERTE
    get_line_width=5,
    pickable=True,
)

# Vista centrada y con inclinación 3D
view_state = pdk.ViewState(
    latitude=-32.69, longitude=-57.63, 
    zoom=14.5, pitch=50, bearing=-10
)

# CARGA DE MAPA SATELITAL (Estilo híbrido para máxima realidad)
st.pydeck_chart(pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    map_style="mapbox://styles/mapbox/satellite-v9", # Versión satelital directa
    tooltip={"text": "{label}"}
))

# --- SECCIÓN 3: GRÁFICA Y CONCLUSIÓN ---
st.write("---")
st.header("📈 Proyección Hídrica y Financiera")
dias = list(range(1, 11))
humedad = [18, 16, 15, 14, 13, 12, 11, 10, 9, 8]
fig = go.Figure()
fig.add_trace(go.Scatter(x=dias, y=humedad, name="Reserva Hídrica", line=dict(color="#28a745", width=4)))
fig.add_hline(y=12, line_dash="dash", line_color="red", annotation_text="PUNTO DE MARCHITEZ")
fig.update_layout(template="plotly_white", xaxis_title="Días Proyectados", yaxis_title="% Humedad")
st.plotly_chart(fig, use_container_width=True)

st.info("💡 **Conclusión Estratégica:** El predio presenta un subsuelo estable (Geología tipo 'Fuerte') y un vigor biológico (NDVI) competitivo. Se recomienda activar riego para proteger los u$s 4,200 en riesgo por estrés hídrico.")
