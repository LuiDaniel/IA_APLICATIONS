import Header from "./components/Header.jsx";
import Hero from "./components/Hero.jsx";
import TeamBlock from "./components/TeamBlock.jsx";
import SessionCard from "./components/SessionCard.jsx";
import Footer from "./components/Footer.jsx";
import { equipo, sesiones } from "./data/portfolio.js";

export default function App() {
  return (
    <div id="top">
      <Header escuela={equipo.escuela} />
      <Hero equipo={equipo} sesiones={sesiones} />
      <TeamBlock equipo={equipo} />

      <main id="sesiones" className="sessions wrap">
        <p className="section-heading">Sesiones del portafolio</p>
        {sesiones.map((s) => (
          <SessionCard key={s.id} sesion={s} />
        ))}
      </main>

      <Footer equipo={equipo} />
    </div>
  );
}
