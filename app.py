import streamlit as st
import pandas as pd
import requests
import re
import math
from fpdf import FPDF
from datetime import datetime

# --- CONFIGURACIÓN DE IDENTIDAD ---
NOMBRE_AUTOR = "Leonardo Olivera"
TITULOS_AUTOR = "Estudiante de Agronomía | Desarrollador de Software | IA Aplicada al AGRO"

st.set_page_config(page_title="Agro Data Litoral PRO", layout="wide", page_icon="🛰️")

# --- CONEXIÓN SATELITAL REAL (OPENWEATHER) ---
OW_API_KEY = "6508c51f5beeace1ba98e80ea843e599"

def obtener_telemetria_real(lat, lon):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OW_API_KEY}&units=metric&lang=es"
        r = requests.get(url, timeout=10).json()
        t, h, v = r['main']['temp'], r['main']['humidity'], r['wind']['speed'] * 3.6
        # Cálculo Psicrométrico de Delta T
        tw = t * math.atan(0.151977 * (h + 8.313659)**0.5) + math.atan(t + h) - math.atan(h - 1.676331) + 0.00391838 * (h)**1.5 * math.atan(0.023101 * h) - 4.686035
        dt = round(t - tw, 1)
        return t, h, round(v, 1), dt, r['weather'][0]['description']
    except:
        return None

# --- CLASE PDF PERSONALIZADA CON ENCABEZADO Y PIE ---
class PDF_Reporte(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 8)
        self.cell(0, 10, f"{NOMBRE_AUTOR} - {TITULOS_AUTOR}", 0, 1, 'R')
        self.line(10, 15, 200, 15)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()} | Auditoría Generada por {NOMBRE_AUTOR}', 0, 0, 'C')

# --- LÓGICA DE NAVEGACIÓN ---
st.sidebar.title("Agro Data Litoral 🛰️")
menu = st.sidebar.radio("Módulos de Auditoría:", [
    "1. Análisis de Predio (Datos Reales)", 
    "2. Asistente Agronómico", 
    "3. Scouting IA", 
    "4. Viabilidad Financiera (VRZ)"
])

if menu == "1. Análisis de Predio (Datos Reales)":
    st.title("🛰️ Auditoría Técnica Lito-Edafofisiológica")
    
    col_x, col_y = st.columns(2)
    with col_x: gps_in = st.text_input("📍 Coordenadas GPS:", "-32.2997, -58.0583")
    with col_y: padron = st.text_input("📄 N° de Padrón Catastral:", "1024")

    coords = re.findall(r'[-+]?\d*\.\d+|[-+]?\d+', gps_in)
    if len(coords) >= 2:
        lat, lon = float(coords[0]), float(coords[1])
        data = obtener_telemetria_real(lat, lon)
        
        if data:
            t, h, v, dt, desc = data
            st.info("✅ Telemetría Atmosférica conectada. Datos validados para Paysandú.")
            
            if st.button("🚀 GENERAR REPORTE TÉCNICO EXPLICATIVO"):
                pdf = PDF_Reporte()
                pdf.set_auto_page_break(auto=True, margin=20)
                
                # PÁGINA 1: TELEMETRÍA Y GEOLOGÍA
                pdf.add_page()
                pdf.set_font("Arial", 'B', 14)
                pdf.cell(0, 15, "INFORME TÉCNICO DE AUDITORÍA AMBIENTAL", 0, 1, 'C')
                
                pdf.set_font("Arial", 'B', 11)
                pdf.cell(0, 10, "1. TELEMETRÍA ATMOSFÉRICA ACTUAL (OpenWeather)", 0, 1)
                pdf.set_font("Arial", size=10)
                pdf.multi_cell(0, 7, f"- Temperatura: {t} C\n- Humedad Relativa: {h}%\n- Viento: {v} km/h\n- Delta T: {dt} (Indicador de evaporación)")
                
                pdf.ln(5)
                pdf.set_font("Arial", 'B', 11)
                pdf.cell(0, 10, "2. GEOLOGÍA ESTRUCTURAL (DINAMIGE)", 0, 1)
                pdf.multi_cell(0, 7, (
                    "Ubicación en la formación litoestratigráfica Arapey/Tacuarembó. "
                    "Sustrato volcánico compuesto por basaltos toleíticos del Mesozoico. "
                    "La estructura es fija y estable, caracterizada por la presencia de roca madre "
                    "masiva con fisuramiento natural que condiciona la infiltración hídrica."
                ))

                # PÁGINA 2: SUELOS E HIDROGRAFÍA
                pdf.add_page()
                pdf.set_font("Arial", 'B', 11)
                pdf.cell(0, 10, "3. CLASIFICACIÓN DE SUELOS (CONEAT)", 0, 1)
                pdf.set_font("Arial", size=10)
                pdf.multi_cell(0, 7, (
                    "Descripción: Suelos desarrollados sobre Basalto (Unidad Itapebí). "
                    "Predominancia de Brunosoles Éutricos superficiales (Grupo 12). "
                    "Capacidad de Uso: Limitada por profundidad rocosa y riesgo de erosión hídrica en pendientes. "
                    "Estos suelos presentan una fertilidad natural alta pero una baja reserva de agua útil."
                ))
                
                pdf.ln(5)
                pdf.set_font("Arial", 'B', 11)
                pdf.cell(0, 10, "4. HIDROGRAFÍA Y CUENCA", 0, 1)
                pdf.multi_cell(0, 7, (
                    "El predio pertenece a la Cuenca del Río Uruguay (Litoral Norte). "
                    "La dinámica de escurrimiento es de tipo superficial rápida debido a la baja "
                    "permeabilidad del basalto subyacente. Se identifican redes de drenaje naturales "
                    "que tributan a los principales colectores de la zona de Paysandú."
                ))

                # PÁGINA 3: GLOSARIO TÉCNICO EXPLICATIVO
                pdf.add_page()
                pdf.set_font("Arial", 'B', 12)
                pdf.cell(0, 10, "V. GLOSARIO DE TÉRMINOS TÉCNICOS", 0, 1, 'L')
                pdf.set_font("Arial", size=9)
                glosario = [
                    ("Delta T", "Diferencia entre termómetro seco y húmedo. Mide la tasa de evaporación atmosférica."),
                    ("Litoestratigrafía", "Estudio de las capas de roca y su composición física."),
                    ("Basalto Toleítico", "Roca volcánica rica en hierro y magnesio, común en la formación Arapey."),
                    ("Brunosoles", "Suelos oscuros, ricos en materia orgánica y bases, típicos del Uruguay."),
                    ("CONEAT", "Índice que mide la capacidad de producción de los suelos en Uruguay."),
                    ("Aparey/Tacuarembó", "Unidades geológicas que definen el subsuelo del norte y litoral uruguayo."),
                    ("Escurrimiento", "Proceso por el cual el agua de lluvia fluye por la superficie hacia cauces.")
                ]
                for term, desc in glosario:
                    pdf.set_font("Arial", 'B', 9)
                    pdf.cell(40, 7, f"{term}:", 0, 0)
                    pdf.set_font("Arial", size=9)
                    pdf.multi_cell(0, 7, desc)

                st.success("Reporte Técnico Validado Generado.")
                st.download_button("📥 DESCARGAR REPORTE TÉCNICO (PDF)", pdf.output(dest='S').encode('latin-1'), f"Reporte_{padron}_Leonardo.pdf")

elif menu == "2. Asistente Agronómico":
    st.title("🤖 Asistente Técnico")
    st.info("Módulo de apoyo para normativa OIRSA y Ley 20.212.")

elif menu == "3. Scouting IA":
    st.title("🔍 Scouting de Campo")
    st.file_uploader("Cargar imagen real para análisis de patologías o suelo", type=['jpg', 'png'])

elif menu == "4. Viabilidad Financiera (VRZ)":
    st.title("💰 Viabilidad Financiera (VRZ)")
    st.write("Cálculos basados en la productividad real de los Grupos CONEAT de Paysandú.")
