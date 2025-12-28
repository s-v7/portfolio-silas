import {
  useEffect,
  useMemo,
  useState,
  useDeferredValue,
  ChangeEvent,
} from "react";
import { motion, useReducedMotion } from "framer-motion";


interface Project {
  nome: string;
  descricao: string;
  tecnologias?: string[];
  stacks?: string[];
  link: string;
}

interface Filter {
  key: string;
  label: string;
}


const IconGithub: React.FC<React.SVGProps<SVGSVGElement>> = (props) => (
  <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" {...props}>
    <path d="M12 .5a12 12 0 0 0-3.79 23.4c.6.11.82-.26.82-.58v-2.02c-3.34.73-4.04-1.61-4.04-1.61-.55-1.39-1.35-1.76-1.35-1.76-1.1-.75.08-.74.08-.74 1.22.09 1.86 1.26 1.86 1.26 1.08 1.85 2.84 1.32 3.53 1.01.11-.8.42-1.32.76-1.62-2.66-.3-5.46-1.33-5.46-5.93 0-1.31.47-2.38 1.25-3.22-.13-.31-.54-1.57.12-3.27 0 0 1.01-.32 3.3 1.23a11.48 11.48 0 0 1 6 0c2.28-1.55 3.29-1.23 3.29-1.23.66 1.7.25 2.96.13 3.27.78.84 1.25 1.91 1.25 3.22 0 4.61-2.8 5.62-5.47 5.92.43.37.81 1.09.81 2.2v3.26c0 .32.21.7.83.58A12 12 0 0 0 12 .5Z" />
  </svg>
);

const IconOpen: React.FC<React.SVGProps<SVGSVGElement>> = (props) => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" {...props}>
    <path strokeWidth="2" d="M14 3h7v7M10 14 21 3M21 14v7h-7" />
    <rect x="3" y="10" width="8" height="11" rx="2" strokeWidth="2" />
  </svg>
);


const DATA: Project[] = [
  {
    nome: "Audit System",
    descricao: "Application for auditing using Flask and Angular.",
    tecnologias: ["Python", "Angular", "SQLite"],
    stacks: ["python", "data"],
    link: "https://github.com/s-v7/sistema-auditoria",
  },
  {
    nome: "Blockchain CREA-PI",
    descricao: "Blockchain network for CREA-PI data integration.",
    tecnologias: ["Blockchain", "Node.js"],
    stacks: ["blockchain", "node"],
    link: "https://github.com/s-v7/blockchain-crea-pi",
  },
  {
    nome: "RegistrationTrackingWorks",
    descricao:
      "Robust and modular system for managing information related to civil construction works.",
    tecnologias: ["Python", "Angular", "PostgreSQL", "SQLite"],
    stacks: ["python", "data"],
    link: "https://github.com/s-v7/CadastroRastreamentoObras",
  },
  {
    nome: "Sistema CREA-PI (Legacy → Modern)",
    descricao:
      "Java EE / JSF monolith modernization: PrimeFaces 3 → 13, layout refactor, dynamic config panels.",
    tecnologias: ["Java", "JSF", "PrimeFaces", "EJB", "Maven"],
    stacks: ["java", "legacy"],
    link: "https://github.com/s-v7",
  },
];

const FILTERS: Filter[] = [
  { key: "all", label: "All" },
  { key: "python", label: "Python" },
  { key: "java", label: "Java" },
  { key: "blockchain", label: "Blockchain" },
  { key: "data", label: "Data/DB" },
  { key: "legacy", label: "Legacy Modernization" },
];


const container = {
  hidden: { opacity: 0 },
  show: { opacity: 1, transition: { staggerChildren: 0.08 } },
};

const card = {
  hidden: { opacity: 0, y: 18, scale: 0.98 },
  show: {
    opacity: 1,
    y: 0,
    scale: 1,
    transition: { duration: 0.35, ease: "easeOut" },
  },
};


const escapeRegExp = (value: string): string =>
  value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");

const highlight = (text: string, term: string): React.ReactNode => {
  if (!term) return text;

  const re = new RegExp(`(${escapeRegExp(term)})`, "ig");
  return String(text)
    .split(re)
    .map((part, i) =>
      re.test(part) ? (
        <mark
          key={i}
          className="rounded px-1 bg-indigo-500/30 text-white"
        >
          {part}
        </mark>
      ) : (
        <span key={i}>{part}</span>
      )
    );
};


const Projects: React.FC = () => {
  const prefersReduce = useReducedMotion();
  const [query, setQuery] = useState<string>("");
  const [active, setActive] = useState<string>("all");

  /* URL sync */
  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const q = params.get("q") ?? "";
    const f = params.get("f") ?? "all";
    setQuery(q);
    setActive(FILTERS.some((x) => x.key === f) ? f : "all");
  }, []);

  useEffect(() => {
    const params = new URLSearchParams();
    if (query) params.set("q", query);
    if (active !== "all") params.set("f", active);
    const qs = params.toString();
    window.history.replaceState({}, "", qs ? `?${qs}` : location.pathname);
  }, [query, active]);

  const dq = useDeferredValue(query);
  const q = dq.trim().toLowerCase();

  const filteredByQuery = useMemo(() => {
    if (!q) return DATA;
    return DATA.filter((p) =>
      `${p.nome} ${p.descricao} ${(p.tecnologias || []).join(" ")} ${(p.stacks ||
        []).join(" ")}`.toLowerCase().includes(q)
    );
  }, [q]);

  const projects = useMemo(() => {
    if (active === "all") return filteredByQuery;
    return filteredByQuery.filter((p) =>
      (p.stacks || []).includes(active)
    );
  }, [filteredByQuery, active]);

  const counts = useMemo(() => {
    const base: Record<string, number> = { all: filteredByQuery.length };
    FILTERS.filter((f) => f.key !== "all").forEach((f) => {
      base[f.key] = filteredByQuery.filter((p) =>
        (p.stacks || []).includes(f.key)
      ).length;
    });
    return base;
  }, [filteredByQuery]);

  return (
    <section className="mx-auto max-w-6xl px-4 py-8 text-slate-200">
      {/* Header */}
      <div className="mb-5 flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <h2 className="text-2xl md:text-3xl font-extrabold">Projects</h2>
          <p className="text-sm text-slate-400">
            Real-time search and stack-based filtering.
          </p>
        </div>

        <input
          value={query}
          onChange={(e: ChangeEvent<HTMLInputElement>) =>
            setQuery(e.target.value)
          }
          placeholder="Search by name, tech, description…"
          className="w-full sm:w-80 rounded-xl border border-white/10 bg-slate-900/60 px-4 py-2 text-sm focus:ring-2 focus:ring-indigo-500/40"
        />
      </div>

      {/* Filters */}
      <div className="mb-3 flex flex-wrap gap-2" role="toolbar">
        {FILTERS.map((f) => (
          <button
            key={f.key}
            onClick={() => setActive(f.key)}
            aria-pressed={active === f.key}
            className={`rounded-full px-3 py-1.5 text-xs font-semibold ring-1 transition ${
              active === f.key
                ? "bg-indigo-500 text-white ring-transparent"
                : "bg-slate-900/60 ring-white/10 hover:bg-slate-800"
            }`}
          >
            {f.label} <span className="opacity-70">({counts[f.key] ?? 0})</span>
          </button>
        ))}
      </div>

      {/* Grid */}
      <motion.div
        variants={container}
        initial="hidden"
        animate="show"
        className="grid gap-6 sm:grid-cols-2"
      >
        {projects.map((p) => (
          <motion.article
            key={p.nome}
            variants={prefersReduce ? undefined : card}
            whileHover={prefersReduce ? undefined : { y: -4 }}
            className="proj-card rounded-2xl p-5"
          >
            <header className="mb-2 flex justify-between gap-3">
              <h3 className="text-lg font-semibold">
                {highlight(p.nome, q)}
              </h3>
              <div className="flex gap-2">
                <a href={p.link} target="_blank" rel="noopener noreferrer">
                  <IconGithub className="h-4 w-4" />
                </a>
                <a href={p.link} target="_blank" rel="noopener noreferrer">
                  <IconOpen className="h-4 w-4" />
                </a>
              </div>
            </header>

            <p className="mb-3 text-sm text-slate-300">
              {highlight(p.descricao, q)}
            </p>

            <div className="flex flex-wrap gap-2">
              {(p.tecnologias || []).map((t) => (
                <button
                  key={t}
                  onClick={() => setQuery(t)}
                  className="rounded-full border border-white/10 bg-slate-900/60 px-2 py-1 text-[11px]"
                >
                  {highlight(t, q)}
                </button>
              ))}
            </div>
          </motion.article>
        ))}
      </motion.div>
    </section>
  );
};

export default Projects;

