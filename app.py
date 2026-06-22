import streamlit as st
import folium
from streamlit_folium import st_folium
import requests
import numpy as np
from sentinelhub import SentinelHubRequest, BBox, CRS, MimeType, SHConfig

# Usaremos un diccionario simple para las colecciones en lugar del objeto directo
# para evitar el error de 'type object'
DATA_COLLECTION_SENTINEL2 = "S2L2A" 

# Configuración básica
st.set_page_config(page_title="Agro Data Litoral PRO", layout="wide")

st.markdown("""
<style>
.main { background-color: #111111; color: #FFFFFF; }
h1, h2, h3, h4 { color: #D4AF37 !important; }
.stButton>button { background-color: #D4AF37; color: #111111; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# =====================================================================
# MOTOR DE DATOS REALES
# =====================================================================
def obtener_ndvi_real(lat, lon):
    config = SHConfig()
    config.sh_client_id = st.secrets["COPERNICUS_CLIENT_ID"]
    config.sh_client_secret = st.secrets["COPERNICUS_CLIENT_SECRET"]
    
    bbox = BBox(bbox=[lon-0.005, lat-0.005, lon+0.005, lat+0.005], crs=CRS.WGS84)
    
    request = SentinelHubRequest(
        evalscript="return [index]",
        input_data=[SentinelHubRequest.input_data(
            data_collection=DATA_COLLECTION_SENTINEL2,
            time_interval=('2026-06-01', '2026-06-22')
        )],
        responses=[SentinelHubRequest.output_response('default', MimeType.TIFF)],
        bbox=bbox,
        config=config
    )
    data = request.get_data()
    return round(float(np.nanmean(data[0])), 2)

# =====================================================================
# INTERFAZ
# =====================================================================
st.sidebar.markdown("# AGRO DATA LITORAL")
st.title("🛰️ Consola de Analítica y Auditoría Agronómica")

coord_input = st.text_input("📍 Ingrese Coordenadas (Lat, Lon):", value="-32.339063, -57.921296")

if st.button("🚀 Iniciar Escaneo REAL"):
    try:
        lat, lon = [float(x.strip()) for x in coord_input.split(",")]
        # Obtenemos datos
        ndvi = obtener_ndvi_real(lat, lon)
        st.success(f"Dato capturado vía Satélite: {ndvi}")
        
        # Mapa
        m = folium.Map(location=[lat, lon], zoom_start=14)
        folium.Marker([lat, lon]).add_to(m)
        st_folium(m, width=900, height=350)
    except Exception as e:
        st.error(f"FALLO DE CONEXIÓN: {e}")
