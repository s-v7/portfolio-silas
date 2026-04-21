import { useState } from "react";
import { useTheme } from "../context/ThemeContext";
import "./Projects.css";

const PROJECTS = [
  {
    id: "sigec",
    tag: "Fiscal Intelligence",
    title: "SIGEC v2 — Fiscal Intelligence Engine",
    desc: "Plataforma de rastreamento de obras com 1.1M+ ARTs em blockchain SHA-256, pipeline Sentinel-2→PostGIS para 20 açudes piauienses (NDWI), FiscalBot Telegram com alertas automáticos (cron seg 06:00 BRT), roteamento NetworkX/TSP nos 224 municípios, orchestrator OpenAI + Claude.",
    stack: [
      "Flask / Gunicorn",
      "FastAPI",
      "Angular 17",
      "PostgreSQL 17",
      "PostGIS",
      "Blockchain",
      "Sentinel-2",
      "NetworkX",
      "Telegram API",
      "Claude API",
    ],
    category: "Gov",
    link: "https://github.com/s-v7/CadastroRastreamentoObras",
    status: "Production",
    year: "2024–2025",
    featured: true,
  },
  {
    id: "creapi-ai",
    tag: "AI · Analytics",
    title: "CREAPI — Intelligent Analytics Platform",
    desc: "Plataforma de analytics preditivo para CREA-PI, integrando modelos ML, pipelines OCR + NLP e monitoramento estatístico de ARTs.",
    stack: ["FastAPI", "PostgreSQL", "OCR", "NLP", "DVC"],
    category: "AI",
    link: null,
    status: "Private",
    year: "2024",
    featured: false,
  },
  {
    id: "fiscalbot",
    tag: "AI · Telegram",
    title: "FiscalBot & ART Engine",
    desc: "Bot Telegram operacional com pipeline de alertas automáticos, processamento de 1.1M+ ARTs com ON CONFLICT DO NOTHING e motor de IA OpenAI + Claude para análise e classificação fiscal.",
    stack: [
      "FastAPI",
      "Telegram Bot API",
      "OpenAI",
      "Claude API",
      "PostgreSQL",
    ],
    category: "AI",
    link: null,
    status: "Production",
    year: "2025",
    featured: false,
  },
  {
    id: "ru-confea",
    tag: "Government · Integration",
    title: "RU ↔ CONFEA Integration Platform",
    desc: "Plataforma oficial de integração automatizando fluxos SRP entre CONFEA e CREAs usando APIs e webhooks. Comunicação bidirecional com garantias de entrega.",
    stack: ["Jakarta EE", "Webhooks", "OpenAPI", "PostgreSQL"],
    category: "Gov",
    link: null,
    status: "Private",
    year: "2024",
    featured: false,
  },
  {
    id: "sistemacrea",
    tag: "Legacy Modernization",
    title: "SistemaCrea — Jakarta EE",
    desc: "Modernização de ERP institucional legacy: Maven multi-module EAR, integração e-MEC (4.328 IES via Dados Abertos MEC), JSF/PrimeFaces 13 com design system vd-* e CSS variables light/dark/dim.",
    stack: [
      "Java EE 8",
      "JSF / PrimeFaces",
      "EJB",
      "JPA",
      "Payara 6",
      "PostgreSQL",
    ],
    category: "Enterprise",
    link: null,
    status: "Active",
    year: "2024–Now",
    featured: false,
  },
  {
    id: "blockchain",
    tag: "Research · Blockchain",
    title: "Blockchain CREA-PI",
    desc: "Rede blockchain para integração e rastreabilidade segura de dados do CREA-PI. Fundação do pipeline de 1.1M ARTs do SIGEC v2.",
    stack: ["Blockchain", "Node.js", "SHA-256"],
    category: "Research",
    link: "https://github.com/s-v7/blockchain-crea-pi",
    status: "Research",
    year: "2023",
    featured: false,
  },
  {
    id: "audit",
    tag: "Enterprise · Full Stack",
    title: "Audit System",
    desc: "Sistema full-stack de auditoria construído com Flask e Angular, com foco em rastreabilidade e arquitetura modular.",
    stack: ["Python", "Flask", "Angular", "SQLite"],
    category: "Enterprise",
    link: "https://github.com/s-v7/sistema-auditoria",
    status: "Public",
    year: "2023",
    featured: false,
  },
  {
    id: "tracking",
    tag: "Enterprise",
    title: "Registration Tracking Works",
    desc: "Sistema para gestão de dados de obras de construção civil com backend modular e banco de dados relacional. Precursor do SIGEC v2.",
    stack: ["Python", "Angular", "PostgreSQL", "SQLite"],
    category: "Enterprise",
    link: "https://github.com/s-v7/CadastroRastreamentoObras",
    status: "Public",
    year: "2022",
    featured: false,
  },
];

const CATS = ["All", "Gov", "AI", "Enterprise", "Research"];
const S_COLOR: Record<string, string> = {
  Production: "var(--g)",
  Active: "var(--g)",
  Public: "var(--g)",
  MVP: "#EF9F27",
  Development: "#EF9F27",
  Private: "var(--text-dim)",
  Research: "var(--text-dim)",
};

export default function Projects() {
  const { theme } = useTheme();
  const isAdmin = theme === "admin";
  const [f, setF] = useState("All");
  const visible =
    f === "All" ? PROJECTS : PROJECTS.filter((p) => p.category === f);

  return (
    <main className="projects-page">
      <div className="container">
        <header className="section-header" style={{ paddingTop: "3rem" }}>
          <span className="section-num">02.</span>
          <h1 className="section-title">{isAdmin ? "Projetos" : "Projects"}</h1>
          <div className="section-rule" />
        </header>
        <div className="filter-bar" role="group">
          {CATS.map((c) => (
            <button
              key={c}
              onClick={() => setF(c)}
              className={`filter-btn${f === c ? " filter-btn--active" : ""}`}
              aria-pressed={f === c}
            >
              {c}
            </button>
          ))}
        </div>
        <div className="projects-full-list">
          {visible.map((p) => (
            <article
              key={p.id}
              id={p.id}
              className={`proj-full-card${p.featured ? " proj-full-card--featured" : ""}`}
            >
              <div className="proj-full-header">
                <div>
                  <p className="proj-full-tag t-label">{p.tag}</p>
                  <h2 className="proj-full-title t-heading">{p.title}</h2>
                </div>
                <div className="proj-full-badges">
                  <span
                    className="proj-status"
                    style={{ "--c": S_COLOR[p.status] } as any}
                  >
                    <span
                      className="proj-status__dot"
                      style={{ background: S_COLOR[p.status] }}
                    />
                    <span style={{ color: S_COLOR[p.status] }}>{p.status}</span>
                  </span>
                  <span className="t-label">{p.year}</span>
                </div>
              </div>
              <p className="proj-full-desc">{p.desc}</p>
              <div className="proj-full-footer">
                <ul className="proj-full-stack">
                  {p.stack.map((t) => (
                    <li key={t} className="tag">
                      {t}
                    </li>
                  ))}
                </ul>
                {p.link && (
                  <a
                    className="btn btn-ghost"
                    href={p.link}
                    target="_blank"
                    rel="noreferrer"
                  >
                    GitHub →
                  </a>
                )}
              </div>
            </article>
          ))}
        </div>
      </div>
    </main>
  );
}
