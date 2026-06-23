import streamlit as st
import ee
import json
import os
import leafmap.foliumap as leafmap

# 1. Configuración de credenciales
# Borra todo lo que tengas en secrets y pega el bloque JSON completo como 'GCP_CREDENTIALS'
if "GCP_CREDENTIALS" in st.secrets:
    # Cargar credenciales desde los secretos
    creds_dict = json.loads(st.secrets["GCP_CREDENTIALS"])
    
    # Guardar temporalmente como archivo JSON para que Earth Engine lo lea
    with open("service_account.json", "w") as f:
        json.dump(creds_dict, f)
        
    # Inicializar con la cuenta de servicio
    ee.Initialize(credentials=ee.ServiceAccountCredentials(creds_dict['client_email'], "service_account.json"))
else:
    # Fallback si no encuentra secretos (por si acaso)
    ee.Initialize(opt_url='https://earthengine-highvolume.googleapis.com')

# 2. Interfaz de la App
st.set_page_config(layout="wide", page_title="Agro Data Litoral PRO")
st.title("🛰️ Agro Data Litoral: Auditoría Agronómica")

coord_input = st.text_input("📍 Ingrese Coordenadas (Lat, Lon):", value="-32.339, -57.921")

if st.button("🚀 Procesar Datos"):
    try:
        lat, lon = [float(x.strip()) for x in coord_input.split(",")]
        point = ee.Geometry.Point([lon, lat])
        
        # Procesamiento satelital
        img = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED') \
            .filterBounds(point) \
            .filterDate('2026-01-01', '2026-06-22') \
            .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)) \
            .median()

        ndvi = img.normalizedDifference(['B8', 'B4']).rename('NDVI')
        
        # Mostrar Mapa
        m = leafmap.Map()
        m.set_center(lon, lat, 14)
        m.add_layer(ndvi, {'min': 0, 'max': 1, 'palette': ['blue', 'white', 'green']}, 'NDVI')
        m.to_streamlit(height=500)
        
        st.success("Datos procesados correctamente.")
        
    except Exception as e:
        st.error(f"Error técnico: {e}")
