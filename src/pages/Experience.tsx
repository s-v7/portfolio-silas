import { useTheme } from "../context/ThemeContext";
import "../styles/pages/Experience.css";
import { ROLES } from "../data/experience";
import type { Lang, Role } from "../types/experience";
import { t } from "../types/experience";

function RoleCard({ r, lang }: { r: Role; lang: Lang }) {
  return (
    <article className="exp-card">
      <div className="exp-card__head">
        <h3 className="exp-card__title">{t(r.title, lang)}</h3>
        {r.current && <span className="exp-card__badge">{lang === "pt" ? "Atual" : "Current"}</span>}
      </div>
      <div className="exp-card__meta">
        <span className="exp-card__org">{r.org}</span>
        <span className="exp-card__dot">·</span>
        <span>{t(r.location, lang)}</span>
        <span className="exp-card__dot">·</span>
        <span>{t(r.period, lang)}</span>
      </div>
      <ul className="exp-card__bullets">
        {r.bullets.map((b, i) => (
          <li key={i}>{t(b, lang)}</li>
        ))}
      </ul>
      <div className="exp-card__stack">
        {r.stack.map((s) => (
          <span key={s} className="tag">{s}</span>
        ))}
      </div>
    </article>
  );
}

export default function Experience() {
  const { theme } = useTheme();
  const isAdmin = theme === "admin";
  const lang: Lang = isAdmin ? "pt" : "en";

  return (
    <main className="exp-page">
      <div className="container">
        <header className="section-header" style={{ paddingTop: "3rem" }}>
          <span className="section-num">03.</span>
          <h1 className="section-title">{isAdmin ? "Experiência" : "Experience"}</h1>
          <div className="section-rule" />
          <span className="t-label">{ROLES.length} {isAdmin ? "cargos" : "roles"}</span>
        </header>
        <div className="exp-list">
          {ROLES.map((r) => (
            <RoleCard key={r.id} r={r} lang={lang} />
          ))}
        </div>
      </div>
    </main>
  );
}
