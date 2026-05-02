import { useTheme } from "../context/ThemeContext";
import "./Projects.css";

type Lang = "en" | "pt";
type I18n = string | { en: string; pt: string };
const t = (v: I18n, lang: Lang): string =>
  typeof v === "string" ? v : v[lang] ?? v.en;

type Size = "featured" | "tall" | "wide" | "med" | "sm";
type Status = "Production" | "Active" | "Public" | "Private" | "Research" | "MVP" | "Development";

interface Project {
  id: string;
  size: Size;
  tag: I18n;
  title: I18n;
  subtitle?: I18n;
  desc: I18n;
  stack: string[];
  status: Status;
  year: string;
  link: string | null;
}

const PROJECTS: Project[] = [
  {
    id: "sigec",
    size: "featured",
    tag: { en: "Fiscal Intelligence · CREA-PI", pt: "Inteligência Fiscal · CREA-PI" },
    title: "SIGEC v2",
    subtitle: { en: "Fiscal Intelligence Engine", pt: "Motor de Inteligência Fiscal" },
    desc: {
      en: "1.1M+ ARTs on a SHA-256 blockchain. Sentinel-2 → PostGIS pipeline monitoring 20 reservoirs (NDWI). FiscalBot Telegram with auto-alerts (cron Mon 06:00 BRT). NetworkX/TSP routing across 224 municipalities of Piauí.",
      pt: "1.1M+ ARTs em blockchain SHA-256. Pipeline Sentinel-2 → PostGIS monitorando 20 açudes (NDWI). FiscalBot Telegram com alertas automáticos (cron seg 06:00 BRT). Roteamento NetworkX/TSP nos 224 municípios do Piauí.",
    },
    stack: ["Flask", "FastAPI", "Angular 17", "PostgreSQL 17", "PostGIS", "Blockchain", "Sentinel-2", "NetworkX"],
    status: "Production",
    year: "2024–2025",
    link: "https://github.com/s-v7/CadastroRastreamentoObras",
  },
  {
    id: "art-engine",
    size: "tall",
    tag: { en: "AI · Auditing", pt: "IA · Auditoria" },
    title: { en: "ART Engine", pt: "Motor ART" },
    desc: {
      en: "Institutional AI for auditing Engineering Responsibility Records. Deterministic rules, DB×PDF cross-check, LLM enrichment with strict guardrails.",
      pt: "IA institucional para auditoria de ARTs. Regras determinísticas, cross-check DB×PDF, enriquecimento LLM com guardrails estritos.",
    },
    stack: ["FastAPI", "LangGraph", "Claude", "OpenAI"],
    status: "Production",
    year: "2025",
    link: null,
  },
  {
    id: "creapi-ai",
    size: "med",
    tag: { en: "AI · Analytics", pt: "IA · Analytics" },
    title: "CREAPI Analytics",
    desc: {
      en: "Predictive analytics platform integrating ML, OCR + NLP pipelines and statistical monitoring of ARTs.",
      pt: "Analytics preditivo, ML, pipelines OCR+NLP e monitoramento estatístico de ARTs.",
    },
    stack: ["FastAPI", "OCR", "NLP", "DVC"],
    status: "Private",
    year: "2024",
    link: null,
  },
  {
    id: "ru-confea",
    size: "med",
    tag: { en: "Gov · Integration", pt: "Gov · Integração" },
    title: { en: "RU ↔ CONFEA", pt: "RU ↔ CONFEA" },
    desc: {
      en: "Official integration platform automating SRP flows between CONFEA and CREAs via APIs and webhooks.",
      pt: "Plataforma oficial automatizando fluxos SRP entre CONFEA e CREAs via APIs e webhooks.",
    },
    stack: ["Jakarta EE", "Webhooks", "OpenAPI"],
    status: "Private",
    year: "2024",
    link: null,
  },
  {
    id: "sistemacrea",
    size: "wide",
    tag: { en: "Legacy Modernization", pt: "Modernização Legada" },
    title: "SistemaCrea — Jakarta EE",
    desc: {
      en: "ERP modernization: multi-module Maven EAR, e-MEC integration (4,328 institutions), JSF/PrimeFaces 13 with vd-* design system and CSS variables for light/dark/dim.",
      pt: "Modernização de ERP: Maven multi-module EAR, integração e-MEC (4.328 IES), JSF/PrimeFaces 13 com design system vd-* e variáveis CSS light/dark/dim.",
    },
    stack: ["Java EE 8", "JSF/PrimeFaces", "EJB", "Payara 6", "PostgreSQL"],
    status: "Active",
    year: "2024–Now",
    link: null,
  },
  {
    id: "blockchain",
    size: "sm",
    tag: { en: "Research", pt: "Pesquisa" },
    title: "Blockchain CREA-PI",
    desc: {
      en: "Blockchain network for secure CREA-PI data traceability. Foundation for SIGEC v2's 1.1M ART pipeline.",
      pt: "Rede blockchain para rastreabilidade de dados do CREA-PI. Base do pipeline de 1.1M ARTs do SIGEC v2.",
    },
    stack: ["Node.js", "SHA-256"],
    status: "Research",
    year: "2023",
    link: "https://github.com/s-v7/blockchain-crea-pi",
  },
  {
    id: "audit",
    size: "sm",
    tag: { en: "Enterprise", pt: "Enterprise" },
    title: { en: "Audit System", pt: "Sistema de Auditoria" },
    desc: {
      en: "Full-stack auditing system in Flask + Angular, focused on traceability and modular architecture.",
      pt: "Sistema full-stack de auditoria em Flask + Angular, com foco em rastreabilidade e arquitetura modular.",
    },
    stack: ["Flask", "Angular", "SQLite"],
    status: "Public",
    year: "2023",
    link: "https://github.com/s-v7/sistema-auditoria",
  },
  {
    id: "tracking",
    size: "sm",
    tag: { en: "Enterprise", pt: "Enterprise" },
    title: { en: "Works Tracking", pt: "Rastreamento de Obras" },
    desc: {
      en: "Construction works data management with modular backend and relational DB. Precursor to SIGEC v2.",
      pt: "Gestão de dados de obras com backend modular e banco relacional. Precursor do SIGEC v2.",
    },
    stack: ["Python", "Angular", "PostgreSQL"],
    status: "Public",
    year: "2022",
    link: "https://github.com/s-v7/CadastroRastreamentoObras",
  },
];

const STATUS_CLASS: Record<Status, string> = {
  Production: "", Active: "", Public: "",
  MVP: "warn", Development: "warn",
  Private: "dim", Research: "dim",
};

function FeaturedViz() {
  return (
    <div className="featured-viz" aria-hidden="true">
      <svg viewBox="0 0 200 160">
        <g stroke="var(--g)" strokeWidth=".5" fill="none" opacity=".6">
          {Array.from({ length: 14 }).map((_, i) => (
            <line
              key={i}
              x1={20 + (i * 13) % 160}
              y1={20 + (i * 37) % 120}
              x2={20 + ((i + 5) * 17) % 160}
              y2={20 + ((i + 3) * 23) % 120}
            />
          ))}
        </g>
        <g fill="var(--g)">
          {Array.from({ length: 18 }).map((_, i) => (
            <circle
              key={i}
              cx={20 + (i * 11) % 160}
              cy={20 + (i * 29) % 120}
              r={1.5}
              opacity={0.35 + (i % 3) * 0.2}
            />
          ))}
        </g>
        <g fill="none" stroke="var(--g)" strokeWidth=".7" opacity=".7">
          <rect x="10" y="120" width="22" height="22" />
          <rect x="36" y="120" width="22" height="22" />
          <rect x="62" y="120" width="22" height="22" />
          <line x1="32" y1="131" x2="36" y2="131" />
          <line x1="58" y1="131" x2="62" y2="131" />
        </g>
      </svg>
    </div>
  );
}

function ProjectCard({ p, lang }: { p: Project; lang: Lang }) {
  const onMove = (e: React.MouseEvent<HTMLElement>) => {
    const el = e.currentTarget;
    const r = el.getBoundingClientRect();
    el.style.setProperty("--mx", ((e.clientX - r.left) / r.width) * 100 + "%");
    el.style.setProperty("--my", ((e.clientY - r.top) / r.height) * 100 + "%");
  };

  const maxStack = p.size === "featured" ? 10 : p.size === "sm" ? 3 : 6;
  const cls = `bento-card${STATUS_CLASS[p.status] ? " " + STATUS_CLASS[p.status] : ""}`;

  const content = (
    <>
      <div className="bento-card__top">
        <div className="bento-card__tag">{t(p.tag, lang)}</div>
        <div className={`bento-card__status${STATUS_CLASS[p.status] ? " " + STATUS_CLASS[p.status] : ""}`}>
          <span className="sd" />
          {p.status}
        </div>
      </div>
      <h3 className="bento-card__title">
        {t(p.title, lang)}
        {p.subtitle && (
          <span className="bento-card__subtitle">{t(p.subtitle, lang)}</span>
        )}
      </h3>
      <p className="bento-card__desc">{t(p.desc, lang)}</p>
      <div className="bento-card__stack">
        {p.stack.slice(0, maxStack).map((s) => (
          <span key={s} className="tag">{s}</span>
        ))}
      </div>
      <div className="bento-card__foot">
        <span>{p.year}</span>
        <span className="bento-card__arrow">{p.link ? "↗" : "→"}</span>
      </div>
      {p.size === "featured" && <FeaturedViz />}
    </>
  );

  if (p.link) {
    return (
      <a className={cls} data-size={p.size} href={p.link} target="_blank" rel="noreferrer" onMouseMove={onMove}>
        {content}
      </a>
    );
  }
  return (
    <div className={cls} data-size={p.size} onMouseMove={onMove}>
      {content}
    </div>
  );
}

export default function Projects() {
  const { theme } = useTheme();
  const isAdmin = theme === "admin";
  const lang: Lang = isAdmin ? "pt" : "en";

  return (
    <main className="projects-page">
      <div className="container">
        <header className="section-header" style={{ paddingTop: "3rem" }}>
          <span className="section-num">02.</span>
          <h1 className="section-title">{isAdmin ? "Projetos" : "Projects"}</h1>
          <div className="section-rule" />
          <span className="t-label">{PROJECTS.length} cards</span>
        </header>
        <div className="proj-bento">
          {PROJECTS.map((p) => (
            <ProjectCard key={p.id} p={p} lang={lang} />
          ))}
        </div>
      </div>
    </main>
  );
}
