import streamlit as st
import folium
from streamlit_folium import st_folium
import numpy as np
import pandas as pd
import requests

# =====================================================================
# 🛰️ CONFIGURACIÓN DE LA PÁGINA E IDENTIDAD VISUAL EXECUTIVE GOLD
# =====================================================================
st.set_page_config(
    page_title="Agro Data Litoral PRO",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main { background-color: #111111; color: #FFFFFF; }
    h1, h2, h3, h4 { color: #D4AF37 !important; font-family: 'Helvetica Neue', sans-serif; }
    .stButton>button {
        background-color: #D4AF37;
        color: #111111;
        font-weight: bold;
        border-radius: 5px;
        border: none;
        width: 100%;
        padding: 10px;
        transition: 0.3s;
    }
    .stButton>button:hover { background-color: #AA8515; color: #FFFFFF; }
    div[data-testid="stMetricValue"] { color: #D4AF37 !important; font-weight: bold; }
    .report-box {
        border: 1px solid #D4AF37;
        padding: 18px;
        border-radius: 5px;
        background-color: #1a1a1a;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# =====================================================================
# 🌤️ FUNCIÓN PARA OBTENER CLIMA REAL (INTEGRACIÓN NUEVA)
# =====================================================================
def obtener_clima_real(lat, lon):
    try:
        api_key = st.secrets["OPENWEATHER_API_KEY"]
        url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric&lang=es"
        res = requests.get(url).json()
        temp = res['main']['temp']
        hum = res['main']['humidity']
        viento = res['wind']['speed'] * 3.6
        return temp, hum, viento
    except:
        return 0.0, 0.0, 0.0

# =====================================================================
# 🏢 PANEL LATERAL
# =====================================================================
st.sidebar.image("https://img.icons8.com/plots/100/D4AF37/satellite.png", width=70)
st.sidebar.markdown("# AGRO DATA LITORAL")
st.sidebar.markdown("### **Leonardo Olivera**")
st.sidebar.markdown("*Estudiante de Agronomía | Perito en Granos | Software e IA Aplicada*")
st.sidebar.markdown("---")

opcion_menu = st.sidebar.radio(
    "Seleccione el módulo de trabajo:",
    ["🛰️ Consola de Auditoría Satelital y Suelos", "📐 Laboratorio de Funciones Matemáticas Especiales"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style='background-color: #1a1a1a; padding: 10px; border-radius: 5px; border: 1px solid #D4AF37;'>
📞 <b>Contacto Directo Uruguay:</b><br>
<span style='color: #D4AF37; font-size: 14pt;'><b>099 417 716</b></span><br>
📍 <i>Búnker Analítico Base, Paysandú</i>
</div>
""", unsafe_allow_html=True)

# =====================================================================
# 🛰️ MÓDULO PRINCIPAL: AUDITORÍA SATELITAL, SUELOS Y CLIMA
# =====================================================================
if opcion_menu == "🛰️ Consola de Auditoría Satelital y Suelos":
    st.title("🛰️ Consola de Analítica y Auditoría Agronómica")
    st.markdown("### Diagnóstico Espacial, Edafológico e Hidrológico por Coordenadas GPS")
    st.markdown("---")

    coordenadas_input = st.text_input("📍 Ingrese Coordenadas GPS (Latitud, Longitud):", value="-32.339063, -57.921296")
    procesar_auditoria = st.button("🚀 Iniciar Escaneo y Consulta Satelital Cloud")

    lat, lon = -32.339063, -57.921296
    try:
        partes = coordenadas_input.split(",")
        lat, lon = float(partes[0].strip()), float(partes[1].strip())
    except:
        st.error("❌ Formato de coordenadas inválido.")

    # --- Lógica de cálculo original ---
    es_punto_urbano = (abs(lat - (-32.3181)) < 0.005 and abs(lon - (-58.0799)) < 0.005)
    if es_punto_urbano:
        ndvi, evi, ndwi, ndre, lst, biomasa = 0.22, 0.19, 0.35, 0.16, 21.0, 0.8
        temp_aire, humedad_aire, viento, delta_t, vertiente = 11.59, 87, 23.4, 1.4, 12.8
        grupo_coneat, suelo_tipo, uso_suelo = "12", "Brunosoles", "Urbano"
        tesis_narrativa = "ANÁLISIS EDAFOLÓGICO Y SATELITAL: Firma de cobertura artificial."
        sugerencia_campo = "Terreno no apto para cultivos extensivos."
    else:
        ndvi, evi, ndwi, ndre, lst, biomasa = 0.61, 0.52, 0.42, 0.46, 14.3, 7.3
        temp_aire, humedad_aire, viento, delta_t, vertiente = 10.78, 86, 21.6, 1.5, 12.6
        grupo_coneat, suelo_tipo = "12", "Brunosoles Típicos del Litoral"
        tesis_narrativa = "ANÁLISIS EDAFOLÓGICO: Excelente saturación de bases, AU limitada a 60,000 L/Ha."
        sugerencia_campo = "Priorizar siembra directa estricta."

    # --- INTEGRACIÓN CLIMA REAL ---
    if procesar_auditoria:
        temp_aire, humedad_aire, viento = obtener_clima_real(lat, lon)

    st.markdown("### 🗺️ Georreferenciación Satelital")
    m = folium.Map(location=[lat, lon], zoom_start=14)
    folium.Marker([lat, lon]).add_to(m)
    st_folium(m, width=900, height=350)
    
    st.markdown("### 🌡️ Telemetría Atmosférica")
    col_c1, col_c2, col_c3, col_c4 = st.columns(4)
    col_c1.metric("TEMP. AIRE", f"{temp_aire:.1f} °C")
    col_c2.metric("HUMEDAD REL.", f"{humedad_aire:.0f} %")
    col_c3.metric("VEL. VIENTO", f"{viento:.1f} km/h")
    col_c4.metric("DELTA T (ΔT)", f"{delta_t}")
    
    # ... (Aquí mantienes todos tus bloques de NDVI, CIC, Suelos y Tesis intactos)
    st.info(tesis_narrativa)
    st.success(f"🌱 {sugerencia_campo}")

# =====================================================================
# 📐 MÓDULO: LABORATORIO DE FUNCIONES MATEMÁTICAS
# =====================================================================
elif opcion_menu == "📐 Laboratorio de Funciones Matemáticas Especiales":
    # ... (Aquí insertas exactamente todo tu código de los 3 algoritmos originales: Relieve, CIC y Biótico)
    st.write("Tu código original de algoritmos va aquí intacto.")
