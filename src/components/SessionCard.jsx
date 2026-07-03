import { useEffect, useRef, useState } from "react";
import PreviewPanel from "./PreviewPanel.jsx";

export default function SessionCard({ sesion }) {
  const ref = useRef(null);
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setVisible(true);
          observer.disconnect();
        }
      },
      { threshold: 0.15 }
    );
    observer.observe(el);
    return () => observer.disconnect();
  }, []);

  const tieneLink = Boolean(sesion.colabUrl);

  return (
    <article
      id={sesion.id}
      ref={ref}
      className={`session${visible ? " in-view" : ""}`}
      style={{ "--accent": sesion.accent }}
    >
      <div className="session-body">
        <div className="tag-row">
          <span className="session-num">{sesion.numero}</span>
          <span className="session-icon">{sesion.icono}</span>
          <span className="session-sub">{sesion.subtitulo}</span>
        </div>

        <h3>{sesion.titulo}</h3>
        <p className="resumen">{sesion.resumen}</p>
        <span className="dato-clave">{sesion.dato}</span>

        <div className="hallazgo">
          <span className="hallazgo-label">Hallazgo principal</span>
          {sesion.hallazgo}
        </div>

        {tieneLink ? (
          <a
            className="demo-btn"
            href={sesion.colabUrl}
            target="_blank"
            rel="noopener noreferrer"
          >
            Probar demo <span className="arrow">→</span>
          </a>
        ) : (
          <span className="demo-btn disabled">Próximamente en Colab</span>
        )}

        {sesion.notaEspecial && (
          <p className="nota-especial">{sesion.notaEspecial}</p>
        )}

        {sesion.descargas && (
          <div className="descargas">
            {sesion.descargas.map((d) => (
              <a key={d.href} href={d.href} download>
                ↓ {d.nombre}
              </a>
            ))}
          </div>
        )}
      </div>

      <PreviewPanel preview={sesion.preview} notebook={sesion.notebook} />
    </article>
  );
}
