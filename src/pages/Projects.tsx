import {
  useMemo,
  useState,
  useDeferredValue,
} from "react";
import { motion, useReducedMotion, cubicBezier } from "framer-motion";


interface Project {
  id: string;
  name: string;
  description: string;
  stacks: string[];
  technologies: string[];
  category: "Enterprise" | "Gov" | "AI" | "Research" | "Legacy";
  visibility: "public" | "private";
  repoUrl?: string;
  highlights: string[];
}

const IconGithub: React.FC<React.SVGProps<SVGSVGElement>> = (props) => (
  <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" {...props}>
    <path d="M12 .5a12 12 0 0 0-3.79 23.4c.6.11.82-.26.82-.58v-2.02c-3.34.73-4.04-1.61-4.04-1.61-.55-1.39-1.35-1.76-1.35-1.76-1.1-.75.08-.74.08-.74 1.22.09 1.86 1.26 1.86 1.26 1.08 1.85 2.84 1.32 3.53 1.01.11-.8.42-1.32.76-1.62-2.66-.3-5.46-1.33-5.46-5.93 0-1.31.47-2.38 1.25-3.22-.13-.31-.54-1.57.12-3.27 0 0 1.01-.32 3.3 1.23a11.48 11.48 0 0 1 6 0c2.28-1.55 3.29-1.23 3.29-1.23.66 1.7.25 2.96.13 3.27.78.84 1.25 1.91 1.25 3.22 0 4.61-2.8 5.62-5.47 5.92.43.37.81 1.09.81 2.2v3.26c0 .32.21.7.83.58A12 12 0 0 0 12 .5Z" />
  </svg>
);

const DATA: Project[] = [
  {
    id: "creapi-ai",
    name: "CREAPI – Intelligent Analytics Platform",
    description: "Intelligent analytics platform for a public-sector organization, integrating predictive models, OCR + NLP pipelines and statistical monitoring.",
    category: "AI",
    visibility: "private",
    stacks: ["python", "ai", "data"],
    technologies: ["FastAPI", "PostgreSQL", "OCR", "NLP", "DVC"],
    highlights: []
  },
  {
    id: "ru-confea",
    name: "RU ↔ CONFEA Integration Platform",
    description: "Official integration platform automating SRP flows between CONFEA and CREAs using APIs and webhooks.",
    category: "Gov",
    visibility: "private",
    stacks: ["java", "enterprise"],
    technologies: ["Jakarta EE", "Webhooks", "OpenAPI", "PostgreSQL"],
    highlights: []
  },
  {
    id: "crea-legacy",
    name: "Sistema CREA-PI (Legacy → Modern)",
    description: "Modernization of a Java EE / JSF monolith: PrimeFaces 3 → 13, layout refactor and dynamic configuration panels.",
    category: "Legacy",
    visibility: "private",
    stacks: ["java", "legacy"],
    technologies: ["Java", "JSF", "PrimeFaces", "Maven"],
    highlights: []
  },
  {
    id: "audit-system",
    name: "Audit System",
    description: "Full-stack auditing system built with Flask and Angular, focusing on traceability and modular architecture.",
    category: "Enterprise",
    visibility: "public",
    stacks: ["python", "data"],
    technologies: ["Python", "Flask", "Angular", "SQLite"],
    repoUrl: "https://github.com/s-v7/sistema-auditoria",
    highlights: []
  },
  {
    id: "blockchain-crea",
    name: "Blockchain CREA-PI",
    description: "Blockchain-based network for secure CREA-PI data integration and traceability.",
    category: "Research",
    visibility: "public",
    stacks: ["blockchain"],
    technologies: ["Blockchain", "Node.js"],
    repoUrl: "https://github.com/s-v7/blockchain-crea-pi",
    highlights: []
  },
  {
    id: "registration-works",
    name: "Registration Tracking Works",
    description: "Robust system for managing civil construction works data with modular backend and relational databases.",
    category: "Enterprise",
    visibility: "public",
    stacks: ["python", "data"],
    technologies: ["Python", "Angular", "PostgreSQL", "SQLite"],
    repoUrl: "https://github.com/s-v7/CadastroRastreamentoObras",
    highlights: []
  },
];


const FILTERS = [
  { key: "all", label: "All" },
  { key: "Gov", label: "Government" },
  { key: "Enterprise", label: "Enterprise" },
  { key: "AI", label: "AI & Data" },
  { key: "Legacy", label: "Legacy Modernization" },
  { key: "Research", label: "Research" },
];



const card = {
  hidden: { opacity: 0, y: 18, scale: 0.98 },
  show: {
    opacity: 1,
    y: 0,
    scale: 1,
    transition: { duration: 0.35, ease: cubicBezier(0.25, 0.46, 0.45, 0.94) },
  },
};


const Projects: React.FC = () => {
  const prefersReduce = useReducedMotion();
  const [query, setQuery] = useState("");
  const [active, setActive] = useState("all");

  const dq = useDeferredValue(query);
  const q = dq.trim().toLowerCase();

  const filtered = useMemo(() => {
    let base = DATA;

    if (active !== "all") {
      base = base.filter(p => p.category === active);
    }

    if (!q) return base;

    return base.filter(p =>
      `${p.name} ${p.description} ${p.technologies.join(" ")}`.toLowerCase().includes(q)
    );
  }, [q, active]);

  return (
    <section className="mx-auto max-w-6xl px-4 py-8 text-slate-200">
      {/* Header */}
      <div className="mb-6 flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <h2 className="text-3xl font-extrabold">Projects</h2>
          <p className="text-sm text-slate-400">
            Selected professional and research projects.
          </p>
        </div>

        <input
          value={query}
          onChange={e => setQuery(e.target.value)}
          placeholder="Search projects…"
          className="w-full sm:w-80 rounded-xl border border-white/10 bg-slate-900/60 px-4 py-2 text-sm focus:ring-2 focus:ring-indigo-500/40"
        />
      </div>

      {/* Grid */}
      <motion.div
        initial="hidden"
        animate="show"
        className="grid gap-6"
        style={{ gridTemplateColumns: "repeat(auto-fit, minmax(420px, 1fr))" }}
      >

        {filtered.map(p => (
          <motion.article
            key={p.id}
            variants={prefersReduce ? undefined : card}
            whileHover={prefersReduce ? undefined : { y: -4 }}
            className="ds-card ds-card-pad ds-card-proj"
          >

            <header className="mb-2 flex items-center justify-between gap-3">
              <h3 className="text-lg font-semibold">{p.name}</h3>
              {p.visibility === "private" && (
                <span className="ds-chip text-xs">Private</span>
              )}
            </header>

            <p className="mb-3 text-sm text-slate-300">
              {p.description}
            </p>

            <div className="mb-4 flex flex-wrap gap-2">
              {p.technologies.map(t => (
                <span key={t} className="ds-chip text-xs">
                  {t}
                </span>
              ))}
            </div>

            <div className="flex items-center justify-between">
              <span className="text-xs text-slate-400">
                {p.category}
              </span>

              {p.repoUrl ? (
                <a href={p.repoUrl} target="_blank" rel="noopener noreferrer">
                  <IconGithub className="h-4 w-4" />
                </a>
              ) : (
                <span className="text-xs text-slate-500">
                  Private repository
                </span>
              )}
            </div>
          </motion.article>
        ))}
      </motion.div>
    </section>
  );
};


export default Projects;

