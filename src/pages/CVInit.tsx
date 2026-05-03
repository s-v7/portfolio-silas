import { useTheme } from "../context/ThemeContext";
import "./CVInit.css";

const SKILLS = [
  {
    group: "Languages",
    items: "Java · Python · TypeScript · JavaScript (ES6+) · C",
  },
  {
    group: "Web",
    items:
      "Angular 17+ · React · JSF (PrimeFaces) · Spring Boot · FastAPI · Node.js",
  },
  { group: "Databases", items: "PostgreSQL · PostGIS · MongoDB" },
  {
    group: "DevOps",
    items:
      "Git · Docker · Kubernetes · CI/CD · Nginx · Cloudflare · Linux / systemd",
  },
  {
    group: "Data & AI",
    items:
      "Pandas · NumPy · TensorFlow · Scikit-learn · OpenAI API · Claude API · Sentinel-2",
  },
  {
    group: "Security",
    items: "Pentest · OWASP · Log auditing · Cryptography · LGPD compliance",
  },
];

const EXP = [
  {
    role: "Technology & Information Security Advisor",
    org: "CREA-PI — Teresina, Brasil",
    period: "May 2024 — Present",
    bullets: [
      "Sole architect of the FIE ecosystem: SIGEC v2, FiscalBot, ART Engine, SistemaCrea and SertLedgerToken.",
      "Java EE 8 systems development and enhancement (GlassFish, JSF/PrimeFaces, Hibernate, PostgreSQL, Linux).",
      "Sentinel-2→PostgreSQL pipeline for water resource monitoring of Piauí reservoirs via NDWI spectral analysis.",
      "Shell script automation and Telegram bot integration for institutional alerts.",
      "Security analysis, vulnerability mitigation and compliance reviews for government systems.",
    ],
  },
  {
    role: "Java Full Stack Developer",
    org: "EDM Software — Florianópolis, Brasil",
    period: "May 2022 — Sep 2022",
    bullets: [
      "Developed and maintained enterprise web application features using JSF (PrimeFaces), JavaScript, XHTML/CSS.",
      "Bug fixes and continuous improvement support for the main product.",
    ],
  },
];

export default function CVInit() {
  const { theme } = useTheme();
  const isAdmin = theme === "admin";
  return (
    <main className="cv-page">
      <div className="container">
        <header className="cv-header">
          <div>
            <h1 className="cv-name t-display">Silas Vasconcelos </h1>
            <p className="cv-subtitle">
              Full Stack Developer — Java / Python / TypeScript + DevOps &
              Distributed Systems
            </p>
            <div className="cv-contacts">
              <a href="mailto:svasconceloscruz7@gmail.com">
                svasconceloscruz7@gmail.com
              </a>
              <span>·</span>
              <a
                href="https://github.com/s-v7"
                target="_blank"
                rel="noreferrer"
              >
                github.com/s-v7
              </a>
              <span>·</span>
              <a
                href="https://www.linkedin.com/in/silas-v-053293255/"
                target="_blank"
                rel="noreferrer"
              >
                linkedin.com/in/s-v7
              </a>
              <span>·</span>
              <span>PI — Brasil</span>
            </div>
          </div>
          <a
            className="btn btn-primary"
            href="/Silas_Vasconcelos_CV.pdf"
            download
          >
            ↓ Download PDF
          </a>
        </header>

        <section className="cv-block">
          <p className="cv-block__label t-label">
            {isAdmin ? "// Resumo" : "// Summary"}
          </p>
          <p className="cv-block__text">
            Full Stack Developer with experience building distributed web
            applications in Java and Python. Skilled in front-end development
            (React, Angular) and back-end frameworks (Spring Boot, FastAPI),
            with hands-on DevOps experience (Docker, Kubernetes, CI/CD). Sole
            architect of the FIE ecosystem at CREA-PI — 1.1M+ engineering
            records on-chain, Sentinel-2 geospatial analytics, fiscal AI
            orchestration across 224 municipalities of Piauí. Designed for
            national adoption by CONFEA across 27 regional councils.
          </p>
        </section>

        <section className="cv-block">
          <p className="cv-block__label t-label">
            {isAdmin ? "// Competências" : "// Skills"}
          </p>
          <div className="cv-skills">
            {SKILLS.map(({ group, items }) => (
              <div key={group} className="cv-skill-row">
                <span className="cv-skill-group">{group}</span>
                <span className="cv-skill-items">{items}</span>
              </div>
            ))}
          </div>
        </section>

        <section className="cv-block">
          <p className="cv-block__label t-label">
            {isAdmin ? "// Experiência" : "// Experience"}
          </p>
          {EXP.map((e) => (
            <div key={e.role} className="cv-exp-item">
              <div className="cv-exp-header">
                <div>
                  <h2 className="cv-exp-role t-heading">{e.role}</h2>
                  <p className="cv-exp-org">{e.org}</p>
                </div>
                <time className="t-label">{e.period}</time>
              </div>
              <ul className="cv-exp-bullets">
                {e.bullets.map((b) => (
                  <li key={b}>{b}</li>
                ))}
              </ul>
            </div>
          ))}
        </section>

        <section className="cv-block">
          <p className="cv-block__label t-label">
            {isAdmin ? "// Formação" : "// Education"}
          </p>
          <div className="cv-exp-item">
            <div className="cv-exp-header">
              <div>
                <h2 className="cv-exp-role t-heading">
                  Technologist in Information Security (Distance Learning)
                </h2>
                <p className="cv-exp-org">
                  Universidade Paulista (UNIP) — Brasil
                </p>
              </div>
              <time className="t-label">Aug 2024 — Dec 2026 (expected)</time>
            </div>
          </div>
        </section>
      </div>
    </main>
  );
}
