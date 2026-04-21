import { Link } from "react-router-dom";
import { useTheme } from "../context/ThemeContext";
import "./WhatIDo.css";

const PROJECTS = [
  {
    tag: "Fiscal Intelligence · CREA-PI",
    title: "SIGEC v2 — Fiscal Intelligence Engine",
    desc: "1.1M+ ARTs em blockchain SHA-256, pipeline Sentinel-2→PostGIS para monitoramento hídrico, FiscalBot Telegram e roteamento NetworkX/TSP nos 224 municípios do Piauí.",
    stack: [
      "Flask + FastAPI",
      "Angular 17",
      "PostgreSQL",
      "Blockchain",
      "PostGIS",
    ],
    href: "/projects#sigec",
    featured: true,
  },
  {
    tag: "Legacy Modernization",
    title: "SistemaCrea — Jakarta EE",
    desc: "Modernização de ERP institucional: Maven EAR, integração e-MEC (4.328 IES), JSF/PrimeFaces 13 com design system CSS variables.",
    stack: ["Java EE 8", "JSF/PrimeFaces", "Payara 6", "PostgreSQL"],
    href: "/projects#sistemacrea",
    featured: false,
  },
  {
    tag: "AI · Telegram",
    title: "FiscalBot & ART Engine",
    desc: "Bot Telegram operacional com alertas automáticos (cron seg 06:00 BRT), processamento de ARTs em massa e motor OpenAI + Claude.",
    stack: ["FastAPI", "Telegram API", "OpenAI", "Claude API"],
    href: "/art-engine",
    featured: false,
  },
];

export default function WhatIDo() {
  const { theme } = useTheme();
  const isAdmin = theme === "admin";
  return (
    <section
      className="section reveal"
      id="projects"
      aria-labelledby="whatido-title"
    >
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
