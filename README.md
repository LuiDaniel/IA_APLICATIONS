# Portafolio U3 — Web en React

Página web minimalista para mostrar las 5 sesiones del portafolio final de
**Introducción a las Ciencias de la Computación**, con vista previa y botón
de demo en Google Colab para cada una.

## 1. Instalar y correr en local

```bash
npm install
npm run dev
```

Abre lo que te indique la terminal (normalmente `http://localhost:5173`).

## 2. Pegar tus enlaces de Google Colab

Este es **el único paso manual necesario**. Abre:

```
src/data/portfolio.js
```

y busca el bloque `colabLinks` al inicio del archivo. Por cada notebook:

1. Entra a **https://colab.research.google.com**
2. Pestaña **"Subir"** → selecciona el `.ipynb` correspondiente (están en la
   carpeta `portafolio_code` que ya tenías). Colab lo guarda en tu Google
   Drive (`Mi unidad/Colab Notebooks/`).
3. Clic en **"Compartir"** (arriba a la derecha) → "Cualquier persona con
   el enlace" → copia el link.
4. Pégalo en el campo correspondiente (`s1`, `s2`, `s3`, `s4` o `s5`).

Mientras un enlace esté vacío, el botón de esa sesión muestra "Próximamente
en Colab" en vez de romperse o llevar a un link falso.

**Atajo con GitHub:** si subes la carpeta de notebooks a un repositorio de
GitHub, cada uno se abre directo con una URL así, sin subir nada a mano:

```
https://colab.research.google.com/github/<usuario>/<repo>/blob/main/01_ciencia_datos.ipynb
```

## 3. Sobre la Sesión 5 (cámara web)

El notebook `05_ia_desarrollo_software.ipynb` **sí se puede abrir y correr
en Colab** sin problema: documenta el prompt y el código generado como
texto, no ejecuta la cámara.

Los scripts que sí usan cámara en tiempo real (`script2_expresiones.py` y
`script2_mejorado_IA.py`) **no funcionan en Colab** porque Colab no tiene
acceso a cámara ni ventanas gráficas. Por eso, en la tarjeta de la Sesión 5
la web ofrece botones de **descarga directa** de esos scripts para que
cualquiera los corra en su propia máquina:

```bash
pip install -r requirements.txt
python script2_expresiones.py       # versión original
python script2_mejorado_IA.py       # versión mejorada por la IA
```

Esos archivos ya están incluidos en `public/downloads/`.

## 4. Editar textos, equipo o colores

Todo el contenido (equipo, curso, resúmenes, hallazgos, colores por sesión)
vive en `src/data/portfolio.js`. No necesitas tocar ningún componente para
cambiar texto. Los estilos globales están en `src/index.css`.

## 5. Publicar la web (para obtener el link que pide el portafolio)

Genera la build de producción:

```bash
npm run build
```

Esto crea la carpeta `dist/`. Puedes subirla gratis a:

- **Vercel**: `npx vercel dist --prod` (o conecta el repo desde vercel.com)
- **Netlify**: arrastra la carpeta `dist/` a app.netlify.com/drop
- **GitHub Pages**: sube `dist/` a una rama `gh-pages`

El link que te den es el que va en la tabla "Enlace al portafolio web" del
documento Word.

## Estructura del proyecto

```
src/
  data/portfolio.js       ← equipo + las 5 sesiones (contenido y links)
  components/             ← Header, Hero, TeamBlock, SessionCard, PreviewPanel, Footer
  App.jsx
  index.css               ← sistema de diseño (colores, tipografía, layout)
public/
  previews/                ← gráficos reales exportados de los notebooks 1 y 4
  downloads/               ← scripts de la Sesión 5 para ejecución local
```
