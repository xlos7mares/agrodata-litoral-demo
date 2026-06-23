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

# --- 2. INTERFAZ PROFESIONAL ---
st.set_page_config(layout="wide", page_title="Agro Data Litoral PRO")
st.title("🛰️ Agro Data Litoral: Auditoría Agronómica de Precisión")

col1, col2 = st.columns([1, 3])
with col1:
    coord_input = st.text_input("📍 Coordenadas (Lat, Lon):", value="-32.339, -57.921")
    fecha_fin = st.date_input("📅 Fecha:")
    btn_procesar = st.button("🚀 Ejecutar Análisis Multiespectral")

if btn_procesar:
    try:
        lat, lon = [float(x.strip()) for x in coord_input.split(",")]
        point = ee.Geometry.Point([lon, lat])
        fecha_inicio = fecha_fin - timedelta(days=30)
        
        # --- PROCESAMIENTO CIENTÍFICO ---
        # Sentinel-2 (Multiespectral)
        s2 = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED').filterBounds(point).filterDate(str(fecha_inicio), str(fecha_fin)).median()
        
        # Índices (Botánicos/Biológicos)
        ndvi = s2.normalizedDifference(['B8', 'B4']).rename('NDVI') # Salud Vegetal
        ndwi = s2.normalizedDifference(['B3', 'B8']).rename('NDWI') # Estrés Hídrico
        evi = s2.expression('2.5 * ((NIR - RED) / (NIR + 6 * RED - 7.5 * BLUE + 1))', {
            'NIR': s2.select('B8'), 'RED': s2.select('B4'), 'BLUE': s2.select('B2')
        }).rename('EVI') # Biomasa densa
        
        # Terreno (Trigonometría y Geometría del Suelo)
        dem = ee.Image('USGS/SRTMGL1_003')
        slope = ee.Terrain.slope(dem).clip(point.buffer(5000).bounds()) # Pendiente (%)
        aspect = ee.Terrain.aspect(dem).clip(point.buffer(5000).bounds()) # Orientación (Grados)
        
        # Climáticos (Meteorología)
        meteo = ee.ImageCollection('ECMWF/ERA5_LAND/DAILY_AGGR').filterDate(str(fecha_fin), str(fecha_fin)).first()
        temp_k = meteo.select('temperature_2m').reduceRegion(ee.Reducer.mean(), point, 1000).getInfo()['temperature_2m']
        viento = meteo.select('u_component_wind_10m').reduceRegion(ee.Reducer.mean(), point, 1000).getInfo()['u_component_wind_10m']

        # --- PRESENTACIÓN ---
        st.subheader("📊 Análisis Técnico")
        tabs = st.tabs(["KPIs Bio-Físicos", "Análisis de Suelo", "Visualización"])
        
        with tabs[0]:
            k1, k2, k3, k4 = st.columns(4)
            k1.metric("NDVI (Salud)", f"{ndvi.reduceRegion(ee.Reducer.mean(), point, 30).getInfo()['NDVI']:.2f}")
            k2.metric("Temp. (C°)", f"{temp_k - 273.15:.2f}")
            k3.metric("NDWI (Hídrico)", f"{ndwi.reduceRegion(ee.Reducer.mean(), point, 30).getInfo()['NDWI']:.2f}")
            k4.metric("Viento (m/s)", f"{abs(viento):.2f}")
            
        with tabs[1]:
            st.write("### Análisis Trigonométrico del Terreno")
            st.write("El cálculo de la pendiente y orientación determina la susceptibilidad a la erosión hídrica y la retención de nutrientes.")
            st.write(f"Pendiente estimada: {slope.reduceRegion(ee.Reducer.mean(), point, 30).getInfo()['slope']:.2f} grados")
            
        with tabs[2]:
            m = leafmap.Map(center=[lat, lon], zoom=14)
            m.add_ee_layer(ndvi, {'min': 0, 'max': 1, 'palette': ['blue', 'white', 'green']}, 'NDVI')
            m.add_ee_layer(slope, {'min': 0, 'max': 30, 'palette': ['yellow', 'orange', 'red']}, 'Pendiente')
            m.to_streamlit(height=500)
            
    except Exception as e:
        st.error(f"Error técnico: {e}")
