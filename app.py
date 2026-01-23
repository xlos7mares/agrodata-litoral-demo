import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from streamlit_folium import folium_static
import folium

# 1. Configuración de Ingeniería Pro
st.set_page_config(page_title="AgroData Litoral - Centro de Comando", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    div[data-testid="stMetric"] {
        background-color: #f1f8f5;
        border: 2px solid #28a745;
        border-radius: 15px;
        padding: 20px;
    }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; background-color: #f8f9fa; border-radius: 10px; padding: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛰️ AgroData Litoral: Sistema Global de Monitoreo")
st.subheader("Simulación de Escaneo Multiespectral - Padrón 5900")

# --- MENÚ DE TABS PARA ORDENAR EL "LLAVE EN MANO" ---
tabs = st.tabs(["📊 Tablero de Control", "🗺️ Mapa Geográfico", "📚 Base de Datos Agro", "📥 Reportes"])

with tabs[0]:
    st.header("🎛️ Métricas en Tiempo Real (NASA / ESA)")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Índice de Clorofila (RECI)", "0.82", "+0.02", 
                  help="SATÉLITE: Sentinel-2. UTILIDAD: Detecta niveles de nitrógeno. DESCRIPCIÓN: Mide la densidad de clorofila. Un valor bajo indica necesidad inminente de fertilización.")
    with col2:
        st.metric("Evapotranspiración (ETR)", "5.2 mm/día", "ALTA", 
                  help="SATÉLITE: Landsat-8/9. UTILIDAD: Mide la pérdida de agua por transpiración de la planta y evaporación del suelo. Indica el 'gasto' hídrico diario.")
    with col3:
        st.metric("Reserva de Agua Útil", "18%", "-5% CRÍTICO", delta_color="inverse",
                  help="DATOS: NASA SMAP. UTILIDAD: Indica cuánta agua disponible queda en el perfil de 1 metro antes de la muerte celular del cultivo.")

with tabs[1]:
    st.header("🌐 Visualización Satelital de Precisión")
    # Mapa de Google Hybrid que ya probamos y te gustó
    lat, lon = -32.6585, -57.6455
    m = folium.Map(location=[lat, lon], zoom_start=16, tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google')
    folium.Polygon(
        locations=[[-32.6565, -57.6485], [-32.6565, -57.6425], [-32.6615, -57.6445], [-32.6615, -57.6475], [-32.6585, -57.6490], [-32.6565, -57.6485]],
        color="#FFFFFF", weight=4, fill=True, fill_color="#39FF14", fill_opacity=0.35,
        tooltip="DETECTOR DE VETAS HÍDRICAS ACTIVO"
    ).add_to(m)
    folium_static(m, width=1200)

with tabs[2]:
    st.header("📚 Fundamentos Agronómicos (Libro de Campo)")
    st.markdown("""
    **Cálculos Estándar aplicados:**
    * **Punto de Marchitez Permanente (PMP):** Calculado para suelos franco-arcillosos de la zona de Young.
    * **Constante Dieléctrica:** Procesada para eliminar interferencia de vegetación sobre la lectura de suelo húmedo.
    * **Grados Día Calor (GDC):** Acumulados desde la fecha de siembra para predecir fecha de cosecha óptima.
    """)

with tabs[3]:
    st.header("📄 Generación de Documentación Técnica")
    st.write("Seleccione el tipo de documento a exportar:")
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        if st.button("👁️ VER MUESTRA PDF (BÁSICA)"):
            st.success("Muestra generada. (En un caso real, aquí se abriría un PDF con datos de ejemplo)")
    with col_d2:
        if st.button("🔒 GENERAR PDF PROFESIONAL (PADRÓN 5900)"):
            st.error("ACCESO RESTRINGIDO: Se requiere validación de giro u$s 150.")
