import { Link } from "react-router-dom";
import { useTheme } from "../../context/ThemeContext";
import "../../styles/components/CTASection.css";

import { ROLES } from '../../data/experience';

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
          {ROLES.map((e) => (
            <article key={e.id} className="exp-item">
              <time className="exp-date t-label">{typeof e.period === "string" ? e.period : e.period.en}</time>
              <div>
                <h3 className="exp-role t-heading">{typeof e.title === "string" ? e.title : e.title.en}</h3>
                <p className="exp-org">{e.org} · {typeof e.location === "string" ? e.location : e.location.pt}</p>
                <p className="exp-desc">{typeof e.bullets[0] === "string" ? e.bullets[0] : e.bullets[0].pt}</p>
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
