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
st.title("🛰️ Agro Data Litoral: Diagnóstico Satelital")

coord_text = st.text_input("📍 Pega Coordenadas (Lat, Lon):", value="-32.339, -57.921")
btn_analizar = st.button("🚀 Ejecutar Análisis Satelital")

if btn_analizar:
    try:
        lat, lon = [float(x.strip()) for x in coord_text.split(",")]
        point = ee.Geometry.Point([lon, lat])
        
        # --- ANÁLISIS SATELITAL (Independiente) ---
        col = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED').filterBounds(point).filterDate('2026-05-01', '2026-06-23')
        
        if col.size().getInfo() > 0:
            s2 = col.median()
            ndvi = s2.normalizedDifference(['B8', 'B4']).rename('NDVI')
            stats = ndvi.reduceRegion(ee.Reducer.mean(), point, 30).getInfo()
            
            st.metric("Biomasa (NDVI)", f"{stats.get('NDVI', 0):.2f}")
            
            # Mapa
            m = leafmap.Map(center=[lat, lon], zoom=15)
            m.add_ee_layer(ndvi, {'min': 0, 'max': 0.8, 'palette': ['red', 'yellow', 'green']}, 'NDVI')
            m.to_streamlit(height=400)
        else:
            st.warning("No hay datos satelitales claros para esta fecha.")

        # --- ANÁLISIS CLIMÁTICO (Blindado) ---
        st.write("---")
        st.write("### 🌡️ Datos Meteorológicos")
        try:
            api_key = st.secrets.get("WEATHER_API_KEY")
            if api_key:
                url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
                res = requests.get(url).json()
                if 'main' in res:
                    st.metric("Temp. Real (°C)", f"{res['main']['temp']:.1f}")
                else:
                    st.error("No se pudieron obtener datos meteorológicos (Revisar API Key).")
            else:
                st.info("API Key no configurada. Omitiendo datos de temperatura.")
        except Exception:
            st.error("Error en la conexión con el servidor meteorológico.")

    except Exception as e: 
        st.error(f"Error técnico crítico: {e}")
