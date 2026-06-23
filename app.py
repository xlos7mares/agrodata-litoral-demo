import streamlit as st
import ee
import json
import leafmap.foliumap as leafmap
from datetime import timedelta

# --- 1. CONFIGURACIÓN ---
def authenticate_ee():
    try:
        creds_dict = json.loads(st.secrets["GCP_CREDENTIALS"])
        json_file_path = "service_account.json"
        with open(json_file_path, "w") as f: json.dump(creds_dict, f)
        ee.Initialize(credentials=ee.ServiceAccountCredentials(creds_dict['client_email'], json_file_path))
    except Exception as e: st.stop()

authenticate_ee()

st.set_page_config(layout="wide", page_title="Agro Data Litoral PRO")
st.title("📊 Panel Científico: Diagnóstico Geo-Agronómico Real")

m = leafmap.Map(center=[-32.339, -57.921], zoom=14)
m.add_draw_control()
m.to_streamlit(height=400)

if st.button("🚀 Procesar Auditoría Científica"):
    geometry = m.user_roi
    if geometry:
        try:
            # Fuentes de datos reales
            s2 = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED').filterBounds(geometry).filterDate('2026-05-01', '2026-06-23').median()
            dem = ee.Image('USGS/SRTMGL1_003').clip(geometry)
            meteo = ee.ImageCollection('ECMWF/ERA5_LAND/DAILY_AGGR').filterDate('2026-06-20', '2026-06-23').mean()

            # Cálculos de Geometría Analítica y Trigonometría
            slope = ee.Terrain.slope(dem)
            aspect = ee.Terrain.aspect(dem)
            
            # Cálculos Bio-Físicos
            ndvi = s2.normalizedDifference(['B8', 'B4']).rename('NDVI')
            ndwi = s2.normalizedDifference(['B3', 'B8']).rename('NDWI')
            
            # Extracción de métricas
            stats = ndvi.reduceRegion(ee.Reducer.mean(), geometry, 30).getInfo()
            slope_val = slope.reduceRegion(ee.Reducer.mean(), geometry, 30).getInfo().get('slope', 0)
            temp_k = meteo.select('temperature_2m').reduceRegion(ee.Reducer.mean(), geometry, 10000).getInfo().get('temperature_2m', 293)
            
            # --- PANEL DE DATOS ---
            st.subheader("📋 Resumen Geocientífico")
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Salud Vegetal (NDVI)", f"{stats.get('NDVI', 0):.2f}")
            c2.metric("Temp. Superficie (°C)", f"{float(temp_k)-273.15:.1f}")
            c3.metric("Pendiente (Grados)", f"{slope_val:.2f}")
            c4.metric("Estrés Hídrico (NDWI)", f"{ndwi.reduceRegion(ee.Reducer.mean(), geometry, 30).getInfo().get('NDWI', 0):.2f}")
            
            st.write("---")
            st.write("### 🔍 Interpretación Científica")
            st.write(f"- **Geología/Relieve:** Pendiente media de {slope_val:.2f}°. Una pendiente mayor a 5° requiere manejo de curvas de nivel para evitar escorrentía superficial.")
            st.write(f"- **Estado Biológico:** Valor NDVI de {stats.get('NDVI', 0):.2f}. Indica nivel de actividad fotosintética. Valores bajos sugieren senescencia o déficit nutricional.")
            st.write("- **Datos Pluviales/Clima:** Basado en ERA5-Land (Reanálisis meteorológico global).")

        except Exception as e: st.error(f"Error: {e}")
