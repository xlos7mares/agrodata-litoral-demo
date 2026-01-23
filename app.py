import streamlit as st
import pandas as pd
import numpy as np
import time

# Configuración de la página con estilo tecnológico
st.set_page_config(page_title="AgroData Litoral Pro", layout="wide")

st.title("🌾 AgroData Litoral: Inteligencia Predictiva")
st.subheader("Sistema de Alerta Temprana de Estrés Hídrico")

# --- BARRA LATERAL: EL DISPARADOR DE LA VENTA ---
st.sidebar.header("📍 Mi Establecimiento")
campo_id = st.sidebar.text_input("Ingrese ID de Productor o Coordenadas GPS")

if st.sidebar.button("ANALIZAR MI CAMPO"):
    st.sidebar.error("❌ ACCESO RESTRINGIDO")
    st.sidebar.write("Su cuenta no tiene una suscripción activa para este padrón.")
    st.sidebar.info("Para activar su campo y recibir el estudio de predicción hídrica 2026, realice el giro de activación.")
    st.sidebar.markdown("[👉 SOLICITAR CUENTA PARA GIRO](https://wa.me/59899417716)")

# --- CUERPO DE LA APP: LA DEMO ADICTIVA (Campo Ficticio) ---
st.warning("⚠️ MODO DEMO: Visualizando 'Establecimiento El Milagro' (Young, Río Negro)")

col1, col2, col3 = st.columns(3)

# Métrica 1: Humedad de Suelo (Simulando datos NASA)
with col1:
    st.metric(label="Humedad Suelo (Profundidad 1m)", value="18%", delta="-5% CRÍTICO", delta_color="inverse")
    st.write("🔴 Alerta: Punto de marchitez cercano.")

# Métrica 2: Predicción de Lluvias (Próximos 7 días)
with col2:
    st.metric(label="Precipitación Estimada", value="2.5 mm", delta="Inminente Déficit")
    st.write("🟡 Probabilidad de lluvia: 15%")

# Métrica 3: Ganancia/Pérdida Proyectada
with col3:
    st.metric(label="Rendimiento Estimado (Soja/Maíz)", value="2.1 Tn/Ha", delta="-0.8 Tn/Ha", delta_color="inverse")
    st.write("💸 Riesgo económico: u$s 14,200 por cuadro.")

# --- EL GRÁFICO "ADICTIVO" ---
st.subheader("📈 Proyección Hídrica vs. Potencial de Cosecha")
chart_data = pd.DataFrame(
    np.random.randn(20, 2),
    columns=['Humedad Real', 'Necesidad del Cultivo']
)
st.line_chart(chart_data)

# --- EL CIERRE DE VENTA INEVITABLE ---
st.divider()
st.subheader("🚀 ¿Quiere salvar su cosecha?")
st.write("""
Nuestro algoritmo ha detectado un patrón de sequía que afectará su zona en los próximos 14 días. 
No adivine. Use datos satelitales de precisión para decidir cuándo regar o cuándo aplicar fertilizante.
""")

if st.button("GENERAR REPORTE DE PREDICCIÓN COMPLETO"):
    with st.spinner('Calculando vectores de riesgo...'):
        time.sleep(3)
        st.error("EL REPORTE ESTÁ LISTO PERO BLOQUEADO")
        st.write("Para descargar el PDF con el mapa de calor de su campo y las recomendaciones técnicas:")
        st.success("1. Gire u$s [Monto] a la cuenta MiDinero / BROU de Leonardo Olivera.")
        st.success("2. Envíe el comprobante.")
        st.success("3. Reciba su reporte en menos de 30 minutos.")