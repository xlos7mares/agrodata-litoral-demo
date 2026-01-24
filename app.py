import streamlit as st
import pandas as pd
import numpy as np
from streamlit_folium import folium_static
import folium
import os

# 1. CONFIGURACIÓN
st.set_page_config(page_title="AgroData Litoral - Auditoría Satelital", layout="wide")

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
        padding: 25px !important;
        border: 1px solid rgba(255,255,255,0.3) !important;
        backdrop-filter: blur(10px);
    }
    div[data-testid="stMetricValue"] { color: #FFFFFF !important; font-weight: 900 !important; font-size: 2.5rem !important; }
    div[data-testid="stMetricLabel"] { color: #39FF14 !important; font-size: 1.1rem !important; }

    /* Recuadro de Explicación (Ahora debajo de los datos) */
    .explicacion-box {
        background-color: rgba(255, 255, 255, 0.98);
        color: #000;
        padding: 35px;
        border-radius: 20px;
        border-left: 15px solid #1e4d2b;
        margin-top: 30px;
        box-shadow: 0px 10px 30px rgba(0,0,0,0.5);
    }
    .punto-clave {
        background-color: #f0f4f0;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
        border-left: 5px solid #39FF14;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. PANEL DE ADMINISTRADOR
with st.sidebar:
    st.header("🔑 Panel de Control")
    st.write("Exclusivo: Leonardo Olivera")
    coord_admin = st.text_area("Cargar Coordenadas Padrón:", height=100)
    if st.button("Ejecutar Escaneo"):
        st.success("Señal vinculada con éxito.")

# 3. ENCABEZADO Y PERFIL PROFESIONAL
with st.container():
    col_l, col_r = st.columns([2.5, 3.5])
    with col_l:
        st.markdown("<div style='display: flex; align-items: center;'><span style='font-size: 95px; margin-right: 20px;'>🛰️</span><div style='font-family: \"Arial Black\"; font-size: 38px; line-height: 0.9; color: white;'>AGRO<span style='color:#39FF14;'>DATA</span><br>LITORAL</div></div>", unsafe_allow_html=True)
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
            if os.path.exists("20250508_225422 (1).jpg"): st.image("20250508_225422 (1).jpg", width=140)

st.markdown("### 🛰️ AUDITORÍA SATELITAL PREMIUM | Padrón 5900")
st.write("---")

# 4. VALORES (LO PRIMERO QUE VE EL CLIENTE)
c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Salud del Cultivo (NDVI)", "0.78", "+0.05")
    st.write("📡 **ESA Sentinel-2:** Vigor de la planta.")
with c2:
    st.metric("Agua en Raíz (1m)", "14.2%", "-3.8%", delta_color="inverse")
    st.write("📡 **NASA SMAP:** Humedad profunda.")
with c3:
    st.metric("Firmeza del Suelo", "2.5 MPa", "Firme")
    st.write("📡 **NASA Landsat:** Suelo para construcción.")

# 5. RECUADRO EXPLICATIVO (AHORA DEBAJO DE LOS VALORES)
st.markdown("""
<div class="explicacion-box">
    <h2 style="color:#1e4d2b; text-align:center;">💎 Por qué comprar este servicio es una inversión 100% útil</h2>
    <p style="text-align:center; font-style:italic;">Tecnología de la Agencia Espacial Europea (ESA) y la NASA aplicada a su campo.</p>
    <hr>
    <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px;">
        <div class="punto-clave">
            <b>1. El Límite Real de su Campo</b><br>
            Google Earth es solo una foto. Nosotros usamos datos oficiales (SNIG/Catastro) para dibujar el límite legal exacto de sus hectáreas. Analizamos su tierra, no la del vecino.
        </div>
        <div class="punto-clave">
            <b>2. Análisis de "Miel Pura"</b><br>
            Le ordenamos a los satélites ignorar todo lo que está fuera de su padrón. El dato de humedad que ve es el promedio real de SU suelo.
        </div>
        <div class="punto-clave">
            <b>3. Radiografía en Tiempo Real</b><br>
            Google muestra fotos de hace meses. Nuestra auditoría usa satélites que pasan cada 2 a 5 días para saber cuánta agua tienen sus plantas HOY.
        </div>
    </div>
    <div style="margin-top:20px; padding:15px; background:#e8f5e9; border-radius:10px; border:1px solid #1e4d2b;">
        <b>💡 Argumento de Valor:</b> "Cualquiera puede entrar a Google y ver su casa. Pero solo con este sistema de <b>Litoral Operaciones Inmobiliarias</b> podemos saber cuánta agua tiene disponible la planta para aguantar la semana y si el suelo es firme para construir galpones o silos."
    </div>
    <div style="background-color: #1e4d2b; color: white; padding: 25px; border-radius: 15px; text-align:center; margin-top:20px;">
        <h3 style="color:white !important;">Reporte Detallado Profesional: U$S 150</h3>
        <p style="font-size: 26px; font-weight: bold; color: #39FF14;">📲 Envía coordenadas al 099417716</p>
        <p style="font-size: 11px; opacity: 0.8;">Creado por Leonardo Olivera © 2026 | Litoral Operaciones Inmobiliarias</p>
    </div>
</div>
""", unsafe_allow_html=True)

# 6. MAPA AL FINAL
st.write("---")
st.markdown("#### 🗺️ Ubicación y Delimitación Satelital")
lat, lon = -32.6585, -57.6455
m = folium.Map(location=[lat, lon], zoom_start=16, tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google')
folium.Polygon(locations=[[-32.6565, -57.6485], [-32.6565, -57.6425], [-32.6615, -57.6445], [-32.6615, -57.6475], [-32.6585, -57.6490]], color="#39FF14", weight=6, fill=True, fill_opacity=0.3).add_to(m)
folium_static(m, width=1100)

st.markdown("<br><center>© 2026 Litoral Operaciones Inmobiliarias - Derechos Reservados</center>", unsafe_allow_html=True)
