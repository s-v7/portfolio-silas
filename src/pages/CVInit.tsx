import { useTheme } from "../context/ThemeContext";
import "../styles/pages/CVInit.css";

import { SKILLS } from "../data/cv";
import { ROLES } from "../data/experience";

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
          {ROLES.map((e) => (
            <div key={e.id} className="cv-exp-item">
              <div className="cv-exp-header">
                <div>
                  <h2 className="cv-exp-role t-heading">{typeof e.title === "string" ? e.title : e.title.en}</h2>
                  <p className="cv-exp-org">{e.org} — {typeof e.location === "string" ? e.location : e.location.pt}</p>
                </div>
                <time className="t-label">{typeof e.period === "string" ? e.period : e.period.en}</time>
              </div>
              <ul className="cv-exp-bullets">
                {e.bullets.map((b) => (
                  <li key={typeof b === "string" ? b : b.en}>{typeof b === "string" ? b : b.en}</li>
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
                  computer engineering
                </h2>
                <p className="cv-exp-org">
                  Brasil
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
