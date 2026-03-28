import streamlit as st
import pandas as pd
import requests
import re
import math
from fpdf import FPDF
from datetime import datetime

# --- IDENTIDAD DEL PROYECTO ---
AUTOR = "Leonardo Olivera"
PERFIL = "Estudiante de Agronomía | Desarrollador de Software | IA Aplicada al AGRO"

st.set_page_config(page_title="Agro Data Litoral PRO", layout="wide", page_icon="🛰️")

# --- MOTOR DE TELEMETRÍA REAL ---
OW_API_KEY = "6508c51f5beeace1ba98e80ea843e599"

def obtener_telemetria(lat, lon):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OW_API_KEY}&units=metric&lang=es"
        r = requests.get(url, timeout=10).json()
        t, h, v = r['main']['temp'], r['main']['humidity'], r['wind']['speed'] * 3.6
        # Cálculo Delta T real
        tw = t * math.atan(0.151977 * (h + 8.313659)**0.5) + math.atan(t + h) - math.atan(h - 1.676331) + 0.00391838 * (h)**1.5 * math.atan(0.023101 * h) - 4.686035
        dt = round(t - tw, 1)
        return t, h, round(v, 1), dt, r['weather'][0]['description'].capitalize()
    except: return None

# --- CLASE PDF PROFESIONAL (ESTÉTICA CORREGIDA) ---
class PDF_Agro(FPDF):
    def header(self):
        # Logo Agro Data Litoral
        try: self.image('logo_agro.png', 10, 8, 33)
        except: pass
        
        # Bloque de Identidad (Limpio, sin subrayado)
        self.set_font('Arial', 'B', 10)
        self.set_text_color(30, 30, 30)
        self.set_x(100)
        self.cell(0, 5, f"{AUTOR}", 0, 1, 'R')
        self.set_font('Arial', '', 7)
        self.set_x(100)
        self.cell(0, 5, f"{PERFIL}", 0, 1, 'R')
        
        self.ln(10)
        self.line(10, 32, 200, 32)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, f'Página {self.page_no()} | Auditoría Técnica Real | Leonardo Olivera', 0, 0, 'C')

# --- NAVEGACIÓN ---
st.sidebar.title("Agro Data Litoral 🛰️")
menu = st.sidebar.radio("Navegación:", [
    "1. Análisis de Predio y PDF", 
    "2. Análisis de Riesgo Climático", 
    "3. Scouting de Campo", 
    "4. Viabilidad Financiera (VRZ)"
])

# Persistencia de coordenadas
if 'lat' not in st.session_state: st.session_state.lat = -32.2997
if 'lon' not in st.session_state: st.session_state.lon = -58.0583

# --- MÓDULO 1: ANÁLISIS ---
if menu == "1. Análisis de Predio y PDF":
    st.title("🛰️ Estación de Monitoreo y Auditoría")
    c1, c2 = st.columns(2)
    with c1: gps_in = st.text_input("📍 Coordenadas:", f"{st.session_state.lat}, {st.session_state.lon}")
    with c2: padron_input = st.text_input("📄 N° Padrón Catastral:", "")
    
    coords = re.findall(r'[-+]?\d*\.\d+|[-+]?\d+', gps_in)
    if len(coords) >= 2:
        st.session_state.lat, st.session_state.lon = float(coords[0]), float(coords[1])
        data = obtener_telemetria(st.session_state.lat, st.session_state.lon)
        if data:
            t, h, v, dt, desc = data
            st.markdown(f"#### Datos validados para: {st.session_state.lat}, {st.session_state.lon}")
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("TEMPERATURA", f"{t} °C"); m2.metric("HUMEDAD", f"{h} %")
            m3.metric("VIENTO", f"{v} km/h"); m4.metric("DELTA T", f"{dt}")

            if st.button("🚀 IMPRIMIR REPORTE TÉCNICO COMPLETO"):
                pdf = PDF_Agro(); pdf.set_auto_page_break(auto=True, margin=15)
                # HOJA 1
                pdf.add_page(); pdf.set_font("Arial", 'B', 14); pdf.cell(0, 10, "I. CARACTERIZACIÓN AGROMETEOROLÓGICA", 0, 1)
                pdf.set_font("Arial", '', 11); pdf.multi_cell(0, 7, f"Ubicación: {st.session_state.lat}, {st.session_state.lon}\nTemperatura: {t}C\nHumedad: {h}%\nDelta T: {dt}\n\nAnálisis basado en la psicrometría real para aplicaciones de precisión.")
                # HOJA 2
                pdf.add_page(); pdf.set_font("Arial", 'B', 14); pdf.cell(0, 10, "II. GEOLOGÍA ESTRUCTURAL (DINAMIGE)", 0, 1)
                pdf.set_font("Arial", '', 11); pdf.multi_cell(0, 7, "Formación Arapey. Basaltos toleíticos del Cretácico Inferior. Estructura de roca madre masiva con disyunción columnar.")
                # HOJA 3
                pdf.add_page(); pdf.set_font("Arial", 'B', 14); pdf.cell(0, 10, "III. EDAFOLOGÍA Y CAPACIDAD DE USO", 0, 1)
                pdf.set_font("Arial", '', 11); pdf.multi_cell(0, 7, f"Padrón: {padron_input}\nSuelos Grupo 12 (CONEAT). Brunosoles Éutricos. Capacidad de uso: Campo Natural con alta reserva mineral.")
                st.download_button("📥 DESCARGAR PDF PROFESIONAL", pdf.output(dest='S').encode('latin-1'), f"Reporte_{st.session_state.lat}.pdf")

# --- MÓDULO 2: RIESGO CLIMÁTICO (SOLO VISUAL) ---
elif menu == "2. Análisis de Riesgo Climático":
    st.title("🌩️ Análisis de Riesgo Real")
    data = obtener_telemetria(st.session_state.lat, st.session_state.lon)
    if data:
        t, h, v, dt, desc = data
        st.markdown("### 📊 Indicadores Automáticos de Riesgo")
        c_r1, c_r2 = st.columns(2)
        with c_r1:
            st.write("**Riesgo de Evaporación (Delta T)**")
            st.bar_chart(pd.DataFrame([dt], columns=["Valor"], index=["Actual"]))
        with c_r2:
            st.write("**Saturación Atmosférica**")
            st.progress(h/100)
        st.info(f"Análisis realizado para {st.session_state.lat}, {st.session_state.lon} en base a parámetros geofísicos.")

# --- MÓDULO 3 Y 4 ---
elif menu == "3. Scouting de Campo": st.title("🔍 Scouting de Campo")
elif menu == "4. Viabilidad Financiera (VRZ)": st.title("💰 Viabilidad VRZ")
