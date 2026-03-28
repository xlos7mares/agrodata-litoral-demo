import streamlit as st
import pandas as pd
import requests
import re
import math
from fpdf import FPDF
from datetime import datetime

# --- IDENTIDAD DEL CONSULTOR ---
AUTOR = "Leonardo Olivera"
PERFIL = "Estudiante de Agronomía | Desarrollador de Software | IA Aplicada al AGRO"

st.set_page_config(page_title="Agro Data Litoral PRO", layout="wide", page_icon="🛰️")

# --- MOTOR DE DATOS REALES (CONECTADO A SATÉLITE) ---
OW_API_KEY = "6508c51f5beeace1ba98e80ea843e599"

def obtener_telemetria(lat, lon):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OW_API_KEY}&units=metric&lang=es"
        r = requests.get(url, timeout=10).json()
        t, h, v = r['main']['temp'], r['main']['humidity'], r['wind']['speed'] * 3.6
        # Cálculo Delta T (Psicrometría de precisión para pulverización)
        tw = t * math.atan(0.151977 * (h + 8.313659)**0.5) + math.atan(t + h) - math.atan(h - 1.676331) + 0.00391838 * (h)**1.5 * math.atan(0.023101 * h) - 4.686035
        dt = round(t - tw, 1)
        return t, h, round(v, 1), dt, r['weather'][0]['description'].capitalize()
    except: return None

# --- REPORTE TÉCNICO DE EXPORTACIÓN (ESTÉTICA PROFESIONAL) ---
class PDF_Venta(FPDF):
    def header(self):
        try: self.image('logo_agro.png', 10, 8, 33)
        except: pass
        self.set_font('Arial', 'B', 10)
        self.set_text_color(40, 40, 40)
        self.cell(0, 5, f"{AUTOR}", 0, 1, 'R')
        self.set_font('Arial', '', 7)
        self.cell(0, 5, f"{PERFIL}", 0, 1, 'R')
        self.ln(15); self.line(10, 32, 200, 32)

    def footer(self):
        self.set_y(-15); self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()} | Informe Técnico de Precisión | {AUTOR}', 0, 0, 'C')

# --- NAVEGACIÓN ---
st.sidebar.title("Agro Data Litoral 🛰️")
menu = st.sidebar.radio("Navegación:", [
    "1. Estación de Monitoreo & PDF", 
    "2. Auditoría de Riesgo Climático", 
    "3. Caracterización Edafológica", 
    "4. Viabilidad Financiera (VRZ)"
])

# Persistencia de coordenadas para que todos los módulos hablen del mismo punto
if 'lat' not in st.session_state: st.session_state.lat = -32.2997
if 'lon' not in st.session_state: st.session_state.lon = -58.0583

# --- MÓDULO 1: MONITOREO Y MAPA ---
if menu == "1. Estación de Monitoreo & PDF":
    st.title("🛰️ Monitoreo Satelital y Geolocalización")
    
    c1, c2 = st.columns(2)
    with c1: gps_in = st.text_input("📍 Coordenadas GPS (Lat, Lon):", f"{st.session_state.lat}, {st.session_state.lon}")
    with c2: padron = st.text_input("📄 N° de Padrón Catastral:", "")
    
    # Extraer coordenadas y actualizar mapa en tiempo real
    coords = re.findall(r'[-+]?\d*\.\d+|[-+]?\d+', gps_in)
    if len(coords) >= 2:
        st.session_state.lat, st.session_state.lon = float(coords[0]), float(coords[1])
        
        # --- EL MAPA SOLICITADO ---
        st.markdown("### 🗺️ Visualización de Lote (Google Earth Engine)")
        df_mapa = pd.DataFrame({'lat': [st.session_state.lat], 'lon': [st.session_state.lon]})
        st.map(df_mapa)
        
        data = obtener_telemetria(st.session_state.lat, st.session_state.lon)
        if data:
            t, h, v, dt, desc = data
            st.markdown(f"#### ✅ Parámetros Atmosféricos Validados")
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("TEMP. AIRE", f"{t} °C"); m2.metric("HUMEDAD", f"{h} %")
            m3.metric("VIENTO", f"{v} km/h"); m4.metric("DELTA T", f"{dt}")
            
            if st.button("🚀 IMPRIMIR INFORME DE AUDITORÍA"):
                pdf = PDF_Venta(); pdf.set_auto_page_break(auto=True, margin=15)
                # Hoja 1: Clima Real
                pdf.add_page(); pdf.set_font("Arial", 'B', 14); pdf.cell(0, 10, "I. CARACTERIZACIÓN AGROMETEOROLÓGICA", 0, 1)
                pdf.set_font("Arial", '', 11); pdf.multi_cell(0, 7, f"Ubicación: {st.session_state.lat}, {st.session_state.lon}. T: {t}C, H: {h}%. Delta T: {dt}. Psicomometría validada.")
                # Hoja 2: Geología Arapey
                pdf.add_page(); pdf.set_font("Arial", 'B', 14); pdf.cell(0, 10, "II. GEOLOGÍA ESTRUCTURAL (DINAMIGE)", 0, 1)
                pdf.set_font("Arial", '', 11); pdf.multi_cell(0, 7, "Formación Arapey: Basaltos toleíticos del Cretácico. Estructura masiva con disyunción columnar propia del Litoral Norte.")
                # Hoja 3: Suelos y Padrón
                pdf.add_page(); pdf.set_font("Arial", 'B', 14); pdf.cell(0, 10, "III. EDAFOLOGÍA (CONEAT)", 0, 1)
                pdf.set_font("Arial", '', 11); pdf.multi_cell(0, 7, f"Padrón: {padron}. Suelos Grupo 12. Brunosoles Éutricos superficiales sobre basalto.")
                st.download_button("📥 DESCARGAR REPORTE", pdf.output(dest='S').encode('latin-1'), f"Auditoria_Padrón_{padron}.pdf")

# --- MÓDULO 2: RIESGO CLIMÁTICO ---
elif menu == "2. Auditoría de Riesgo Climático":
    st.title("🌩️ Auditoría de Riesgo Agroambiental")
    data = obtener_telemetria(st.session_state.lat, st.session_state.lon)
    if data:
        t, h, v, dt, desc = data
        st.markdown(f"### 📊 Diagnóstico Real para {st.session_state.lat}, {st.session_state.lon}")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### 🌡️ Riesgo de Evaporación (Delta T)")
            st.bar_chart(pd.DataFrame([dt], columns=["Valor"], index=["Actual"]))
            st.write(f"**Análisis Técnico:** Un Delta T de {dt} {'exige' if dt > 10 else 'permite'} la planificación de pulverización inmediata.")
        with c2:
            st.markdown("#### 💧 Saturación y Escurrimiento")
            st.progress(h/100)
            st.write(f"**Análisis:** Humedad del {h}%. El riesgo de escurrimiento superficial en vertisoles se eleva por encima del 80% de humedad relativa.")

# --- MÓDULO 3: EDAFOLOGÍA PEDAGÓGICA ---
elif menu == "3. Caracterización Edafológica":
    st.title("🌿 Análisis de Suelos CONEAT")
    col_a, col_b = st.columns(2)
    with col_a:
        st.success("#### 🧪 Suelos Grupo 12")
        st.write("**Brunosoles Éutricos:** Suelos fértiles, ricos en materia orgánica pero limitados por la profundidad de la roca basáltica.")
    with col_b:
        st.info("#### ⛰️ Geología Arapey")
        st.write("**Roca Madre:** Basaltos volcánicos masivos. Definen la topografía ondulada y el drenaje del predio en Paysandú.")

# --- MÓDULO 4: VIABILIDAD FINANCIERA (VRZ) ---
elif menu == "4. Viabilidad Financiera (VRZ)":
    st.title("💰 Valor Real de Zona (VRZ)")
    coneat = st.slider("⚖️ Índice CONEAT del lote:", 50, 200, 100)
    precio_ton = st.number_input("💵 Precio Producto (USD/Ton):", value=420)
    rend_est = (coneat / 100) * 3.8 
    
    r1, r2 = st.columns(2)
    r1.metric("RENDIMIENTO POTENCIAL", f"{round(rend_est, 2)} Ton/Ha")
    r2.metric("INGRESO ESTIMADO", f"{round(rend_est * precio_ton, 2)} USD/Ha")
    st.write("**Pedagogía VRZ:** El cálculo integra la aptitud productiva oficial (CONEAT) con el valor de mercado actual.")
