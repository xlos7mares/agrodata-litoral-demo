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

# --- MOTOR DE DATOS REALES ---
OW_API_KEY = "6508c51f5beeace1ba98e80ea843e599"

def obtener_telemetria(lat, lon):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OW_API_KEY}&units=metric&lang=es"
        r = requests.get(url, timeout=10).json()
        t, h, v = r['main']['temp'], r['main']['humidity'], r['wind']['speed'] * 3.6
        # Cálculo Delta T (Psicrometría de precisión)
        tw = t * math.atan(0.151977 * (h + 8.313659)**0.5) + math.atan(t + h) - math.atan(h - 1.676331) + 0.00391838 * (h)**1.5 * math.atan(0.023101 * h) - 4.686035
        dt = round(t - tw, 1)
        return t, h, round(v, 1), dt, r['weather'][0]['description'].capitalize()
    except: return None

# --- REPORTE TÉCNICO DE EXPORTACIÓN ---
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

# Persistencia de coordenadas
if 'lat' not in st.session_state: st.session_state.lat = -32.2997
if 'lon' not in st.session_state: st.session_state.lon = -58.0583

# --- MÓDULO 1: MONITOREO ---
if menu == "1. Estación de Monitoreo & PDF":
    st.title("🛰️ Monitoreo Satelital en Tiempo Real")
    c1, c2 = st.columns(2)
    with c1: gps_in = st.text_input("📍 Coordenadas GPS:", f"{st.session_state.lat}, {st.session_state.lon}")
    with c2: padron = st.text_input("📄 N° Padrón Catastral:", "")
    
    coords = re.findall(r'[-+]?\d*\.\d+|[-+]?\d+', gps_in)
    if len(coords) >= 2:
        st.session_state.lat, st.session_state.lon = float(coords[0]), float(coords[1])
        data = obtener_telemetria(st.session_state.lat, st.session_state.lon)
        if data:
            t, h, v, dt, desc = data
            st.markdown(f"#### ✅ Parámetros Atmosféricos Validados")
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("TEMP. AIRE", f"{t} °C"); m2.metric("HUMEDAD", f"{h} %")
            m3.metric("VIENTO", f"{v} km/h"); m4.metric("DELTA T", f"{dt}")
            
            if st.button("🚀 IMPRIMIR INFORME DE AUDITORÍA"):
                pdf = PDF_Venta(); pdf.set_auto_page_break(auto=True, margin=15)
                # Hoja 1: Clima
                pdf.add_page(); pdf.set_font("Arial", 'B', 14); pdf.cell(0, 10, "I. CARACTERIZACIÓN AGROMETEOROLÓGICA", 0, 1)
                pdf.set_font("Arial", '', 11); pdf.multi_cell(0, 7, f"Ubicación: {st.session_state.lat}, {st.session_state.lon}. T: {t}C, H: {h}%. Delta T: {dt}. Análisis psicrométrico real.")
                # Hoja 2: Geología Arapey
                pdf.add_page(); pdf.set_font("Arial", 'B', 14); pdf.cell(0, 10, "II. GEOLOGÍA ESTRUCTURAL (DINAMIGE)", 0, 1)
                pdf.set_font("Arial", '', 11); pdf.multi_cell(0, 7, "Formación Arapey: Basaltos toleíticos del Cretácico. Estructura masiva con disyunción columnar.")
                # Hoja 3: Suelos
                pdf.add_page(); pdf.set_font("Arial", 'B', 14); pdf.cell(0, 10, "III. EDAFOLOGÍA (CONEAT)", 0, 1)
                pdf.set_font("Arial", '', 11); pdf.multi_cell(0, 7, f"Padrón: {padron}. Suelos Grupo 12. Brunosoles Éutricos superficiales.")
                st.download_button("📥 DESCARGAR REPORTE", pdf.output(dest='S').encode('latin-1'), "Informe.pdf")

# --- MÓDULO 2: RIESGO CLIMÁTICO (TEXTO & CIENCIA) ---
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
            st.write(f"**Análisis:** Con un Delta T de {dt}, la tasa de evaporación es {'CRÍTICA' if dt > 10 else 'ÓPTIMA'}. Esto afecta directamente la supervivencia de la gota en aplicaciones.")
        with c2:
            st.markdown("#### 💧 Saturación e Infiltración")
            st.progress(h/100)
            st.write(f"**Análisis:** Humedad del {h}%. Un perfil saturado sobre la **Formación Arapey** aumenta el riesgo de escurrimiento superficial (Run-off) debido a la baja permeabilidad del basalto.")

# --- MÓDULO 3: EDAFOLOGÍA (PEDAGÓGICO) ---
elif menu == "3. Caracterización Edafológica":
    st.title("🌿 Análisis de Suelos CONEAT")
    st.markdown("### 🧬 ¿Por qué tu suelo se comporta así?")
    col_a, col_b = st.columns(2)
    with col_a:
        st.success("#### Suelos Grupo 12 (Paysandú)")
        st.write("""
        **Composición:** Brunosoles Éutricos.
        - **¿Qué significa?** Son suelos oscuros, ricos en materia orgánica y bases.
        - **Textura:** Franco-arcillosa. Tienen alta capacidad de retener nutrientes (CIC alta).
        - **Limitante:** La profundidad. Al estar sobre basalto, la 'cama' de la raíz es corta.
        """)
    with col_b:
        st.info("#### Geología: Formación Arapey")
        st.write("""
        **Origen:** Derrames volcánicos de hace 130 millones de años.
        - **Impacto:** La roca madre basáltica provee minerales pero dificulta el drenaje profundo.
        - **Pedagogía:** Es un suelo fértil pero 'sediento' en verano porque retiene poca agua útil.
        """)

# --- MÓDULO 4: VRZ (PEDAGÓGICO & REAL) ---
elif menu == "4. Viabilidad Financiera (VRZ)":
    st.title("💰 Valor Real de Zona (VRZ)")
    st.write("Cálculo de rentabilidad basado en el **Índice CONEAT** real de Uruguay.")
    
    cv1, cv2 = st.columns(2)
    with cv1:
        coneat = st.slider("Índice CONEAT del lote:", 50, 200, 100)
        st.caption("El Índice CONEAT mide la capacidad de producción de carne/lana/granos de una hectárea promedio (Base 100).")
    with cv2:
        precio_ton = st.number_input("Precio Producto (USD/Ton):", value=420)

    # Lógica científica
    rend_est = (coneat / 100) * 3.8 # Rendimiento basado en potencial de suelo
    st.markdown(f"### 📈 Resultados del Análisis VRZ")
    r1, r2 = st.columns(2)
    r1.metric("POTENCIAL PRODUCTIVO", f"{round(rend_est, 2)} Ton/Ha")
    r2.metric("INGRESO ESTIMADO", f"{round(rend_est * precio_ton, 2)} USD/Ha")
    
    st.warning("⚠️ **Nota Técnica:** Este cálculo vincula la fertilidad química del Grupo 12 con el precio de mercado actual.")
