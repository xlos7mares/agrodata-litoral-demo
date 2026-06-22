import streamlit as st
import folium
from streamlit_folium import st_folium
import numpy as np
from sentinelhub import SentinelHubRequest, DataCollection, BBox, CRS, MimeType, SHConfig

# Configuración básica
st.set_page_config(page_title="Agro Data Litoral PRO", layout="wide")

# =====================================================================
# MOTOR DE DATOS REALES (CONFIGURACIÓN MODERNA)
# =====================================================================
def obtener_ndvi_real(lat, lon):
    # Configuración de credenciales
    config = SHConfig()
    config.sh_client_id = st.secrets["COPERNICUS_CLIENT_ID"]
    config.sh_client_secret = st.secrets["COPERNICUS_CLIENT_SECRET"]
    
    # Definición correcta de la colección usando el objeto DataCollection
    # Esta es la forma que la librería espera en las versiones actuales
    collection = DataCollection.SENTINEL2_L2A
    
    bbox = BBox(bbox=[lon-0.005, lat-0.005, lon+0.005, lat+0.005], crs=CRS.WGS84)
    
    request = SentinelHubRequest(
        evalscript="return [index]",
        input_data=[SentinelHubRequest.input_data(
            data_collection=collection,
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
st.title("🛰️ Consola de Analítica y Auditoría Agronómica")
coord_input = st.text_input("📍 Ingrese Coordenadas (Lat, Lon):", value="-32.339063, -57.921296")

if st.button("🚀 Iniciar Escaneo REAL"):
    try:
        lat, lon = [float(x.strip()) for x in coord_input.split(",")]
        ndvi = obtener_ndvi_real(lat, lon)
        st.success(f"Dato capturado vía Satélite: {ndvi}")
        
        m = folium.Map(location=[lat, lon], zoom_start=14)
        folium.Marker([lat, lon]).add_to(m)
        st_folium(m, width=900, height=350)
    except Exception as e:
        st.error(f"FALLO DE CONEXIÓN: {e}")
