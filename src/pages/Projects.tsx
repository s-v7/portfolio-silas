import { useTheme } from "../context/ThemeContext";
import "../styles/pages/Projects.css";
import { PROJECTS } from "../data/projects";
import type { Lang, ProjectStatus } from "../types/project";
import { t } from "../types/project";


const STATUS_CLASS: Record<ProjectStatus, string> = {
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
