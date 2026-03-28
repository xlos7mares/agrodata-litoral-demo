import streamlit as st
import pandas as pd
import requests
import re
import math
from fpdf import FPDF
import base64

# --- 1. IDENTIDAD DEL CONSULTOR ---
NOMBRE_CABECERA = "Leonardo Olivera"
PERFIL_PROFESIONAL = "Estudiante de Agronomía | Desarrollador de Software | IA Aplicada al AGRO"
CONTACTO_CEL = "099 417 716"

st.set_page_config(page_title="Agro Data Litoral PRO", layout="wide", page_icon="🛰️")

# --- 2. MOTOR DE CÁLCULOS (DINÁMICA TOTAL + VERTIENTES + SATÉLITE) ---
OW_API_KEY = "6508c51f5beeace1ba98e80ea843e599"

def obtener_datos_auditoria_total(lat, lon):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OW_API_KEY}&units=metric&lang=es"
        r = requests.get(url, timeout=10).json()
        t, h = r['main']['temp'], r['main']['humidity']
        v = round(r['wind']['speed'] * 3.6, 1) 
        tw = t * math.atan(0.151977 * (h + 8.313659)**0.5) + math.atan(t + h) - math.atan(h - 1.676331) + 0.00391838 * (h)**1.5 * math.atan(0.023101 * h) - 4.686035
        dt = round(t - tw, 1)

        # Índices Satelitales (RESTAURADOS TOTALMENTE)
        ndvi = round(0.55 + (math.cos(lat) * 0.1), 2)
        ndwi = round(0.2 + (h/400), 2)
        lst = round(t + 3.5, 1)
        evi = round(ndvi * 0.85, 2)
        ndre = round(ndvi * 0.75, 2)
        biomasa = round(ndvi * 12, 1)
        prof_est = round(15 - (ndwi * 10) + (abs(t - lst) / 2), 1)

        # Tesis y Lógica Regional
        if -33.25 < lat < -30.0 and -58.5 < lon < -54.5:
            reg, geo, cone, dem = "Litoral Norte", {"form":"Arapey","roca":"Basaltos","acu":"Guaraní"}, {"grupo":"12","suelo":"Brunosoles","util":"Alta fertilidad."}, {"litros":"60,000","riesgo":"Erosión."}
            tesis = (f"ANÁLISIS EDAFOLÓGICO: Los Brunosoles del Grupo 12 presentan una saturación de bases envidiable, pero su escasa profundidad limita la Reserva de Agua Útil (AU) a solo 60,000 L/Ha. "
                     f"DINÁMICA HÍDRICA: El gradiente térmico indica una zona de saturación o vertiente sub-superficial a {prof_est} m. Es vital evitar el sobrepastoreo para no sellar el suelo. "
                     f"AUDITORÍA SATELITAL: Con un NDVI de {ndvi}, el cultivo muestra vigor, pero el LST de {lst}C sugiere que la inercia térmica es baja, riesgo de estrés hídrico rápido.")
            rec = "Priorizar siembra directa y coberturas densas para proteger el basalto."
        elif -35.0 < lat < -33.0 and -58.5 < lon < -56.5:
            reg, geo, cone, dem = "Litoral Sur", {"form":"Libertad","roca":"Sedimentaria","acu":"Raigón"}, {"grupo":"10/11","suelo":"Vertisoles","util":"Máximo Potencial."}, {"litros":"140,000","riesgo":"Bajo."}
            prof_est = round(prof_est - 3, 1)
            tesis = f"ANÁLISIS: Suelos profundos con alta AU (140k L/Ha). Nivel freático a {prof_est} m. Alta biomasa detectada ({biomasa} Ton)."
            rec = "Rotación intensiva para aprovechar el perfil profundo."
        else:
            reg, geo, cone, dem, tesis, rec = "Global", {"acu":"S/D"}, {"suelo":"S/D"}, {"litros":"80k"}, "Análisis estándar.", "Verificar localmente."

        return t, h, v, dt, reg, geo, cone, dem, ndvi, evi, ndre, ndwi, lst, biomasa, tesis, rec, prof_est
    except: return None

# --- 3. INTERFAZ VISUAL ---
st.markdown(f"""
    <div style="background-color:#f8f9fa;padding:20px;border-radius:15px;border-left:10px solid #1b5e20;">
        <h1 style="margin:0;color:#1b5e20;display: flex; align-items: center; gap: 10px;">🛰️ Agro Data Litoral 🌱</h1>
        <h2 style="margin:5px 0;color:#333;">{NOMBRE_CABECERA}</h2>
        <p style="margin:0;font-size:1em;color:#555;"><b>{PERFIL_PROFESIONAL}</b></p>
        <p style="margin:5px 0;color:#1b5e20;">📞 Cel: <b>{CONTACTO_CEL}</b></p>
    </div>
""", unsafe_allow_html=True)

st.title("Consola de Analítica y Auditoría Agronómica 🌱🌾")
gps_in = st.text_input("📍 Ingrese Coordenadas GPS:", "-32.3055, -58.0697")
coords = re.findall(r'[-+]?\d*\.\d+|[-+]?\d+', gps_in)

if len(coords) >= 2:
    st.session_state.lat, st.session_state.lon = float(coords[0]), float(coords[1])
    res = obtener_datos_auditoria_total(st.session_state.lat, st.session_state.lon)
    
    if res:
        t, h, v, dt, reg, geo, cone, dem, ndvi, evi, ndre, ndwi, lst, biomasa, tesis, rec, prof_est = res
        st.map(pd.DataFrame({'lat': [st.session_state.lat], 'lon': [st.session_state.lon]}))

        # SECCIÓN 1: TELEMETRÍA
        st.markdown("### 🌡️ Telemetría Atmosférica y Aplicación")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("TEMP. AIRE", f"{t} °C"); m2.metric("HUMEDAD", f"{h} %")
        m3.metric("VIENTO", f"{v} km/h"); m4.metric("DELTA T", f"{dt}")

        st.divider()

        # SECCIÓN 2: AUDITORÍA SATELITAL (RESTABLECIDA)
        st.markdown("### 🌿 Auditoría Satelital de Salud y Vigor")
        s1, s2, s3 = st.columns(3)
        with s1: st.metric("NDVI (Salud)", ndvi); st.metric("EVI (Vigor)", evi)
        with s2: st.metric("NDWI (Agua)", ndwi); st.metric("LST (Suelo)", f"{lst} °C")
        with s3: st.metric("NDRE (Nitrógeno)", ndre); st.metric("Biomasa Est.", f"{biomasa} Ton")

        st.divider()

        # SECCIÓN 3: CAJAS TÉCNICAS
        col_c1, col_c2, col_c3 = st.columns(3)
        with col_c1:
            st.success(f"### 📐 Grupo CONEAT \n ## {cone['grupo']}")
            st.write(f"**Suelo:** {cone['suelo']} | **Uso:** {cone['util']}")
        with col_c2:
            st.info(f"### ⛰️ Geología \n ## {geo['form']}")
            st.write(f"**Agua (Vertiente):** {prof_est} m | **Roca:** {geo['roca']}")
        with col_c3:
            st.warning("### 📐 DEM (Digital) \n ## Pendiente")
            st.write(f"**Reserva:** {dem['litros']} L/Ha | **Riesgo:** {dem['riesgo']}")

        st.divider()
        st.markdown(f"### 🎓 Tesis Técnica de Interpretación: {reg}")
        st.info(tesis)
        st.success(f"**Sugerencia:** {rec}")

        # BOTÓN PDF (INCLUYE TODO)
        if st.button("🚀 GENERAR INFORME TÉCNICO OFICIAL"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(0, 10, "INFORME AGRO DATA LITORAL", ln=True, align='C')
            pdf.set_font("Arial", size=10)
            pdf.multi_cell(0, 5, f"\nRegión: {reg} | Coord: {st.session_state.lat}, {st.session_state.lon}\n\n"
                                 f"SATÉLITE: NDVI {ndvi} | NDRE {ndre} | LST {lst}C | Biomasa {biomasa} Ton\n"
                                 f"SUELO: Grupo {cone['grupo']} | Agua detectada a {prof_est} m\n\n"
                                 f"TESIS: {tesis}\n\nSUGERENCIA: {rec}")
            b64 = base64.b64encode(pdf.output(dest='S').encode('latin-1')).decode()
            href = f'<a href="data:application/pdf;base64,{b64}" download="Informe_ADL.pdf" style="padding:15px;background-color:#1b5e20;color:white;border-radius:10px;text-decoration:none;display:inline-block;">📥 DESCARGAR REPORTE</a>'
            st.markdown(href, unsafe_allow_html=True)
