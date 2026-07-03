"""
=============================================================
 SCRIPT 2: Detección de Expresiones Faciales en Tiempo Real
 Visión por Computadora — Unidad 3, Sesión 2
 Universidad Peruana Unión · EP Ingeniería de Sistemas · 2026-1
 Ing. Bonnier Nilss Mamani Larico
=============================================================

 ¿QUÉ DETECTA?
   ✅ Rostro (Haar Cascade — sin modelos externos)
   ✅ Ojos abiertos / cerrados (Haar Cascade de ojos)
   ✅ Sonrisa (Haar Cascade de sonrisa)
   ✅ Estado general: SONRIENDO / OJOS CERRADOS / NEUTRO

 REQUISITOS:
   pip install opencv-python numpy
   (Solo OpenCV — sin MediaPipe, sin TensorFlow)

 EJECUCIÓN:
   python script2_expresiones.py

 CONTROLES:
   Q  → salir
=============================================================

 CONCEPTO CLAVE — Haar Cascade:
   Algoritmo de Viola-Jones (2001). Usa miles de "features"
   rectangulares para detectar objetos en tiempo real.
   Cada feature verifica si una región de la imagen tiene
   cierta diferencia de brillo entre zonas contiguas.
   Un clasificador en cascada filtra rápidamente las regiones
   donde NO hay el objeto buscado, acelerando la detección.
=============================================================
"""

import cv2
import numpy as np

# ─────────────────────────────────────────────────────────────
# UMBRALES AJUSTABLES
#   Si la sonrisa no se detecta bien, baja SONRISA_MIN_VECINOS.
#   Si detecta sonrisas falsas, súbelo.
# ─────────────────────────────────────────────────────────────
CARA_ESCALA        = 1.3    # Factor de escala para detección de rostro
CARA_MIN_VECINOS   = 5      # Mínimo de vecinos para confirmar rostro
OJO_ESCALA         = 1.1    # Factor de escala para detección de ojos
OJO_MIN_VECINOS    = 3      # Mínimo de vecinos para confirmar ojo
                             # ↑ Subir si detecta ojos donde no los hay
                             # ↓ Bajar si siempre aparece como "cerrado"
SONRISA_ESCALA     = 1.7    # Factor de escala para sonrisa
SONRISA_MIN_VEC    = 22     # Mínimo de vecinos para confirmar sonrisa
                             # ↑ Subir si detecta sonrisas falsas
                             # ↓ Bajar si no detecta la sonrisa

# ─────────────────────────────────────────────────────────────
# 1. CARGAR CLASIFICADORES HAAR CASCADE
#    Estos archivos vienen incluidos con OpenCV — no hay que
#    descargar nada adicional.
# ─────────────────────────────────────────────────────────────
ruta = cv2.data.haarcascades

detector_cara    = cv2.CascadeClassifier(ruta + 'haarcascade_frontalface_default.xml')
detector_ojos    = cv2.CascadeClassifier(ruta + 'haarcascade_eye_tree_eyeglasses.xml')
detector_sonrisa = cv2.CascadeClassifier(ruta + 'haarcascade_smile.xml')

print("✅ Clasificadores Haar Cascade cargados.")
print("   · frontalface_default  → detección de rostro")
print("   · eye                  → detección de ojos")
print("   · smile                → detección de sonrisa")
print()
print("📷 Iniciando cámara...")
print("   Q → salir")
print()


def detectar_expresiones(frame_gris, cara_x, cara_y, cara_w, cara_h):
    """
    Dada la región del rostro en escala de grises, detecta ojos y sonrisa.

    La detección se hace SOLO dentro del rectángulo del rostro —
    esto mejora la velocidad y reduce falsos positivos.

    Para los ojos, solo miramos la mitad superior del rostro.
    Para la sonrisa, solo miramos la mitad inferior.

    Args:
        frame_gris          : frame completo en escala de grises
        cara_x, cara_y      : posición del rostro en el frame
        cara_w, cara_h      : tamaño del rostro detectado

    Returns:
        ojos_detectados (int) : número de ojos detectados (0, 1 o 2)
        sonrisa (bool)        : True si se detectó sonrisa
        roi_ojos              : región de interés para ojos (para debug)
        roi_sonrisa           : región de interés para sonrisa
    """
    # Región de interés del rostro completo
    roi_cara = frame_gris[cara_y:cara_y + cara_h, cara_x:cara_x + cara_w]

    # Mitad superior del rostro → para ojos
    mitad_y = cara_h // 2
    roi_ojos = roi_cara[0:mitad_y, :]

    # Mitad inferior del rostro → para sonrisa
    roi_sonrisa = roi_cara[mitad_y:, :]

    # Detectar ojos en la mitad superior
    ojos = detector_ojos.detectMultiScale(
        roi_ojos,
        scaleFactor=OJO_ESCALA,
        minNeighbors=OJO_MIN_VECINOS,
        minSize=(15, 15)
    )

    # Detectar sonrisa en la mitad inferior
    sonrisas = detector_sonrisa.detectMultiScale(
        roi_sonrisa,
        scaleFactor=SONRISA_ESCALA,
        minNeighbors=SONRISA_MIN_VEC,
        minSize=(30, 20)
    )

    ojos_detectados = len(ojos)
    sonrisa = len(sonrisas) > 0

    return ojos_detectados, sonrisa, ojos, sonrisas, mitad_y


def determinar_estado(ojos_detectados, sonriendo):
    """
    Determina el estado facial a partir de los detectores.

    Lógica:
      - 0 ojos → ambos cerrados (o fuera de ángulo)
      - 1 ojo  → un ojo cerrado (guiño posible)
      - 2 ojos + sonrisa → sonriendo con ojos abiertos
      - 2 ojos sin sonrisa → neutral

    Returns:
        texto (str), color BGR, emoji
    """
    if ojos_detectados == 0:
        return "OJOS CERRADOS", (0, 0, 255), "😴"
    elif ojos_detectados == 1:
        return "UN OJO CERRADO", (0, 165, 255), "😉"
    elif sonriendo:
        return "SONRIENDO", (0, 215, 255), "😊"
    else:
        return "NEUTRO", (200, 200, 200), "😐"


def dibujar_panel(frame, cara, ojos_det, sonriendo, estado, color_estado):
    """
    Dibuja todos los elementos visuales sobre el frame:
      - Rectángulo del rostro
      - Rectángulos de ojos detectados
      - Panel de estado superior
      - Indicadores de ojos y sonrisa
    """
    alto, ancho = frame.shape[:2]
    cara_x, cara_y, cara_w, cara_h = cara

    # Rectángulo del rostro
    cv2.rectangle(frame,
                  (cara_x, cara_y),
                  (cara_x + cara_w, cara_y + cara_h),
                  color_estado, 2)

    # Etiqueta del estado sobre el rostro
    cv2.putText(frame, estado,
                (cara_x, cara_y - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.65, color_estado, 2)

    # Panel superior semitransparente
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (ancho, 85), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)

    # Indicadores en el panel
    # Ojo izquierdo
    col_oi = (0, 255, 0) if ojos_det >= 1 else (0, 0, 255)
    txt_oi = "OJO IZQ: ABIERTO" if ojos_det >= 1 else "OJO IZQ: CERRADO"
    cv2.putText(frame, txt_oi, (10, 28),
                cv2.FONT_HERSHEY_SIMPLEX, 0.55, col_oi, 2)

    # Ojo derecho
    col_od = (0, 255, 0) if ojos_det >= 2 else (0, 0, 255)
    txt_od = "OJO DER: ABIERTO" if ojos_det >= 2 else "OJO DER: CERRADO"
    cv2.putText(frame, txt_od, (10, 55),
                cv2.FONT_HERSHEY_SIMPLEX, 0.55, col_od, 2)

    # Sonrisa
    col_s = (0, 215, 255) if sonriendo else (150, 150, 150)
    txt_s = "SONRISA: SI" if sonriendo else "SONRISA: NO"
    cv2.putText(frame, txt_s, (10, 78),
                cv2.FONT_HERSHEY_SIMPLEX, 0.55, col_s, 2)

    # Número de ojos detectados (útil para debug)
    cv2.putText(frame, f"Ojos detectados: {ojos_det}",
                (ancho - 220, 28),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (180, 180, 180), 1)

    # Instrucción
    cv2.putText(frame, "Q: salir",
                (ancho - 100, alto - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, (150, 150, 150), 1)

    return frame


# ─────────────────────────────────────────────────────────────
# 2. BUCLE PRINCIPAL
# ─────────────────────────────────────────────────────────────
camara = cv2.VideoCapture(0)

if not camara.isOpened():
    print("❌ No se pudo abrir la cámara.")
    print("   Prueba cambiando el 0 por 1: cv2.VideoCapture(1)")
    exit()

while True:
    ret, frame = camara.read()
    if not ret:
        print("❌ Error leyendo frame.")
        break

    # Efecto espejo
    frame = cv2.flip(frame, 1)
    alto, ancho = frame.shape[:2]

    # Convertir a escala de grises para los detectores Haar
    # Los Haar Cascades trabajan en escala de grises (más rápido)
    gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Ecualizar histograma — mejora detección con poca luz
    gris = cv2.equalizeHist(gris)

    # ── Detección de rostro ──────────────────────────────────
    caras = detector_cara.detectMultiScale(
        gris,
        scaleFactor=CARA_ESCALA,
        minNeighbors=CARA_MIN_VECINOS,
        minSize=(80, 80)   # Ignorar rostros muy pequeños
    )

    if len(caras) == 0:
        # Sin rostro — mostrar mensaje
        cv2.putText(frame,
                    "Acercate a la camara y mira de frente",
                    (30, alto // 2),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(frame, "Q: salir",
                    (ancho - 100, alto - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (150, 150, 150), 1)
    else:
        # Tomar el rostro más grande detectado
        cara = max(caras, key=lambda c: c[2] * c[3])
        cx, cy, cw, ch = cara

        # ── Detectar ojos y sonrisa ──────────────────────────
        ojos_det, sonriendo, ojos, sonrisas, mitad_y = detectar_expresiones(
            gris, cx, cy, cw, ch
        )

        # ── Determinar estado ────────────────────────────────
        estado, color_estado, emoji = determinar_estado(ojos_det, sonriendo)

        # ── Dibujar resultados ───────────────────────────────
        frame = dibujar_panel(frame, cara, ojos_det, sonriendo, estado, color_estado)

        # Dibujar rectángulos de ojos detectados
        for (ox, oy, ow, oh) in ojos:
            # Ojos están en la mitad superior del rostro
            cv2.rectangle(frame,
                          (cx + ox, cy + oy),
                          (cx + ox + ow, cy + oy + oh),
                          (0, 255, 0), 1)

        # Dibujar rectángulo de sonrisa
        for (sx, sy, sw, sh) in sonrisas:
            # Sonrisa está en la mitad inferior
            cv2.rectangle(frame,
                          (cx + sx, cy + mitad_y + sy),
                          (cx + sx + sw, cy + mitad_y + sy + sh),
                          (0, 215, 255), 1)

    cv2.imshow("Expresiones Faciales - Haar Cascade | UPeU 2026-1", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("\n👋 Cerrando...")
        break

# ─────────────────────────────────────────────────────────────
# 3. LIBERAR RECURSOS
# ─────────────────────────────────────────────────────────────
camara.release()
cv2.destroyAllWindows()
print("✅ Listo.")
