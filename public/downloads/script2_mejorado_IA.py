"""
=============================================================
 SCRIPT 2 MEJORADO — Generado por IA a partir de script2_expresiones.py
 Sección 05 del Portafolio Final — IA en Desarrollo de Software
 Universidad Peruana Unión · EP Ingeniería de Sistemas · 2026-1
=============================================================

 QUÉ CAMBIÓ RESPECTO AL ORIGINAL (script2_expresiones.py):
   - Reemplaza los 3 clasificadores Haar Cascade (rostro, ojos, sonrisa)
     por MediaPipe Face Mesh (468 landmarks faciales con seguimiento temporal).
   - El estado del ojo ya no es un conteo binario (0/1/2 "ojos detectados"),
     sino una métrica geométrica continua: el Eye Aspect Ratio (EAR).
   - Se agrega suavizado temporal (HISTORIAL) para evitar falsos "cerrado"
     de un solo frame, algo que el original no tenía.

 LIMITACIÓN CONOCIDA (ver informe, Sección 5.4):
   - Este script NO reimplementa la detección de sonrisa del original.
     Es una regresión funcional identificada en el análisis crítico.

 REQUISITOS:
   pip install opencv-python mediapipe numpy

 EJECUCIÓN (LOCAL, no en Google Colab — requiere cámara y ventana gráfica):
   python script2_mejorado_IA.py

 CONTROLES:
   Q  → salir
=============================================================
"""

import cv2
import mediapipe as mp
import numpy as np
from collections import deque

# --- 1. Face Mesh en vez de Haar Cascade ---
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1, refine_landmarks=True,
    min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Índices de landmarks del ojo izquierdo (formato MediaPipe Face Mesh)
OJO_IZQ = [362, 385, 387, 263, 373, 380]


def distancia(a, b):
    return np.linalg.norm(np.array(a) - np.array(b))


def calcular_EAR(landmarks, indices, ancho, alto):
    """Eye Aspect Ratio: EAR = (||p2-p6|| + ||p3-p5||) / (2*||p1-p4||)"""
    pts = [(landmarks[i].x * ancho, landmarks[i].y * alto) for i in indices]
    p1, p2, p3, p4, p5, p6 = pts
    return (distancia(p2, p6) + distancia(p3, p5)) / (2 * distancia(p1, p4))


UMBRAL_EAR = 0.21             # por debajo de este valor, ojo cerrado
HISTORIAL = deque(maxlen=5)   # suaviza el parpadeo natural (evita falsos "cerrado")

camara = cv2.VideoCapture(0)
if not camara.isOpened():
    print("❌ No se pudo abrir la cámara.")
    exit()

while True:
    ok, frame = camara.read()
    if not ok:
        break
    frame = cv2.flip(frame, 1)
    alto, ancho = frame.shape[:2]
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    resultado = face_mesh.process(rgb)

    estado = "SIN ROSTRO"
    if resultado.multi_face_landmarks:
        lm = resultado.multi_face_landmarks[0].landmark
        ear = calcular_EAR(lm, OJO_IZQ, ancho, alto)
        HISTORIAL.append(ear)
        ear_suavizado = sum(HISTORIAL) / len(HISTORIAL)
        estado = "OJOS CERRADOS" if ear_suavizado < UMBRAL_EAR else "OJOS ABIERTOS"

    cv2.putText(frame, estado, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    cv2.putText(frame, "Q: salir", (10, alto - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
    cv2.imshow("Deteccion robusta - MediaPipe + EAR", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camara.release()
cv2.destroyAllWindows()
