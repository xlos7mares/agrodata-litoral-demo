import streamlit as st
import ee
import leafmap.foliumap as leafmap

# Inicialización de Earth Engine
try:
    ee.Initialize()
except Exception:
    ee.Authenticate()
    ee.Initialize()

st.set_page_config(layout="wide", page_title="Agro Data Litoral PRO")
st.title("🛰️ Agro Data Litoral: Auditoría Agronómica")

# ... (El resto de tu código sigue igual, solo cambia el import)
# Reemplaza 'geemap.Map()' por 'leafmap.Map()'
