import streamlit as st
import ee
import leafmap.foliumap as leafmap

# 1. INICIALIZACIÓN PÚBLICA (Sin llaves ni archivos)
try:
    # Intentamos conectar a los servicios públicos de GEE
    ee.Initialize(opt_url='https://earthengine-highvolume.googleapis.com')
except Exception:
    # Si la sesión no está iniciada, avisamos que debe autorizarse
    st.warning("Sesión de Earth Engine no iniciada. Por favor, asegúrate de estar logueado en tu cuenta de Google.")
    st.stop()

st.set_page_config(layout="wide", page_title="Agro Data Litoral PRO")
st.title("🛰️ Agro Data Litoral: Auditoría Agronómica")

# 2. ENTRADA DE DATOS
coord_input = st.text_input("📍 Ingrese Coordenadas (Lat, Lon):", value="-32.339, -57.921")

if st.button("🚀 Procesar Datos Satelitales"):
    try:
        lat, lon = [float(x.strip()) for x in coord_input.split(",")]
        point = ee.Geometry.Point([lon, lat])
        
        # Cargar colección pública (Sentinel-2 SR)
        img = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED') \
            .filterBounds(point) \
            .filterDate('2026-01-01', '2026-06-22') \
            .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)) \
            .median()

        # Cálculo de NDVI (B8=NIR, B4=Red)
        ndvi = img.normalizedDifference(['B8', 'B4']).rename('NDVI')
        
        # Cálculo de pendiente (DEM)
        dem = ee.Image('USGS/SRTMGL1_003')
        slope = ee.Terrain.slope(dem)
        
        # Extracción de valores
        valor_ndvi = ndvi.reduceRegion(reducer=ee.Reducer.mean(), geometry=point, scale=30).get('NDVI').getInfo()
        valor_slope = slope.reduceRegion(reducer=ee.Reducer.mean(), geometry=point, scale=30).get('slope').getInfo()

        # 3. INTERFAZ DE RESULTADOS
        col1, col2 = st.columns(2)
        col1.metric("NDVI", f"{valor_ndvi:.3f}" if valor_ndvi else "N/A")
        col2.metric("Pendiente (°)", f"{valor_slope:.1f}" if valor_slope else "N/A")
        
        # Mapa
        m = leafmap.Map()
        m.set_center(lon, lat, 14)
        m.add_layer(ndvi, {'min': 0, 'max': 1, 'palette': ['blue', 'white', 'green']}, 'NDVI')
        m.to_streamlit(height=500)
        
    except Exception as e:
        st.error(f"Error procesando datos: {e}")
