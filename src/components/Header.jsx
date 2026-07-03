export default function Header({ escuela }) {
  return (
    <header className="site-header">
      <div className="wrap">
        <span className="brand">
          <strong>UPeU</strong> · {escuela}
        </span>
        <nav className="header-nav">
          <a href="#sesiones">Sesiones</a>
          <a href="#equipo">Equipo</a>
        </nav>
      </div>
    </header>
  );
}
