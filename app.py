import streamlit as st
import ee
import json
import leafmap.foliumap as leafmap

# 1. Cargar credenciales desde los secretos
creds_dict = json.loads(st.secrets["GCP_CREDENTIALS"])

# 2. Inicialización directa (sin archivos externos)
# Usamos ServiceAccountCredentials pasando el diccionario directamente
credentials = ee.ServiceAccountCredentials(
    email=creds_dict['client_email'], 
    key=creds_dict['private_key']
)

# Inicializar con las credenciales cargadas
ee.Initialize(credentials=credentials)

# ... (El resto de tu código sigue igual)
