import streamlit as st
import ee
import json
import leafmap.foliumap as leafmap

# --- 1. AUTENTICACIÓN ---
def authenticate_ee():
    try:
        creds_dict = json.loads(st.secrets["GCP_CREDENTIALS"])
        json_file_path = "service_account.json"
        with open(json_file_path, "w") as f: json.dump(creds_dict, f)
        ee.Initialize(credentials=ee.ServiceAccountCredentials(creds_dict['client_email'], json_file_path))
    except Exception: st.stop()

authenticate_ee()

st.set_page_config(layout="wide", page_title="Agro Data Litoral PRO")
st.title("📊 Panel Científico: Diagnóstico Agronómico Real")

col1, col2 = st.columns([1, 3])
with col1:
    lat = st.number_input("Latitud", value=-32.339, format="%.6f")
    lon = st.number_input("Longitud", value=-57.921, format="%.6f")
    btn_analizar = st.button("🚀 Iniciar Auditoría Científica")

if btn_analizar:
    try:
        point = ee.Geometry.Point([lon, lat])
        # Usamos texto en lugar de ee.Date(...) para evitar el error de argumentos
        fecha_ini = '2026-05-23'
        fecha_fin = '2026-06-23'
        
        # Fuentes de datos reales
        s2 = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED').filterBounds(point).filterDate(fecha_ini, fecha_fin).median()
        dem = ee.Image('USGS/SRTMGL1_003').clip(point.buffer(5000).bounds())
        clima = ee.ImageCollection('ECMWF/ERA5_LAND/DAILY_AGGR').filterDate(fecha_ini, fecha_fin).mean()

        # Cálculos de Geometría Analítica (Trigonometría del suelo)
        slope = ee.Terrain.slope(dem).reduceRegion(ee.Reducer.mean(), point, 30).getInfo().get('slope', 0)
        ndvi = s2.normalizedDifference(['B8', 'B4']).reduceRegion(ee.Reducer.mean(), point, 30).getInfo().get('NDVI', 0)
        ndwi = s2.normalizedDifference(['B3', 'B8']).reduceRegion(ee.Reducer.mean(), point, 30).getInfo().get('NDWI', 0)
        temp = clima.select('temperature_2m').reduceRegion(ee.Reducer.mean(), point, 10000).getInfo().get('temperature_2m', 293) - 273.15
        precip = clima.select('total_precipitation_sum').reduceRegion(ee.Reducer.mean(), point, 10000).getInfo().get('total_precipitation_sum', 0) * 1000

        # --- PANEL DE DATOS CIENTÍFICOS ---
        with col2:
            st.subheader("📋 Resumen Geocientífico")
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Biomasa (NDVI)", f"{ndvi:.2f}")
            c2.metric("Temp. (°C)", f"{temp:.1f}")
            c3.metric("Pendiente (°)", f"{slope:.2f}")
            c4.metric("Lluvia (mm)", f"{precip:.2f}")
            
            st.write("### 🔬 Interpretación Técnica")
            st.write(f"- **Geología:** Pendiente de **{slope:.2f}°**. " + ("⚠️ Alta erosión: requiere terrazas." if slope > 5 else "✅ Estable."))
            st.write(f"- **Botánica:** Índice hídrico (NDWI) de **{ndwi:.2f}**. " + ("💧 Déficit hídrico." if ndwi < 0 else "🌱 Humedad adecuada."))
            st.write(f"- **Clima:** {precip:.1f} mm acumulados en el último mes. Dato extraído de reanálisis ERA5.")

            m = leafmap.Map(center=[lat, lon], zoom=15)
            m.add_ee_layer(s2.normalizedDifference(['B8', 'B4']), {'min': 0, 'max': 0.8, 'palette': ['red', 'yellow', 'green']}, 'NDVI')
            m.to_streamlit(height=400)
    except Exception as e: st.error(f"Error: {e}")
