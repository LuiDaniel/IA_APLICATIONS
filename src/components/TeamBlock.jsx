export default function TeamBlock({ equipo }) {
  return (
    <section id="equipo" className="wrap">
      <pre className="meta-block">
        <span className="cm"># -----------------------------------------------</span>
        {"\n"}
        <span className="key">universidad</span>
        <span className="cm">:</span> <span className="val">{equipo.universidad}</span>
        {"\n"}
        <span className="key">facultad</span>
        <span className="cm">:</span> <span className="val">{equipo.facultad}</span>
        {"\n"}
        <span className="key">escuela</span>
        <span className="cm">:</span> <span className="val">{equipo.escuela}</span>
        {"\n"}
        <span className="cm"># -----------------------------------------------</span>
        {"\n"}
        <span className="key">equipo</span>
        <span className="cm">:</span> <span className="val">{equipo.nombreEquipo}</span>
        {"\n"}
        <span className="key">seccion</span>
        <span className="cm">:</span> <span className="val">{equipo.seccionAula}</span>
        {"\n"}
        <span className="key">fecha</span>
        <span className="cm">:</span> <span className="val">{equipo.fecha}</span>
        {"\n"}
        <span className="key">integrantes</span>
        <span className="cm">:</span>
        {equipo.integrantes.map((n) => (
          <span key={n}>
            {"\n  - "}
            <span className="val">{n}</span>
          </span>
        ))}
      </pre>
    </section>
  );
}
