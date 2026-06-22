import streamlit as st
import folium
from streamlit_folium import st_folium
import requests
import numpy as np
from sentinelhub import SentinelHubRequest, DataCollection, BBox, CRS, MimeType

# =====================================================================
# 🛰️ CONFIGURACIÓN Y ESTILO
# =====================================================================
st.set_page_config(page_title="Agro Data Litoral PRO", layout="wide")

st.markdown("""
<style>
.main { background-color: #111111; color: #FFFFFF; }
h1, h2, h3, h4 { color: #D4AF37 !important; }
.stButton>button { background-color: #D4AF37; color: #111111; font-weight: bold; border-radius: 5px; }
</style>
""", unsafe_allow_html=True)

# =====================================================================
# 🛰️ MOTOR DE DATOS SATELITALES REALES (INTEGRACIÓN ESA/COPERNICUS)
# =====================================================================
def obtener_ndvi_real(lat, lon):
    try:
        # BBox definido para el lote
        bbox = BBox(bbox=[lon-0.005, lat-0.005, lon+0.005, lat+0.005], crs=CRS.WGS84)
        
        # Script técnico de evaluación espectral NDVI
        evalscript = """
        //VERSION=3
        function setup() { return { input: ["B04", "B08"], output: { bands: 1 } }; }
        function evaluatePixel(sample) {
            let ndvi = (sample.B08 - sample.B04) / (sample.B08 + sample.B04);
            return [ndvi];
        }
        """
        
        request = SentinelHubRequest(
            evalscript=evalscript,
            input_data=[SentinelHubRequest.input_data(
                data_collection=DataCollection.SENTINEL2,
                time_interval=('2026-06-01', '2026-06-22')
            )],
            responses=[SentinelHubRequest.output_response('default', MimeType.TIFF)],
            bbox=bbox,
            config=st.secrets["COPERNICUS_CLIENT_ID"]
        )
        data = request.get_data()
        return round(float(np.nanmean(data[0])), 2)
    except Exception as e:
        return 0.0 # Valor de respaldo si no hay datos satelitales hoy

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
# 🏢 INTERFAZ PRINCIPAL
# =====================================================================
st.sidebar.markdown("# AGRO DATA LITORAL")
opcion_menu = st.sidebar.radio("Módulo:", ["🛰️ Consola de Auditoría Satelital y Suelos", "📐 Laboratorio de Funciones Matemáticas Especiales"])

if opcion_menu == "🛰️ Consola de Auditoría Satelital y Suelos":
    st.title("🛰️ Consola de Analítica y Auditoría Agronómica")
    if "datos_cargados" not in st.session_state: st.session_state.datos_cargados = False
    
    coord_input = st.text_input("📍 Ingrese Coordenadas (Lat, Lon):", value="-32.339063, -57.921296")
    
    if st.button("🚀 Iniciar Escaneo Real"):
        lat, lon = [float(x.strip()) for x in coord_input.split(",")]
        temp, hum, viento = obtener_clima_real(lat, lon)
        ndvi = obtener_ndvi_real(lat, lon)
        
        st.session_state.datos_cargados = True
        st.session_state.t, st.session_state.h, st.session_state.v = temp, hum, viento
        st.session_state.lat, st.session_state.lon = lat, lon
        st.session_state.ndvi = ndvi

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
    # [Resto de tu lógica de laboratorio aquí...]
