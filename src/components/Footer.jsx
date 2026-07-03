export default function Footer({ equipo }) {
  return (
    <footer className="site-footer">
      <div className="wrap" style={{ display: "flex", justifyContent: "space-between", width: "100%", flexWrap: "wrap", gap: 16 }}>
        <span>{equipo.escuela} · {equipo.unidad}</span>
        <a href="#top">Volver arriba ↑</a>
      </div>
    </footer>
  );
}
