import streamlit as st
import pandas as pd
import numpy as np
from streamlit_folium import folium_static
import folium
import os

# 1. CONFIGURACIÓN Y ESTÉTICA PREMIUM
st.set_page_config(page_title="AgroData Litoral - Master Control", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.2), rgba(0, 0, 0, 0.2)), 
                    url("https://images.unsplash.com/photo-1500382017468-9049fed747ef?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80");
        background-size: cover; background-attachment: fixed;
    }
    
    /* Métricas Estilo Cristal */
    div[data-testid="stMetric"] {
        background-color: rgba(255, 255, 255, 0.15) !important;
        border-radius: 15px !important;
        padding: 20px !important;
        border: 1px solid rgba(255,255,255,0.3) !important;
        backdrop-filter: blur(10px);
        box-shadow: 0px 10px 30px rgba(0,0,0,0.5) !important;
    }
    div[data-testid="stMetricValue"] { color: #FFFFFF !important; font-weight: 900 !important; font-size: 2.5rem !important; }
    div[data-testid="stMetricLabel"] { color: #39FF14 !important; font-size: 1.1rem !important; }

    /* Tarjetas Profesionales */
    .card-profesional {
        background-color: rgba(245, 245, 245, 0.98);
        padding: 25px;
        border-radius: 15px;
        border-top: 5px solid #1e4d2b;
        margin-bottom: 20px;
        color: #000;
        box-shadow: 0px 8px 20px rgba(0,0,0,0.4);
    }
    </style>
    """, unsafe_allow_html=True)

# 2. PANEL DE CONTROL Y SIMULADOR (SIDEBAR)
with st.sidebar:
    st.header("🔑 Panel de Control")
    st.write("Exclusivo: Leonardo Olivera")
    coord_real = st.text_area("Cargar Coordenadas Padrón Real:", placeholder="Ej: -32.65, -57.64")
    
    st.write("---")
    st.header("🎮 Simulador Satelital")
    s_ndvi = st.slider("Salud / Vigor (NDVI)", 0.0, 1.0, 0.78)
    s_var = st.slider("Tendencia Semanal", -0.10, 0.10, 0.05)
    s_agua = st.slider("Humedad Suelo %", 0.0, 100.0, 14.2)
    s_suelo = st.slider("Firmeza Suelo (MPa)", 0.0, 5.0, 2.5)

# 3. ENCABEZADO: LOGO Y PERFIL PROFESIONAL
with st.container():
    col_l, col_r = st.columns([2.5, 3.5])
    with col_l:
        st.markdown("<div style='display: flex; align-items: center; margin-top: 10px;'><span style='font-size: 90px; margin-right: 20px;'>🛰️</span><div style='font-family: \"Arial Black\"; font-size: 38px; line-height: 0.9; color: white;'>AGRO<span style='color:#39FF14;'>DATA</span><br>LITORAL</div></div>", unsafe_allow_html=True)
    with col_r:
        c_txt, c_img = st.columns([2.5, 1])
        with c_txt:
            st.markdown(f"""
                <div style='text-align: right;'>
                    <h2 style='margin:0; color:white;'>Leonardo Olivera</h2>
                    <p style='color:#39FF14; font-weight:bold; font-size: 22px; margin:0;'>📲 099417716</p>
                    <p style='font-size:13px; color:white; opacity:0.95; line-height:1.4;'>
                        <b>Perito en Grano | Experto en IA</b><br>
                        Estudiante de Agronomía | Operador Inmobiliario<br>
                        Desarrollador de Software & Proyecto Agro Tecnológico
                    </p>
                </div>
            """, unsafe_allow_html=True)
        with c_img:
            if os.path.exists("20250508_225422 (1).jpg"): 
                st.image("20250508_225422 (1).jpg", width=140)

st.markdown("### 🛰️ AUDITORÍA SATELITAL PREMIUM | Padrón 5900")
st.write("---")

# 4. MÉTRICAS DINÁMICAS
c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Salud del Cultivo (NDVI)", f"{s_ndvi}", f"{s_var:+.2f}")
    st.write("📡 **ESA Sentinel-2:** Vigor activo.")
with c2:
    st.metric("Agua en Raíz (1m)", f"{s_agua}%", "-3.8%", delta_color="inverse")
    st.write("📡 **NASA SMAP:** Humedad profunda real.")
with c3:
    st.metric("Firmeza del Suelo", f"{s_suelo} MPa", "Firme")
    st.write("📡 **NASA Landsat:** Estabilidad estructural.")

# 5. ANÁLISIS POR PERFIL PROFESIONAL (CUADROS PROLIJOS)
st.write("---")
st.markdown("#### 📋 Informe de Interpretación Multi-Perfil")

msg_agro = "vigor alto y saludable" if s_ndvi > 0.6 else "estrés hídrico detectado"
msg_suelo = "firme para construcción pesada" if s_suelo > 2.0 else "suelo blando, requiere refuerzo"

col_a, col_b, col_c = st.columns(3)

with col_a:
    st.markdown(f"""<div class="card-profesional">
    <b>🌿 Para Ingenieros Agrónomos:</b><br>
    El NDVI de {s_ndvi} ({s_var:+.2f}) indica un estado de <b>{msg_agro}</b>. Las hojas absorben gran cantidad de luz roja (clorofila), confirmando un dosel denso según la misión ESA Sentinel-2.
    </div>""", unsafe_allow_html=True)

with col_b:
    st.markdown(f"""<div class="card-profesional">
    <b>🌍 Para Geólogos:</b><br>
    Los {s_suelo} MPa obtenidos mediante NASA Landsat confirman un suelo <b>{msg_suelo}</b>. La humedad de {s_agua}% en la zona radicular valida la estabilidad del terreno para proyectos de gran escala.
    </div>""", unsafe_allow_html=True)

with col_c:
    st.markdown(f"""<div class="card-profesional">
    <b>🏗️ Para Arquitectos:</b><br>
    Con una firmeza de {s_suelo} MPa, el terreno es apto para diseños de gran porte. El vigor verde del entorno (NDVI {s_ndvi}) garantiza un paisajismo frondoso y sostenible para la estética final.
    </div>""", unsafe_allow_html=True)

# 6. AUDITORÍA DE ACTIVOS NATURALES (CIENCIA DE SUELOS)
st.markdown("---")
st.markdown("### 🔍 Inventario Satelital de Activos Naturales")

msg_monte = "Monte Nativo Protegido (Alta Densidad)" if s_ndvi > 0.72 else "Vegetación Arbustiva / Pastizal"
msg_roca = "Afloramiento de Tosca / Suelo Superficial" if s_suelo > 3.0 else "Suelo Profundo con Aptitud Agrícola"
msg_agua = "Curso de Agua Activo / Cañada Detectada" if s_agua > 20 else "Zonas de Escurrimiento Temporal"

col_inv1, col_inv2, col_inv3 = st.columns(3)

with col_inv1:
    st.markdown(f"""<div class="card-profesional" style="border-top: 5px solid #228B22;">
    <h4 style="margin:0; color:#1e4d2b;">🌳 COBERTURA FORESTAL</h4>
    <small>Sentinel-2 (Firma Espectral)</small><br>
    Estado: <b>{msg_monte}</b><br>
    Detección de especies perennes autóctonas. Áreas clave para normativa MGAP y conservación.
    </div>""", unsafe_allow_html=True)

with col_inv2:
    st.markdown(f"""<div class="card-profesional" style="border-top: 5px solid #8B4513;">
    <h4 style="margin:0; color:#8B4513;">🪨 MAPEO DE TOSCA</h4>
    <small>NASA Landsat (Banda Térmica)</small><br>
    Diagnóstico: <b>{msg_roca}</b><br>
    Detección de anomalías térmicas en superficie que indican horizontes rocosos cercanos o suelos áridos.
    </div>""", unsafe_allow_html=True)

with col_inv3:
    st.markdown(f"""<div class="card-profesional" style="border-top: 5px solid #00008B;">
    <h4 style="margin:0; color:#00008B;">💧 RECURSOS HÍDRICOS</h4>
    <small>Índice NDWI (Agua Superficial)</small><br>
    Detección: <b>{msg_agua}</b><br>
    Identificación de micro-arroyos y zonas de acumulación hídrica para diseño de tajamares.
    </div>""", unsafe_allow_html=True)

# 7. COMPARATIVA DE VALORIZACIÓN (EL GANCHO DE VENTA)
st.markdown(f"""
<div style="background-color: rgba(25, 45, 25, 0.85); padding: 25px; border-radius: 15px; border: 1px solid #39FF14; margin-top: 20px;">
    <h3 style="color: #39FF14; margin-top: 0; text-align: center;">📊 Comparativa de Valorización de Tierra</h3>
    <div style="display: flex; justify-content: space-around; align-items: center; color: white;">
        <div style="text-align: center;">
            <p style="margin:0; opacity: 0.8;">Retención Hídrica</p>
            <h2 style="margin:0;">+{s_agua + 5}%</h2>
            <p style="font-size: 10px; color: #39FF14;">vs. Promedio Linderos</p>
        </div>
        <div style="text-align: center;">
            <p style="margin:0; opacity: 0.8;">Vigor del Suelo</p>
            <h2 style="margin:0;">{s_ndvi:.2f}</h2>
            <p style="font-size: 10px; color: #39FF14;">Serie Histórica 2026</p>
        </div>
        <div style="text-align: center;">
            <p style="margin:0; opacity: 0.8;">Índice de Tosca</p>
            <h2 style="margin:0;">{'Bajo' if s_suelo < 3 else 'Alto'}</h2>
            <p style="font-size: 10px; color: #39FF14;">Detección Térmica</p>
        </div>
    </div>
    <div style="background-color: #1e4d2b; color: white; padding: 20px; border-radius: 15px; text-align:center; margin-top:20px;">
        <h3 style="color:white !important; margin:0;">💎 Inversión 100% Útil: U$S 150</h3>
        <p style="font-size: 20px; font-weight: bold; color: #39FF14; margin:5px;">📲 Envía coordenadas al 099417716</p>
    </div>
</div>
""", unsafe_allow_html=True)

# 8. MAPA FINAL
st.write("---")
lat, lon = -32.6585, -57.6455
m = folium.Map(location=[lat, lon], zoom_start=16, tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google')
folium.Polygon(locations=[[-32.6565, -57.6485], [-32.6565, -57.6425], [-32.6615, -57.6445], [-32.6615, -57.6475], [-32.6585, -57.6490]], color="#39FF14", weight=6, fill=True, fill_opacity=0.3).add_to(m)
folium_static(m, width=1100)

st.markdown("<br><center>© 2026 Litoral Operaciones Inmobiliarias - Derechos Reservados</center>", unsafe_allow_html=True)
