import streamlit as st
import ee
import json
import leafmap.foliumap as leafmap

def authenticate_ee():
    try:
        creds_dict = json.loads(st.secrets["GCP_CREDENTIALS"])
        json_file_path = "service_account.json"
        with open(json_file_path, "w") as f: json.dump(creds_dict, f)
        ee.Initialize(credentials=ee.ServiceAccountCredentials(creds_dict['client_email'], json_file_path))
    except Exception: st.stop()

authenticate_ee()

st.set_page_config(layout="wide", page_title="Agro Data Litoral PRO")
st.title("📊 Panel Científico: Auditoría Real")

# --- ENTRADA DE DATOS UNIFICADA ---
coord_input = st.text_input("📍 Pega las coordenadas (Lat, Lon):", value="-32.339, -57.921")
btn_analizar = st.button("🚀 Ejecutar Análisis Científico")

m = leafmap.Map(center=[-32.339, -57.921], zoom=14)
m.add_draw_control()
m.to_streamlit(height=400)

if btn_analizar:
    try:
        # Extraer lat/lon del texto pegado
        lat, lon = [float(x.strip()) for x in coord_input.split(",")]
        # Si dibujaste algo, usa esa área; si no, usa el punto
        geom = m.user_roi if m.user_roi else ee.Geometry.Point([lon, lat])
        
        # Procesar datos reales
        s2 = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED').filterBounds(geom).filterDate('2026-05-01', '2026-06-23').median()
        ndvi = s2.normalizedDifference(['B8', 'B4']).rename('NDVI')
        
        # Reducción de datos (mean) sobre la geometría seleccionada
        stats = ndvi.reduceRegion(ee.Reducer.mean(), geom, 30).getInfo()
        val_ndvi = stats.get('NDVI', 0)
        
        # Si da 0, es que la fecha/zona no tiene datos limpios, buscamos en un rango más amplio
        if val_ndvi == 0:
            s2_wide = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED').filterBounds(geom).filterDate('2026-01-01', '2026-06-23').median()
            val_ndvi = s2_wide.normalizedDifference(['B8', 'B4']).reduceRegion(ee.Reducer.mean(), geom, 30).getInfo().get('NDVI', 0)

        st.metric("Biomasa Real (NDVI)", f"{val_ndvi:.2f}")
        st.info("Nota: Si el valor es 0, el satélite no tiene datos limpios (sin nubes) para esta zona en la fecha seleccionada.")
        
    except Exception as e: st.error(f"Error procesando coordenadas: {e}")
