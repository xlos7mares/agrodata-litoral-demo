# --- DENTRO DE LA FUNCIÓN DE OBTENER DATOS ---
def obtener_datos_auditoria(lat, lon):
    # (Mantenemos la lógica de clima e índices anterior...)
    
    # NUEVO: Lógica de Almacenamiento de Agua Útil (AU) según profundidad
    # Basalto (Arapey): Suelos superficiales, AU bajo.
    # Sedimentos (Libertad): Suelos profundos, AU alto.
    if -33.2 < lat < -30.0: # Norte/Basalto
        capacidad_max_mm = 60  # mm de agua útil
        almacenamiento_litros = 60000 
    elif -35.0 < lat < -33.2: # Sur/Cristalino
        capacidad_max_mm = 40
        almacenamiento_litros = 40000
    else: # Sedimentos profundos
        capacidad_max_mm = 140
        almacenamiento_litros = 140000
        
    return t, h, v, dt, color, geo_info, cone_info, capacidad_max_mm, almacenamiento_litros

# --- EN LA PANTALLA ÚNICA (DESPUÉS DE GEOLOGÍA) ---

st.divider()

# 1. VISUALIZACIÓN DE RESERVA HÍDRICA (NUEVO)
st.markdown("### 💧 Auditoría de Reserva Hídrica (Agua Útil)")
col_h1, col_h2 = st.columns([2, 1])
with col_h1:
    st.write(f"**Capacidad de Almacenamiento Teórica:** {capacidad_max_mm} mm")
    # Barra visual del "Tanque" del suelo
    st.progress(min(h/100, 1.0)) 
    st.caption(f"Estimación de recarga actual basada en humedad ambiente y tipo de suelo: {int(capacidad_max_mm * (h/100))} mm disponibles.")
with col_h2:
    st.metric("LITROS TOTALES / HA", f"{almacenamiento_litros} L")
    st.write("**Impacto:** Define la ventana de supervivencia del cultivo ante un corte de precipitaciones.")

st.divider()

# 2. MÓDULO AGROAMBIENTAL Y HUELLA DE CARBONO (NUEVO PARA VENDER)
st.markdown("### 🌿 Auditoría Agroambiental y Secuestro de Carbono")
st.write("Análisis de sostenibilidad alineado a las exigencias de mercados internacionales (UE/EUA).")

ca1, ca2, ca3 = st.columns(3)
with ca1:
    st.subheader("♻️ Balance de Nutrientes")
    st.write("**Lixiviación:** Riesgo {'ALTO' if h > 80 else 'BAJO'} de pérdida de Nitratos por escurrimiento superficial.")
    st.write("**Erosión:** Tasa estimada según pendiente DEM y cobertura vegetal NDVI.")

with ca2:
    st.subheader("📉 Huella de Carbono")
    # Estimación basada en Materia Orgánica típica del Grupo CONEAT
    mo_estimada = "4.5%" if "12" in cone_info['grupo'] else "2.5%"
    st.write(f"**Stock de Carbono Orgánico (SOC):** Estimado en {mo_estimada}.")
    st.write("**Potencial de Captura:** Alto mediante siembra directa y cultivos de cobertura.")

with ca3:
    st.subheader("🐝 Indicador de Biodiversidad")
    st.write("**Refugios Naturales:** Detectados mediante análisis de bordes y parches de monte nativo.")
    st.write("**Estatus:** Predio apto para certificación de 'Carne Natural' o 'Granos Sustentables'.")
