import { useTheme } from "../context/ThemeContext";
import "./ArtEngine.css";

const CAPS = [
  {
    title: "Deterministic audit rules",
    sub: "Reproducible, no LLM drift on rule decisions",
  },
  {
    title: "DB × PDF divergence detection",
    sub: "Cross-validates database records against PDF documents",
  },
  { title: "Sensitive data masking", sub: "PII stripped before any LLM call" },
  {
    title: "DAG execution pipeline",
    sub: "Directed acyclic graph — full audit traceability",
  },
  {
    title: "LLM semantic enrichment",
    sub: "OpenAI + Claude with strict governance guardrails",
  },
  {
    title: "Human-in-the-loop learning",
    sub: "Auditor feedback improves classification over time",
  },
  {
    title: "Multi-CREA scalable model",
    sub: "Designed for CONFEA federation — 27 regional councils",
  },
  {
    title: "Blockchain traceability",
    sub: "SHA-256 chained records, 1.1M+ ARTs stored on-chain",
  },
];

const PIPELINE = [
  "DB Extraction",
  "PDF Parsing",
  "Cross-check",
  "Rule Scoring",
  "Guard Filters",
  "LLM Enrichment",
  "Traceable Storage",
];

const GOV = [
  "Masked inputs only",
  "No legal conclusions generated",
  "Structured JSON outputs",
  "Confidence tagging",
  "Human review flags",
  "Prompt versioning",
];
const LEARN = [
  "Markov transition weighting",
  "Graph versioning",
  "Rule feedback loop",
  "Reviewer-confirmed corrections",
];
const DEPLOY = [
  "On-premise compatible",
  "Government cloud ready",
  "API + CLI + Dashboard modes",
  "Designed for CREA federation scale",
  "8 systemd services in production",
  "Cloudflare Tunnel (zero-config TLS)",
];

export default function ArtEngine() {
  const { theme } = useTheme();
  const isAdmin = theme === "admin";
  return (
    <main className="art-page">
      <div className="container">
        <header className="section-header" style={{ paddingTop: "3rem" }}>
          <span className="section-num">AI.</span>
          <h1 className="section-title">ART Intelligence Engine</h1>
          <div className="section-rule" />
        </header>

        <p
          style={{
            fontFamily: isAdmin ? "var(--mono)" : "Inter, sans-serif",
            fontSize: "13px",
            color: "var(--text-dim)",
            maxWidth: "680px",
            lineHeight: "1.7",
            marginBottom: "2rem",
          }}
        >
          {isAdmin
            ? "Motor de IA institucional para auditoria de ARTs (Anotações de Responsabilidade Técnica). Combina regras determinísticas, cross-check DB×PDF, normalização semântica e enriquecimento LLM com governança estrita."
            : "Institutional AI engine for auditing Engineering Responsibility Records (ARTs). Combines deterministic rules, DB×PDF cross-validation, semantic normalization and LLM enrichment under strict governance guardrails."}
        </p>

        {/* Stats */}
        <div className="art-stats">
          {[
            ["1.1M+", "ARTs on-chain"],
            ["224", "Municípios PI"],
            ["8", "Serviços systemd"],
            ["2,045", "ARTs/second"],
          ].map(([n, l]) => (
            <div className="art-stat" key={l}>
              <div className="art-stat__n">{n}</div>
              <div className="art-stat__l">{l}</div>
            </div>
          ))}
        </div>

        {/* Pipeline */}
        <div className="section-header" style={{ marginBottom: "1rem" }}>
          <span className="section-num">—</span>
          <h2 className="section-title" style={{ fontSize: "1.1rem" }}>
            {isAdmin ? "Pipeline de execução" : "Execution pipeline"}
          </h2>
        </div>
        <div className="pipeline">
          {PIPELINE.map((s, i) => (
            <>
              <div
                key={s}
                className={`pipe-step${i === 4 || i === 5 ? " pipe-step--accent" : ""}`}
              >
                {s}
              </div>
              {i < PIPELINE.length - 1 && (
                <span className="pipe-arrow" key={`a${i}`}>
                  →
                </span>
              )}
            </>
          ))}
        </div>

        {/* Capabilities */}
        <div className="section-header" style={{ marginBottom: "1rem" }}>
          <span className="section-num">—</span>
          <h2 className="section-title" style={{ fontSize: "1.1rem" }}>
            {isAdmin ? "Capacidades" : "Core capabilities"}
          </h2>
        </div>
        <div className="art-caps">
          {CAPS.map((c) => (
            <div className="art-cap" key={c.title}>
              <span className="art-cap__check" aria-hidden="true">
                ✔
              </span>
              <div>
                <div className="art-cap__title">{c.title}</div>
                <div className="art-cap__sub">{c.sub}</div>
              </div>
            </div>
          ))}
        </div>

        {/* Governance + Learning */}
        <div className="art-blocks">
          <div className="art-block">
            <p className="art-block__label t-label">// LLM Governance Model</p>
            <ul className="art-block__list">
              {GOV.map((g) => (
                <li key={g}>{g}</li>
              ))}
            </ul>
          </div>
          <div className="art-block">
            <p className="art-block__label t-label">// Continuous Learning</p>
            <ul className="art-block__list">
              {LEARN.map((l) => (
                <li key={l}>{l}</li>
              ))}
            </ul>
          </div>
        </div>

        {/* Deployment */}
        <div className="art-deploy">
          <div className="art-deploy__col">
            <p className="art-deploy__label t-label">// Deployment model</p>
            <div className="art-deploy__items">
              {DEPLOY.map((d) => (
                <span key={d} className="tag">
                  {d}
                </span>
              ))}
            </div>
          </div>
          <div className="art-deploy__col">
            <p className="art-deploy__label t-label">// Stack</p>
            <div className="art-deploy__items">
              {[
                "FastAPI",
                "LangGraph",
                "OpenAI",
                "Claude API",
                "PostgreSQL",
                "PostGIS",
                "Cloudflare",
                "systemd",
              ].map((t) => (
                <span key={t} className="tag tag-active">
                  {t}
                </span>
              ))}
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
