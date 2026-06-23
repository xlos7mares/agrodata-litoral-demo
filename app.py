import streamlit as st
import ee
import geemap.foliumap as geemap

# 1. INICIALIZACIÓN DE GEE
# Nota: La primera vez, esto te pedirá autenticación vía navegador
try:
    ee.Initialize()
except Exception:
    ee.Authenticate()
    ee.Initialize()

st.set_page_config(layout="wide", page_title="Agro Data Litoral PRO")

st.title("🛰️ Agro Data Litoral: Auditoría Agronómica Avanzada")

# 2. ENTRADA DE DATOS
coord_input = st.text_input("📍 Ingrese Coordenadas (Lat, Lon):", value="-32.339, -57.921")

if st.button("🚀 Procesar Datos Satelitales"):
    lat, lon = [float(x.strip()) for x in coord_input.split(",")]
    point = ee.Geometry.Point([lon, lat])
    
    # Cargar datos Sentinel-2 reales
    img = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED') \
        .filterBounds(point) \
        .filterDate('2026-01-01', '2026-06-22') \
        .median()

    # FUNCIONES CIENTÍFICAS
    # Química/Física: Cálculo de NDVI (Índice de Vegetación)
    ndvi = img.normalizedDifference(['B8', 'B4']).rename('NDVI')
    
    # Trigonometría: Cálculo de pendiente (Slope) usando un modelo digital de elevación
    dem = ee.Image('USGS/SRTMGL1_003')
    slope = ee.Terrain.slope(dem)
    
    # Extracción de valores
    valor_ndvi = ndvi.reduceRegion(reducer=ee.Reducer.mean(), geometry=point, scale=10).get('NDVI').getInfo()
    valor_pendiente = slope.reduceRegion(reducer=ee.Reducer.mean(), geometry=point, scale=30).get('slope').getInfo()

    # 3. RESULTADOS EN PANTALLA
    c1, c2 = st.columns(2)
    c1.metric("NDVI (Salud Cultivo)", f"{valor_ndvi:.3f}")
    c2.metric("Pendiente (Trigonometría)", f"{valor_pendiente:.1f}°")
    
    # Visualización cartográfica
    m = geemap.Map()
    m.set_center(lon, lat, 15)
    m.add_layer(ndvi, {'min': 0, 'max': 1, 'palette': ['blue', 'white', 'green']}, 'NDVI')
    m.to_streamlit(height=500)
