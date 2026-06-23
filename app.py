import streamlit as st
import ee
import json
import leafmap.foliumap as leafmap

# --- AUTENTICACIÓN ---
def authenticate_ee():
    try:
        creds_dict = json.loads(st.secrets["GCP_CREDENTIALS"])
        json_file_path = "service_account.json"
        with open(json_file_path, "w") as f: json.dump(creds_dict, f)
        ee.Initialize(credentials=ee.ServiceAccountCredentials(creds_dict['client_email'], json_file_path))
    except Exception: st.stop()

authenticate_ee()

st.set_page_config(layout="wide", page_title="Agro Data Litoral PRO")
st.title("🛰️ Agro Data Litoral: Auditoría Científica")

coord_text = st.text_input("📍 Pega Coordenadas (Lat, Lon):", value="-32.339, -57.921")
if st.button("🚀 Ejecutar Auditoría Científica Completa"):
    try:
        lat, lon = [float(x.strip()) for x in coord_text.split(",")]
        point = ee.Geometry.Point([lon, lat])
        
        # 1. DATOS SATELITALES (S2: Biomasa, NDWI: Hídrico)
        s2 = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED').filterBounds(point).filterDate('2026-05-01', '2026-06-23').median()
        ndvi = s2.normalizedDifference(['B8', 'B4']).rename('NDVI')
        ndwi = s2.normalizedDifference(['B3', 'B8']).rename('NDWI')
        
        # 2. DATOS GEOFÍSICOS (SRTM: Pendiente, Aspecto/Orientación solar)
        dem = ee.Image('USGS/SRTMGL1_003').clip(point.buffer(5000).bounds())
        slope = ee.Terrain.slope(dem).rename('Pendiente')
        aspect = ee.Terrain.aspect(dem).rename('Aspecto')
        
        # 3. EXTRACCIÓN DE DATOS REALES (Sin API externas)
        stats = ee.Image.cat([ndvi, ndwi, slope, aspect]).reduceRegion(ee.Reducer.mean(), point, 30).getInfo()
        
        # --- DASHBOARD DE DATOS REALES ---
        st.subheader("📋 Métricas del Terreno y Cultivo")
        cols = st.columns(4)
        cols[0].metric("Biomasa (NDVI)", f"{stats.get('NDVI', 0):.2f}")
        cols[1].metric("Hídrico (NDWI)", f"{stats.get('NDWI', 0):.2f}")
        cols[2].metric("Pendiente (°)", f"{stats.get('Pendiente', 0):.2f}")
        cols[3].metric("Orientación (°)", f"{stats.get('Aspecto', 0):.1f}")
        
        # --- ANÁLISIS ESTRATÉGICO ---
        st.write("### 🧠 Diagnóstico del Productor")
        st.info(f"**Análisis Geológico:** La pendiente de {stats.get('Pendiente', 0):.2f}° combinada con la orientación solar de {stats.get('Aspecto', 0):.1f}° "
                "indica una tasa de insolación específica para esta ladera.")
        
        if stats.get('NDWI', 0) < 0:
            st.error("⚠️ Estrés Hídrico: El índice hídrico sugiere bajo contenido de agua en la vegetación.")
        else:
            st.success("✅ Estado Hídrico: El contenido de humedad en la vegetación es adecuado.")
            
        # Mapa
        m = leafmap.Map(center=[lat, lon], zoom=15)
        m.add_ee_layer(ndvi, {'min': 0, 'max': 0.8, 'palette': ['red', 'yellow', 'green']}, 'Salud Vegetal')
        m.to_streamlit(height=400)
        
    except Exception as e: st.error(f"Error técnico: {e}")
