import streamlit as st
import pandas as pd
import numpy as np
from streamlit_folium import folium_static
import folium
import os

# 1. CONFIGURACIÓN Y ESTÉTICA PREMIUM
st.set_page_config(page_title="AgroData Litoral - Auditoría Satelital", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.3), rgba(0,0,0,0.3)), 
                    url("https://images.unsplash.com/photo-1500382017468-9049fed747ef?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80");
        background-size: cover; background-attachment: fixed;
    }
    .perfil-box { text-align: right; color: white; line-height: 1.2; }
    .card-profesional {
        background-color: rgba(245, 245, 245, 0.98);
        padding: 20px;
        border-radius: 12px;
        border-top: 5px solid #1e4d2b;
        color: #000;
        margin-bottom: 15px;
    }
    /* Estilo para la Declaración Técnica */
    .transparencia-box {
        background-color: #0a1f0a;
        color: #e0e0e0;
        padding: 30px;
        border-radius: 15px;
        border: 1px solid #39FF14;
        margin-top: 30px;
        line-height: 1.6;
    }
    .highlight-verde { color: #39FF14; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. BARRA LATERAL (SIMULADOR DE EJEMPLOS)
with st.sidebar:
    st.header("⚙️ MODO SIMULACRO")
    st.write("Seleccione un escenario para ver cómo responde la inteligencia satelital:")
    escenario = st.radio("Escenarios de Ejemplo:", 
                         ["Salud Vegetal / Monte", "Detección de Agua", "Detección de Tosca"])
    
    if escenario == "Salud Vegetal / Monte":
        s_ndvi, s_agua, s_suelo = 0.82, 12.0, 1.8
    elif escenario == "Detección de Agua":
        s_ndvi, s_agua, s_suelo = 0.45, 65.0, 1.2
    else: # Tosca
        s_ndvi, s_agua, s_suelo = 0.35, 8.0, 4.2

    st.write("---")
    st.header("📍 Carga de Padrón")
    coord_input = st.text_area("Coordenadas Reales (Para Auditoría Final):", "-32.6585, -57.6455")
    if st.button("Vincular con Satélite"):
        st.info("Esperando coordenadas correctas del campo real...")

# 3. ENCABEZADO (PERFIL PROFESIONAL)
with st.container():
    col_l, col_r = st.columns([2.5, 3.5])
    with col_l:
        st.markdown("<h1 style='color:white; margin:0;'>AGRO<span style='color:#39FF14;'>DATA</span> LITORAL</h1>", unsafe_allow_html=True)
    with col_r:
        st.markdown(f"""
            <div class="perfil-box">
                <h2 style="margin:0;">Leonardo Olivera</h2>
                <p style="color:#39FF14; font-weight:bold; font-size:20px; margin:0;">📲 099417716</p>
                <p style="font-size:12px; opacity:0.9;">Perito en Grano | Experto en IA | Agronomía | Inmobiliaria</p>
            </div>
        """, unsafe_allow_html=True)

st.write("---")

# 4. MÉTRICAS DINÁMICAS
c1, c2, c3 = st.columns(3)
c1.metric("Salud (NDVI)", s_ndvi)
c2.metric("Humedad %", f"{s_agua}%")
c3.metric("Firmeza (MPa)", s_suelo)

# 5. LÓGICA DEL MAPA (COLORES POR EJEMPLO)
if escenario == "Salud Vegetal / Monte":
    color_mapa = "#228B22" # Verde Bosque
    label_mapa = "🌳 MONTE NATIVO DETECTADO"
elif escenario == "Detección de Agua":
    color_mapa = "#0000FF" # Azul
    label_mapa = "💧 CURSO DE AGUA DETECTADO"
else:
    color_mapa = "#8B4513" # Marrón
    label_mapa = "🪨 AFLORAMIENTO DE TOSCA DETECTADO"

# 6. MAPA Y LEYENDA
st.markdown(f"#### 🗺️ Mapa de Auditoría: {label_mapa}")
lat, lon = -32.6585, -57.6455
m = folium.Map(location=[lat, lon], zoom_start=16, tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google')
folium.Polygon(
    locations=[[-32.6565, -57.6485], [-32.6565, -57.6425], [-32.6615, -57.6445], [-32.6615, -57.6475], [-32.6585, -57.6490]],
    color=color_mapa, weight=5, fill=True, fill_opacity=0.4
).add_to(m)
folium_static(m, width=1100)

# 7. DECLARACIÓN TÉCNICA (TU TEXTO DE TRANSPARENCIA)
st.markdown(f"""
<div class="transparencia-box">
    <h3 style="color:#39FF14; text-align:center;">📋 Verdad Técnica: Del Simulacro a la Auditoría Real</h3>
    <p>Como profesional, mi activo más valioso es la <b>credibilidad</b>. Lo que observa arriba es un simulacro interactivo para mostrar la capacidad del tablero de control. Una vez insertadas las coordenadas reales, el sistema realiza una consulta en tiempo vivo mediante conexiones directas (API).</p>
    
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
        <div>
            <h4 class="highlight-verde">1. La Diferencia Crucial</h4>
            <p style="font-size:13px;"><b>Hoy:</b> Un simulador técnico para demostrar qué es capaz de hacer el software.<br>
            <b>Realidad:</b> Conectamos con servicios como <i>Google Earth Engine</i> o <i>Sentinel Hub</i> para obtener los datos exactos del Padrón de ayer mismo.</p>
        </div>
        <div>
            <h4 class="highlight-verde">2. ¿Cómo se logra la Verdad Satelital?</h4>
            <ul style="font-size:13px;">
                <li><span class="highlight-verde">Monte Nativo:</span> Banda 8 (Infrarrojo Cercano). Valor > 0.7 persistente indica monte real.</li>
                <li><span class="highlight-verde">Agua (NDWI):</span> Absorción de infrarrojo. El valor negativo confirma agua física en el suelo.</li>
                <li><span class="highlight-verde">Tosca:</span> Detección por Inercia Térmica. La roca retiene calor a las 2 AM de forma distinta a la tierra.</li>
            </ul>
        </div>
    </div>
    <p style="text-align:center; font-weight:bold; margin-top:15px; border-top: 1px solid #39FF14; padding-top:10px;">
        Este nivel de precisión justifica la inversión de u$s 150 por el acceso a datos nivel 1 a 4 de la NASA/ESA.
    </p>
</div>
""", unsafe_allow_html=True)

# 8. PIE DE PÁGINA
st.markdown("<br><center style='color:white;'>© 2026 Litoral Operaciones Inmobiliarias | Leonardo Olivera</center>", unsafe_allow_html=True)
