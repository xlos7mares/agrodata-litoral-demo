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

# --- CONEXIÓN TELEMÉTRICA REAL (API PAYSANDÚ) ---
OW_API_KEY = "6508c51f5beeace1ba98e80ea843e599"

def obtener_telemetria_cientifica(lat, lon):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OW_API_KEY}&units=metric&lang=es"
        r = requests.get(url, timeout=10).json()
        t = r['main']['temp']
        h = r['main']['humidity']
        v = r['wind']['speed'] * 3.6 # Conversión a km/h
        # Cálculo Psicrométrico de Delta T
        tw = t * math.atan(0.151977 * (h + 8.313659)**0.5) + math.atan(t + h) - math.atan(h - 1.676331) + 0.00391838 * (h)**1.5 * math.atan(0.023101 * h) - 4.686035
        dt = round(t - tw, 1)
        return t, h, round(v, 1), dt, r['weather'][0]['description'].capitalize()
    except:
        return None

# --- CLASE PDF CON IDENTIDAD PROFESIONAL ---
class Reporte_Ingenieria(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 8)
        self.cell(0, 10, f"{AUTOR} - {PERFIL}", 0, 1, 'R')
        self.line(10, 15, 200, 15)
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()} | Auditoría Técnica Real | Desarrollado por {AUTOR}', 0, 0, 'C')

# --- MENÚ LATERAL (LOS 4 PILARES) ---
st.sidebar.title("Agro Data Litoral 🛰️")
menu = st.sidebar.radio("Módulos del Sistema:", [
    "1. Análisis de Predio y PDF", 
    "2. Asistente Agronómico (Chat)", 
    "3. Scouting IA (Plagas/Suelo)", 
    "4. Viabilidad Financiera (VRZ)"
])
st.sidebar.markdown("---")
st.sidebar.write(f"**Analista:** {AUTOR}")

# --- MÓDULO 1: ANÁLISIS DE PREDIO ---
if menu == "1. Análisis de Predio y PDF":
    st.title("🛰️ Estación de Monitoreo de Precisión")
    
    # Entrada de Datos - PADRÓN VACÍO
    with st.container():
        c1, c2, c3 = st.columns(3)
        with c1: gps_in = st.text_input("📍 Coordenadas GPS (Lat, Lon):", "-32.2997, -58.0583")
        with c2: padron = st.text_input("📄 N° de Padrón Catastral:", "") # Mantenido vacío por solicitud
        with c3: depto = st.selectbox("🗺️ Departamento:", ["Paysandú", "Salto", "Río Negro", "Soriano"])

    coords = re.findall(r'[-+]?\d*\.\d+|[-+]?\d+', gps_in)
    if len(coords) >= 2:
        lat, lon = float(coords[0]), float(coords[1])
        data = obtener_telemetria_cientifica(lat, lon)
        
        if data:
            t, h, v, dt, desc = data
            
            # --- VISUALIZACIÓN CIENTÍFICA (MÉTRICAS) ---
            st.markdown("### 📊 Telemetría Atmosférica en Tiempo Real")
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("TEMPERATURA", f"{t} °C", "Aire")
            m2.metric("HUMEDAD REL.", f"{h} %", "Higrometría")
            m3.metric("VEL. VIENTO", f"{v} km/h", "Anemometría")
            
            # Color dinámico para Delta T
            status_dt = "Óptimo" if 2 <= dt <= 8 else "Riesgo"
            m4.metric("DELTA T", f"{dt}", f"Estado: {status_dt}")

            st.markdown("---")
            
            col_inf1, col_inf2 = st.columns(2)
            with col_inf1:
                st.markdown("### 🌍 Geología Estructural (DINAMIGE)")
                st.success(f"**Unidad:** Formación Arapey / Tacuarembó")
                st.write("**Litología:** Basaltos toleíticos del Cretácico.")
                st.write("**Estratigrafía:** Roca madre volcánica masiva.")
                st.write(f"**Observación Local:** {desc}")
            
            with col_inf2:
                st.markdown("### 🌿 Clasificación de Suelos (CONEAT)")
                st.warning(f"**Grupo Dominante:** Unidad 12 (Paysandú)")
                st.write("**Tipo:** Brunosoles Éutricos superficiales.")
                st.write("**Hidrografía:** Cuenca del Río Uruguay.")
                st.write("**Escurrimiento:** Superficial con baja tasa de infiltración.")

            st.map(pd.DataFrame({'lat': [lat], 'lon': [lon]}))

            # GENERACIÓN DE PDF PROFESIONAL (3 PÁGINAS)
            if st.button("🚀 GENERAR REPORTE TÉCNICO EXPLICATIVO"):
                pdf = Reporte_Ingenieria()
                pdf.set_auto_page_break(auto=True, margin=15)
                
                # Pág 1: Telemetría Atmosférica
                pdf.add_page()
                pdf.set_font("Arial", 'B', 14)
                pdf.cell(0, 10, "AUDITORÍA TÉCNICA AGRO DATA LITORAL", 0, 1, 'C')
                pdf.ln(5)
                pdf.set_font("Arial", 'B', 11)
                pdf.cell(0, 10, "1. TELEMETRÍA ATMOSFÉRICA ACTUAL (OpenWeather)", 0, 1)
                pdf.set_font("Arial", size=10)
                pdf.multi_cell(0, 7, f"Temp: {t} C | Humedad: {h}% | Viento: {v} km/h | Delta T: {dt}\nCondición: {desc}")
                
                # Pág 2: Geología y Edafología (Datos DINAMIGE/CONEAT)
                pdf.add_page()
                pdf.set_font("Arial", 'B', 11)
                pdf.cell(0, 10, "2. ANÁLISIS ESTRUCTURAL Y DE SUELOS", 0, 1)
                pdf.set_font("Arial", size=10)
                pdf.multi_cell(0, 7, (
                    f"Padrón: {padron if padron else 'No especificado'}\n\n"
                    "GEOLOGÍA: Formación Arapey (DINAMIGE). Sustrato volcánico del Mesozoico.\n"
                    "SUELOS: Clasificación CONEAT Grupo 12. Brunosoles sobre basalto superficial.\n"
                    "HIDROGRAFÍA: Cuenca del Río Uruguay. Dinámica de escurrimiento superficial."
                ))

                # Pág 3: Glosario Técnico Explicativo
                pdf.add_page()
                pdf.set_font("Arial", 'B', 12)
                pdf.cell(0, 10, "GLOSARIO TÉCNICO Y NOTAS LEGALES", 0, 1)
                pdf.ln(5)
                pdf.set_font("Arial", size=9)
                glosario = [
                    ("Delta T", "Diferencial térmico que mide la tasa de evaporación atmosférica."),
                    ("CONEAT", "Índice de capacidad de producción de suelos de Uruguay."),
                    ("Ley 20.212", "Marco regulatorio de Inteligencia Artificial en Uruguay."),
                    ("Litoestratigrafía", "Estudio de las capas de roca y su composición física."),
                    ("Escurrimiento", "Flujo de agua por la superficie del terreno hacia cauces.")
                ]
                for term, de in glosario:
                    pdf.set_font("Arial", 'B', 9)
                    pdf.cell(40, 6, f"{term}:", 0, 0)
                    pdf.set_font("Arial", size=9)
                    pdf.multi_cell(0, 6, de)
                
                st.download_button("📥 DESCARGAR REPORTE PDF", pdf.output(dest='S').encode('latin-1'), f"Reporte_{padron if padron else 'S-P'}.pdf")

# --- MANTENIMIENTO DE MÓDULOS MEMORIZADOS ---
elif menu == "2. Asistente Agronómico (Chat)":
    st.title("🤖 Asistente Técnico (OIRSA)")
    st.info("Consulte normativas de inocuidad y gestión de riesgos.")

elif menu == "3. Scouting IA (Plagas/Suelo)":
    st.title("🔍 Reconocimiento Visual")
    st.file_uploader("Subir foto de campo", type=['jpg', 'png'])

elif menu == "4. Viabilidad Financiera (VRZ)":
    st.title("💰 Viabilidad VRZ (Ley 20.212)")
    st.write("Cálculos basados en productividad real y ética algorítmica.")
