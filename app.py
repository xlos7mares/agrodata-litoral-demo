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
        with open(json_file_path, "w") as f: json.dump(creds_dict, f)
        ee.Initialize(credentials=ee.ServiceAccountCredentials(creds_dict['client_email'], json_file_path))
    except Exception as e: 
        st.error("Error de autenticación.")
        st.stop()

authenticate_ee()

st.set_page_config(layout="wide", page_title="Agro Data Litoral PRO")
st.title("📊 Panel de Diagnóstico Agronómico - Datos Reales")

# --- 2. CONFIGURACIÓN ---
col1, col2 = st.columns([1, 3])
with col1:
    lat = st.number_input("Latitud", value=-32.339, format="%.6f")
    lon = st.number_input("Longitud", value=-57.921, format="%.6f")
    btn_analizar = st.button("🚀 Iniciar Auditoría Científica")

if btn_analizar:
    try:
        point = ee.Geometry.Point([lon, lat])
        # Rango de 30 días para asegurar datos reales
        fecha_fin = ee.Date(2026, 6, 23)
        fecha_inicio = fecha_fin.advance(-30, 'day')
        
        # Procesamiento
        s2 = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED').filterBounds(point).filterDate(fecha_inicio, fecha_fin).median()
        dem = ee.Image('USGS/SRTMGL1_003')
        clima = ee.ImageCollection('ECMWF/ERA5_LAND/DAILY_AGGR').filterDate(fecha_inicio, fecha_fin).mean()
        
        # Métricas científicas
        ndvi = s2.normalizedDifference(['B8', 'B4']).reduceRegion(ee.Reducer.mean(), point, 30).getInfo().get('NDVI', 0)
        slope = ee.Terrain.slope(dem).reduceRegion(ee.Reducer.mean(), point, 30).getInfo().get('slope', 0)
        temp = clima.select('temperature_2m').reduceRegion(ee.Reducer.mean(), point, 10000).getInfo().get('temperature_2m', 293) - 273.15
        precip = clima.select('total_precipitation_sum').reduceRegion(ee.Reducer.mean(), point, 10000).getInfo().get('total_precipitation_sum', 0) * 1000
        
        # --- 3. DASHBOARD DE RESULTADOS ---
        with col2:
            st.subheader("📋 Resumen Geocientífico")
            k1, k2, k3, k4 = st.columns(4)
            k1.metric("Salud (NDVI)", f"{ndvi:.2f}")
            k2.metric("Temp (°C)", f"{temp:.1f}")
            k3.metric("Pendiente (°)", f"{slope:.2f}")
            k4.metric("Lluvia (mm)", f"{precip:.2f}")
            
            st.write("### 🔍 Interpretación para el Inversor")
            if ndvi < 0.3: st.error("Diagnóstico: Estrés vegetal detectado. Revisar nutrición del cultivo.")
            else: st.success("Diagnóstico: Actividad fotosintética normal.")
            
            st.write(f"**Análisis de Suelo:** La pendiente de {slope:.2f}° indica una {'alta' if slope > 5 else 'baja'} susceptibilidad a la erosión hídrica.")
            
            # Mapa simple (Sin funciones que den error)
            m = leafmap.Map(center=[lat, lon], zoom=15)
            m.add_marker([lat, lon])
            m.to_streamlit(height=400)
            
    except Exception as e: st.error(f"Error técnico: {e}")
