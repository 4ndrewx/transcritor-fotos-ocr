import easyocr
import numpy as np
from PIL import Image, ImageOps
import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Transcripción de Texto por Cámara", page_icon="📷", layout="wide"
)

# --- CARGAR EASYOCR EN CACHÉ ---
@st.cache_resource
def load_reader():
  return easyocr.Reader(["es", "en"], gpu=False)


with st.spinner("Cargando motor de reconocimiento OCR..."):
  reader = load_reader()

# --- BARRA LATERAL (CONFIGURACIÓN EXACTA A LA REFERENCIA) ---
st.sidebar.markdown("### ⚙️ Configuración")
st.sidebar.markdown("---")
st.sidebar.markdown("**Procesamiento de imagen:**")

filtro_opcion = st.sidebar.radio(
    "Filtro", ["Sin Filtro", "Con Filtro (Invertir colores)"], label_visibility="collapsed"
)

st.sidebar.markdown("---")
st.sidebar.info(
    "💡 **Consejo:** Usar el filtro de inversión puede ayudar a la lectura si el"
    " fondo es muy oscuro."
)

# --- CONTENIDO PRINCIPAL ---
st.markdown("Toma una foto para transcribir:")

# Widget de la cámara de Streamlit (idéntico al de tu imagen de referencia)
foto_capturada = st.camera_input(
    "Toma una foto para transcribir:", label_visibility="collapsed"
)

st.markdown("---")

# Secciones inferiores en dos columnas: Imagen procesada y Texto detectado
col1, col2 = st.columns(2)

with col1:
  st.markdown("### 🖼️ Imagen procesada")
  if foto_capturada is not None:
    # Abrir la imagen tomada desde la cámara
    image = Image.open(foto_capturada)

    # Aplicar el filtro según la selección de la barra lateral
    if filtro_opcion == "Con Filtro (Invertir colores)":
      image = ImageOps.invert(image.convert("RGB"))

    st.image(image, use_container_width=True)
  else:
    st.info("Esperando a que tomes una fotografía...")

with col2:
  st.markdown("### 📄 Texto detectado")
  if foto_capturada is not None:
    with st.spinner("Extrayendo texto de la fotografía..."):
      # Convertir imagen para EasyOCR
      img_array = np.array(image)
      resultados = reader.readtext(img_array)

      # Unir todo el texto encontrado
      texto_extraido = " ".join([res[1] for res in resultados])

    if texto_extraido.strip() != "":
      st.success("¡Transcripción exitosa!")
      st.text_area(
          "Resultado:", value=texto_extraido, height=180, label_visibility="collapsed"
      )
    else:
      st.warning(
          "No se logró detectar texto en la imagen. Intenta enfocar mejor o"
          " usar el filtro."
      )
  else:
    st.warning("No se logró detectar texto en la imagen.")
