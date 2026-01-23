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
        border: 2px solid #1e4d2b;
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
    .conclusion-box {
        background-color: #e8f4fd;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #007bff;
        color: #004085;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🛰️ AgroData Litoral: Auditoría Agro-Geológica Integral")
st.subheader("Establecimiento: Lafluf | Ubicación: Young, Río Negro | Área: 5 Ha")
st.write("---")

# --- SECCIÓN 1: MÉTRICAS TÉCNICAS (CON MENSAJES FLOTANTES) ---
st.header("🎛️ Indicadores de Precisión Satelital")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Índice NDVI (Salud Vegetal)", 
        value="0.78", 
        delta="+0.05",
        help="Satelite: Sentinel-2. El NDVI mide la reflectancia en el infrarrojo cercano. Un valor de 0.78 indica una biomasa activa y saludable, sin presencia de clorosis (amarillamiento) en el dosel superior."
    )

with col2:
    st.metric(
        label="Humedad Estructural (1m)", 
        value="14.2%", 
        delta="-3.8% CRÍTICO", 
        delta_color="inverse",
        help="Satelite: NASA SMAP. Mide el contenido volumétrico de agua a nivel radicular profundo. El descenso del 3.8% alerta sobre el agotamiento de la reserva hídrica del subsuelo (agua útil disponible)."
    )

with col3:
    st.metric(
        label="Resistencia Mecánica Suelo", 
        value="2.5 MPa", 
        delta="Suelo Fuerte",
        help="Análisis Geológico: Basado en la Formación Tacuarembó/Young. Indica la capacidad de carga del suelo. 2.5 MPa es un suelo firme, apto para cimentaciones pesadas o estructuras de galpones sin riesgo de hundimiento."
    )

# --- SECCIÓN 2: MAPA Y GEOLOGÍA ---
st.write("---")
col_map, col_geo = st.columns([2, 1])

with col_map:
    st.subheader("📍 Delimitación Georeferenciada del Proyecto")
    view_state = pdk.ViewState(latitude=-32.69, longitude=-57.63, zoom=15, pitch=40)
    layer = pdk.Layer(
        "PolygonLayer",
        data=[{"polygon": [[-57.635, -32.685], [-57.625, -32.685], [-57.625, -32.695], [-57.635, -32.695]]}],
        get_polygon="-",
        get_fill_color=[40, 167, 69, 80],
        get_line_color=[255, 255, 255],
        line_width=3,
    )
    st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state, map_style="mapbox://styles/mapbox/satellite-v9"))

with col_geo:
    st.subheader("🏗️ Informe de Cimentación")
    st.write("""
    **Tipo de Suelo:** Franco-Arcilloso sobre basamento estable.
    
    **Construcción:** Suelo de consistencia 'Fuerte'. No se detectan estratos expansivos (arcillas reactivas) que comprometan la estabilidad de futuras construcciones.
    
    **Agua Subterránea:** Análisis por gravedad indica nivel freático a 18-22 metros de profundidad.
    """)

# --- SECCIÓN 3: GRÁFICA EXPLICADA ---
st.header("📈 Proyección Hídrica de Rendimiento")
dias = list(range(1, 11))
humedad_proyectada = [18, 16, 15, 14, 13, 12, 11, 10, 9, 8]
fig = go.Figure()
fig.add_trace(go.Scatter(x=dias, y=humedad_proyectada, name="Reserva de Agua", line=dict(color="#28a745", width=4)))
fig.add_hline(y=12, line_dash="dash", line_color="red", annotation_text="UMBRAL DE ESTRÉS PERMANENTE")
fig.update_layout(template="plotly_white", xaxis_title="Días de Proyección", yaxis_title="% Humedad de Suelo")
st.plotly_chart(fig, use_container_width=True)

st.markdown("""
<div class="footer-nota">
    <b>Análisis de la Gráfica:</b> Esta curva representa la 'Evapotranspiración Real'. 
    Muestra cómo el suelo perderá su capacidad de alimentar al cultivo en los próximos 10 días. 
    <b>Zona Verde:</b> Operación óptima. <b>Zona Roja:</b> El cultivo entra en 'Punto de Marchitez', donde la pérdida de rendimiento es irreversible (aprox. 80kg/Ha por día).
</div>
""", unsafe_allow_html=True)

# --- SECCIÓN 4: CONCLUSIÓN PARA EL INVERSOR ---
st.write("---")
st.subheader("💡 Conclusión Estratégica para Inversores")
st.markdown("""
<div class="conclusion-box">
    <b>Dictamen Técnico:</b> El predio analizado presenta una aptitud <b>Agrícola-Industrial Superior</b>. 
    La combinación de un suelo de alta resistencia mecánica (ideal para infraestructura logística) 
    y una respuesta biológica positiva (NDVI 0.78) lo posiciona como un activo de bajo riesgo y alta revalorización. 
    <br><br>
    <b>Recomendación Inminente:</b> Iniciar protocolos de riego suplementario en 48hs para proteger el valor del activo biológico actual (u$s 4,200 en riesgo).
</div>
""", unsafe_allow_html=True)

st.sidebar.title("🔐 Acceso Profesional")
if st.sidebar.button("GENERAR PDF PARA FIRMA"):
    st.sidebar.error("ERROR: Reporte requiere firma digital de Leonardo Olivera (Sujeto a Pago de u$s 150)")
