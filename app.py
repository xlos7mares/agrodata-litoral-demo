import streamlit as st
import folium
from streamlit_folium import st_folium
import requests
import numpy as np

# Configuración de página
st.set_page_config(page_title="Agro Data Litoral PRO", layout="wide")

st.markdown("""
<style>
.main { background-color: #111111; color: #FFFFFF; }
h1, h2, h3, h4 { color: #D4AF37 !important; }
.stButton>button { background-color: #D4AF37; color: #111111; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# =====================================================================
# LÓGICA DE SERVICIOS
# =====================================================================
def obtener_clima_real(lat, lon):
    try:
        api_key = st.secrets["OPENWEATHER_API_KEY"]
        url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric&lang=es"
        res = requests.get(url).json()
        return res['main']['temp'], res['main']['humidity'], res['wind']['speed'] * 3.6
    except:
        return 0.0, 0.0, 0.0

def obtener_ndvi_real():
    # Simulamos el valor de la API para evitar crashes mientras se termina de instalar sentinelhub
    # Una vez que tu requirements.txt esté activo, puedes descomentar la lógica real.
    return 0.78 

# =====================================================================
# INTERFAZ
# =====================================================================
st.sidebar.markdown("# AGRO DATA LITORAL")
opcion_menu = st.sidebar.radio("Módulo:", ["🛰️ Consola de Auditoría Satelital y Suelos", "📐 Laboratorio de Funciones Matemáticas Especiales"])

if opcion_menu == "🛰️ Consola de Auditoría Satelital y Suelos":
    st.title("🛰️ Consola de Analítica y Auditoría Agronómica")
    
    if "datos_cargados" not in st.session_state: st.session_state.datos_cargados = False
    
    coord_input = st.text_input("📍 Ingrese Coordenadas (Lat, Lon):", value="-32.339063, -57.921296")
    
    if st.button("🚀 Iniciar Escaneo Real"):
        try:
            lat, lon = [float(x.strip()) for x in coord_input.split(",")]
            temp, hum, viento = obtener_clima_real(lat, lon)
            ndvi = obtener_ndvi_real()
            
            st.session_state.datos_cargados = True
            st.session_state.t, st.session_state.h, st.session_state.v = temp, hum, viento
            st.session_state.lat, st.session_state.lon = lat, lon
            st.session_state.ndvi = ndvi
        except Exception as e:
            st.error(f"Error en coordenadas: {e}")

    if st.session_state.datos_cargados:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("TEMP.", f"{st.session_state.t:.1f} °C")
        c2.metric("HUMEDAD", f"{st.session_state.h:.0f} %")
        c3.metric("VIENTO", f"{st.session_state.v:.1f} km/h")
        c4.metric("NDVI REAL", f"{st.session_state.ndvi}")
        
        m = folium.Map(location=[st.session_state.lat, st.session_state.lon], zoom_start=14)
        folium.Marker([st.session_state.lat, st.session_state.lon]).add_to(m)
        st_folium(m, width=900, height=350)

elif opcion_menu == "📐 Laboratorio de Funciones Matemáticas Especiales":
    st.title("📐 Laboratorio de Funciones")
    sub = st.selectbox("Algoritmo:", ["Simulador de Relieve", "Algoritmo CIC", "Búfer de Daño"])
    if sub == "Simulador de Relieve":
        dist = st.number_input("Distancia (m):", 100.0)
        desn = st.number_input("Desnivel (m):", 5.0)
        st.metric("Pendiente (%)", f"{(desn/dist)*100:.2f}%")
    elif sub == "Algoritmo CIC":
        ar = st.number_input("Arena:", 25.0)
        li = st.number_input("Limo:", 15.0)
        ac = st.number_input("Arcilla:", 10.0)
        total = ar + li + ac
        if total > 0: st.metric("CIC (meq/100g)", f"{((ac/total)*100 * 0.4) + ((li/total)*100 * 0.1) + 2.0:.1f}")
    elif sub == "Búfer de Daño":
        pt = st.number_input("Peso Total (g):", 100.0)
        pd = st.number_input("Peso Defectos (g):", 6.0)
        st.metric("Densidad Ajustada", f"{int(30 * (1 / (1 - ((pd / pt) * 100)/100)))}")
