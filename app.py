import streamlit as st
import ee
import json
import leafmap.foliumap as leafmap
import requests

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
st.title("📊 Panel de Diagnóstico Agronómico - Tiempo Real")

coord_text = st.text_input("📍 Pega Coordenadas (Lat, Lon):", value="-32.339, -57.921")
btn_ejecutar = st.button("🚀 Iniciar Auditoría")

if btn_ejecutar:
    lat, lon = [float(x.strip()) for x in coord_text.split(",")]
    
    # --- DATOS CLIMÁTICOS REALES (OpenWeather API) ---
    # Reemplaza 'TU_API_KEY' por la que obtengas en OpenWeatherMap
    api_key = st.secrets.get("WEATHER_API_KEY", "TU_API_KEY_AQUI")
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    res = requests.get(url).json()
    
    temp_real = res['main']['temp']
    humedad = res['main']['humidity']
    viento = res['wind']['speed']

    # --- DATOS SATELITALES (Sentinel-2) ---
    point = ee.Geometry.Point([lon, lat])
    col = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED').filterBounds(point).filterDate('2026-05-01', '2026-06-23')
    
    if col.size().getInfo() > 0:
        ndvi = col.median().normalizedDifference(['B8', 'B4']).reduceRegion(ee.Reducer.mean(), point, 30).getInfo().get('NDVI', 0)
        
        # --- DASHBOARD ---
        st.subheader("📋 Resumen Geocientífico en Tiempo Real")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Biomasa (NDVI)", f"{ndvi:.2f}")
        c2.metric("Temp. Real (°C)", f"{temp_real:.1f}")
        c3.metric("Humedad (%)", f"{humedad}%")
        c4.metric("Viento (m/s)", f"{viento:.1f}")
        
        st.info("Nota: La temperatura y viento son datos obtenidos de la red meteorológica más cercana a tu ubicación, igual que en Google.")
        
        m = leafmap.Map(center=[lat, lon], zoom=15)
        m.add_ee_layer(col.median().normalizedDifference(['B8', 'B4']), {'min': 0, 'max': 0.8, 'palette': ['red', 'yellow', 'green']}, 'NDVI')
        m.to_streamlit(height=400)
    else:
        st.warning("No hay imágenes claras para esta fecha.")
