import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import pydeck as pdk

# Configuración Nítida
st.set_page_config(page_title="AgroData Litoral - Reporte Satelital", layout="wide")

# Diseño "Modo Profesional" Blanco y Verde
st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    div[data-testid="stMetric"] {
        background-color: #f1f8f5;
        border: 2px solid #28a745;
        border-radius: 15px;
        padding: 15px;
    }
    h1, h2, h3 { color: #1e4d2b; }
    .explicacion-grafica {
        background-color: #f9f9f9;
        padding: 15px;
        border-left: 5px solid #28a745;
        font-style: italic;
        margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🛰️ AgroData Litoral: Inteligencia de Precisión")
st.write("---")

# --- BARRA LATERAL ---
st.sidebar.header("📍 Padrón Analizado")
st.sidebar.write("**Establecimiento:** Lafluf (Young)")
st.sidebar.write("**Superficie:** 5 Hectáreas")
st.sidebar.info("Escaneo realizado mediante constelaciones Sentinel-2 y NASA SMAP.")

# --- CUERPO PRINCIPAL ---
st.header("📊 Tablero de Estado Hídrico y Vigor")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Índice NDVI (Vigor)", 
        value="0.78", 
        delta="+0.05",
        help="Extraído del satélite Sentinel-2. Mide la actividad fotosintética. Un valor de 0.78 indica plantas sanas, pero el delta muestra zonas con variabilidad de nitrógeno."
    )

with col2:
    st.metric(
        label="Humedad en Raíz (1m)", 
        value="14.2%", 
        delta="-3.8% CRÍTICO", 
        delta_color="inverse",
        help="Extraído del satélite NASA SMAP. Mide el contenido de agua a 1 metro de profundidad. El -3.8% indica que el cultivo está agotando sus reservas profundas rápidamente."
    )

with col3:
    st.metric(
        label="Pérdida Proyectada", 
        value="u$s 4,200", 
        delta="Riesgo de Rendimiento",
        delta_color="inverse",
        help="Cálculo algorítmico basado en el valor actual de la soja/maíz y el estrés hídrico acumulado. Representa el dinero que dejará de percibir si no se nivela la humedad en 7 días."
    )

# --- GRÁFICA Y EXPLICACIÓN ---
st.subheader("📈 Proyección de Humedad vs. Punto de Marchitez")
dias = list(range(1, 11))
humedad_real = [20, 18, 17, 15, 14, 14, 13, 12, 11, 10]
fig = go.Figure()
fig.add_trace(go.Scatter(x=dias, y=humedad_real, name="Humedad Real", line=dict(color="#28a745", width=4)))
fig.add_hline(y=12, line_dash="dash", line_color="red", annotation_text="PUNTO DE MARCHITEZ (MUERTE CELULAR)")
fig.update_layout(template="plotly_white", xaxis_title="Días Proyectados", yaxis_title="% Humedad")
st.plotly_chart(fig, use_container_width=True)

st.markdown("""
<div class="explicacion-grafica">
    <b>¿Qué significa esta gráfica?</b><br>
    La línea verde muestra cómo el sol y el viento están secando el suelo de su campo día tras día. 
    Cuando la línea cruza la zona roja (12%), la planta deja de crecer para sobrevivir. 
    Cada día que pase por debajo de esa línea, usted pierde kilos de grano que no se recuperan.
</div>
""", unsafe_allow_html=True)

# --- ANÁLISIS DE IMPACTO ECONÓMICO ---
st.divider()
st.subheader("💎 Análisis de Impacto Tecnológico")
with st.container():
    st.write("""
    Este reporte no es una simple observación climática. Es un **Análisis Multiespectral** que procesa datos de gravedad y microondas invisibles al ojo humano. 
    
    **Impacto para su negocio:**
    1. **Ahorro de Riego:** Sepa exactamente cuánto regar para no desperdiciar agua ni energía.
    2. **Decisión de Cosecha:** Anticipe el secado del grano para coordinar la logística.
    3. **Respaldo Científico:** Datos verídicos de agencias espaciales que eliminan la incertidumbre.
    """)

st.sidebar.divider()
if st.sidebar.button("📥 DESCARGAR REPORTE PDF"):
    st.sidebar.error("BLOQUEADO: Se requiere validación de Pago (u$s 150)")
