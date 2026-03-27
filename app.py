import streamlit as st
import pandas as pd
import numpy as np
import io
import re
from fpdf import FPDF
import google.generativeai as genai
from PIL import Image

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Agro Data Litoral PRO", layout="wide", page_icon="🛰️")

# --- CONEXIÓN CON GEMINI PRO ---
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    modelo_ia = genai.GenerativeModel('gemini-1.5-pro')
    ia_activa = True
except Exception as e:
    ia_activa = False
    st.sidebar.error("⚠️ Falta configurar GEMINI_API_KEY en los secrets.")

# --- TRADUCTOR INTELIGENTE DE COORDENADAS ---
def convertir_coordenadas(texto_coords):
    texto = texto_coords.upper()
    if '°' in texto or 'S' in texto or 'W' in texto or "'" in texto:
        numeros = re.findall(r'[\d\.]+', texto)
        letras = re.findall(r'[NSWE]', texto)
        if len(numeros) >= 6 and len(letras) >= 2:
            lat = float(numeros[0]) + float(numeros[1])/60 + float(numeros[2])/3600
            lon = float(numeros[3]) + float(numeros[4])/60 + float(numeros[5])/3600
            if letras[0] == 'S': lat = -lat
            if letras[1] == 'W': lon = -lon
            return lat, lon
            
    numeros_decimales = re.findall(r'[-+]?\d*\.\d+|[-+]?\d+', texto)
    if len(numeros_decimales) >= 2:
        return float(numeros_decimales[0]), float(numeros_decimales[1])
        
    return None, None

# --- CLASE PARA EL INFORME PDF ---
class AgroInformeFinal(FPDF):
    def __init__(self, cliente, lat, lon, padron, depto):
        super().__init__()
        self.cliente = cliente
        self.lat, self.lon = lat, lon
        self.padron, self.depto = padron, depto

    def header(self):
        self.set_font('Helvetica', 'B', 16)
        self.set_text_color(0, 77, 64)
        self.cell(0, 10, "AGRO DATA LITORAL - AUDITORIA INTELIGENTE", 0, 1, 'C')
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(100)
        self.cell(0, 5, "INTELIGENCIA ARTIFICIAL APLICADA AL AGRO", 0, 1, 'C')
        self.line(10, 30, 200, 30)
        self.ln(15)

    def footer(self):
        self.set_y(-25)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128)
        self.multi_cell(0, 4, f"Desarrollado por: Leonardo Olivera | Agro Data Litoral\nTecnología y Agronomía Aplicada\nPágina {self.page_no()}", 0, 'C')

    def portada(self):
        self.add_page()
        self.ln(40)
        self.set_font('Helvetica', 'B', 26)
        self.cell(0, 20, "REPORTE AGRONÓMICO ASISTIDO POR IA", 0, 1, 'C')
        self.ln(10)
        self.set_font('Helvetica', '', 14)
        self.cell(0, 10, f"SOLICITANTE: {self.cliente.upper()}", 0, 1, 'C')
        self.ln(20)
        
        self.set_fill_color(240, 240, 240)
        self.set_font('Helvetica', 'B', 12)
        self.cell(0, 10, "  IDENTIFICACIÓN DEL ACTIVO", 1, 1, 'L', fill=True)
        self.set_font('Helvetica', '', 11)
        self.cell(95, 10, f" PADRÓN: {self.padron}", 1, 0)
        self.cell(95, 10, f" DEPTO: {self.depto}", 1, 1)
        self.cell(95, 10, f" LATITUD: {self.lat:.4f}", 1, 0)
        self.cell(95, 10, f" LONGITUD: {self.lon:.4f}", 1, 1)

# --- MENÚ LATERAL ---
st.sidebar.title("🛰️ Agro Data Litoral")
menu = st.sidebar.radio("Navegación", [
    "1. Análisis de Predio y PDF", 
    "2. Asistente Agronómico (Chat)", 
    "3. Scouting IA (Plagas/Suelo)",
    "4. Viabilidad Financiera (VRZ)"
])
st.sidebar.divider()

# ==========================================
# MÓDULO 1: ANÁLISIS DE PREDIO Y REPORTE PDF
# ==========================================
if menu == "1. Análisis de Predio y PDF":
    st.title("🗺️ Panel de Control y Auditoría Satelital")
    
    col_input1, col_input2 = st.columns(2)
    with col_input1:
        url_input = st.text_input("Enlace Google Maps / Coordenadas:", "32°17'59.0\"S 58°03'29.0\"W")
        cliente = st.text_input("Cliente / Empresa:", "Productor Litoral")
    with col_input2:
        padron = st.text_input("Padrón:", "1234")
        depto = st.selectbox("Departamento:", ["Paysandú", "Río Negro", "Soriano", "Salto", "Artigas"])

    try:
        lat, lon = convertir_coordenadas(url_input)
        
        if lat is not None and lon is not None:
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("🌡️ TEMP. SUELO", "22.5°C")
            c2.metric("🌿 VIGOR (NDVI)", "0.82")
            c3.metric("🪨 SUELO PREDOMINANTE", "Franco")
            c4.metric("💧 HUMEDAD", "65%")

            st.map(pd.DataFrame({'lat': [lat], 'lon': [lon]}), zoom=13)

            if st.button("🚀 GENERAR AUDITORÍA PROFESIONAL CON IA", use_container_width=True):
                if ia_activa:
                    with st.spinner('Procesando datos del terreno con Gemini Pro...'):
                        prompt_pdf = f"Actúa como un ingeniero agrónomo de Agro Data Litoral. Redacta un informe técnico de 3 párrafos sobre el potencial agrícola, tipo de suelo esperado y riesgos climáticos para un campo en {depto}, Uruguay (Padrón {padron}). Usa lenguaje técnico, formal y no uses asteriscos de formato."
                        respuesta_ia = modelo_ia.generate_content(prompt_pdf).text
                        
                        pdf = AgroInformeFinal(cliente, lat, lon, padron, depto)
                        pdf.portada()
                        pdf.add_page()
                        pdf.set_font('Helvetica', 'B', 14)
                        pdf.cell(0, 10, "EVALUACIÓN AGRONÓMICA ESTRUCTURAL", 0, 1)
                        pdf.set_font('Helvetica', '', 11)
                        
                        texto_limpio = respuesta_ia.replace('**', '').replace('*', '').replace('“', '"').replace('”', '"').replace('—', '-')
                        texto_limpio = texto_limpio.encode('latin-1', 'ignore').decode('latin-1')
                        
                        pdf.multi_cell(0, 6, texto_limpio)
                        
                        pdf_bytes = pdf.output(dest='S')
                        if isinstance(pdf_bytes, str):
                            pdf_bytes = pdf_bytes.encode('latin-1', errors='replace')
                            
                        st.session_state['pdf_final'] = pdf_bytes
                        st.success("✅ Auditoría Generada Exitosamente")
                else:
                    st.error("La IA no está conectada. Revisa tu API Key.")
                    
            if 'pdf_final' in st.session_state:
                st.download_button("📥 DESCARGAR INFORME EN PDF", st.session_state['pdf_final'], f"Auditoria_{padron}_{depto}.pdf")

        else:
            st.warning("⚠️ Formato de coordenada no reconocido. Intenta usar números (ej: -32.32, -58.07) o grados (ej: 32°17'59\"S 58°03'29\"W).")

    except Exception as e:
        st.error(f"Error interno detectado: {e}")

# ==========================================
# MÓDULO 2: ASISTENTE AGRONÓMICO (TIPO ORTH)
# ==========================================
elif menu == "2. Asistente Agronómico (Chat)":
    st.title("🤖 Asistente Virtual IA")
    st.caption("Consulta sobre manejo de cultivos, clima, carencias y herbicidas. El asistente recuerda el contexto.")

    if "mensajes_chat" not in st.session_state:
        st.session_state.mensajes_chat = [{"role": "assistant", "content": "Hola. Soy el cerebro de Agro Data Litoral. ¿En qué etapa de la zafra te encuentras hoy?"}]

    for mensaje in st.session_state.mensajes_chat:
        with st.chat_message(mensaje["role"]):
            st.markdown(mensaje["content"])

    if prompt := st.chat_input("Escribe tu consulta agronómica aquí..."):
        st.session_state.mensajes_chat.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        if ia_activa:
            with st.chat_message("assistant"):
                historial = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.mensajes_chat[-5:]])
                instruccion = "Eres el asistente de la aplicación Agro Data Litoral en Uruguay. Responde como un ingeniero agrónomo experto, directo y preciso. Prioriza la rentabilidad y el cuidado del suelo."
                prompt_completo = f"{instruccion}\nHistorial reciente:\n{historial}\n\nResponde a lo último."
                
                respuesta = modelo_ia.generate_content(prompt_completo).text
                st.markdown(respuesta)
                st.session_state.mensajes_chat.append({"role": "assistant", "content": respuesta})

# ==========================================
# MÓDULO 3: SCOUTING ASISTIDO POR IA VISIÓN
# ==========================================
elif menu == "3. Scouting IA (Plagas/Suelo)":
    st.title("🔍 Módulo de Scouting en Campo")
    st.write("Sube una foto de una hoja enferma, una plaga o el estado del suelo para obtener un diagnóstico inmediato.")
    
    archivo_foto = st.file_uploader("Cargar imagen", type=['jpg', 'jpeg', 'png'])
    if archivo_foto is not None:
        imagen = Image.open(archivo_foto)
        st.image(imagen, caption="Imagen cargada", use_column_width=True)
        
        if st.button("Analizar Imagen con IA", use_container_width=True):
            if ia_activa:
                with st.spinner('Analizando patología vegetal...'):
                    prompt_vision = "Eres un fitopatólogo experto. Analiza esta imagen. Identifica qué cultivo es, si existe alguna enfermedad, deficiencia nutricional o plaga, y recomienda un plan de acción para el Litoral de Uruguay."
                    respuesta_vision = modelo_ia.generate_content([prompt_vision, imagen])
                    
                    st.subheader("📋 Diagnóstico Agro Data Litoral:")
                    st.write(respuesta_vision.text)
            else:
                 st.error("IA no conectada.")

# ==========================================
# MÓDULO 4: ANÁLISIS VRZ
# ==========================================
elif menu == "4. Viabilidad Financiera (VRZ)":
    st.title("📉 Análisis de Viabilidad y Riesgo de Zafra")
    st.write("Calculadora rápida de márgenes brutos para toma de decisiones.")
    
    c1, c2, c3 = st.columns(3)
    cultivo = c1.selectbox("Cultivo", ["Soja", "Trigo", "Maíz", "Sorgo"])
    precio_usd = c2.number_input(f"Precio Estimado (USD/Tn)", value=400)
    rinde_esperado = c3.number_input("Rendimiento (Tn/Ha)", value=3.0)
    
    costo_labores = st.slider("Costos de Labores e Insumos (USD/Ha)", 100, 1000, 450)
    costo_arrendamiento = st.number_input("Arrendamiento (USD/Ha) - 0 si es propio", value=0)
    
    ingreso_bruto = precio_usd * rinde_esperado
    costo_total = costo_labores + costo_arrendamiento
    margen_neto = ingreso_bruto - costo_total
    
    st.divider()
    if margen_neto > 0:
        st.success(f"📈 Margen Positivo: **${margen_neto:.2f} USD por Hectárea**")
    else:
        st.error(f"📉 Alerta de Riesgo - Margen Negativo: **${margen_neto:.2f} USD por Hectárea**")
    
    st.info(f"Punto de equilibrio de rendimiento: **{costo_total / precio_usd:.2f} Tn/Ha** para cubrir costos.")