import streamlit as st
from streamlit_folium import folium_static
import folium

st.subheader("🌐 Escaneo Satelital de Alta Resolución (Google Hybrid)")

# Coordenadas de las 5 hectáreas en Young (Lafluf)
lat, lon = -32.6915, -57.6295

# Crear el mapa con fondo Satelital Real de Google
m = folium.Map(location=[lat, lon], zoom_start=16, tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google')

# Dibujar el polígono Flúor con borde blanco
puntos_poligono = [
    [-32.689, -57.632], [-32.689, -57.627], 
    [-32.694, -57.627], [-32.694, -57.632]
]
folium.Polygon(
    locations=puntos_poligono,
    color="#FFFFFF",      # Borde Blanco
    weight=4,
    fill=True,
    fill_color="#39FF14", # VERDE FLÚOR NEÓN
    fill_opacity=0.4,
    tooltip="ÁREA DE ANÁLISIS: LAFLUF"
).add_to(m)

# Mostrar el mapa en la app
folium_static(m)
