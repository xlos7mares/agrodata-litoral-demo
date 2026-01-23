import streamlit as st
import pandas as pd
import numpy as np
from streamlit_folium import folium_static
import folium
from fpdf import FPDF
import os

# 1. CONFIGURACIÓN Y ESTÉTICA DE ALTA PRECISIÓN
st.set_page_config(page_title="AgroData Litoral - Auditoría Premium", layout="wide")

st.markdown("""
    <style>
    /* Fondo de campo vivo */
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.1), rgba(0, 0, 0, 0.2)), 
                    url("https://images.unsplash.com/photo-1500382017468-9049fed747ef?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80");
        background-size: cover;
        background-attachment: fixed;
    }
    
    /* Recuadros de Datos Delicados (Efecto Cristal) */
    div[data-testid="stMetric"] {
        background-color: rgba(255, 255, 255, 0.95) !important;
        border-radius: 12px !important;
        padding: 20px !important;
        border-left: 10px solid #28a745 !important;
        box-shadow: 0px 10px 25px rgba(0,0,0,0.3) !important;
    }
    /* Forzar texto negro en métricas para legibilidad sobre blanco */
    div[data-testid="stMetricLabel"], div[data-testid="stMetricValue"], div[data-testid="stMetricDelta"] {
        color: #000000 !important;
        font-weight: bold !important;
    }

    /* Panel Informativo Inferior */
    .info-box-final {
        background-color: rgba(0, 0, 0, 0.85);
        color: white;
        padding: 35px;
        border-radius: 20px;
        border: 2px solid #39FF14;
        margin-top: 30px;
    }

    .perfil-text {
        text-align: right;
        color: white;
        text-shadow: 2px 2px 4px #000;
    }

    h1, h2, h3, h4 { color: white !important; text-shadow: 2px 2px 5px black; }
    </style>
    """, unsafe_allow_html=True)

# 2. ENCABEZADO ALINEADO
with st.container():
    col_izq, col_der = st.columns([2.5, 3])
    with col_izq:
        st.markdown("""
            <div style="display: flex; align-items: center; margin-top: 10px;">
                <span style="font-size: 80px; margin-right: 20px;">🛰️</span>
                <div style="font-family: 'Arial Black'; font-size: 35px; line-height: 0.9; color: white;">
                    AGRO<span style="color:#39FF14;">DATA</span><br>LITORAL
                </div>
            </div>
        """, unsafe_allow_html=True)
    with col_der:
        c_text, c_img = st.columns([2, 1])
        with c_text:
            st.markdown(f"""
                <div class="perfil-text">
                    <h2 style="margin:0; font-size: 28px;">Leonardo Olivera</h2>
                    <p style="margin:0; color:#39FF14; font-weight:bold; font-size: 20px;">📲 099417716</p>
                    <p style="font-size:12px; line-height:1.3; opacity: 0.9;">
                        Desarrollador de Software & Proyecto Agro Tecnológico<br>
                        Estudiante de Agronomía | Experto Informático (+20 años exp.)<br>
                        Perito en Grano | Operador Inmobiliario | Especialista en IA
                    </p>
                </div>
            """, unsafe_allow_html=True)
        with c_img:
            foto_path = "20250508_225422 (1).jpg"
            if os.path.exists(foto_path):
                st.image(foto_path, width=130)

st.markdown("### 🛰️ AUDITORÍA SATELITAL DE PRECISIÓN | SERVICIO PREMIUM")
st.write("---")

# 3. TABS TÉCNICAS
tabs = st.tabs(["📊 MÉTRICAS CIENTÍFICAS", "🗺️ MAPA DE TERRENO", "🔬 CIENCIA APLICADA"])

with tabs[0]:
    st.markdown("#### 🔬 Análisis de Horizonte y Biomasa")
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Salud (NDVI)", "0.78", "+0.05", help="Indice de vigor fotosintético.")
    with c2: st.metric("Humedad Perfil", "14.2%", "-3.8%", delta_color="inverse", help="Escaneo SMAP a 1m.")
    with c3: st.metric("Suelo (MPa)", "2.5", "Firme", help="Resistencia mecánica para carga.")
    with c4: st.metric("Evaporación", "5.2 mm", help="Pérdida hídrica diaria.")

with tabs[1]:
    lat, lon = -32.6585, -57.6455
    m = folium.Map(location=[lat, lon], zoom_start=16, tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google')
    folium.Polygon(locations=[[-32.6565, -57.6485], [-32.6565, -57.6425], [-32.6615, -57.6445], [-32.6615, -57.6475], [-32.6585, -57.6490]], 
                   color="#39FF14", weight=5, fill=True, fill_opacity=0.2).add_to(m)
    folium_static(m, width=1100)

with tabs[2]:
    st.info("Sincronización total con: **MGAP, SNIG, DIEA, INIA e OPYPA (Uruguay)**.")

# 4. SECCIÓN EXPLICATIVA CORREGIDA (SIN ERRORES DE CÓDIGO VISIBLE)
st.markdown("""
<div class="info-box-final">
    <h2 style='color:#39FF14 !important; text-align:center;'>📊 ¿Por qué elegir AgroData Litoral?</h2>
    <p style='text-align:center;'><i>Diferencias críticas entre una imagen común y una Auditoría de Inteligencia Espacial</i></p>
    
    <div style='display: flex; flex-wrap: wrap; gap: 20px; margin-top:20px;'>
        <div style='flex: 1; min-width: 250px;'>
            <h4 style='color:#39FF14 !important;'>1. Geometría Oficial</h4>
            <p style='font-size:14px;'>Google Earth es una imagen plana. Nuestro sistema extrae el <b>Límite de Padrón</b> real mediante coordenadas oficiales. El análisis es exclusivo de su tierra, eliminando errores por campos linderos.</p>
        </div>
        <div style='flex: 1; min-width: 250px;'>
            <h4 style='color:#39FF14 !important;'>2. Análisis Específico</h4>
            <p style='font-size:14px;'>A diferencia de sistemas generales, hacemos un <b>recorte de máscara</b>. Los satélites analizan píxel por píxel dentro de su campo, entregando promedios reales de humedad y vigor del cultivo.</p>
        </div>
        <div style='flex: 1; min-width: 250px;'>
            <h4 style='color:#39FF14 !important;'>3. Auditoría vs. Foto</h4>
            <p style='font-size:14px;'>Google ofrece fotos históricas. AgroData entrega una <b>radiografía actual</b>. Detectamos lo invisible: estrés hídrico profundo y resistencia mecánica para inversiones en infraestructura.</p>
        </div>
    </div>
    
    <div style='background: rgba(57, 255, 20, 0.1); padding: 25px; border-radius: 15px; border: 1px dashed #39FF14; margin-top:25px; text-align:center;'>
        <h3 style='margin:0;'>💰 Reporte Detallado a Pedido</h3>
        <p style='font-size:18px;'>Obtenga su análisis profesional y detallado en su celular por tan solo <b>u$s 150</b>.</p>
        <p style='font-size:24px; color:#39FF14; font-weight:bold;'>📲 Envía coordenadas al 099417716</p>
        <p style='font-size:13px; opacity:0.8;'>Válido para Uruguay y el resto del mundo. Desarrollado por Leonardo Olivera © 2026. Litoral Operaciones Inmobiliarias.</p>
    </div>
</div>
""", unsafe_allow_html=True)

# 5. PIE DE PÁGINA
st.markdown("<div style='text-align: center; color: white; padding: 20px;'>© 2026 Litoral Operaciones Inmobiliarias - Todos los derechos reservados</div>", unsafe_allow_html=True)
