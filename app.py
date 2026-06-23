import streamlit as st
import ee
import json
import leafmap.foliumap as leafmap

# 1. Configuración de autenticación (Usa GCP_CREDENTIALS en tus Secrets)
def authenticate_ee():
    try:
        # Cargamos el JSON de los secretos
        creds_dict = json.loads(st.secrets["GCP_CREDENTIALS"])
        
        # Usamos json_key para evitar errores de tipo con las llaves privadas
        credentials = ee.ServiceAccountCredentials(json_key=creds_dict)
        
        # Inicializamos
        ee.Initialize(credentials=credentials)
    except Exception as e:
        st.error(f"Error en la autenticación: {e}")
        st.stop()

# Llamamos a la autenticación
authenticate_ee()

# 2. Configuración de la Interfaz
st.set_page_config(layout="wide", page_title="Agro Data Litoral PRO")
st.title("🛰️ Agro Data Litoral: Auditoría Agronómica")

# 3. Entrada de datos
coord_input = st.text_input("📍 Ingrese Coordenadas (Lat, Lon):", value="-32.339, -57.921")

if st.button("🚀 Procesar Datos Satelitales"):
    try:
        # Convertimos input a coordenadas
        lat, lon = [float(x.strip()) for x in coord_input.split(",")]
        point = ee.Geometry.Point([lon, lat])
        
        # Colección Sentinel-2 (Pública)
        img = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED') \
            .filterBounds(point) \
            .filterDate('2026-01-01', '2026-06-22') \
            .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)) \
            .median()

        # Cálculo de NDVI
        ndvi = img.normalizedDifference(['B8', 'B4']).rename('NDVI')
        
        # Mapa
        m = leafmap.Map()
        m.set_center(lon, lat, 14)
        m.add_layer(ndvi, {'min': 0, 'max': 1, 'palette': ['blue', 'white', 'green']}, 'NDVI')
        m.to_streamlit(height=500)
        
        st.success("Mapa generado exitosamente.")
        
    except Exception as e:
        st.error(f"Error procesando los datos: {e}")
