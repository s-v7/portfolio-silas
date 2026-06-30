import { useTheme } from "../context/ThemeContext";
import "../styles/pages/Education.css";

import { EDU, CERTS, LANGS } from "../data/education";


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
          <div className="cert-grid">
            {CERTS.map((c) => (
              <article key={c.name} className="cert-card">
                <div>
                  <h3 className="cert-card__title">{c.name}</h3>
                  <p className="cert-card__issuer">{c.issuer}</p>
                </div>
                <div className="cert-card__meta">
                  <span>{c.year}</span>
                  {c.hours && <span>{c.hours}</span>}
                </div>
              </article>
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
