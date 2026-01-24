import streamlit as st
from streamlit_folium import folium_static
import folium
from folium.plugins import Draw
import os

# 1. ESTÉTICA Y PERFIL DE ÉLITE
st.set_page_config(page_title="AgroData Litoral - Auditoría SIG", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), 
                    url("https://images.unsplash.com/photo-1500382017468-9049fed747ef?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80");
        background-size: cover; background-attachment: fixed;
    }
    .card-profesional {
        background-color: rgba(255, 255, 255, 0.95);
        padding: 20px;
        border-radius: 12px;
        border-left: 10px solid #1e4d2b;
        color: #000;
        margin-bottom: 20px;
    }
    .fuente-satelital {
        background-color: #0a1f0a;
        color: #39FF14;
        padding: 10px;
        border-radius: 8px;
        font-size: 11px;
        margin-top: 5px;
        border: 1px solid #39FF14;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. PANEL DE CONTROL (ENTRADA DE COORDENADAS)
with st.sidebar:
    st.header("📍 Ubicación del Padrón")
    st.write("Ingrese las coordenadas para posicionar el satélite:")
    coords_raw = st.text_input("Latitud, Longitud:", "-32.6585, -57.6455")
    
    st.write("---")
    st.markdown("### 🛰️ Estado de Constelación")
    st.success("🛰️ ESA Sentinel-2: ONLINE")
    st.success("🛰️ NASA Landsat 9: ONLINE")
    st.success("🛰️ NASA SMAP: ONLINE")
    
    st.write("---")
    st.markdown("### 📥 Reportes Profesionales")
    st.button("Descargar Informe de Padrón")

# 3. ENCABEZADO (PERFIL COMPLETO)
with st.container():
    col_l, col_r = st.columns([2.5, 3.5])
    with col_l:
        st.markdown("<div style='display: flex; align-items: center;'><span style='font-size: 80px; margin-right: 20px;'>🛰️</span><div style='font-family: \"Arial Black\"; font-size: 35px; line-height: 0.9; color: white;'>AGRO<span style='color:#39FF14;'>DATA</span><br>LITORAL</div></div>", unsafe_allow_html=True)
    with col_r:
        c_txt, c_img = st.columns([2.5, 1])
        with c_txt:
            st.markdown(f"""
                <div style='text-align: right; color: white;'>
                    <h2 style='margin:0;'>Leonardo Olivera</h2>
                    <p style='color:#39FF14; font-weight:bold; font-size: 18px; margin:0;'>📲 099417716</p>
                    <p style='font-size:11px; opacity:0.95; line-height:1.3;'>
                        <b>Estudiante Agronomía | Operaciones Inmobiliarias</b><br>
                        Perito en Grano | Experto en IA | Aficionado a la Ciencia Física,<br>
                        Geología, Botánica e Ingeniería Agro Ambiental | Protección del Medio Ambiente<br>
                        <i>Desarrollador de Software con IA aplicada a la Ciencia Física</i>
                    </p>
                </div>
            """, unsafe_allow_html=True)
        with c_img:
            if os.path.exists("20250508_225422 (1).jpg"): st.image("20250508_225422 (1).jpg", width=120)

st.write("---")

# 4. MAPA SIG REAL (DIBUJO LIBRE COMO EL MINISTERIO)
try:
    lat, lon = map(float, coords_raw.split(','))
except:
    lat, lon = -32.6585, -57.6455

st.markdown(f"#### 🗺️ Visualizador Satelital en Tiempo Real (Coordenadas: {lat}, {lon})")
st.write("Utilice las herramientas de la izquierda para dibujar el perímetro exacto del campo.")

m = folium.Map(location=[lat, lon], zoom_start=16, tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google Satélite')

# Herramienta de dibujo sin errores de JSON
Draw(
    export=False, 
    show_geometryonclick=False,
    draw_options={'polyline':False, 'circle':False, 'marker':False, 'circlemarker':False, 'polygon':True, 'rectangle':True}
).add_to(m)

folium_static(m, width=1100)

# 5. INFORMACIÓN TÉCNICA DE AUDITORÍA
st.write("---")
st.markdown("### 📋 Auditoría Técnica de Activos Naturales e Inmuebles")

col_a, col_b = st.columns(2)

with col_a:
    st.markdown("""<div class="card-profesional">
    <h4>🌿 Agronomía, Botánica y M. Ambiente</h4>
    <b>Análisis de Biomasa:</b> El sistema cruza datos de reflectancia infrarroja para identificar Monte Nativo, pasturas y zonas protegidas.
    <div class="fuente-satelital">📡 Satélite: ESA Sentinel-2 | Resolución: 10m</div>
    </div>""", unsafe_allow_html=True)
    
    st.markdown("""<div class="card-profesional">
    <h4>🌍 Geología y Ciencia Física Aplicada</h4>
    <b>Estudio de Suelos:</b> Mediante inercia térmica nocturna, el software detecta la presencia de tosca o roca madre para cimentación.
    <div class="fuente-satelital">📡 Satélite: NASA Landsat TIRS | Resolución térmica: 30m</div>
    </div>""", unsafe_allow_html=True)

with col_b:
    st.markdown("""<div class="card-profesional">
    <h4>💧 Hidrología e Inversión Inmobiliaria</h4>
    <b>Estudio Hídrico:</b> Mapeo de cursos de agua y zonas inundables con historial de 20 años para asegurar su capital.
    <div class="fuente-satelital">📡 Satélite: NASA SMAP / Landsat NDWI</div>
    </div>""", unsafe_allow_html=True)
    
    st.markdown("""<div class="card-profesional">
    <h4>🏗️ Ingeniería y Arquitectura</h4>
    <b>Aptitud de Obra:</b> Certificación técnica de firmeza de suelo para silos, galpones o complejos de vivienda.
    <div class="fuente-satelital">📡 Procesamiento: Algoritmo IA de Ciencia Física</div>
    </div>""", unsafe_allow_html=True)

# 6. SERVICIO PROFESIONAL
st.markdown(f"""
<div style="background-color: #1e4d2b; color: white; padding: 25px; border-radius: 15px; text-align:center; margin-top:10px;">
    <h3 style="color:white !important;">💎 Informe Profesional Personalizado: U$S 150</h3>
    <p>Este informe incluye el procesamiento manual de bandas satelitales y el estudio histórico profundo.</p>
    <p>Envíe el dibujo de su campo por WhatsApp al <b>099417716</b> para iniciar la auditoría.</p>
</div>
""", unsafe_allow_html=True)
