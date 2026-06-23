import streamlit as st
import ee
import json
import leafmap.foliumap as leafmap
from datetime import timedelta

# --- 1. AUTENTICACIÓN SEGURA ---
def authenticate_ee():
    try:
        # Cargamos credenciales desde los Secrets de Streamlit
        creds_dict = json.loads(st.secrets["GCP_CREDENTIALS"])
        json_file_path = "service_account.json"
        with open(json_file_path, "w") as f:
            json.dump(creds_dict, f)
        # Inicializamos EE con la cuenta de servicio configurada
        ee.Initialize(credentials=ee.ServiceAccountCredentials(creds_dict['client_email'], json_file_path))
    except Exception as e:
        st.error(f"Error de conexión con la Nube de Google: {e}")
        st.stop()

# Ejecutamos autenticación al cargar la app
authenticate_ee()

# --- 2. INTERFAZ Y CONFIGURACIÓN ---
st.set_page_config(layout="wide", page_title="Agro Data Litoral PRO")
st.title("🛰️ Agro Data Litoral: Auditoría Agronómica de Precisión")
st.markdown("---")

# Barra lateral para parámetros
col1, col2 = st.columns([1, 2])
with col1:
    st.subheader("⚙️ Parámetros")
    coord_input = st.text_input("📍 Coordenadas (Lat, Lon):", value="-32.339, -57.921")
    fecha_fin = st.date_input("📅 Fecha de análisis:")
    btn_procesar = st.button("🚀 Iniciar Auditoría Técnica")
    st.markdown("---")
    st.write("Esta herramienta procesa imágenes satelitales reales para calcular indicadores de biomasa y estrés hídrico.")

# --- 3. PROCESAMIENTO DE DATOS ---
if btn_procesar:
    try:
        lat, lon = [float(x.strip()) for x in coord_input.split(",")]
        point = ee.Geometry.Point([lon, lat])
        
        # Definimos rango de 30 días para asegurar disponibilidad de imágenes
        fecha_inicio = fecha_fin - timedelta(days=30)
        
        # Colección Sentinel-2: Salud vegetal (NDVI)
        img = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED') \
            .filterBounds(point) \
            .filterDate(str(fecha_inicio), str(fecha_fin)) \
            .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 30)) \
            .median()
        
        ndvi = img.normalizedDifference(['B8', 'B4']).rename('NDVI')
        
        # Colección MODIS: Temperatura de superficie (LST)
        temp = ee.ImageCollection('MODIS/061/MOD11A1') \
            .filterDate(str(fecha_inicio), str(fecha_fin)) \
            .mean().select('LST_Day_1km') \
            .multiply(0.02).subtract(273.15)
        
        # Extracción de valores estadísticos
        val_ndvi = ndvi.reduceRegion(ee.Reducer.mean(), point, 30).getInfo()['NDVI']
        val_temp = temp.reduceRegion(ee.Reducer.mean(), point, 1000).getInfo()['LST_Day_1km']
        
        # --- 4. VISUALIZACIÓN ---
        with col2:
            st.subheader("📊 Resultados de la Auditoría")
            kpi1, kpi2 = st.columns(2)
            kpi1.metric("Salud Vegetal (NDVI)", f"{val_ndvi:.2f}" if val_ndvi else "N/A")
            kpi2.metric("Temp. Suelo (°C)", f"{val_temp:.2f}" if val_temp else "N/A")
            
            m = leafmap.Map(center=[lat, lon], zoom=13)
            # Capas visuales
            m.add_ee_layer(ndvi, {'min': 0, 'max': 1, 'palette': ['blue', 'white', 'green']}, 'NDVI')
            m.add_marker([lat, lon], popup="Zona de Estudio")
            m.to_streamlit(height=500)
            
            st.success("Auditoría satelital finalizada.")
            
    except Exception as e:
        st.error(f"Error técnico: {e}")
