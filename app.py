import streamlit as st
import ee
import json
import leafmap.foliumap as leafmap

# 1. Autenticación (la que ya nos funcionó)
def authenticate_ee():
    try:
        creds_dict = json.loads(st.secrets["GCP_CREDENTIALS"])
        json_file_path = "service_account.json"
        with open(json_file_path, "w") as f:
            json.dump(creds_dict, f)
        ee.Initialize(credentials=ee.ServiceAccountCredentials(
            creds_dict['client_email'], json_file_path
        ))
    except Exception as e:
        st.error(f"Error de autenticación: {e}")
        st.stop()

authenticate_ee()

st.set_page_config(layout="wide", page_title="Agro Data Litoral PRO")
st.title("🛰️ Agro Data Litoral: Auditoría Agronómica")

coord_input = st.text_input("📍 Ingrese Coordenadas (Lat, Lon):", value="-32.339, -57.921")

if st.button("🚀 Procesar Datos"):
    try:
        lat, lon = [float(x.strip()) for x in coord_input.split(",")]
        point = ee.Geometry.Point([lon, lat])
        
        img = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED') \
            .filterBounds(point) \
            .filterDate('2026-01-01', '2026-06-22') \
            .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)) \
            .median()

        ndvi = img.normalizedDifference(['B8', 'B4']).rename('NDVI')
        
        # CAMBIO AQUÍ: Usamos una forma más simple de añadir la capa
        m = leafmap.Map()
        m.set_center(lon, lat, 14)
        
        # Esta es la forma más minimalista posible
        m.add_ee_layer(ndvi, {'min': 0, 'max': 1, 'palette': ['blue', 'white', 'green']}, 'NDVI')
        
        m.to_streamlit(height=500)
        st.success("Mapa generado.")
    except Exception as e:
        st.error(f"Error técnico: {e}")
