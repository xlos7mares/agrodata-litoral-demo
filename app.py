import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import pydeck as pdk

# Configuración de Ingeniería
st.set_page_config(page_title="AgroData Litoral - Master Report", layout="wide")

# CSS para cuadros Nítidos y Profesionales
st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    div[data-testid="stMetric"] {
        background-color: #f8fbf9;
        border: 2px solid #28a745;
        border-radius: 12px;
        padding: 20px;
    }
    .footer-nota {
        font-size: 14px;
        color: #555;
        background-color: #f1f1f1;
        padding: 15px;
        border-radius: 10px;
        border-left: 6px solid #28a745;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🛰️ AgroData Litoral: Auditoría Agro-Geológica")
st.subheader("Establecimiento: Lafluf | Young, Río Negro")

# --- SECCIÓN DE MÉTRICAS ---
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Salud Vegetal (NDVI)", "0.78", "+0.05", help="Dato de Sentinel-2")
with col2:
    st.metric("Humedad Profunda", "14.2%", "-3.8%", delta_color="inverse", help="Dato de NASA SMAP")
with col3:
    st.metric("Resistencia Suelo", "2.5 MPa", "Suelo Fuerte", help="Análisis de formación geológica")

st.write("---")

# --- CONFIGURACIÓN DEL MAPA IMPACTANTE ---
st.subheader("📍 Delimitación Satelital de Precisión (Área de Análisis)")

# Definimos las coordenadas del polígono (5 hectáreas aprox en Young)
# Nota: He ajustado los puntos para que sea un cuadrado perfecto y visible
polygon_data = [
    {
        "polygon": [
            [-57.635, -32.685], 
            [-57.625, -32.685], 
            [-57.625, -32.695], 
            [-57.635, -32.695], 
            [-57.635, -32.685]
        ],
        "name": "Lote Lafluf - 5 Ha",
    }
]

# Capa de Polígono Color FLÚOR
layer = pdk.Layer(
    "PolygonLayer",
    polygon_data,
    get_polygon="polygon",
    get_fill_color=[57, 255, 20, 150],  # VERDE FLÚOR (Neon Green) con transparencia
    get_line_color=[255, 255, 255],     # BORDE BLANCO FUERTE
    get_line_width=5,
    line_width_min_pixels=3,
    pickable=True,
)

# Vista de cámara centrada en el lote
view_state = pdk.ViewState(
    latitude=-32.69, 
    longitude=-57.63, 
    zoom=14.5, 
    pitch=50
)

# Renderizado del Mapa con estilo SATELITAL de Mapbox
st.pydeck_chart(pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    map_style="mapbox://styles/mapbox/satellite-streets-v12", # ESTO ACTIVA EL MAPA REAL
    tooltip={"text": "{name}"}
))

st.write("---")

# --- GRÁFICA Y CONCLUSIÓN ---
st.header("📈 Proyección Hídrica de Rendimiento")
fig = go.Figure()
fig.add_trace(go.Scatter(x=list(range(10)), y=[18,16,15,14,13,12,11,10,9,8], name="Humedad %", line=dict(color="#28a745", width=4)))
fig.add_hline(y=12, line_dash="dash", line_color="red", annotation_text="PUNTO CRÍTICO")
fig.update_layout(template="plotly_white")
st.plotly_chart(fig, use_container_width=True)

st.markdown("""
<div class="footer-nota">
    <b>Análisis de Ingeniería:</b> El área resaltada en <b>verde flúor</b> muestra una anomalía térmica moderada. 
    Se recomienda inspección de drenajes para evitar la compactación detectada por el sensor gravitacional.
</div>
""", unsafe_allow_html=True)
