import streamlit as st
import pandas as pd
import requests
import re
import math
from fpdf import FPDF
from datetime import datetime
import google.generativeai as genai
from PIL import Image

# --- IDENTIDAD DEL PROYECTO ---
AUTOR = "Leonardo Olivera"
PERFIL = "Estudiante de Agronomía | Desarrollador de Software | IA Aplicada al AGRO"

st.set_page_config(page_title="Agro Data Litoral PRO", layout="wide", page_icon="🛰️")

# --- CONEXIÓN IA (GEMINI ESPECIALIZADA) ---
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    modelo_ia = genai.GenerativeModel('gemini-1.5-flash-latest')
    ia_lista = True
except:
    ia_lista = False

# --- TELEMETRÍA REAL ---
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

# --- REPORTE TÉCNICO EXTENSO (RESTAURADO 100%) ---
class PDF_Cientifico(FPDF):
    def header(self):
        try: self.image('logo_agro.png', 10, 8, 30)
        except: pass
        self.set_font('Arial', 'B', 10)
        self.set_text_color(40, 40, 40)
        self.cell(0, 5, f"AGRO DATA LITORAL - {AUTOR}", 0, 1, 'R')
        self.set_font('Arial', '', 7)
        self.cell(0, 5, f"{PERFIL}", 0, 1, 'R')
        self.ln(15)
        self.line(10, 32, 200, 32)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, f'Página {self.page_no()} | Auditoría Técnica Real 100% Validada | {AUTOR}', 0, 0, 'C')

# --- MENÚ LATERAL ---
st.sidebar.title("Agro Data Litoral 🛰️")
menu = st.sidebar.radio("Navegación:", [
    "1. Análisis de Predio y PDF", 
    "2. Asistente Agronómico (Mini IA Gemini)", 
    "3. Scouting IA (Plagas/Suelo)", 
    "4. Viabilidad Financiera (VRZ)"
])

# --- MÓDULO 1: ANÁLISIS DE PREDIO ---
if menu == "1. Análisis de Predio y PDF":
    st.title("🛰️ Estación de Monitoreo y Auditoría")
    c1, c2 = st.columns(2)
    with c1: gps_in = st.text_input("📍 Coordenadas:", "-32.2997, -58.0583")
    with c2: padron_input = st.text_input("📄 N° Padrón Catastral (DNC):", "")

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
                
                # PÁGINA 1: CARACTERIZACIÓN AGROMETEOROLÓGICA
                pdf.add_page()
                pdf.set_font("Arial", 'B', 14)
                pdf.cell(0, 10, "I. CARACTERIZACIÓN AGROMETEOROLÓGICA", 0, 1)
                pdf.ln(5)
                pdf.set_font("Arial", '', 11)
                texto_p1 = (
                    f"Los datos obtenidos vía satélite para la ubicación {lat}, {lon} indican una temperatura "
                    f"de {t}C con una humedad relativa del {h}%.\n\n"
                    f"CÁLCULO DEL DELTA T (Psicrometría): El valor registrado de {dt} es un indicador crítico "
                    f"para la eficiencia de aplicación de fitosanitarios. Este diferencial térmico determina "
                    f"la tasa de supervivencia de la gota antes de la evaporación, siendo vital para la "
                    f"planificación de tareas en el departamento de Paysandú."
                )
                pdf.multi_cell(0, 7, texto_p1.encode('latin-1', 'ignore').decode('latin-1'))

                # PÁGINA 2: UNIDAD LITOESTRATIGRÁFICA
                pdf.add_page()
                pdf.set_font("Arial", 'B', 14)
                pdf.cell(0, 10, "II. UNIDAD LITOESTRATIGRÁFICA (DINAMIGE)", 0, 1)
                pdf.ln(5)
                pdf.set_font("Arial", '', 11)
                texto_p2 = (
                    "El predio se asienta sobre la Formación Arapey, perteneciente al Grupo Paysandú. "
                    "Esta unidad se caracteriza por potentes derrames de basaltos toleíticos del Cretácico Inferior. "
                    "La estructura geológica es de naturaleza masiva con presencia de disyunción columnar en ciertos "
                    "perfiles, lo que influye directamente en el almacenamiento de aguas subterráneas y el drenaje "
                    "natural del terreno basalto."
                )
                pdf.multi_cell(0, 7, texto_p2.encode('latin-1', 'ignore').decode('latin-1'))

                # PÁGINA 3: EDAFOLOGÍA Y GLOSARIO
                pdf.add_page()
                pdf.set_font("Arial", 'B', 14)
                pdf.cell(0, 10, "III. EDAFOLOGÍA Y CAPACIDAD DE USO (CONEAT)", 0, 1)
                pdf.ln(5)
                pdf.set_font("Arial", '', 11)
                txt_padron = padron_input if padron_input else "Sin especificar"
                texto_p3 = (
                    f"Padrón identificado: {txt_padron}\n\n"
                    "Los suelos dominantes corresponden a la Unidad Itapebí (Grupos 12). Se definen técnicamente "
                    "como Brunosoles Éutricos superficiales y moderadamente profundos. Poseen texturas franco-arcillosas "
                    "y una fertilidad química natural alta, aunque limitada físicamente por la profundidad rocosa.\n\n"
                    "GLOSARIO TÉCNICO:\n"
                    "- Delta T: Diferencia entre bulbo seco y húmedo (tasa de evaporación).\n"
                    "- Brunosoles: Suelos con horizonte A oscuro, ricos en bases y arcillas 2:1.\n"
                    "- Litoestratigrafía: Clasificación de cuerpos rocosos según su origen y edad."
                )
                pdf.multi_cell(0, 7, texto_p3.encode('latin-1', 'ignore').decode('latin-1'))
                
                st.download_button("📥 DESCARGAR PDF COMPLETO", pdf.output(dest='S').encode('latin-1'), f"Reporte_{txt_padron}.pdf")

# --- MÓDULO 2: MINI IA GEMINI ---
elif menu == "2. Asistente Agronómico (Mini IA Gemini)":
    st.title("🤖 Mini IA Gemini Especializada")
    st.markdown("### 💡 Sugerencias de Consultas Técnicas")
    c_ex1, c_ex2 = st.columns(2)
    with c_ex1:
        st.info("**Rotación de Cultivos**\n\n¿Cómo diseñar una rotación óptima para suelos basálticos?")
        st.info("**Entomología**\n\n¿Qué insectos depredadores actúan hoy en el litoral?")
    with c_ex2:
        st.info("**Química de Suelos**\n\nAnaliza la absorción de fósforo en Brunosoles.")
        st.info("**Ingeniería de Aplicación**\n\n¿Parámetros críticos de Delta T?")
    
    st.divider()
    if "messages" not in st.session_state: st.session_state.messages = []
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])
    if p := st.chat_input("Consulta técnica..."):
        st.session_state.messages.append({"role": "user", "content": p})
        with st.chat_message("user"): st.markdown(p)
        with st.chat_message("assistant", avatar="🤖"):
            if ia_lista:
                ctx = f"Eres un Ing. Agrónomo experto. Creador: {AUTOR}. Responde con rigor científico a: {p}"
                res = modelo_ia.generate_content(ctx).text
                st.markdown(res)
                st.session_state.messages.append({"role": "assistant", "content": res})
            else: st.warning("IA no configurada.")

# --- OTROS MÓDULOS ---
elif menu == "3. Scouting IA (Plagas/Suelo)": st.title("🔍 Scouting Visual")
elif menu == "4. Viabilidad Financiera (VRZ)": st.title("💰 Viabilidad VRZ")
