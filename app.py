import streamlit as st
import folium
from streamlit_folium import st_folium
import requests
import numpy as np
from sentinelhub import SentinelHubRequest, DataCollection, BBox, CRS, MimeType, SHConfig

st.set_page_config(page_title="Agro Data Litoral PRO", layout="wide")

# =====================================================================
# CONEXIÓN REAL - SIN RESPALDOS FICTICIOS
# =====================================================================
def obtener_ndvi_real(lat, lon):
    config = SHConfig()
    config.sh_client_id = st.secrets["COPERNICUS_CLIENT_ID"]
    config.sh_client_secret = st.secrets["COPERNICUS_CLIENT_SECRET"]
    
    bbox = BBox(bbox=[lon-0.005, lat-0.005, lon+0.005, lat+0.005], crs=CRS.WGS84)
    
    # Intentamos la conexión directa
    request = SentinelHubRequest(
        evalscript="""
        //VERSION=3
        function setup() { return { input: ["B04", "B08"], output: { bands: 1 } }; }
        function evaluatePixel(sample) {
            let ndvi = (sample.B08 - sample.B04) / (sample.B08 + sample.B04);
            return [ndvi];
        }
        """,
        input_data=[SentinelHubRequest.input_data(
            data_collection=DataCollection.SENTINEL2,
            time_interval=('2026-06-01', '2026-06-22')
        )],
        responses=[SentinelHubRequest.output_response('default', MimeType.TIFF)],
        bbox=bbox,
        config=config
    )
    # Si esta línea falla, el error técnico será visible en la pantalla
    data = request.get_data()
    return round(float(np.nanmean(data[0])), 2)

# =====================================================================
# INTERFAZ (LOGICA DE VISUALIZACIÓN)
# =====================================================================
st.sidebar.markdown("# AGRO DATA LITORAL")
if st.sidebar.button("🚀 Iniciar Escaneo REAL"):
    try:
        # Aquí forzamos la conexión
        lat, lon = -32.339, -57.921
        ndvi = obtener_ndvi_real(lat, lon)
        st.success(f"Dato capturado vía Satélite: {ndvi}")
    except Exception as e:
        st.error(f"FALLO DE CONEXIÓN: {e}")
