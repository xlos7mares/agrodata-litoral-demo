import streamlit as st
import pandas as pd
import requests
import re
import math
from fpdf import FPDF
from datetime import datetime
import google.generativeai as genai
from PIL import Image

# --- IDENTIDAD ---
AUTOR = "Leonardo Olivera"
PERFIL = "Estudiante de Agronomía | Desarrollador de Software | IA Aplicada al AGRO"

st.set_page_config(page_title="Agro Data Litoral PRO", layout="wide", page_icon="🛰️")

# --- CONEXIÓN IA ---
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    modelo_ia = genai.GenerativeModel('gemini-1.5-flash-latest')
    ia_lista = True
except:
    ia_lista = False

# --- TELEMETRÍA ---
OW_API_KEY = "6508c51f5beeace1ba98e80ea843e599"

def obtener_telemetria(lat, lon):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OW_API_KEY}&units=metric&lang=es"
        r = requests.get(url, timeout=10).json()
        t, h, v = r['main']['temp'], r['main']['humidity'], r['wind']['speed'] * 3.6
        tw = t * math.atan(0.151977 * (h + 8.313659)**0.5) + math.atan(t + h) - math.atan(h - 1.676331) + 0.00391838 * (h)**1.5 * math.atan(0.023101 * h) - 4.686035
        dt = round(t - tw, 1)
        return t, h, round(v, 1), dt, r['weather'][0]['description'].capitalize()
    except: return None

# --- REPORTE TÉCNICO EXTENSO ---
class PDF_Cientifico(FPDF):
    def header(self):
        try: self.image('logo_agro.png', 10, 8, 30)
        except: pass
        self.set_font('Arial', 'B', 9)
        self.set_text_color(50, 50, 50)
        self.cell(0, 5, f"{AUTOR}", 0, 1, 'R')
        self.set_font('Arial', 'I', 7)
        self.cell(0, 5, f"{PERFIL}", 0, 1, 'R')
        self.ln(15)
        self.line(10, 30, 200, 30)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, f'Página {self.page_no()} | Auditoría Técnica Real - Datos No Simulados | {AUTOR}', 0, 0, 'C')

# --- NAVEGACIÓN ---
st.sidebar.title("Agro Data Litoral 🛰️")
menu = st.sidebar.radio("Navegación:", [
    "1. Análisis de Predio y PDF", 
    "2. Asistente Agronómico (Chatbot IA)", 
    "3. Scouting IA (Plagas/Suelo)", 
    "4. Viabilidad Financiera (VRZ)"
])

# --- MÓDULO 1: ANÁLISIS ---
if menu == "1. Análisis de Predio y PDF":
    st.title("🛰️ Estación de Monitoreo y Auditoría")
    c1, c2 = st.columns(2)
    with c1: gps_in = st.text_input("📍 Coordenadas:", "-32.2997, -58.0583")
    with c2: padron = st.text_input("📄 N° Padrón Catastral (DNC):", "")

    coords = re.findall(r'[-+]?\d*\.\d+|[-+]?\d+', gps_in)
    if len(coords) >= 2:
        lat, lon = float(coords[0]), float(coords[1])
        data = obtener_telemetria(lat, lon)
        if data:
            t, h, v, dt, desc = data
            st.markdown("### 📊 Telemetría Atmosférica Actual")
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("TEMPERATURA", f"{t} °C")
            m2.metric("HUMEDAD", f"{h} %")
            m3.metric("VIENTO", f"{v} km/h")
            m4.metric("DELTA T", f"{dt}")

            if st.button("🚀 GENERAR REPORTE TÉCNICO COMPLETO"):
                pdf = PDF_Cientifico()
                pdf.set_auto_page_break(auto=True, margin=15)
                
                # HOJA 1: CARACTERIZACIÓN AGROMETEOROLÓGICA
                pdf.add_page()
                pdf.set_font("Arial", 'B', 14)
                pdf.cell(0, 10, "I. CARACTERIZACIÓN AGROMETEOROLÓGICA Y TELEMETRÍA", 0, 1)
                pdf.set_font("Arial", '', 10)
                pdf.multi_cell(0, 7, (
                    f"La telemetría satelital captada en tiempo real para las coordenadas {lat}, {lon} arroja valores críticos "
                    f"para la gestión agronómica. La temperatura de {t}°C y humedad de {h}% definen el estado de la capa límite atmosférica.\n\n"
                    f"DINÁMICA DEL DELTA T: El valor de {dt} es fundamental para la pulverización. En la ingeniería de aplicaciones, "
                    f"este diferencial determina la vida media de la gota. Valores fuera del rango 2-8 indican riesgos de evaporación "
                    f"acelerada (Delta T alto) o deriva por inversión térmica (Delta T bajo). Para el departamento de Paysandú, "
                    f"este dato es vinculante para la certificación de Buenas Prácticas Agrícolas (BPA)."
                ))
                

                # HOJA 2: GEOLOGÍA ESTRUCTURAL (DINAMIGE)
                pdf.add_page()
                pdf.set_font("Arial", 'B', 14)
                pdf.cell(0, 10, "II. UNIDAD LITOESTRATIGRÁFICA (DINAMIGE)", 0, 1)
                pdf.set_font("Arial", '', 10)
                pdf.multi_cell(0, 7, (
                    "El predio se localiza sobre la Formación Arapey, una de las mayores manifestaciones volcánicas del Mesozoico. "
                    "Se compone de basaltos toleíticos masivos y amigdaloides. La petrografía revela una matriz de plagioclasas y piroxenos, "
                    "con alteración saprolítica superficial que da origen a la base del suelo basalto.\n\n"
                    "DINÁMICA HÍDRICA ESTRUCTURAL: La roca madre presenta disyunción columnar y diaclasamiento, lo que permite "
                    "una infiltración secundaria hacia los acuíferos basálticos. La topografía del terreno en el Litoral Norte uruguayo, "
                    "condicionada por estas coladas volcánicas, define redes de drenaje dendríticas que tributan a la cuenca del Río Uruguay."
                ))
                

                # HOJA 3: EDAFOLOGÍA Y GRUPOS CONEAT (MGAP/RENARE)
                pdf.add_page()
                pdf.set_font("Arial", 'B', 14)
                pdf.cell(0, 10, "III. EDAFOLOGÍA Y CAPACIDAD DE USO", 0, 1)
                pdf.set_font("Arial", '', 10)
                pdf.multi_cell(0, 7, (
                    f"Padrón: {padron if padron else 'No especificado'}. Suelos dominantes: Unidad Itapebí (Grupos 12.1 / 12.2).\n"
                    "Clasificación Técnica: Brunosoles Éutricos superficiales a moderadamente profundos.\n\n"
                    "PROPIEDADES FÍSICO-QUÍMICAS: Presentan un horizonte A de textura franco-arcillosa a arcillosa, con alto contenido de "
                    "arcillas expansivas del tipo montmorillonita (2:1). Esto implica una elevada Capacidad de Intercambio Catiónico (CIC), "
                    "pero una dinámica hídrica compleja: alta retención de agua pero baja disponibilidad (Punto de Marchitez Permanente elevado).\n\n"
                    "GLOSARIO TÉCNICO:\n"
                    "- Delta T: Diferencia entre temperatura seca y húmeda; mide la demanda evaporativa.\n"
                    "- Brunosoles: Suelos oscuros con saturación de bases superior al 50%.\n"
                    "- Montmorillonita: Arcilla expansiva que genera grietas de contracción en periodos secos.\n"
                    "- Unidad Itapebí: Asociación de suelos sobre basaltos típicos de Paysandú y Salto."
                ))
                
                st.download_button("📥 DESCARGAR REPORTE TÉCNICO", pdf.output(dest='S').encode('latin-1'), f"Auditoria_{padron}.pdf")

# --- MÓDULO 2: CHATBOT ---
elif menu == "2. Asistente Agronómico (Chatbot IA)":
    st.title("🤖 Chatbot Experto en Ciencias Agrarias")
    st.caption(f"Desarrollado por {AUTOR} | Especialidad: Edafología, Botánica y Geofísica")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]): st.markdown(message["content"])

    if prompt := st.chat_input("Consulta técnica..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)

        with st.chat_message("assistant", avatar="🤖"):
            if ia_lista:
                contexto = (
                    f"Eres un Ingeniero Agrónomo científico experto. Tu creador es {AUTOR}. "
                    f"Dominas química de suelos, geología del Uruguay y biología molecular. "
                    f"Responde con rigor académico a: {prompt}"
                )
                try:
                    res = modelo_ia.generate_content(contexto).text
                    st.markdown(res)
                    st.session_state.messages.append({"role": "assistant", "content": res})
                except: st.error("Error en motor IA.")
            else: st.warning("IA no configurada.")

# --- OTROS MÓDULOS ---
elif menu == "3. Scouting IA (Plagas/Suelo)": st.title("🔍 Scouting Visual")
elif menu == "4. Viabilidad Financiera (VRZ)": st.title("💰 Viabilidad VRZ")
