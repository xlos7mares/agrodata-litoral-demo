import streamlit as st
import numpy as np
import pandas as pd

# ==========================================
# CONFIGURACIÓN DE LA PÁGINA Y ESTILO CLIENTE
# ==========================================
st.set_page_config(
    page_title="Agro Data Litoral PRO",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estética ejecutiva y moderna: tonos oscuros y dorados
st.markdown("""
    <style>
    .main { background-color: #111111; color: #FFFFFF; }
    h1, h2, h3 { color: #D4AF37 !important; }
    .stButton>button {
        background-color: #D4AF37;
        color: #111111;
        font-weight: bold;
        border-radius: 5px;
        border: none;
        width: 100%;
        transition: 0.3s;
    }
    .stButton>button:hover { background-color: #AA8515; color: #FFFFFF; }
    div[data-testid="stMetricValue"] { color: #D4AF37 !important; }
    .report-box {
        border: 1px solid #D4AF37;
        padding: 15px;
        border-radius: 5px;
        background-color: #1a1a1a;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# PANEL LATERAL - IDENTIDAD Y RECOLECCIÓN
# ==========================================
st.sidebar.image("https://img.icons8.com/plots/100/D4AF37/satellite.png", width=80)
st.sidebar.title("AGRO DATA LITORAL")
st.sidebar.markdown("---")
st.sidebar.info("🔬 **Búnker Analítico Base**\nPaysandú, Uruguay\nContacto: **099 417 716**")

# Selector de Módulo principal
modulo = st.sidebar.radio(
    "Seleccione la Solución Analítica:",
    [
        "Simulador de Relieve Dinámico",
        "Algoritmo de Intercambio Catiónico (Suelo)",
        "Búfer de Compensación por Daño Biótico (Semilla)"
    ]
)

# ==========================================
# MÓDULO 1: SIMULADOR DE RELIEVE DINÁMICO
# ==========================================
if modulo == "Simulador de Relieve Dinámico":
    st.title("📐 Simulador de Relieve Dinámico y Escorrentía Superficial")
    st.markdown("""
    **Fundamento Técnico:** Esta máquina algebraica utiliza relaciones trigonométricas y geometría analítica para proyectar vectores de movimiento del agua sobre un plano inclinado, prediciendo zonas de pérdida de insumos por escurrimiento hídrico.
    """)
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Datos Métricos del Terreno")
        distancia = st.number_input("Distancia horizontal entre puntos de control (metros):", min_value=1.0, value=100.0, step=10.0)
        desnivel = st.number_input("Desnivel o diferencia de altura (metros):", min_value=0.0, value=5.0, step=0.5)
        superficie_ha = st.number_input("Superficie del ambiente afectado (Hectáreas):", min_value=1, value=80, step=5)
    
    # --- LA MÁQUINA MATEMÁTICA (Funciones trigonométricas) ---
    # Pendiente (m) = desnivel / distancia
    pendiente_porcentaje = (desnivel / distancia) * 100
    # Ángulo en radianes usando arcoseno
    angulo_rad = np.arcsin(desnivel / distancia) if distancia >= desnivel else 0
    angulo_grados = np.degrees(angulo_rad)

    with col2:
        st.subheader("Diagnóstico Estructural de Escorrentía")
        st.metric(label="Pendiente Calculada", value=f"{pendiente_porcentaje:.2f} %")
        st.metric(label="Ángulo de Inclinación", value=f"{angulo_grados:.2f}°")

    st.markdown("---")
    st.subheader("📋 Reporte Técnico Automatizado")
    
    with st.container():
        if pendiente_porcentaje > 4.0:
            st.error(f"⚠️ **ALTA CRITICIDAD DETECTADA EN {superficie_ha} HECTÁREAS**")
            st.markdown(f"""
            <div class="report-box">
            <b>Diagnóstico de Dinámica Hídrica:</b> La pendiente supera el umbral crítico de absorción. El agua pluvial generará vectores de arrastre de alta velocidad hacia las cotas inferiores.<br><br>
            <b>Recomendación Profesional:</b> Evitar aplicaciones de fertilizantes nitrogenados o enmiendas en superficie antes de precipitaciones pronosticadas mayores a 15 mm. Se sugiere fraccionar la dosificación o realizar siembras en contorno (siguiendo curvas de nivel trigonométricas) para interrumpir el flujo del agua.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.success(f"✅ **ESTABILIDAD DINÁMICA DETECTADA EN {superficie_ha} HECTÁREAS**")
            st.markdown(f"""
            <div class="report-box">
            <b>Diagnóstico de Dinámica Hídrica:</b> El relieve presenta una inclinación controlada ({pendiente_porcentaje:.2f} %). La velocidad de infiltración supera la velocidad de escorrentía superficial.<br><br>
            <b>Recomendación Profesional:</b> Zona apta para optimización del rendimiento mediante fertilización estándar basal. El riesgo de lavado horizontal de nutrientes es mínimo.
            </div>
            """, unsafe_allow_html=True)

# ==========================================
# MÓDULO 2: ALGORITMO DE INTERCAMBIO CATIÓNICO
# ==========================================
elif modulo == "Algoritmo de Intercambio Catiónico (Suelo)":
    st.title("🧪 Algoritmo de Intercambio Catiónico y Balance de Humedad Crítica")
    st.markdown("""
    **Fundamento Técnico:** Transforma las mediciones físicas milimétricas obtenidas en el proceso de sedimentación física (método del frasco) en coeficientes químicos estimados de retención de nutrientes (Capacidad de Intercambio Catiónico - CIC) sin costo de reactivos.
    """)
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Entrada de Datos de Sedimentación (Regla Milimétrica)")
        h_arena = st.number_input("Capa Inferior - Arena (mm):", min_value=0.0, value=25.0, step=1.0)
        h_limo = st.number_input("Capa Intermedia - Limo (mm):", min_value=0.0, value=15.0, step=1.0)
        h_arcilla = st.number_input("Capa Superior - Arcilla (mm):", min_value=0.0, value=10.0, step=1.0)
        
        ejecutar_suelo = st.button("Procesar Muestra de Suelo")

    if ejecutar_suelo or h_arena > 0:
        h_total = h_arena + h_limo + h_arcilla
        if h_total > 0:
            pct_arena = (h_arena / h_total) * 100
            pct_limo = (h_limo / h_total) * 100
            pct_arcilla = (h_arcilla / h_total) * 100

            # --- LA MÁQUINA MATEMÁTICA (Función de estimación lineal de retención / CIC) ---
            # La arcilla aporta la mayor cantidad de cargas negativas al suelo
            cic_estimada = (pct_arcilla * 0.4) + (pct_limo * 0.1) + 2.0 

            with col2:
                st.subheader("Composición Física Porcentual")
                st.write(f"**Arena (Estructura Macroporosa):** {pct_arena:.1f}%")
                st.write(f"**Limo (Estructura Media):** {pct_limo:.1f}%")
                st.write(f"**Arcilla (Estructura Microporosa):** {pct_arcilla:.1f}%")
                st.metric(label="Capacidad de Retención Química Estimada (CIC)", value=f"{cic_estimada:.1f} meq/100g")

            st.markdown("---")
            st.subheader("📋 Diagnóstico de Textura y Nutrición")
            
            with st.container():
                if pct_arena > 60.0:
                    st.warning("⚠️ **SUELO TEXTURALMENTE LIGERO (FRANCO-ARENOSO / ARENOSO)**")
                    st.markdown(f"""
                    <div class="report-box">
                    <b>Comportamiento Físico-Químico:</b> Alta tasa de macroporos. El agua drena con excesiva velocidad vertical. Sus 'imanes' químicos estructurales son reducidos debido al bajo porcentaje de arcilla.<br><br>
                    <b>Impacto Operativo:</b> Si aplica dosis masivas de Urea o nitrógeno líquido, gran parte se lixiviará al subsuelo antes de ser captado por el cultivo.<br><br>
                    <b>Estrategia Recomendada:</b> Fraccionar la fertilización nitrogenada en 2 o 3 aplicaciones a lo largo del ciclo biológico.
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.success("✅ **SUELO TEXTURALMENTE EQUILIBRADO / PESADO**")
                    st.markdown(f"""
                    <div class="report-box">
                    <b>Comportamiento Físico-Químico:</b> Excelente balance de retención hídrica y microporos. La arcilla presente ({pct_arcilla:.1f}%) confiere un búfer catiónico estable que retiene cationes (K+, Ca++, Mg++, NH4+).<br><br>
                    <b>Impacto Operativo:</b> Capacidad de respuesta óptima a la fertilización pesada de fondo. Riesgo mínimo de lavado de nutrientes bajo condiciones de lluvia normales.
                    </div>
                    """, unsafe_allow_html=True)

# ==========================================
# MÓDULO 3: BÚFER DE COMPENSACIÓN POR DAÑO BIÓTICO
# ==========================================
elif modulo == "Búfer de Compensación por Daño Biótico (Semilla)":
    st.title("🌿 Búfer de Compensación por Daño Biótico en Semilla y Densidad")
    st.markdown("""
    **Fundamento Técnico:** Función de optimización biológica que procesa el porcentaje físico de granos dañados (identificados bajo microscopía/lupa macro) para corregir matemáticamente la densidad de siembra real, previniendo fallas en el Índice de Área Foliar (LAI).
    """)
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Muestreo Físico de Laboratorio (Base 100g)")
        peso_total = st.number_input("Peso total de la submuestra analizada (gramos):", min_value=10.0, value=100.0, step=10.0)
        peso_danados = st.number_input("Peso de granos con defectos bióticos observados (gramos):", min_value=0.0, value=6.0, step=0.5)
        
        st.markdown("**Parámetros de Siembra Originales:**")
        densidad_objetivo = st.number_input("Plantas objetivo por metro cuadrado (diseño original):", min_value=10, value=30, step=5)
        costo_bolsa = st.number_input("Costo por bolsa de semilla (USD):", min_value=1.0, value=45.0, step=5.0)
        has_totales = st.number_input("Superficie Total a Sembrar (Hectáreas):", min_value=1, value=200, step=10)

    # --- LA MÁQUINA MATEMÁTICA (Función de compensación morfológica) ---
    pct_dano = (peso_danados / peso_total) * 100
    
    # Coeficiente de pérdida: el grano dañado reduce la germinación real de forma exponencial/lineal corregida
    factor_correccion = 1 / (1 - (pct_dano / 100))
    densidad_corregida = densidad_objetivo * factor_correccion
    
    # Simulación financiera de ahorro por precisión
    semilla_ahorrada_por_ajuste = (densidad_corregida - densidad_objetivo) * 0.05 * has_totales # Estimación física simulada
    ahorros_usd = np.clip(semilla_ahorrada_por_ajuste * (costo_bolsa / 40), 0.0, 15000.0)

    with col2:
        st.subheader("Métricas de Laboratorio y Densidad Dinámica")
        st.metric(label="Porcentaje de Daño en Semilla", value=f"{pct_dano:.2f} %")
        st.metric(label="Densidad Recomendada Ajustada", value=f"{int(np.ceil(densidad_corregida))} pl/m²", delta=f"+{int(np.ceil(densidad_corregida - densidad_objetivo))} pl/m²")
        st.metric(label="Retorno Económico Estimado por Corrección", value=f"USD {ahorros_usd:.2f}")

    st.markdown("---")
    st.subheader("📋 Recomendación de Manejo Biológico")
    
    with st.container():
        st.markdown(f"""
        <div class="report-box">
        <b>Análisis Fisiológico de la Muestra:</b> El lote presenta un {pct_dano:.2f}% de daño estructural (físico/biótico). Las plantas viables resultantes manifestarán una reducción en la tasa de expansión foliar inicial.<br><br>
        <b>Acción de Precisión:</b> Para alcanzar el Índice de Área Foliar óptimo y cerrar el entresurco a tiempo, la densidad mecánica de siembra debe incrementarse exactamente a <b>{int(np.ceil(densidad_corregida))} plantas por metro cuadrado</b> en las zonas afectadas.<br><br>
        <b>Impacto de Negocio:</b> Al calibrar la sembradora con este factor de búfer en lugar de sobredosificar el campo completo de {has_totales} hectáreas a ciegas, se proyecta una optimización de insumos valorada en <b>USD {ahorros_usd:.2f}</b>.
        </div>
        """, unsafe_allow_html=True)
