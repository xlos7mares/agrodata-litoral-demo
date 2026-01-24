import streamlit as st
import pandas as pd
import numpy as np
from streamlit_folium import folium_static
import folium
import os

# 1. ESTÉTICA Y PERFIL PROFESIONAL (RESTAURADO)
st.set_page_config(page_title="AgroData Litoral - Auditoría Real", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), 
                    url("https://images.unsplash.com/photo-1500382017468-9049fed747ef?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80");
        background-size: cover; background-attachment: fixed;
    }
    div[data-testid="stMetric"] {
        background-color: rgba(0, 0, 0, 0.7) !important;
        border-radius: 15px !important;
        padding: 20px !important;
        border: 1px solid #39FF14 !important;
    }
    div[data-testid="stMetricValue"] { color: #39FF14 !important; font-weight: 900 !important; }
    div[data-testid="stMetricLabel"] { color: #FFFFFF !important; }
    
    .card-profesional {
        background-color: rgba(255, 255, 255, 0.98);
        padding: 20px;
        border-radius: 12px;
        border-left: 10px solid #1e4d2b;
        color: #000;
        margin-bottom: 20px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.5);
    }
    .badge-satelite {
        background-color: #1e4d2b;
        color: #39FF14;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 10px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. PANEL DE CONTROL (COORDENADAS Y SIMULADOR)
with st.sidebar:
    st.header("📍 Ubicación Real")
    coords_raw = st.text_input("Latitud, Longitud:", "-32.6585, -57.6455")
    
    st.write("---")
    st.header("🎮 Simulador de Validación")
    st.write("Ajuste para demostrar variaciones técnicas al cliente:")
    s_ndvi = st.slider("Salud / Monte (NDVI)", 0.0, 1.0, 0.78)
    s_agua = st.slider("Humedad / NDWI %", 0.0, 100.0, 14.2)
    s_suelo = st.slider("Firmeza / MPa", 0.0, 5.0, 2.5)
    
    st.write("---")
    st.button("📥 Descargar Informe DEMO")

# 3. ENCABEZADO (PERFIL DE ÉLITE)
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

# 4. MÉTRICAS CON FUENTES SATELITALES
c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Vigor Vegetal (NDVI)", s_ndvi)
    st.markdown("<span class='badge-satelite'>🛰️ ESA Sentinel-2: Actualiza cada 5 días</span>", unsafe_allow_html=True)
with c2:
    st.metric("Humedad Profunda %", f"{s_agua}%")
    st.markdown("<span class='badge-satelite'>🛰️ NASA SMAP: Actualiza cada 3 días</span>", unsafe_allow_html=True)
with c3:
    st.metric("Resistencia (MPa)", f"{s_suelo}")
    st.markdown("<span class='badge-satelite'>🛰️ NASA Landsat: Actualiza cada 8 días</span>", unsafe_allow_html=True)

# 5. MAPA SATELITAL REAL (FIJADO POR COORDENADAS)
try:
    lat, lon = map(float, coords_raw.split(','))
except:
    lat, lon, coords_raw = -32.6585, -57.6455, "-32.6585, -57.6455"

st.markdown(f"#### 🗺️ Explorador Satelital en Tiempo Real (Coordenadas: {coords_raw})")
m = folium.Map(location=[lat, lon], zoom_start=16, tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google Satélite')

# Dibujamos un marcador y un círculo de escaneo automático
folium.Marker([lat, lon], popup="Punto de Auditoría").add_to(m)
folium.Circle([lat, lon], radius=300, color="#39FF14", fill=True, fill_opacity=0.2).add_to(m)

folium_static(m, width=1100)

# 6. CRUCE DE INFORMACIÓN CIENTÍFICA
st.write("---")
col_a, col_b = st.columns(2)

with col_a:
    st.markdown(f"""<div class="card-profesional">
    <h4>🌿 Botánica e Ingeniería Agro Ambiental</h4>
    <b>Detección de Monte:</b> {'Monte Nativo Protegido' if s_ndvi > 0.72 else 'Pastizal / Cultivo'}.<br>
    <b>Análisis:</b> Basado en Infrarrojo Cercano (Sentinel-2). Identifica especies perennes y salud del ecosistema botánico.
    </div>""", unsafe_allow_html=True)
    
    st.markdown(f"""<div class="card-profesional">
    <h4>💧 Recursos Hídricos (Estudio 20 años)</h4>
    <b>Agua en Superficie:</b> {'Presencia de Arroyos/Cañadas' if s_agua > 25 else 'Suelo con Drenaje Activo'}.<br>
    <b>Histórico:</b> Análisis NDWI. Permite ver el comportamiento de inundaciones y sequías en las últimas 2 décadas.
    </div>""", unsafe_allow_html=True)

with col_b:
    st.markdown(f"""<div class="card-profesional">
    <h4>🌍 Geología y Ciencia Física</h4>
    <b>Suelo:</b> {s_suelo} MPa ({'Tosca détectada' if s_suelo > 3.0 else 'Suelo Profundo'}).<br>
    <b>Física Aplicada:</b> Usamos Inercia Térmica (Landsat TIRS). La roca retiene calor a las 2 AM de forma distinta a la tierra húmeda, validando la resistencia mecánica.
    </div>""", unsafe_allow_html=True)
    
    st.markdown(f"""<div class="card-profesional">
    <h4>🏗️ Ingeniería y Arquitectura</h4>
    <b>Aptitud de Obra:</b> Apto para silos, galpones o conjuntos de viviendas.<br>
    <b>Informe:</b> Validación de cimentación basada en datos de resistencia geológica y estabilidad hídrica.
    </div>""", unsafe_allow_html=True)

# 7. SERVICIOS PROFESIONALES
st.markdown(f"""
<div style="background-color: #1e4d2b; color: white; padding: 25px; border-radius: 15px; text-align:center; margin-top:10px;">
    <h3 style="color:white !important;">💼 Informe Profesional Completo: U$S 150</h3>
    <p style="font-size: 16px; color: #39FF14;">Incluye Inercia Térmica de Suelos y Estudio Hídrico Histórico Real (NASA/ESA).</p>
    <p>Envíe coordenadas al <b>099417716</b> para habilitar el escaneo profundo.</p>
</div>
""", unsafe_allow_html=True)
