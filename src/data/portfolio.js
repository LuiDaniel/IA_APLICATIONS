// =====================================================================
// DATOS DEL PORTAFOLIO
// Este es el único archivo que necesitas tocar para personalizar la web.
// =====================================================================

export const equipo = {
  universidad: "Universidad Peruana Unión",
  facultad: "Facultad de Ingeniería y Arquitectura",
  escuela: "Escuela Profesional de Ingeniería de Sistemas",
  curso: "Introducción a las Ciencias de la Computación",
  unidad: "Unidad 3 · UPeU 2026-1",
  tituloPortafolio: "Aplicaciones de IA y Ciencia de Datos en Diversos Contextos",
  nombreEquipo: "[Completar con el nombre del equipo]",
  seccionAula: "[Completar]",
  fecha: "03 de julio de 2026",
  integrantes: [
    "Quecara Machaca, Luis Daniel",
    "Sullca Laura, Smith Jheremy",
    "Mamani Dueñas, Jhosep",
    "Condori Flores, Bernabe Shantell",
  ],
};

// -----------------------------------------------------------------------
// ENLACES DE GOOGLE COLAB
// -----------------------------------------------------------------------
// Sube cada .ipynb a https://colab.research.google.com (pestaña "Subir"),
// luego "Compartir" → "Cualquier persona con el enlace" → copia el link
// y pégalo aquí abajo. Instrucciones completas en el README del proyecto.
// Mientras un link esté vacío (""), el botón mostrará "Próximamente".
// -----------------------------------------------------------------------
const colabLinks = {
  s1: "https://colab.research.google.com/drive/1Hnsg0pkY3O-z9uiHfA5jejx9RImZ5nK5?usp=sharing",
  s2: "https://colab.research.google.com/drive/1rInWavqy6YrrWZ_sRQyM20BAusYxnkfn?usp=sharing",
  s3: "https://colab.research.google.com/drive/1YXphlFpu_4VMtFepf8pL8D4pEEhBKFzF?usp=sharing",
  s4: "https://colab.research.google.com/drive/1oGFvgCCRm68vFoRL9GHkWNV6CrjLc0DU?usp=sharing",
  s5: "https://colab.research.google.com/drive/1-eIA50mkKSj_nwpUU6fZeYDJNylNjXqo?usp=sharing",
};

export const sesiones = [
  {
    id: "s1",
    numero: "01",
    accent: "#1F6F5C",
    icono: "📊",
    titulo: "Ciencia de Datos",
    subtitulo: "Análisis y visualización",
    notebook: "01_ciencia_datos.ipynb",
    colabUrl: colabLinks.s1,
    resumen:
      "Limpieza y análisis exploratorio del dataset Students Performance in Exams (Kaggle, 1000 registros). Se verificaron nulos, duplicados y rangos válidos, y se compararon los puntajes de estudiantes según si completaron un curso de preparación.",
    dato: "1000 registros · 0 nulos · 0 duplicados",
    hallazgo:
      "Los estudiantes que completaron el curso de preparación obtuvieron en promedio más puntaje en las tres materias, con la brecha más amplia en escritura (+9.9 puntos).",
    preview: { tipo: "imagen", src: "/previews/sesion01-histograma.png", alt: "Histograma de la distribución del puntaje de Matemática" },
  },
  {
    id: "s2",
    numero: "02",
    accent: "#5B4B8A",
    icono: "🤖",
    titulo: "Inteligencia Artificial",
    subtitulo: "Análisis de aplicación real",
    notebook: "02_inteligencia_artificial.ipynb",
    colabUrl: colabLinks.s2,
    resumen:
      "Estudio del motor de recomendación de Netflix: aprendizaje híbrido que combina filtrado colaborativo (no supervisado) con un modelo de ranking (supervisado) sobre embeddings de usuarios y títulos.",
    dato: "Embeddings · filtrado colaborativo · ranking",
    hallazgo:
      "La ventaja es la personalización a gran escala; el riesgo documentado es la 'burbuja de filtro', que reduce gradualmente la diversidad de contenido descubierto.",
    preview: {
      tipo: "codigo",
      lenguaje: "python",
      lineas: [
        "similitud = coseno(usuario_emb, titulo_emb)",
        "score = sigmoid(ranking_model(similitud))",
        "# título con mayor score → primera posición",
      ],
    },
  },
  {
    id: "s3",
    numero: "03",
    accent: "#A63D40",
    icono: "🛡️",
    titulo: "Ciberseguridad e IA",
    subtitulo: "Amenazas y mitigación",
    notebook: "03_ciberseguridad_ia.ipynb",
    colabUrl: colabLinks.s3,
    resumen:
      "Caso real: fraude por videollamada deepfake contra Arup (Hong Kong, 2024), donde un empleado transfirió US$25.6M tras una videollamada con ejecutivos generados por IA a partir de material público.",
    dato: "Caso Arup · US$25.6M · CNN Business, 2024",
    hallazgo:
      "La mitigación combina detección de phishing por ML/NLP, detección de deepfakes por visión computacional, un enfoque IDS sobre transacciones, y verificación obligatoria fuera de banda.",
    preview: {
      tipo: "codigo",
      lenguaje: "texto",
      lineas: [
        "ALERTA: 15 transferencias inusuales",
        "→ mismo día, cuentas nuevas",
        "acción: verificación fuera de banda",
      ],
    },
  },
  {
    id: "s4",
    numero: "04",
    accent: "#B8842C",
    icono: "👁️",
    titulo: "Visión por Computadora",
    subtitulo: "Aplicación industrial",
    notebook: "04_vision_computacional.ipynb",
    colabUrl: colabLinks.s4,
    resumen:
      "Inspección automática de defectos en placas de circuito impreso (PCBA) con PCBA-YOLO, una arquitectura de detección de objetos de una sola etapa adaptada a manufactura electrónica.",
    dato: "mAP 97.3% · 322 FPS",
    hallazgo:
      "La fórmula IoU (Área de intersección / Área de unión) es central para evaluar el modelo y para eliminar cajas redundantes durante la inferencia (NMS).",
    preview: { tipo: "imagen", src: "/previews/sesion04-iou.png", alt: "Diagrama de Intersection over Union (IoU) aplicado a inspección de PCB" },
  },
  {
    id: "s5",
    numero: "05",
    accent: "#2A5C8A",
    icono: "💻",
    titulo: "IA en Desarrollo de Software",
    subtitulo: "Análisis crítico",
    notebook: "05_ia_desarrollo_software.ipynb",
    colabUrl: colabLinks.s5,
    resumen:
      "Se pidió a una IA generativa mejorar script2_expresiones.py (detección de expresiones con Haar Cascade). La IA propuso reemplazar los clasificadores por MediaPipe Face Mesh y el Eye Aspect Ratio (EAR).",
    dato: "Haar Cascade → MediaPipe + EAR",
    hallazgo:
      "La mejora es real (métrica continua, suavizado temporal), pero la IA eliminó silenciosamente la detección de sonrisa del script original: una regresión que solo se detecta revisando la cobertura funcional.",
    preview: {
      tipo: "codigo",
      lenguaje: "python",
      lineas: [
        "ear = calcular_EAR(landmarks, OJO_IZQ)",
        "historial.append(ear)",
        "estado = 'CERRADOS' if avg(historial) < 0.21 else 'ABIERTOS'",
      ],
    },
    notaEspecial:
      "Este notebook documenta el código como texto y no requiere cámara, por lo que sí se puede abrir y revisar en Colab. Los scripts originales sí usan cámara web en tiempo real y necesitan ejecutarse en tu equipo — puedes descargarlos abajo.",
    descargas: [
      { nombre: "script2_expresiones.py (original)", href: "/downloads/script2_expresiones.py" },
      { nombre: "script2_mejorado_IA.py (mejorado)", href: "/downloads/script2_mejorado_IA.py" },
      { nombre: "requirements.txt", href: "/downloads/requirements.txt" },
    ],
  },
];
