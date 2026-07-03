"""
=============================================================
 SCRIPT 1: Clasificación de Imágenes en Tiempo Real
 Visión por Computadora — Unidad 3, Sesión 2
 Universidad Peruana Unión · EP Ingeniería de Sistemas · 2026-1
 Ing. Bonnier Nilss Mamani Larico
=============================================================

 REQUISITOS:
   pip install opencv-python tensorflow pillow numpy

 EJECUCIÓN:
   python script1_clasificacion.py

 CONTROLES:
   ESPACIO  → capturar frame y clasificar
   Q        → salir
=============================================================
"""

import cv2
import numpy as np
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions
from PIL import Image

# ─────────────────────────────────────────────────────────────
# 1. CARGA DEL MODELO
#    MobileNetV2 fue entrenado con ImageNet:
#    1.2 millones de imágenes, 1000 categorías.
#    weights='imagenet' descarga los pesos preentrenados.
# ─────────────────────────────────────────────────────────────
print("⏳ Cargando MobileNetV2 preentrenado con ImageNet...")
modelo = MobileNetV2(weights='imagenet')
print("✅ Modelo listo.")
print(f"   Parámetros totales : {modelo.count_params():,}")
print(f"   Categorías         : 1,000")
print()
print("📷 Abriendo cámara...")
print("   ESPACIO → clasificar | Q → salir")
print()


def preprocesar_frame(frame):
    """
    Prepara un frame de la cámara para MobileNetV2.

    MobileNetV2 espera:
      - Tamaño: 224 × 224 píxeles
      - Formato: RGB (OpenCV usa BGR por defecto)
      - Valores normalizados al rango [-1, 1]

    Args:
        frame: imagen BGR capturada por OpenCV

    Returns:
        tensor listo para modelo.predict()  shape: (1, 224, 224, 3)
    """
    # OpenCV trabaja en BGR → convertir a RGB
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Redimensionar a 224×224 (tamaño esperado por MobileNetV2)
    redimensionada = cv2.resize(rgb, (224, 224))

    # Convertir a array numpy y agregar dimensión de batch
    # shape: (224, 224, 3) → (1, 224, 224, 3)
    array = np.expand_dims(np.array(redimensionada), axis=0)

    # Normalizar píxeles de [0,255] a [-1,1]
    return preprocess_input(array)


def dibujar_resultado(frame, predicciones):
    """
    Superpone las top-5 predicciones sobre el frame capturado.

    Dibuja un panel semitransparente en la parte inferior
    con el nombre de cada clase y su probabilidad.

    Args:
        frame      : imagen BGR original
        predicciones: lista de (id, nombre, probabilidad) del modelo
    """
    alto, ancho = frame.shape[:2]

    # Panel de fondo semitransparente (negro con 60% opacidad)
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, alto - 190), (ancho, alto), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)

    # Título del panel
    cv2.putText(frame, "TOP-5 PREDICCIONES", (10, alto - 170),
                cv2.FONT_HERSHEY_SIMPLEX, 0.55, (235, 129, 27), 2)

    # Colores para cada posición (naranja → azul → gris)
    colores = [
        (0, 165, 255),   # 1° naranja
        (255, 100, 50),  # 2° azul oscuro
        (150, 150, 150), # 3° gris
        (120, 120, 120), # 4° gris
        (100, 100, 100), # 5° gris
    ]

    for i, (_, nombre, prob) in enumerate(predicciones):
        y = alto - 145 + i * 28

        # Barra de probabilidad proporcional al ancho
        ancho_barra = int(prob * (ancho - 200))
        cv2.rectangle(frame, (170, y - 12), (170 + ancho_barra, y + 2),
                      colores[i], -1)

        # Texto: rango + nombre + porcentaje
        etiqueta = f"{i+1}. {nombre.replace('_',' '):<22} {prob*100:5.1f}%"
        cv2.putText(frame, etiqueta, (10, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.48, colores[i], 1)

    return frame


# ─────────────────────────────────────────────────────────────
# 2. CAPTURA DE CÁMARA
#    cv2.VideoCapture(0) abre la cámara por defecto del sistema.
#    Si hay varias cámaras, probar con 1, 2, etc.
# ─────────────────────────────────────────────────────────────
camara = cv2.VideoCapture(0)

if not camara.isOpened():
    print("❌ No se pudo abrir la cámara.")
    print("   Verifica que no esté siendo usada por otra aplicación.")
    exit()

ultimo_resultado = None  # Almacena la última clasificación

while True:
    # Leer un frame de la cámara
    ret, frame = camara.read()

    if not ret:
        print("❌ Error leyendo frame de la cámara.")
        break

    # Voltear horizontalmente (efecto espejo — más natural para el usuario)
    frame = cv2.flip(frame, 1)

    # Instrucciones en la parte superior
    cv2.putText(frame, "ESPACIO: clasificar  |  Q: salir",
                (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1)

    # Si ya tenemos un resultado, mostrarlo sobre el frame actual
    if ultimo_resultado is not None:
        frame = dibujar_resultado(frame, ultimo_resultado)

    cv2.imshow("Vision Computacional - MobileNetV2 | UPeU 2026-1", frame)

    # ── Lectura de teclado ───────────────────────────────────
    tecla = cv2.waitKey(1) & 0xFF

    if tecla == ord('q'):
        # Q → salir del bucle
        print("\n👋 Cerrando aplicación...")
        break

    elif tecla == ord(' '):
        # ESPACIO → clasificar el frame actual
        print("🔍 Clasificando imagen...")

        # Preprocesar y predecir
        tensor = preprocesar_frame(frame)
        predicciones_raw = modelo.predict(tensor, verbose=0)
        top5 = decode_predictions(predicciones_raw, top=5)[0]

        # Guardar resultado para mostrarlo en los frames siguientes
        ultimo_resultado = top5

        # Imprimir en consola
        print(f"   🥇 {top5[0][1].replace('_',' ')} — {top5[0][2]*100:.1f}%")
        print(f"   🥈 {top5[1][1].replace('_',' ')} — {top5[1][2]*100:.1f}%")
        print(f"   🥉 {top5[2][1].replace('_',' ')} — {top5[2][2]*100:.1f}%")
        print()

# ─────────────────────────────────────────────────────────────
# 3. LIBERACIÓN DE RECURSOS
#    Siempre liberar la cámara y cerrar ventanas al terminar.
# ─────────────────────────────────────────────────────────────
camara.release()
cv2.destroyAllWindows()
print("✅ Recursos liberados. Hasta la próxima.")
