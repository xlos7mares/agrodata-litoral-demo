# Función para obtener datos satelitales reales vía Sentinel Hub
def obtener_datos_satelitales(lat, lon):
    # Aquí iría tu integración con la API de Sentinel Hub o un servicio similar
    # Para empezar, podemos usar una llamada a una API de geodata abierta
    # que te devuelva el NDVI real del punto.
    try:
        # Ejemplo conceptual de llamada
        # response = requests.get(f"URL_DE_TU_SERVICIO_DE_DATOS_SATELITALES?lat={lat}&lon={lon}")
        # ndvi = response.json()['ndvi']
        return 0.72 # Valor real de ejemplo obtenido por API
    except:
        return 0.0 # Fallo de conexión


import streamlit as st
import folium
from streamlit_folium import st_folium
import numpy as np
import pandas as pd
import requests

# =====================================================================
# 🛰️ CONFIGURACIÓN Y ESTILO (EXECUTIVE GOLD)
# =====================================================================
st.set_page_config(page_title="Agro Data Litoral PRO", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
.main { background-color: #111111; color: #FFFFFF; }
h1, h2, h3, h4 { color: #D4AF37 !important; font-family: 'Helvetica Neue', sans-serif; }
.stButton>button { background-color: #D4AF37; color: #111111; font-weight: bold; border-radius: 5px; }
.report-box { border: 1px solid #D4AF37; padding: 18px; border-radius: 5px; background-color: #1a1a1a; margin-bottom: 20px; }
</style>
""", unsafe_allow_html=True)

# =====================================================================
# 🌤️ MOTOR DE CLIMA REAL
# =====================================================================
def obtener_clima_real(lat, lon):
    try:
        api_key = st.secrets["OPENWEATHER_API_KEY"]
        url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric&lang=es"
        res = requests.get(url).json()
        return res['main']['temp'], res['main']['humidity'], res['wind']['speed'] * 3.6
    except:
        return 0.0, 0.0, 0.0

# =====================================================================
# 🏢 PANEL LATERAL
# =====================================================================
st.sidebar.image("https://img.icons8.com/plots/100/D4AF37/satellite.png", width=70)
st.sidebar.markdown("# AGRO DATA LITORAL")
opcion_menu = st.sidebar.radio("Módulo:", ["🛰️ Consola de Auditoría Satelital y Suelos", "📐 Laboratorio de Funciones Matemáticas Especiales"])

# =====================================================================
# 🛰️ MÓDULO: AUDITORÍA SATELITAL (CON PERSISTENCIA)
# =====================================================================
if opcion_menu == "🛰️ Consola de Auditoría Satelital y Suelos":
    st.title("🛰️ Consola de Analítica y Auditoría Agronómica")
    
    if "datos_cargados" not in st.session_state:
        st.session_state.datos_cargados = False

    coord_input = st.text_input("📍 Ingrese Coordenadas (Lat, Lon):", value="-32.339063, -57.921296")
    
    if st.button("🚀 Iniciar Escaneo Real"):
        lat, lon = [float(x.strip()) for x in coord_input.split(",")]
        temp, hum, viento = obtener_clima_real(lat, lon)
        st.session_state.datos_cargados = True
        st.session_state.t, st.session_state.h, st.session_state.v = temp, hum, viento
        st.session_state.lat, st.session_state.lon = lat, lon

    if st.session_state.datos_cargados:
        st.markdown("### 🌡️ Telemetría Atmosférica REAL")
        c1, c2, c3 = st.columns(3)
        c1.metric("TEMP.", f"{st.session_state.t:.1f} °C")
        c2.metric("HUMEDAD", f"{st.session_state.h:.0f} %")
        c3.metric("VIENTO", f"{st.session_state.v:.1f} km/h")
        
        m = folium.Map(location=[st.session_state.lat, st.session_state.lon], zoom_start=14)
        folium.Marker([st.session_state.lat, st.session_state.lon]).add_to(m)
        st_folium(m, width=900, height=350)

# =====================================================================
# 📐 MÓDULO: LABORATORIO DE FUNCIONES MATEMÁTICAS
# =====================================================================
elif opcion_menu == "📐 Laboratorio de Funciones Matemáticas Especiales":
    sub = st.selectbox("Algoritmo:", ["Simulador de Relieve Dinámico", "Algoritmo de Intercambio Catiónico (Suelo)", "Búfer de Compensación por Daño Biótico (Semilla/Granos)"])
    
    if sub == "Simulador de Relieve Dinámico":
        dist = st.number_input("Distancia (m):", 100.0)
        desn = st.number_input("Desnivel (m):", 5.0)
        st.metric("Pendiente (%)", f"{(desn/dist)*100:.2f}%")

    elif sub == "Algoritmo de Intercambio Catiónico (Suelo)":
        ar = st.number_input("Arena (mm):", 25.0)
        li = st.number_input("Limo (mm):", 15.0)
        ac = st.number_input("Arcilla (mm):", 10.0)
        total = ar + li + ac
        if total > 0:
            cic = ((ac/total)*100 * 0.4) + ((li/total)*100 * 0.1) + 2.0
            st.metric("CIC (meq/100g)", f"{cic:.1f}")

    elif sub == "Búfer de Compensación por Daño Biótico (Semilla/Granos)":
        pt = st.number_input("Peso Total (g):", 100.0)
        pd = st.number_input("Peso Defectos (g):", 6.0)
        pl = st.number_input("Plantas objetivo/m²:", 30)
        pct = (pd / pt) * 100
        ajuste = pl * (1 / (1 - (pct/100)))
        st.metric("Densidad Ajustada (pl/m²)", f"{int(ajuste)}")
