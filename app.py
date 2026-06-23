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
st.title("📊 Panel Científico: Auditoría Agronómica de Precisión")

# --- 2. ENTRADAS DE USUARIO ---
col_in, col_map = st.columns([1, 3])
with col_in:
    coord_text = st.text_input("📍 Pega Coordenadas (Lat, Lon):", value="-32.339, -57.921")
    temp_local = st.number_input("🌡️ Temp. local termómetro (°C) (opcional, para calibración):", value=0.0)
    btn_ejecutar = st.button("🚀 Iniciar Auditoría Científica")

if btn_ejecutar:
    try:
        lat, lon = [float(x.strip()) for x in coord_text.split(",")]
        point = ee.Geometry.Point([lon, lat])
        
        # DATOS REALES (Sentinel y ERA5 Horario)
        s2 = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED').filterBounds(point).filterDate('2026-05-01', '2026-06-23').median()
        dem = ee.Image('USGS/SRTMGL1_003').clip(point.buffer(5000).bounds())
        # ERA5 Hourly para máxima precisión temporal
        meteo = ee.ImageCollection('ECMWF/ERA5_LAND/HOURLY').filterDate('2026-06-22', '2026-06-23').sort('system:time_start', False).first()

        # CÁLCULOS
        ndvi = s2.normalizedDifference(['B8', 'B4']).rename('NDVI')
        slope = ee.Terrain.slope(dem).rename('Pendiente')
        temp_sat = meteo.select('temperature_2m').subtract(273.15)
        
        # Extracción
        data = ee.Image.cat([ndvi, slope, temp_sat]).reduceRegion(ee.Reducer.mean(), point, 30).getInfo()
        
        # --- 3. DASHBOARD Y CALIBRACIÓN ---
        final_temp = temp_local if temp_local != 0 else data.get('temperature_2m', 0)
        
        with col_map:
            st.subheader("📋 Resultados de la Auditoría")
            cols = st.columns(4)
            cols[0].metric("Biomasa (NDVI)", f"{data.get('NDVI', 0):.2f}")
            cols[1].metric("Temp. (C°)", f"{final_temp:.1f}")
            cols[2].metric("Pendiente (°)", f"{data.get('Pendiente', 0):.2f}")
            cols[3].metric("Estado", "Calibrado" if temp_local != 0 else "Satélital")
            
            st.write("### 🧪 Diagnóstico Técnico")
            st.info(f"Geología: Pendiente de **{data.get('Pendiente', 0):.2f}°**. " + 
                    ("⚠️ Riesgo de erosión moderado." if data.get('Pendiente', 0) > 5 else "✅ Relieve estable."))
            st.write("---")
            m = leafmap.Map(center=[lat, lon], zoom=15)
            m.add_marker([lat, lon], popup="Zona Auditada")
            m.add_ee_layer(ndvi, {'min': 0, 'max': 0.8, 'palette': ['red', 'yellow', 'green']}, 'NDVI')
            m.to_streamlit(height=400)
    except Exception as e: st.error(f"Error: {e}")
