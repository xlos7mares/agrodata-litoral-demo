# --- ENTRADA DE COORDENADAS SEPARADAS ---
st.sidebar.write("### 📍 Ubicación del Padrón")

# Creamos dos columnas pequeñas en la barra lateral
col_lat, col_lon = st.sidebar.columns(2)

with col_lat:
    lat_input = st.text_input("Latitud", value="-32.275611")

with col_lon:
    lon_input = st.text_input("Longitud", value="-58.052861")

# Convertimos los textos a números flotantes para que el mapa los entienda
try:
    lat_num = float(lat_input)
    lon_num = float(lon_input)
except ValueError:
    st.sidebar.error("Por favor, ingresa números válidos")
    lat_num, lon_num = -32.3167, -58.0833 # Valores por defecto de Paysandú
