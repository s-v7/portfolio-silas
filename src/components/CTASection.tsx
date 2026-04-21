import { Link } from "react-router-dom";
import { useTheme } from "../context/ThemeContext";
import "./CTASection.css";

const EXP = [
  {
    date: "May 2024 — Present",
    role: "Technology & Information Security Advisor",
    org: "CREA-PI · Teresina, Brasil",
    desc: "Arquiteto solo do ecossistema FIE — SIGEC v2, FiscalBot, ART Engine, SistemaCrea. Modernização Java EE, análise de segurança e pipeline Sentinel-2 para monitoramento hídrico piauiense.",
  },
  {
    date: "May 2022 — Sep 2022",
    role: "Java Full Stack Developer",
    org: "EDM Software · Florianópolis, Brasil",
    desc: "Desenvolvimento e manutenção de aplicações enterprise JSF/PrimeFaces, correção de bugs e suporte a melhorias contínuas no produto principal.",
  },
];

export default function CTASection() {
  const { theme } = useTheme();
  const isAdmin = theme === "admin";
  return (
    <section
      className="section reveal"
      id="experience"
      aria-labelledby="exp-title"
    >
      <div className="container">
        <header className="section-header">
          <span className="section-num">03.</span>
          <h2 className="section-title" id="exp-title">
            {isAdmin ? "Experiência" : "Experience"}
          </h2>
          <div className="section-rule" />
        </header>
        <div className="exp-list">
          {EXP.map((e) => (
            <article key={e.role} className="exp-item">
              <time className="exp-date t-label">{e.date}</time>
              <div>
                <h3 className="exp-role t-heading">{e.role}</h3>
                <p className="exp-org">{e.org}</p>
                <p className="exp-desc">{e.desc}</p>
              </div>
            </article>
          ))}
        </div>
        <div className="cta-banner">
          <div>
            <p className="t-label" style={{ marginBottom: "6px" }}>
              {isAdmin ? "Próximos passos" : "Next steps"}
            </p>
            <p className="cta-banner__headline t-heading">
              {isAdmin
                ? "Disponível para projetos e colaborações em 2026"
                : "Open to senior engineering roles and consulting in 2026"}
            </p>
          </div>
          <div className="cta-banner__actions">
            <Link className="btn btn-primary" to="/contact">
              {isAdmin ? "✉ Entre em Contato" : "Get in touch"}
            </Link>
            <a
              className="btn btn-ghost"
              href="/Silas_Vasconcelos_CV.pdf"
              download
            >
              {isAdmin ? "↓ Download CV" : "Download CV"}
            </a>
          </div>
        </div>
      </div>
    </section>
  );
}
