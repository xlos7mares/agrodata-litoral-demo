def obtener_datos_unificados(lat, lon):
    try:
        # ... (Mantener los cálculos de Clima y Satélite anteriores) ...

        # LÓGICA DE DETECCIÓN REGIONAL MEJORADA
        # 1. Uruguay Litoral (Zona Basáltica)
        if -33.5 < lat < -30.0 and -58.5 < lon < -56.0:
            reg_desc = "Zona Litoral Norte (Suelos de Basalto)"
            geo_madre = "Basalto Mesozoico"
            geo_formacion = "Formación Arapey" # <--- Aquí agregamos la formación
            geo_unidad = "Basaltos masivos con disyunción columnar"
            geo_desc = "Drenaje limitado por contacto lítico superficial."
            cone_grupo = "Grupo 12"
            cone_suelo = "Brunosoles Éutricos"
            cone_util = "Alta fertilidad, ideal pasturas y granos."
        
        # 2. Uruguay Sur/Este (Pan de Azúcar / Piriápolis)
        elif -35.0 < lat < -33.5 and -56.0 < lon < -53.5:
            reg_desc = "Zona Serrana y Costera del Este"
            geo_madre = "Basamento Cristalino (Precámbrico)"
            geo_formacion = "Grupo Lavalleja / Formación Pan de Azúcar" # <--- Aquí la formación específica
            geo_unidad = "Granitoides, Migmatitas y Rocas Metamórficas"
            geo_desc = "Topografía accidentada con alta pendiente y rocosidad."
            cone_grupo = "Grupo 2 (Serranías)"
            cone_suelo = "Litosoles y Brunosoles Ócricos"
            cone_util = "Ganadería extensiva y forestación. Limitación agrícola severa."

        # 3. Resto del Mundo
        else:
            reg_desc = "Ubicación fuera de la base de datos regional de Uruguay"
            geo_madre = "Corteza Continental"
            geo_formacion = "No Clasificada"
            geo_unidad = "Perfil No Determinado"
            geo_desc = "Se requiere estudio geológico local in-situ."
            cone_grupo = "Internacional"
            cone_suelo = "Suelo No Clasificado"
            cone_util = "Estudio agronómico pendiente."

        return t, h, v, dt, ndvi, ndwi, lst, reg_desc, geo_madre, geo_formacion, geo_unidad, geo_desc, cone_grupo, cone_suelo, cone_util
    except: return None

# --- EN LA PANTALLA PRINCIPAL (MÓDULO 1) ---
# Asegúrate de imprimir la nueva variable 'geo_formacion':

st.markdown(f"#### ⛰️ Geología y Estratigrafía")
c_g1, c_g2 = st.columns(2)
with c_g1:
    st.metric("Sistema/Roca Madre", geo_madre)
    st.write(f"**Formación Específica:** {geo_formacion}") # <--- Ahora se verá en pantalla
with c_g2:
    st.write(f"**Unidad Litológica:** {geo_unidad}")
    st.write(f"**Drenaje de Lote:** {geo_desc}")
