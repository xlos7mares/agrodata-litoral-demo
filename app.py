import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.graph_objects as go

# Configuración de página con fondo claro y diseño profesional
st.set_page_config(page_title="AgroData Litoral Pro", layout="wide")

# Estilo para cuadros BLANCOS y CLAROS (Optimizado para celulares)
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: 2px solid #28a745;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 2px 4px 10px rgba(0,0,0,0.1);
    }
    div[data-testid="stMetricLabel"] { color: #333333 !important; font-size: 18px !important; font-weight: bold !important; }
    div[data-testid="stMetricValue"] { color: #000000 !important; font-size: 32px !important; }
    h1, h2, h3 { color: #1e4d2b !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌾 AgroData Litoral: Inteligencia de Precisión")
st.write("---")

# --- BARRA LATERAL: EL DISPARADOR DE ACCIÓN ---
st.sidebar.header("📍 Gestión de Mi Campo")
padrón = st.sidebar.text_input("Ingrese Nro de Padrón o Coordenadas")

if st.sidebar.button("ANALIZAR MI CAMPO"):
    st.sidebar.error("❌ ACCESO BLOQUEADO")
    st.sidebar.markdown("""
    **Su campo requiere validación de coordenadas.**
    
    Para activar el reporte real de su padrón:
    1. Solicite su ID de acceso.
    2. Envíe ubicación por WhatsApp.
    3. Realice el giro de activación.
    """)
    st.sidebar.link_button("📲 SOLICITAR ACTIVACIÓN", "https://wa.me/59899417716")

# --- CUERPO PRINCIPAL ---
tabs = st.tabs(["📊 Monitor de Riesgo", "💎 ¿Por qué es Vital?", "❓ Preguntas Frecuentes"])

with tabs[0]:
    st.info("⚠️ MODO DEMO: Datos del 'Establecimiento El Milagro' (Young)")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Humedad en Raíz (1m)", "14.2%", "-3.8% CRÍTICO", delta_color="inverse")
    with col2:
        st.metric("Déficit de Lluvia (10 días)", "24mm", "Evapotranspiración Alta")
    with col3:
        st.metric("PÉRDIDA PROYECTADA", "u$s 18,400", "Basado en 100 Ha", delta_color="inverse")

    # GRÁFICO MEJORADO
    st.subheader("📈 El Costo de la Espera: Humedad vs. Rendimiento Económico")
    dias = np.array(range(1, 11))
    humedad = [18, 17, 15, 14, 12, 11, 10, 9, 8, 7]
    perdida_usd = [0, 500, 1200, 2500, 4800, 7000, 10000, 13500, 16000, 18400]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dias, y=humedad, name='Humedad Suelo (%)', line=dict(color='#28a745', width=4)))
    fig.add_trace(go.Bar(x=dias, y=perdida_usd, name='Pérdida Acumulada (u$s)', marker_color='#dc3545', opacity=0.7))
    
    fig.update_layout(
        title="Si la humedad baja del 12%, su dinero desaparece",
        xaxis_title="Días sin lluvia",
        template="plotly_white",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig, use_container_width=True)

with tabs[1]:
    st.header("🚀 ¿Por qué AgroData es Inevitable?")
    st.markdown("""
    ### 💰 El Seguro más barato de su historia
    Un error en la aplicación de fertilizante por falta de humedad le cuesta **u$s 5,000** en una tarde. 
    Entrar con la maquinaria en suelo saturado le rompe la estructura del campo por **3 años**.

    **Con AgroData Litoral usted ahorra:**
    * **Gasoil:** No salga al campo a "ver cómo está" si el satélite ya le dice que no hay piso.
    * **Insumos:** Aplique solo cuando la planta tiene el agua necesaria para procesar el nutriente.
    * **Rendimiento:** Gane entre un **15% y 25% más** de kilos por hectárea.
    """)

with tabs[2]:
    st.header("❓ Respuestas para el Productor Exigente")
    with st.expander("1. ¿En qué se diferencia de AccuWeather o el pronóstico común?"):
        st.write("AccuWeather te dice si llueve en Young. AgroData te dice cuánta agua tiene TU LOTE. El clima es el aire; la humedad del suelo es tu billetera.")

    with st.expander("2. ¿Para qué pagar si tengo pluviómetro?"):
        st.write("El pluviómetro mide lo que cae, no lo que queda. El sol y el viento evaporan el agua. AgroData mide el agua disponible para la raíz por satélite.")

st.divider()
st.subheader("💳 SOLICITAR REPORTE PROFESIONAL")
if st.button("GENERAR PDF DE PREDICCIÓN REAL"):
    st.error("SISTEMA BLOQUEADO: Pendiente de Pago")
    st.write("Favor realizar el giro a Leonardo Olivera para habilitar su padrón.")
