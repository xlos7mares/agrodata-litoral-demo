import streamlit as st
import ee
import json
import leafmap.foliumap as leafmap
import pandas as pd

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
st.title("🔬 Panel de Diagnóstico Geocientífico Avanzado")

# Entrada única para facilitar el pegado de coordenadas
coord_text = st.text_input("📍 Pega Coordenadas (Lat, Lon):", value="-32.339, -57.921")
btn_ejecutar = st.button("🚀 Ejecutar Auditoría Científica Completa")

if btn_ejecutar:
    try:
        lat, lon = [float(x.strip()) for x in coord_text.split(",")]
        point = ee.Geometry.Point([lon, lat])
        
        # PROCESAMIENTO CIENTÍFICO (Fuentes reales: Sentinel, USGS, ERA5)
        s2 = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED').filterBounds(point).filterDate('2026-05-01', '2026-06-23').median()
        dem = ee.Image('USGS/SRTMGL1_003') # Datos geológicos/relieve
        meteo = ee.ImageCollection('ECMWF/ERA5_LAND/DAILY_AGGR').filterDate('2026-06-01', '2026-06-23').mean()

        # CÁLCULOS CIENTÍFICOS
        ndvi = s2.normalizedDifference(['B8', 'B4']).rename('NDVI')
        slope = ee.Terrain.slope(dem).rename('Pendiente') # Trigonometría del terreno
        temp = meteo.select('temperature_2m').subtract(273.15).rename('Temp')
        precip = meteo.select('total_precipitation_sum').multiply(1000).rename('Precip')
        
        # EXTRACCIÓN DE DATOS REALES (Métrica aplicada)
        data = ee.Image.cat([ndvi, slope, temp, precip]).reduceRegion(ee.Reducer.mean(), point, 30).getInfo()

        # DASHBOARD
        st.subheader("📊 Métricas Agronómicas y Geofísicas")
        cols = st.columns(4)
        cols[0].metric("NDVI (Biomasa)", f"{data.get('NDVI', 0):.2f}")
        cols[1].metric("Pendiente (°)", f"{data.get('Pendiente', 0):.2f}")
        cols[2].metric("Temp. (°C)", f"{data.get('Temp', 0):.2f}")
        cols[3].metric("Lluvia (mm)", f"{data.get('Precip', 0):.2f}")

        # ANÁLISIS E INTERPRETACIÓN (Geología analítica y Botánica)
        st.write("### 🧪 Análisis Técnico")
        st.info(f"Geología: El terreno presenta una pendiente de {data.get('Pendiente', 0):.2f}°. " + 
                ("Requiere manejo de curvas de nivel." if data.get('Pendiente', 0) > 5 else "Relieve apto para siembra directa."))
        st.success(f"Botánica: Índice vegetativo de {data.get('NDVI', 0):.2f}. Indica un estado " + 
                   ("saludable." if data.get('NDVI', 0) > 0.4 else "crítico, requiere intervención nutricional."))

        # VISUALIZACIÓN (Mapa sin add_draw_control para evitar errores)
        m = leafmap.Map(center=[lat, lon], zoom=15)
        m.add_ee_layer(ndvi, {'min': 0, 'max': 0.8, 'palette': ['red', 'yellow', 'green']}, 'NDVI')
        m.to_streamlit(height=400)

    except Exception as e: st.error(f"Error en la auditoría: {e}")
