import { useTheme } from "../context/ThemeContext";
import "../styles/pages/CVInit.css";

import { SKILLS } from "../data/cv";
import { EDU } from "../data/education";
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
              Software Engineer — Java / Python / Node.js / TypeScript / IA
              Generativa
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
            {isAdmin
              ? "Software Engineer com experiência no desenvolvimento e modernização de sistemas corporativos utilizando Java, Python, Node.js e TypeScript. Atuação com backend, APIs REST, PostgreSQL, integração entre sistemas e evolução de sistemas legados. Atualmente trabalho na modernização de sistemas Java EE para arquiteturas mais modernas, além do desenvolvimento de serviços com NestJS, Angular e soluções envolvendo IA Generativa, LLMs e automação de processos."
              : "Software Engineer with experience in developing and modernizing corporate systems using Java, Python, Node.js and TypeScript. Skilled in backend development, REST APIs, PostgreSQL, system integration and legacy system modernization. Currently working on the evolution of Java EE systems toward modern architectures, while building services with NestJS, Angular and solutions involving Generative AI, LLMs and process automation."}
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
                  <h2 className="cv-exp-role t-heading">
                    {typeof e.title === "string" ? e.title : e.title.en}
                  </h2>
                  <p className="cv-exp-org">
                    {e.org} —{" "}
                    {typeof e.location === "string"
                      ? e.location
                      : e.location.pt}
                  </p>
                </div>
                <time className="t-label">
                  {typeof e.period === "string" ? e.period : e.period.en}
                </time>
              </div>
              <ul className="cv-exp-bullets">
                {e.bullets.map((b) => (
                  <li key={typeof b === "string" ? b : b.en}>
                    {typeof b === "string" ? b : b.en}
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </section>
      </div>
    </main>
  );
}
