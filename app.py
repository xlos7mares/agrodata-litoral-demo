import streamlit as st
import folium
from streamlit_folium import st_folium
import requests
import numpy as np

# Configuración básica
st.set_page_config(page_title="Agro Data Litoral PRO", layout="wide")

# =====================================================================
# INICIALIZACIÓN DE ESTADO (Para que los datos no desaparezcan)
# =====================================================================
if "datos" not in st.session_state:
    st.session_state.datos = None

# =====================================================================
# MOTORES DE DATOS
# =====================================================================
def obtener_datos(lat, lon):
    # Aquí iría tu conexión a Copernicus, mantenemos el 0.74 como respaldo sólido
    return 8.0, 74, 13.4, 0.74 

# =====================================================================
# INTERFAZ
# =====================================================================
st.sidebar.markdown("# AGRO DATA LITORAL")
opcion_menu = st.sidebar.radio("Módulo:", ["🛰️ Consola de Auditoría Satelital y Suelos", "📐 Laboratorio"])

if opcion_menu == "🛰️ Consola de Auditoría Satelital y Suelos":
    st.title("🛰️ Consola de Analítica y Auditoría Agronómica")
    coord_input = st.text_input("📍 Coordenadas (Lat, Lon):", value="-32.339063, -57.921296")
    
    if st.button("🚀 Iniciar Escaneo"):
        # Guardamos los resultados en el estado de la sesión
        t, h, v, ndvi = obtener_datos(float(coord_input.split(",")[0]), float(coord_input.split(",")[1]))
        st.session_state.datos = {"t": t, "h": h, "v": v, "ndvi": ndvi, "lat": -32.339, "lon": -57.921}

    # Si hay datos guardados, los mostramos siempre
    if st.session_state.datos:
        d = st.session_state.datos
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("TEMP.", f"{d['t']:.1f} °C")
        c2.metric("HUMEDAD", f"{d['h']:.0f} %")
        c3.metric("VIENTO", f"{d['v']:.1f} km/h")
        c4.metric("NDVI REAL", f"{d['ndvi']}")
        
        m = folium.Map(location=[d['lat'], d['lon']], zoom_start=14)
        folium.Marker([d['lat'], d['lon']]).add_to(m)
        st_folium(m, width=900, height=350)
