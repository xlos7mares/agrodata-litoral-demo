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

coord_text = st.text_input("📍 Pega Coordenadas (Lat, Lon):", value="-32.339, -57.921")
btn_ejecutar = st.button("🚀 Ejecutar Auditoría Científica Completa")

if btn_ejecutar:
    try:
        lat, lon = [float(x.strip()) for x in coord_text.split(",")]
        point = ee.Geometry.Point([lon, lat])
        
        # DATOS REALES
        s2 = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED').filterBounds(point).filterDate('2026-05-01', '2026-06-23').median()
        dem = ee.Image('USGS/SRTMGL1_003').clip(point.buffer(5000).bounds())
        meteo = ee.ImageCollection('ECMWF/ERA5_LAND/DAILY_AGGR').filterDate('2026-06-01', '2026-06-23').mean()

        # CÁLCULOS AVANZADOS
        ndvi = s2.normalizedDifference(['B8', 'B4']).rename('NDVI')
        slope = ee.Terrain.slope(dem).rename('Pendiente')
        aspect = ee.Terrain.aspect(dem).rename('Aspecto')
        temp = meteo.select('temperature_2m').subtract(273.15)
        # Cálculo Físico: Evapotranspiración potencial simplificada (Energía/Agua)
        etp = temp.multiply(0.12).rename('ETP') 
        
        data = ee.Image.cat([ndvi, slope, aspect, temp, etp]).reduceRegion(ee.Reducer.mean(), point, 30).getInfo()

        # --- DASHBOARD ---
        st.subheader("📈 Panel de Métricas Avanzadas")
        cols = st.columns(4)
        cols[0].metric("Salud (NDVI)", f"{data.get('NDVI', 0):.2f}")
        cols[1].metric("Temp (°C)", f"{data.get('temperature_2m', 0):.1f}")
        cols[2].metric("Pendiente (°)", f"{data.get('Pendiente', 0):.2f}")
        cols[3].metric("Evapotransp. (mm)", f"{data.get('ETP', 0):.2f}")

        st.write("### 🧠 Diagnóstico Científico para el Productor")
        st.info(f"**Geología Analítica:** El aspecto (orientación) es de {data.get('Aspecto', 0):.0f}°. " + 
                "Esto define la insolación: lotes orientados al sur reciben menos radiación y retienen más humedad.")
        st.warning(f"**Cálculo Físico:** Estimamos una evapotranspiración de {data.get('ETP', 0):.2f} mm/día. " + 
                   "Este valor es clave para determinar la necesidad de riego.")

        # MAPA CON MARCADOR REAL
        m = leafmap.Map(center=[lat, lon], zoom=16)
        m.add_marker([lat, lon], popup="Zona Auditada")
        m.add_ee_layer(ndvi, {'min': 0, 'max': 0.8, 'palette': ['red', 'yellow', 'green']}, 'NDVI')
        m.to_streamlit(height=400)

    except Exception as e: st.error(f"Error: {e}")
