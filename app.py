import streamlit as st
import ee
import json
import leafmap.foliumap as leafmap
from datetime import timedelta

# --- 1. AUTENTICACIÓN ---
def authenticate_ee():
    try:
        creds_dict = json.loads(st.secrets["GCP_CREDENTIALS"])
        json_file_path = "service_account.json"
        with open(json_file_path, "w") as f:
            json.dump(creds_dict, f)
        ee.Initialize(credentials=ee.ServiceAccountCredentials(creds_dict['client_email'], json_file_path))
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        st.stop()

authenticate_ee()

# --- 2. INTERFAZ ---
st.set_page_config(layout="wide", page_title="Agro Data Litoral PRO")
st.title("🛰️ Agro Data Litoral: Auditoría Agronómica de Precisión")

col1, col2 = st.columns([1, 3])
with col1:
    coord_input = st.text_input("📍 Coordenadas (Lat, Lon):", value="-32.339, -57.921")
    fecha_fin = st.date_input("📅 Fecha de análisis:")
    btn_procesar = st.button("🚀 Ejecutar Análisis Científico")

if btn_procesar:
    try:
        lat, lon = [float(x.strip()) for x in coord_input.split(",")]
        point = ee.Geometry.Point([lon, lat])
        fecha_inicio = fecha_fin - timedelta(days=30)
        
        # --- PROCESAMIENTO CIENTÍFICO ---
        # Sentinel-2 (Multiespectral)
        s2 = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED').filterBounds(point).filterDate(str(fecha_inicio), str(fecha_fin)).median()
        
        ndvi = s2.normalizedDifference(['B8', 'B4']).rename('NDVI')
        ndwi = s2.normalizedDifference(['B3', 'B8']).rename('NDWI')
        
        # Terreno (DEM)
        dem = ee.Image('USGS/SRTMGL1_003')
        slope = ee.Terrain.slope(dem).clip(point.buffer(5000).bounds())
        
        # Climáticos (ERA5 - Promedio de 3 días para evitar el error de rango vacío)
        meteo = ee.ImageCollection('ECMWF/ERA5_LAND/DAILY_AGGR').filterDate(str(fecha_fin - timedelta(days=3)), str(fecha_fin)).mean()
        clima_vals = meteo.reduceRegion(ee.Reducer.mean(), point, 10000).getInfo()
        
        temp_k = clima_vals.get('temperature_2m', 293.15) # Default 20C si falla
        viento_u = clima_vals.get('u_component_wind_10m', 0)
        
        # --- PRESENTACIÓN ---
        st.subheader("📊 Análisis Técnico")
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("NDVI (Salud)", f"{ndvi.reduceRegion(ee.Reducer.mean(), point, 30).getInfo().get('NDVI', 0):.2f}")
        k2.metric("Temp. (C°)", f"{float(temp_k) - 273.15:.2f}")
        k3.metric("NDWI (Hídrico)", f"{ndwi.reduceRegion(ee.Reducer.mean(), point, 30).getInfo().get('NDWI', 0):.2f}")
        k4.metric("Viento (U)", f"{float(viento_u):.2f}")
        
        m = leafmap.Map(center=[lat, lon], zoom=14)
        m.add_ee_layer(ndvi, {'min': 0, 'max': 1, 'palette': ['blue', 'white', 'green']}, 'NDVI')
        m.add_ee_layer(slope, {'min': 0, 'max': 30, 'palette': ['yellow', 'orange', 'red']}, 'Pendiente')
        m.to_streamlit(height=500)
            
    except Exception as e:
        st.error(f"Error técnico de Earth Engine: {e}")
