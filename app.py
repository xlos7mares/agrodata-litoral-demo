import streamlit as st
import ee
import json
import leafmap.foliumap as leafmap

# --- AUTENTICACIÓN ---
def authenticate_ee():
    try:
        creds_dict = json.loads(st.secrets["GCP_CREDENTIALS"])
        json_file_path = "service_account.json"
        with open(json_file_path, "w") as f:
            json.dump(creds_dict, f)
        ee.Initialize(credentials=ee.ServiceAccountCredentials(creds_dict['client_email'], json_file_path))
    except Exception as e:
        st.error(f"Error de conexión con la Nube Satelital: {e}")
        st.stop()

authenticate_ee()

# --- INTERFAZ PROFESIONAL ---
st.set_page_config(layout="wide", page_title="Agro Data Litoral PRO")
st.title("🛰️ Agro Data Litoral: Auditoría Agronómica de Precisión")
st.markdown("---")

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("⚙️ Parámetros de Análisis")
    coord_input = st.text_input("📍 Coordenadas (Lat, Lon):", value="-32.339, -57.921")
    fecha = st.date_input("📅 Fecha de análisis:")
    btn_procesar = st.button("🚀 Iniciar Auditoría Técnica")

with col2:
    st.info("La plataforma procesa datos satelitales en tiempo real para determinar salud vegetal, temperatura de superficie y morfología del terreno.")

if btn_procesar:
    try:
        lat, lon = [float(x.strip()) for x in coord_input.split(",")]
        point = ee.Geometry.Point([lon, lat])
        
        # 1. DATOS SATELITALES (Sentinel-2)
        img = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED').filterBounds(point).filterDate(str(fecha), '2026-06-22').median()
        ndvi = img.normalizedDifference(['B8', 'B4']).rename('NDVI')
        
        # 2. DATOS CLIMÁTICOS (MODIS Temperatura)
        temp = ee.ImageCollection('MODIS/061/MOD11A1').filterDate(str(fecha), '2026-06-22').mean().select('LST_Day_1km').multiply(0.02).subtract(273.15)
        
        # 3. ANÁLISIS MORFOLÓGICO (Trigonometría sobre DEM)
        dem = ee.Image('USGS/SRTMGL1_003')
        slope = ee.Terrain.slope(dem).clip(point.buffer(5000).bounds())
        aspect = ee.Terrain.aspect(dem).clip(point.buffer(5000).bounds())
        
        # Extraer valores reales
        val_ndvi = ndvi.reduceRegion(ee.Reducer.mean(), point, 30).getInfo()['NDVI']
        val_temp = temp.reduceRegion(ee.Reducer.mean(), point, 1000).getInfo()['LST_Day_1km']
        
        # --- PRESENTACIÓN ---
        st.subheader("📊 Resultados de la Auditoría")
        kpi1, kpi2, kpi3 = st.columns(3)
        kpi1.metric("Índice Vegetal (NDVI)", f"{val_ndvi:.2f}")
        kpi2.metric("Temp. Suelo (°C)", f"{val_temp:.2f}")
        kpi3.metric("Pendiente (°)", "Datos en mapa")

        m = leafmap.Map(center=[lat, lon], zoom=13)
        m.add_ee_layer(ndvi, {'min': 0, 'max': 1, 'palette': ['blue', 'white', 'green']}, 'NDVI')
        m.add_ee_layer(slope, {'min': 0, 'max': 30, 'palette': ['yellow', 'orange', 'red']}, 'Pendiente')
        m.add_marker([lat, lon], popup="Zona de Estudio")
        m.to_streamlit(height=500)
        
    except Exception as e:
        st.error(f"Error en el procesamiento de datos: {e}")
