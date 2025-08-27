import React, { useEffect, useMemo, useState, useDeferredValue } from "react";
import { motion, useReducedMotion } from "framer-motion";

/* Ícones inline (sem dependência) */
const IconGithub = (props) => (
  <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" {...props}>
    <path d="M12 .5a12 12 0 0 0-3.79 23.4c.6.11.82-.26.82-.58v-2.02c-3.34.73-4.04-1.61-4.04-1.61-.55-1.39-1.35-1.76-1.35-1.76-1.1-.75.08-.74.08-.74 1.22.09 1.86 1.26 1.86 1.26 1.08 1.85 2.84 1.32 3.53 1.01.11-.8.42-1.32.76-1.62-2.66-.3-5.46-1.33-5.46-5.93 0-1.31.47-2.38 1.25-3.22-.13-.31-.54-1.57.12-3.27 0 0 1.01-.32 3.3 1.23a11.48 11.48 0 0 1 6 0c2.28-1.55 3.29-1.23 3.29-1.23.66 1.7.25 2.96.13 3.27.78.84 1.25 1.91 1.25 3.22 0 4.61-2.8 5.62-5.47 5.92.43.37.81 1.09.81 2.2v3.26c0 .32.21.7.83.58A12 12 0 0 0 12 .5Z" />
  </svg>
);
const IconOpen = (props) => (
  <svg
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    aria-hidden="true"
    {...props}
  >
    <path strokeWidth="2" d="M14 3h7v7M10 14 21 3M21 14v7h-7" />
    <rect x="3" y="10" width="8" height="11" rx="2" strokeWidth="2" />
  </svg>
);

/* DADOS */
const DATA = [
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
      "Java EE/JSF monolith modernization: PrimeFaces 3.1 → 13 (Poseidon), layout fixes, dynamic config panel, legacy compatibility.",
    tecnologias: [
      "Java 8",
      "JSF 2.3",
      "PrimeFaces 13",
      "Poseidon",
      "EJB",
      "EAR",
      "Maven",
    ],
    stacks: ["java", "legacy"],
    link: "https://github.com/s-v7",
  },
];

/* Filtros */
const FILTERS = [
  { key: "all", label: "All" },
  { key: "python", label: "Python" },
  { key: "java", label: "Java" },
  { key: "blockchain", label: "Blockchain" },
  { key: "data", label: "Data/DB" },
  { key: "legacy", label: "Legacy Modernization" },
];

/* Animações */
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

/* utils */
const escapeRegExp = (s) => s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
const highlight = (text, term) => {
  if (!term) return text;
  const re = new RegExp(`(${escapeRegExp(term)})`, "ig");
  const parts = String(text).split(re);
  return parts.map((part, i) =>
    re.test(part) ? (
      <mark key={i} className="rounded px-1 bg-indigo-500/30 text-white">
        {part}
      </mark>
    ) : (
      <span key={i}>{part}</span>
    )
  );
};

export default function Projects() {
  const prefersReduce = useReducedMotion();
  const [query, setQuery] = useState("");
  const [active, setActive] = useState("all");

  /* Estado na URL (q, f) */
  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const q = params.get("q") || "";
    const f = params.get("f") || "all";
    setQuery(q);
    setActive(FILTERS.some((x) => x.key === f) ? f : "all");
  }, []);
  useEffect(() => {
    const params = new URLSearchParams();
    if (query) params.set("q", query);
    if (active !== "all") params.set("f", active);
    const qs = params.toString();
    const url = qs ? `?${qs}` : window.location.pathname;
    window.history.replaceState({}, "", url);
  }, [query, active]);

  /* Debounce com React 18 */
  const dq = useDeferredValue(query);
  const q = dq.trim().toLowerCase();

  /* Filtra por busca + filtro ativo */
  const filteredByQuery = useMemo(() => {
    if (!q) return DATA;
    return DATA.filter((p) => {
      const hay = `${p.nome} ${p.descricao} ${(p.tecnologias || []).join(
        " "
      )} ${(p.stacks || []).join(" ")}`.toLowerCase();
      return hay.includes(q);
    });
  }, [q]);

  const projects = useMemo(() => {
    if (active === "all") return filteredByQuery;
    return filteredByQuery.filter((p) => (p.stacks || []).includes(active));
  }, [filteredByQuery, active]);

  /* Contadores dos filtros (respeitam a busca) */
  const counts = useMemo(() => {
    const base = { all: filteredByQuery.length };
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
          <h2 className="text-2xl md:text-3xl font-extrabold tracking-tight">
            Projects
          </h2>
          <p className="text-sm text-slate-400">
            Filtros por stack + busca em tempo real.
          </p>
        </div>

        <label className="w-full sm:w-80">
          <span className="sr-only">Search projects</span>
          <input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search by name, tech, description…"
            aria-label="Search projects"
            className="w-full rounded-xl border border-white/10 bg-slate-900/60 px-4 py-2 text-sm placeholder:text-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/40"
          />
        </label>
      </div>

      {/* Filtros */}
      <div
        className="mb-2 flex flex-wrap gap-2"
        role="toolbar"
        aria-label="Project filters"
      >
        {FILTERS.map((f) => (
          <button
            key={f.key}
            onClick={() => setActive(f.key)}
            aria-pressed={active === f.key}
            className={
              "rounded-full px-3.5 py-1.5 text-xs font-semibold ring-1 ring-inset transition " +
              (active === f.key
                ? "bg-indigo-500 text-white ring-transparent"
                : "bg-slate-900/60 text-slate-200 ring-white/10 hover:bg-slate-800")
            }
          >
            {f.label}{" "}
            <span className="ml-1 opacity-70">({counts[f.key] ?? 0})</span>
          </button>
        ))}
      </div>

      {/* Contagem de resultados (a11y) */}
      <div className="mb-4 text-xs text-slate-400" aria-live="polite">
        {projects.length} resultado{projects.length === 1 ? "" : "s"}
        {q && (
          <>
            {" "}
            para <span className="font-semibold text-slate-200">“{dq}”</span>
          </>
        )}
        {active !== "all" && (
          <>
            {" "}
            em{" "}
            <span className="font-semibold text-slate-200">
              {FILTERS.find((f) => f.key === active)?.label}
            </span>
          </>
        )}
      </div>

      {/* Grid de Cards */}
      <motion.div
        variants={container}
        initial="hidden"
        animate={prefersReduce ? "show" : "show"}
        className="grid gap-6 sm:grid-cols-2 lg:grid-cols-2"
      >
        {projects.map((p) => (
          <motion.article
            key={p.nome}
            variants={prefersReduce ? undefined : card}
            whileHover={prefersReduce ? undefined : { y: -4 }}
            className="proj-card group relative overflow-hidden rounded-2xl p-5"
          >
            {/* glow sutil */}
            <div className="pointer-events-none absolute inset-0 rounded-2xl ring-0 ring-indigo-500/0 transition group-hover:ring-4 group-hover:ring-indigo-500/20" />

            <header className="mb-2 flex items-start justify-between gap-3">
              <h3 className="text-lg font-semibold text-white leading-snug">
                {highlight(p.nome, q)}
              </h3>

              <div className="flex shrink-0 items-center gap-2">
                <a
                  href={p.link}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="btn-ghost inline-flex items-center gap-1 rounded-lg border border-white/10 bg-slate-900/50 px-2.5 py-1.5 text-xs font-semibold hover:bg-slate-800 transition"
                  title="View on GitHub"
                >
                  <span className="icon-16" aria-hidden>
                    <IconGithub />
                  </span>
                  GitHub
                </a>
                <a
                  href={p.link}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="btn-primary inline-flex items-center gap-1 rounded-lg bg-indigo-500 px-2.5 py-1.5 text-xs font-semibold text-white hover:brightness-110 transition"
                  title="Open project"
                >
                  <span className="icon-16" aria-hidden>
                    <IconOpen />
                  </span>
                  Open
                </a>
              </div>
            </header>

            <p className="mb-3 text-sm leading-relaxed text-slate-300">
              {highlight(p.descricao, q)}
            </p>

            <div className="flex flex-wrap gap-2">
              {(p.tecnologias || []).map((t) => (
                <button
                  key={t}
                  className="chip cursor-pointer rounded-full border border-white/10 bg-slate-900/60 px-2.5 py-1 text-[11px] text-slate-200 hover:bg-slate-800 transition"
                  onClick={() => setQuery(t)}
                  title={`Filtrar por ${t}`}
                >
                  {highlight(t, q)}
                </button>
              ))}
            </div>

            <div className="pointer-events-none absolute inset-x-0 bottom-0 h-1 bg-gradient-to-r from-transparent via-indigo-500/30 to-transparent" />
          </motion.article>
        ))}
      </motion.div>

      {projects.length === 0 && (
        <div className="mt-10 proj-card rounded-2xl p-6 text-center text-slate-400">
          Nada encontrado para{" "}
          <span className="font-semibold text-slate-200">“{dq}”</span>
          {active !== "all" && (
            <>
              {" "}
              com o filtro{" "}
              <span className="font-semibold text-slate-200">
                {FILTERS.find((f) => f.key === active)?.label}
              </span>
            </>
          )}
          .
        </div>
      )}
    </section>
  );
}
