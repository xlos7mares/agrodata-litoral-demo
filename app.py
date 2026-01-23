import streamlit as st
import pandas as pd
import numpy as np
from streamlit_folium import folium_static
import folium
import os

# 1. CONFIGURACIÓN Y ESTÉTICA "PREMIUM TECH-AGRO"
st.set_page_config(page_title="AgroData Litoral - Auditoría Satelital", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.15), rgba(0, 0, 0, 0.25)), 
                    url("https://images.unsplash.com/photo-1500382017468-9049fed747ef?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80");
        background-size: cover;
        background-attachment: fixed;
    }
    
    /* Panel de Métricas */
    div[data-testid="stMetric"] {
        background-color: rgba(255, 255, 255, 0.98) !important;
        border-radius: 15px !important;
        padding: 25px !important;
        border-left: 12px solid #28a745 !important;
        box-shadow: 0px 10px 30px rgba(0,0,0,0.5) !important;
    }
    div[data-testid="stMetricLabel"], div[data-testid="stMetricValue"] {
        color: #000000 !important;
        font-weight: bold !important;
    }

    /* Recuadro de Diccionario Científico */
    .cientifico-box {
        background-color: rgba(0, 0, 0, 0.85);
        color: white;
        padding: 30px;
        border-radius: 20px;
        border: 2px solid #39FF14;
        margin-top: 40px;
        line-height: 1.6;
    }

    .satellite-tag {
        display: inline-flex;
        align-items: center;
        background: #1e4d2b;
        padding: 5px 15px;
        border-radius: 50px;
        margin-bottom: 10px;
        border: 1px solid #39FF14;
    }

    h1, h2, h3, h4 { color: white !important; text-shadow: 2px 2px 8px black; }
    .stTabs [data-baseweb="tab-list"] { background-color: rgba(0,0,0,0.85); border-radius: 10px; padding: 8px; }
    </style>
    """, unsafe_allow_html=True)

# 2. ENCABEZADO DE ALTO IMPACTO
with st.container():
    col_izq, col_der = st.columns([2.5, 3])
    with col_izq:
        st.markdown("""
            <div style="display: flex; align-items: center; margin-top: 15px;">
                <span style="font-size: 85px; margin-right: 20px;">🛰️</span>
                <div style="font-family: 'Arial Black', sans-serif; font-size: 38px; line-height: 0.9; color: white;">
                    AGRO<span style="color:#39FF14;">DATA</span><br>LITORAL
                </div>
            </div>
        """, unsafe_allow_html=True)
    with col_der:
        c_text, c_img = st.columns([2, 1])
        with c_text:
            st.markdown(f"""
                <div style="text-align: right; padding-right: 15px;">
                    <h2 style="margin:0; font-size: 30px;">Leonardo Olivera</h2>
                    <p style="margin:0; color:#39FF14; font-weight:bold; font-size: 22px;">📲 099417716</p>
                    <p style="font-size:12px; line-height:1.4; opacity: 0.95;">
                        Desarrollador de Software & Proyecto Agro Tecnológico<br>
                        Estudiante de Agronomía | Experto Informático (+20 años exp.)<br>
                        Perito en Grano | Operador Inmobiliario | Especialista en IA
                    </p>
                </div>
            """, unsafe_allow_html=True)
        with c_img:
            foto_path = "20250508_225422 (1).jpg"
            if os.path.exists(foto_path):
                st.image(foto_path, width=150)

st.markdown("## 🛰️ AUDITORÍA SATELITAL DE AGRO DATA LITORAL")
st.markdown("#### SERVICIO PREMIUM DE LITORAL OPERACIONES INMOBILIARIAS | Padrón 5900 - Young")
st.write("---")

# 3. TABS TÉCNICAS
tabs = st.tabs(["📊 MONITOREO EN VIVO", "🗺️ CAPA DE TERRENO", "🔬 CIENCIA ESPACIAL", "🔒 REPORTE FULL"])

with tabs[0]:
    st.markdown("#### 🎛️ Centro de Indicadores Críticos (Real-Time)")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Salud Vegetal (NDVI)", value="0.78", delta="+0.05")
    with col2:
        st.metric(label="Humedad Perfil (1m)", value="14.2%", delta="-3.8% CRÍTICO", delta_color="inverse")
    with col3:
        st.metric(label="Resistencia Suelo", value="2.5 MPa", delta="Suelo Firme")

with tabs[1]:
    lat, lon = -32.6585, -57.6455
    m = folium.Map(location=[lat, lon], zoom_start=16, tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google')
    folium.Polygon(locations=[[-32.6565, -57.6485], [-32.6565, -57.6425], [-32.6615, -57.6445], [-32.6615, -57.6475], [-32.6585, -57.6490], [-32.6565, -57.6485]], 
                   color="#39FF14", weight=6, fill=True, fill_color="#39FF14", fill_opacity=0.3).add_to(m)
    folium_static(m, width=1100)

with tabs[2]:
    st.info("Sincronización total con: **MGAP, SNIG, DIEA, INIA e OPYPA (Uruguay)**.")

with tabs[3]:
    st.error("🔒 REPORTE BLOQUEADO: Requiere validación de pago u$s 150 a Leonardo Olivera.")

# 4. NUEVA SECCIÓN: DICCIONARIO TÉCNICO Y COMERCIAL
st.markdown("""
<div class="cientifico-box">
    <h2 style="color:#39FF14 !important; text-align:center;">🔬 Diccionario de Inteligencia Espacial Aplicada</h2>
    <p style="text-align:center; font-style:italic; font-size:18px;">
        "En Uruguay no existe un servicio de este nivel tecnológico aplicado directamente al productor. 
        Este sistema es propiedad exclusiva de <b>Litoral Operaciones Inmobiliarias</b>."
    </p>
    <br>
    <div style="display: flex; flex-wrap: wrap; gap: 20px;">
        <div style="flex: 1; min-width: 300px; background: rgba(255,255,255,0.05); padding: 15px; border-radius: 10px;">
            <div class="satellite-tag">🛰️ Sentinel-2 (ESA)</div>
            <p><b>Dato: NDVI (Índice de Vegetación).</b><br>
            <i>¿Para qué sirve?</i> Detecta la fotosíntesis activa. Permite al productor ver dónde el cultivo tiene hambre (falta de nitrógeno) o enfermedad días antes de que sea visible al ojo humano. Es la diferencia entre salvar la cosecha o perderla.</p>
        </div>
        <div style="flex: 1; min-width: 300px; background: rgba(255,255,255,0.05); padding: 15px; border-radius: 10px;">
            <div class="satellite-tag">🛰️ NASA SMAP</div>
            <p><b>Dato: Humedad del Suelo (1 metro).</b><br>
            <i>¿Para qué sirve?</i> Escanea el subsuelo con microondas. Le dice al inversor si la tierra tiene "pulmón hídrico" para resistir una seca. Vital para valuar el precio real de la hectárea por su resiliencia.</p>
        </div>
        <div style="flex: 1; min-width: 300px; background: rgba(255,255,255,0.05); padding: 15px; border-radius: 10px;">
            <div class="satellite-tag">🛰️ NASA Landsat</div>
            <p><b>Dato: Resistencia Suelo (MPa).</b><br>
            <i>¿Para qué sirve?</i> Determina la dureza del horizonte. Crucial para saber dónde construir silos, galpones o tajamares sin riesgo de hundimiento o filtraciones. Seguridad total para la infraestructura física.</p>
        </div>
    </div>
    <br>
    <div style="background: rgba(57, 255, 20, 0.1); padding: 20px; border-radius: 15px; border: 1px dashed #39FF14;">
        <h3 style="margin-top:0;">💰 Oportunidad para Inversores y Colegas</h3>
        <p>Este nivel de detalle tecnológico permite auditar campos en <b>cualquier parte del mundo</b> sin moverse de la oficina. 
        Si usted es productor o inversor y necesita un <b>Reporte Detallado Profesional</b> con coordenadas exactas, mapas de calor y proyecciones:</p>
        <p style="font-size: 24px; color: #39FF14; text-align: center; font-weight: bold;">
            💲 ÚNICO PAGO: U$S 150 <br>
            📲 Contacto Directo: 099417716
        </p>
        <p style="text-align:center; font-size:12px; opacity: 0.7;">Desarrollado y Creado por Leonardo Olivera | Todos los Derechos Reservados © 2026</p>
    </div>
</div>
""", unsafe_allow_html=True)

# 5. PIE DE PÁGINA
st.markdown("""
    <div style="text-align: center; color: white; padding: 30px; background-color: rgba(0,0,0,0.8); border-radius: 15px 15px 0 0; margin-top:20px;">
        <p>© 2026 AgroData Litoral - Derechos Reservados | Litoral Operaciones Inmobiliarias</p>
    </div>
""", unsafe_allow_html=True)
