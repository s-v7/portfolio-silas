import { useTheme } from "../context/ThemeContext";
import "./Education.css";
const EDU = [
  {
    degree: "Tecnólogo em Segurança da Informação",
    inst: "Universidade Paulista (UNIP)",
    period: "Aug 2024 — Dec 2026 (expected)",
    mode: "Distance Learning",
    status: "In progress",
    topics: [
      "Cryptography",
      "Pentesting",
      "Networks",
      "LGPD",
      "Application Security",
      "Vulnerability Analysis",
    ],
  },
];
const CERTS = [
  { name: "Docker & Kubernetes — Fundamentals", issuer: "Udemy", year: "2023" },
  { name: "Java EE — Enterprise Applications", issuer: "Alura", year: "2022" },
  { name: "Advanced PostgreSQL", issuer: "Dio", year: "2022" },
  { name: "Machine Learning with Python", issuer: "Coursera", year: "2021" },
  { name: "React — Fundamentals & Hooks", issuer: "Rocketseat", year: "2021" },
];
const LANGS = [
  { lang: "Portuguese", level: "Native", pct: 100 },
  {
    lang: "English",
    level: "Intermediate (reading) / Basic (writing)",
    pct: 58,
  },
];
export default function Education() {
  const { theme } = useTheme();
  const isAdmin = theme === "admin";
  return (
    <main className="edu-page">
      <div className="container">
        <header className="section-header" style={{ paddingTop: "3rem" }}>
          <span className="section-num">ED.</span>
          <h1 className="section-title">Education</h1>
          <div className="section-rule" />
        </header>
        <section className="edu-block">
          <p className="block-label t-label">// Academic</p>
          {EDU.map((e) => (
            <div key={e.degree} className="edu-card">
              <div className="edu-card__header">
                <div>
                  <h2 className="edu-card__degree t-heading">{e.degree}</h2>
                  <p className="edu-card__inst">{e.inst}</p>
                </div>
                <div className="edu-card__meta">
                  <span className="tag tag-active">{e.status}</span>
                  <span className="t-label">
                    {e.mode} · {e.period}
                  </span>
                </div>
              </div>
              <div className="edu-card__topics">
                {e.topics.map((t) => (
                  <span key={t} className="tag">
                    {t}
                  </span>
                ))}
              </div>
            </div>
          ))}
        </section>
        <section className="edu-block">
          <p className="block-label t-label">// Certifications</p>
          <div className="certs-list">
            {CERTS.map((c) => (
              <div key={c.name} className="cert-row">
                <span className="cert-name">{c.name}</span>
                <span className="t-label">{c.issuer}</span>
                <span className="t-label cert-year">{c.year}</span>
              </div>
            ))}
          </div>
        </section>
        <section className="edu-block">
          <p className="block-label t-label">// Languages</p>
          <div className="lang-list">
            {LANGS.map((l) => (
              <div key={l.lang} className="lang-row">
                <div className="lang-info">
                  <span className="lang-name t-heading">{l.lang}</span>
                  <span className="t-label">{l.level}</span>
                </div>
                <div className="lang-bar">
                  <div
                    className="lang-bar__fill"
                    style={{ width: `${l.pct}%` }}
                  />
                </div>
                <span className="t-label lang-pct">{l.pct}%</span>
              </div>
            ))}
          </div>
        </section>
      </div>
    </main>
  );
}
