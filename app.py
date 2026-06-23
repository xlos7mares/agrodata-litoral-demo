import streamlit as st
import ee
import json
import leafmap.foliumap as leafmap

# 1. Autenticación robusta usando archivo temporal
def authenticate_ee():
    try:
        # Cargamos el JSON de los secretos
        creds_dict = json.loads(st.secrets["GCP_CREDENTIALS"])
        
        # Guardamos el archivo físico temporalmente para máxima compatibilidad
        json_file_path = "service_account.json"
        with open(json_file_path, "w") as f:
            json.dump(creds_dict, f)
            
        # Inicializamos usando la ruta del archivo
        ee.Initialize(credentials=ee.ServiceAccountCredentials(
            creds_dict['client_email'], 
            json_file_path
        ))
    except Exception as e:
        st.error(f"Error crítico en autenticación: {e}")
        st.stop()

# Ejecutar autenticación
authenticate_ee()

# 2. Configuración de la Interfaz
st.set_page_config(layout="wide", page_title="Agro Data Litoral PRO")
st.title("🛰️ Agro Data Litoral: Auditoría Agronómica")

# 3. Entrada de datos
coord_input = st.text_input("📍 Ingrese Coordenadas (Lat, Lon):", value="-32.339, -57.921")

if st.button("🚀 Procesar Datos Satelitales"):
    try:
        # Parsear coordenadas
        lat, lon = [float(x.strip()) for x in coord_input.split(",")]
        point = ee.Geometry.Point([lon, lat])
        
        # Procesamiento satelital
        img = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED') \
            .filterBounds(point) \
            .filterDate('2026-01-01', '2026-06-22') \
            .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)) \
            .median()

        ndvi = img.normalizedDifference(['B8', 'B4']).rename('NDVI')
        
        # Mapa con sintaxis corregida
        m = leafmap.Map()
        m.set_center(lon, lat, 14)
        m.add_layer(
            ndvi, 
            vis_params={'min': 0, 'max': 1, 'palette': ['blue', 'white', 'green']}, 
            name='NDVI'
        )
        m.to_streamlit(height=500)
        
        st.success("Mapa generado exitosamente.")
        
    except Exception as e:
        st.error(f"Error procesando los datos: {e}")
