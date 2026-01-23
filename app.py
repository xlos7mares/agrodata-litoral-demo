import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.graph_objects as go

# Configuración de estilo tecnológico y oscuro
st.set_page_config(page_title="AgroData Litoral Pro", layout="wide")

# Estilo personalizado para resaltar el modo "Casino/Adictivo"
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1a1c23; padding: 15px; border-radius: 10px; border: 1px solid #3e4452; }
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
    **Su campo requiere validación de coordenadas satelitales.**
    
    Para activar el reporte real de su padrón:
    1. Solicite su ID de acceso.
    2. Envíe ubicación por WhatsApp.
    3. Realice el giro de activación.
    """)
    st.sidebar.link_button("📲 SOLICITAR ACTIVACIÓN", "https://wa.me/59899417716")

# --- CUERPO PRINCIPAL ---
tabs = st.tabs(["📊 Monitor de Riesgo", "💎 ¿Por qué es Vital?", "❓ Preguntas Frecuentes"])

with tabs[0]:
    st.warning("⚠️ MODO DEMO: Datos del 'Establecimiento El Milagro' (Young)")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Humedad en Raíz (1m)", "14.2%", "-3.8% CRÍTICO", delta_color="inverse")
    with col2:
        st.metric("Déficit de Lluvia (10 días)", "24mm", "Evapotranspiración Alta")
    with col3:
        st.metric("PÉRDIDA PROYECTADA", "u$s 18,400", "Basado en 100 Ha", delta_color="inverse")

    # GRÁFICO ADICTIVO: DÓLARES VS HUMEDAD
    st.subheader("📈 El Costo de la Espera: Humedad vs. Rendimiento Económico")
    dias = np.array(range(1, 11))
    humedad = [18, 17, 15, 14, 12, 11, 10, 9, 8, 7]
    perdida_usd = [0, 500, 1200, 2500, 4800, 7000, 10000, 13500, 16000, 18400]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dias, y=humedad, name='Humedad Suelo (%)', line=dict(color='cyan', width=4)))
    fig.add_trace(go.Bar(x=dias, y=perdida_usd, name='Pérdida Acumulada (u$s)', marker_color='red', opacity=0.5))
    
    fig.update_layout(title="Si la humedad baja del 12%, su dinero desaparece",
                      xaxis_title="Días sin lluvia",
                      template="plotly_dark")
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
    * **Rendimiento:** Gane entre un **15% y 25% más** de kilos por hectárea al evitar el estrés hídrico invisible.
    """)
    st.info("💡 'El que tiene el dato, tiene el mando. El que no, solo tiene esperanza'.")

with tabs[2]:
    st.header("❓ Respuestas para el Productor Exigente")
    
    with st.expander("1. ¿En qué se diferencia de AccuWeather o el pronóstico del tele?"):
        st.write("""
        AccuWeather te dice si llueve en Young. **AgroData te dice cuánta agua tiene TU LOTE.** El clima es lo que pasa en el aire; la humedad del suelo es lo que hace pesar tu grano. 
        Usamos tecnología NASA para ver bajo tierra, algo que ninguna app gratuita puede hacer.
        """)

    with st.expander("2. ¿Para qué voy a pagar si yo tengo pluviómetro y barreno?"):
        st.write("""
        El pluviómetro mide lo que cae, no lo que queda. Si hay sol y viento, el agua se evapora. 
        El barreno te da un dato de un solo punto; AgroData te da un **mapa de calor de todo el padrón**. 
        ¿Vas a arriesgar u$s 50,000 en semillas basándote en un agujerito en la tierra?
        """)

    with st.expander("3. ¿Es difícil de usar?"):
        st.write("""
        Si sabés leer un semáforo, sabés usar AgroData. Verde sembrás, rojo esperás. 
        Nosotros hacemos la ciencia compleja, vos recibís el dinero de la cosecha.
        """)

st.divider()
st.subheader("💳 SOLICITAR REPORTE PROFESIONAL")
if st.button("GENERAR PDF DE PREDICCIÓN REAL"):
    st.error("SISTEMA BLOQUEADO: Pendiente de Giro u$s 200 (Adelanto de Temporada)")
    st.write("Datos para transferencia: MiDinero / BROU - Leonardo Olivera")
