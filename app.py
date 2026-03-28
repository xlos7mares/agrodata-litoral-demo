import streamlit as st
import pandas as pd
import requests
import re
import math
from fpdf import FPDF

# --- IDENTIDAD PROFESIONAL ---
AUTOR = "Leonardo Olivera"
PERFIL = "Estudiante de Agronomía | Desarrollador de Software | IA Aplicada al AGRO"

st.set_page_config(page_title="Agro Data Litoral PRO - Auditoría Total", layout="wide", page_icon="🚜")

# --- MOTOR DE DATOS DINÁMICOS ---
OW_API_KEY = "6508c51f5beeace1ba98e80ea843e599"

def obtener_datos_auditoria(lat, lon):
    try:
        # 1. Telemetría Atmosférica Real
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OW_API_KEY}&units=metric&lang=es"
        r = requests.get(url, timeout=10).json()
        t, h, v = r['main']['temp'], r['main']['humidity'], r['wind']['speed'] * 3.6
        dt = round(t - (t * math.atan(0.151977 * (h + 8.313659)**0.5) + math.atan(t + h) - math.atan(h - 1.676331) + 0.00391838 * (h)**1.5 * math.atan(0.023101 * h) - 4.686035), 1)

        # 2. LÓGICA DE GEOLOGÍA Y SUELOS (MAPA DINÁMICO DE URUGUAY)
        # ZONA NORTE (BASALTO - Formación Arapey)
        if -33.2 < lat < -30.0 and -58.5 < lon < -55.5:
            color = "🟫 (Marrón/Violeta)"
            geo_info = {"form": "Formación Arapey", "era": "Mesozoico (Cretácico)", "roca": "Basaltos masivos", "litros": "30,000 - 50,000 L/Ha (Estratificado)"}
            cone_info = {"grupo": "12 / 1.12", "suelo": "Brunosoles Éutricos", "desc": "Suelos pesados, alta fertilidad química, drenaje lento."}
        
        # ZONA SUR/ESTE (CRISTALINO - Formaciones Antiguas)
        elif -35.0 < lat < -33.2 and -56.5 < lon < -53.5:
            color = "🟥 (Rojo/Rosa)"
            geo_info = {"form": "Grupo Lavalleja / Formación Pan de Azúcar", "era": "Precámbrico (Basamento)", "roca": "Granitos y Metamórficas", "litros": "10,000 - 20,000 L/Ha (Fisuras)"}
            cone_info = {"grupo": "2.11 / 2.21", "suelo": "Litosoles y Brunosoles Ócricos", "desc": "Suelos superficiales, pedregosos, alta pendiente."}

        # ZONA LITORAL SUR / SORIANO-COLONIA (SEDIMENTOS)
        elif -34.5 < lat < -33.0 and -58.5 < lon < -56.5:
            color = "🟨 (Amarillo/Verde Claro)"
            geo_info = {"form": "Formación Libertad / Raigón", "era": "Cenozoico (Cuaternario)", "roca": "Sedimentos Limosos/Arenosos", "litros": "150,000+ L/Ha (Acuíferos Libres)"}
            cone_info = {"grupo": "10 / 11", "suelo": "Vertisoles / Brunosoles", "desc": "Máximo potencial agrícola de Uruguay."}

        # RESTO DEL PAÍS / MUNDO
        else:
            color = "⬜ (Blanco)"
            geo_info = {"form": "No Identificada localmente", "era": "N/A", "roca": "Corteza Terrestre", "litros": "Dato In-situ requerido"}
            cone_info = {"grupo": "S/D", "suelo": "Suelo General", "desc": "Requiere verificación por calicata."}

        return t, h, v, dt, color, geo_info, cone_info
    except: return None

# --- PANTALLA ÚNICA DE AUDITORÍA ---
st.title("🚜 Agro Data Litoral PRO - Consola de Ingeniería Unificada 🌱")
st.markdown(f"**Consultor:** {AUTOR} | {PERFIL}")

gps_in = st.text_input("📍 Ingrese Coordenadas GPS del Lote:", "-32.3, -58.1")
coords = re.findall(r'[-+]?\d*\.\d+|[-+]?\d+', gps_in)

if len(coords) >= 2:
    lat, lon = float(coords[0]), float(coords[1])
    res = obtener_datos_auditoria(lat, lon)
    
    if res:
        t, h, v, dt, color, geo, cone = res
        
        # 1. MAPA Y SATÉLITE
        c_map1, c_map2 = st.columns([2, 1])
        with c_map1:
            st.map(pd.DataFrame({'lat': [lat], 'lon': [lon]}))
        with c_map2:
            st.markdown("### 🗺️ Leyenda Geológica (DINAMIGE)")
            st.write("🟥 **Rojo:** Basamento Cristalino (Antiguo/Duro)")
            st.write("🟫 **Marrón:** Efusivas Basálticas (Arapey/Norte)")
            st.write("🟨 **Amarillo:** Sedimentos (Cenozoico/Fértil)")
            st.info(f"**Ubicación Detectada:** {color}")

        st.divider()

        # 2. TELEMETRÍA Y RIESGO
        st.markdown("### 🌡️ Telemetría Atmosférica y Riesgo de Aplicación")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("TEMPERATURA", f"{t} °C")
        m2.metric("HUMEDAD", f"{h} %")
        m3.metric("VIENTO", f"{v} km/h")
        m4.metric("DELTA T", f"{dt}")
        st.caption("El Delta T es el indicador crítico para la supervivencia de la gota en pulverización.")

        st.divider()

        # 3. GEOLOGÍA E HIDROLOGÍA (PEDAGÓGICO)
        st.markdown("### ⛰️ Auditoría Geológica y Capacidad de Agua")
        g1, g2, g3 = st.columns(3)
        with g1:
            st.subheader("Estratigrafía")
            st.write(f"**Formación:** {geo['form']}")
            st.write(f"**Era Geológica:** {geo['era']}")
        with g2:
            st.subheader("Litología")
            st.write(f"**Roca Madre:** {geo['roca']}")
            st.write(f"**Color en Mapa:** {color}")
        with g3:
            st.subheader("Hidrología")
            st.write(f"**Capacidad Infiltración:** {geo['litros']}")
            st.write("**Uso:** Reserva de agua útil en perfil.")

        st.divider()

        # 4. EDAFOLOGÍA Y VRZ (SUELOS Y FINANZAS)
        st.markdown("### 🧪 Suelos CONEAT y Viabilidad VRZ")
        s1, s2, s3 = st.columns(3)
        with s1:
            st.write(f"**Grupo CONEAT:** {cone['grupo']}")
            st.write(f"**Clasificación:** {cone['suelo']}")
        with s2:
            st.write(f"**Descripción Técnica:** {cone['desc']}")
        with s3:
            coneat_val = st.number_input("Ajustar Índice CONEAT Real:", 100)
            rend_est = (coneat_val / 100) * 3.5
            st.metric("RENDIMIENTO ESTIMADO", f"{round(rend_est, 2)} Ton/Ha")

        if st.button("🚀 GENERAR INFORME TÉCNICO INTEGRAL (PDF)"):
            st.success("Informe generado con éxito. (Aquí se activaría la descarga del PDF unificado)")
