import { Link } from "react-router";
import { useTheme } from "../../context/ThemeContext";
import "../../styles/components/WhatIDo.css";

import { PROJECTS } from "../../data/whatIDo";

export default function WhatIDo() {
  const { theme } = useTheme();
  const isAdmin = theme === "admin";
  return (
    <section className="section reveal" id="projects" aria-labelledby="whatido-title">
      <div className="container">
        <header className="section-header">
          <span className="section-num">02.</span>
          <h2 className="section-title" id="whatido-title">
            {isAdmin ? "Projetos" : "Projects"}
          </h2>
          <div className="section-rule" />
        </header>
        <div className="projects-list">
          {PROJECTS.map((p) => (
            <Link
              key={p.title}
              to={p.href}
              className={`project-card${p.featured ? " project-card--featured" : ""}`}
            >
              <div>
                <p className="project-card__tag t-label">{p.tag}</p>
                <h3 className="project-card__title t-heading">{p.title}</h3>
                <p className="project-card__desc">{p.desc}</p>
              </div>
              <div className="project-card__meta">
                <ul className="project-card__stack">
                  {p.stack.map((t) => (
                    <li key={t} className="tag">
                      {t}
                    </li>
                  ))}
                </ul>
                <span className="project-card__arrow" aria-hidden="true">
                  →
                </span>
              </div>
            </Link>
          ))}
        </div>
        <div className="projects-footer">
          <Link className="btn btn-ghost" to="/projects">
            {isAdmin ? "Ver todos →" : "All projects →"}
          </Link>
        </div>
      </div>
    </section>
  );
}
