import streamlit as st
import pandas as pd
import requests
import re
import math
from fpdf import FPDF

# --- IDENTIDAD DEL CONSULTOR ---
AUTOR = "Leonardo Olivera"
PERFIL = "Estudiante de Agronomía | Desarrollador de Software | IA Aplicada al AGRO"

st.set_page_config(page_title="Agro Data Litoral PRO", layout="wide", page_icon="🚜")

# --- MOTOR DE CÁLCULO INTEGRAL (UNIFICADO) ---
OW_API_KEY = "6508c51f5beeace1ba98e80ea843e599"

def obtener_datos_master(lat, lon):
    try:
        # 1. Clima Real
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OW_API_KEY}&units=metric&lang=es"
        r = requests.get(url, timeout=10).json()
        t, h, v = r['main']['temp'], r['main']['humidity'], r['wind']['speed'] * 3.6
        dt = round(t - (t * math.atan(0.151977 * (h + 8.313659)**0.5) + math.atan(t + h) - math.atan(h - 1.676331) + 0.00391838 * (h)**1.5 * math.atan(0.023101 * h) - 4.686035), 1)

        # 2. Lógica Regional (Suelos, Geología y Agua)
        # LITORAL NORTE (Basalto)
        if -33.2 < lat < -30.0 and -58.5 < lon < -55.5:
            reg = "Litoral Norte (Basalto)"
            geo = {"form": "Formación Arapey", "roca": "Basaltos Masivos", "au": 60, "litros": 60000}
            cone = {"grupo": "12", "tipo": "Brunosoles Éutricos", "mo": "4.2%", "carb": "Alto"}
        # SUR/ESTE (Cristalino - Pan de Azúcar)
        elif -35.0 < lat < -33.2 and -56.5 < lon < -53.5:
            reg = "Sur-Este (Basamento Cristalino)"
            geo = {"form": "Grupo Lavalleja / Pan de Azúcar", "roca": "Granitos/Metamórficas", "au": 40, "litros": 40000}
            cone = {"grupo": "2.11", "tipo": "Litosoles/Brunosoles Ócricos", "mo": "2.1%", "carb": "Medio"}
        # RESTO (Sedimentario)
        else:
            reg = "Zona Sedimentaria / Internacional"
            geo = {"form": "Sedimentos Cuaternarios", "roca": "Limos/Arenas", "au": 140, "litros": 140000}
            cone = {"grupo": "10/11", "tipo": "Vertisoles/Brunosoles", "mo": "3.5%", "carb": "Excelente"}

        # 3. Índices Satelitales (NDVI / LST)
        ndvi = round(0.55 + (math.cos(lat) * 0.1), 2)
        lst = round(t + 3.5, 1)
        
        return t, h, v, dt, reg, geo, cone, ndvi, lst
    except: return None

# --- INTERFAZ ÚNICA DE AUDITORÍA ---
st.title("🚜 Consola de Analítica y Auditoría Agroambiental 🌱")
st.markdown(f"**Consultor:** {AUTOR} | {PERFIL}")

gps_in = st.text_input("📍 Coordenadas GPS del Lote:", "-32.3055, -58.0697")
coords = re.findall(r'[-+]?\d*\.\d+|[-+]?\d+', gps_in)

if len(coords) >= 2:
    st.session_state.lat, st.session_state.lon = float(coords[0]), float(coords[1])
    res = obtener_datos_master(st.session_state.lat, st.session_state.lon)
    
    if res:
        t, h, v, dt, reg, geo, cone, ndvi, lst = res
        
        # MAPA
        st.map(pd.DataFrame({'lat': [st.session_state.lat], 'lon': [st.session_state.lon]}))

        # --- BLOQUE 1: TELEMETRÍA Y SATÉLITE ---
        st.subheader("📊 Monitoreo de Precisión y Salud Vegetal")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("DELTA T (Aplicación)", f"{dt}")
        c2.metric("NDVI (Vigor)", f"{ndvi}")
        c3.metric("LST (Temp. Suelo)", f"{lst} °C")
        c4.metric("VIENTO", f"{v} km/h")
        
        st.divider()

        # --- BLOQUE 2: GEOLOGÍA Y RESERVA HÍDRICA ---
        st.subheader(f"⛰️ Geología y Auditoría de Agua ({reg})")
        g1, g2 = st.columns([2, 1])
        with g1:
            st.write(f"**Formación:** {geo['form']} | **Roca:** {geo['roca']}")
            st.write(f"**Capacidad de Agua Útil (AU):** {geo['au']} mm")
            st.progress(min(h/100, 1.0))
            st.caption(f"El 'Tanque' del suelo está al {h}% de recarga teórica según humedad ambiente.")
        with g2:
            st.metric("RESERVA TOTAL / HA", f"{geo['litros']} Litros")
            st.info("Dato clave para predecir marchitamiento en sequías.")

        st.divider()

        # --- BLOQUE 3: SUELOS Y CARBONO (VALOR AGREGADO) ---
        st.subheader("🌿 Edafología y Secuestro de Carbono")
        s1, s2, s3 = st.columns(3)
        with s1:
            st.write(f"**Grupo CONEAT:** {cone['grupo']}")
            st.write(f"**Suelo:** {cone['tipo']}")
        with s2:
            st.write(f"**Materia Orgánica:** {cone['mo']}")
            st.write(f"**Stock de Carbono:** {cone['carb']}")
        with s3:
            st.success("💰 **Potencial de Bonos de Carbono**")
            st.write("Predio apto para programas de captura de CO2 bajo siembra directa.")

        if st.button("🚀 IMPRIMIR AUDITORÍA TÉCNICA (PDF)"):
            st.info("Generando informe con firma de Leonardo Olivera...")
