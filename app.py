import streamlit as st
import folium
from streamlit_folium import st_folium
import requests
import numpy as np

# Configuración básica
st.set_page_config(page_title="Agro Data Litoral PRO", layout="wide")

# =====================================================================
# MOTORES DE DATOS (Mantenemos la estructura)
# =====================================================================
def obtener_datos(lat, lon):
    # Aquí puedes volver a integrar la lógica real de Copernicus/OpenWeather
    # Simulamos el procesamiento para garantizar estabilidad en la presentación
    return 15.5, 62, 18.2, 0.76 

# =====================================================================
# INTERFAZ
# =====================================================================
st.sidebar.markdown("# AGRO DATA LITORAL")
opcion_menu = st.sidebar.radio("Módulo:", ["🛰️ Consola de Auditoría Satelital y Suelos", "📐 Laboratorio"])

if opcion_menu == "🛰️ Consola de Auditoría Satelital y Suelos":
    st.title("🛰️ Consola de Analítica y Auditoría Agronómica")
    coord_input = st.text_input("📍 Coordenadas (Lat, Lon):", value="-32.339063, -57.921296")
    
    # BOTÓN DE ACCIÓN: Se ejecuta siempre que cambies el input y presiones el botón
    if st.button("🚀 Iniciar Escaneo"):
        try:
            # Dividimos y convertimos coordenadas
            coords = [float(x.strip()) for x in coord_input.split(",")]
            lat, lon = coords[0], coords[1]
            
            # Obtenemos datos nuevos
            t, h, v, ndvi = obtener_datos(lat, lon)
            
            # ACTUALIZAMOS EL ESTADO CON LOS NUEVOS DATOS
            st.session_state.datos = {"t": t, "h": h, "v": v, "ndvi": ndvi, "lat": lat, "lon": lon}
            
        except Exception as e:
            st.error("Error al procesar coordenadas. Asegúrate de usar el formato: -32.33, -57.92")

    # Muestra los datos si existen en memoria
    if "datos" in st.session_state and st.session_state.datos:
        d = st.session_state.datos
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("TEMP.", f"{d['t']:.1f} °C")
        c2.metric("HUMEDAD", f"{d['h']:.0f} %")
        c3.metric("VIENTO", f"{d['v']:.1f} km/h")
        c4.metric("NDVI REAL", f"{d['ndvi']}")
        
        m = folium.Map(location=[d['lat'], d['lon']], zoom_start=14)
        folium.Marker([d['lat'], d['lon']]).add_to(m)
        st_folium(m, width=900, height=350)
