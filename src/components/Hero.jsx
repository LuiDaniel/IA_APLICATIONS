export default function Hero({ equipo, sesiones }) {
  return (
    <section className="hero">
      <div className="wrap">
        <p className="eyebrow">
          {equipo.curso} · {equipo.unidad}
        </p>
        <h1>{equipo.tituloPortafolio}</h1>
        <p className="lede">
          Portafolio final con cinco sesiones de trabajo, cada una con su
          notebook ejecutado, su hallazgo principal y un enlace para
          probarlo en vivo en Google Colab.
        </p>

        <nav className="toc" aria-label="Índice de sesiones">
          {sesiones.map((s) => (
            <a href={`#${s.id}`} key={s.id}>
              <span className="toc-num" style={{ color: s.accent }}>
                {s.numero}
              </span>
              <span className="toc-icon">{s.icono}</span>
              <span className="toc-title">{s.titulo}</span>
              <span className="toc-sub">{s.subtitulo}</span>
              <span className="toc-arrow">↓</span>
            </a>
          ))}
        </nav>
      </div>
    </section>
  );
}
