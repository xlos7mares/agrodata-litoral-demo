import streamlit as st
import folium
from streamlit_folium import st_folium
import numpy as np
from sentinelhub import SentinelHubRequest, DataCollection, BBox, CRS, MimeType, SHConfig

st.set_page_config(page_title="Agro Data Litoral PRO", layout="wide")

def obtener_ndvi_real(lat, lon):
    # FORZAMOS LA CONFIGURACIÓN
    config = SHConfig()
    config.sh_client_id = st.secrets["COPERNICUS_CLIENT_ID"]
    config.sh_client_secret = st.secrets["COPERNICUS_CLIENT_SECRET"]
    
    # IMPORTANTE: Definimos la colección aquí adentro para asegurar compatibilidad
    collection = DataCollection.SENTINEL2_L2A
    
    bbox = BBox(bbox=[lon-0.005, lat-0.005, lon+0.005, lat+0.005], crs=CRS.WGS84)
    
    # SOLICITUD EXPLÍCITA
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
    
    # Esta es la ejecución real
    data = request.get_data()
    return round(float(np.nanmean(data[0])), 2)

st.title("🛰️ Consola de Analítica y Auditoría Agronómica")
coord_input = st.text_input("📍 Coordenadas (Lat, Lon):", value="-32.339063, -57.921296")

if st.button("🚀 Iniciar Escaneo REAL"):
    try:
        lat, lon = [float(x.strip()) for x in coord_input.split(",")]
        # Llamada directa sin red de seguridad
        ndvi = obtener_ndvi_real(lat, lon)
        st.success(f"Dato capturado vía Satélite: {ndvi}")
    except Exception as e:
        # AQUÍ VEREMOS EL ERROR REAL
        st.error(f"DETALLE DEL ERROR: {str(e)}")
