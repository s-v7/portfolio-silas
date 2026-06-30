
export const CAPS = [
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

export const PIPELINE = [
  "DB Extraction",
  "PDF Parsing",
  "Cross-check",
  "Rule Scoring",
  "Guard Filters",
  "LLM Enrichment",
  "Traceable Storage",
];

export const GOV = [
  "Masked inputs only",
  "No legal conclusions generated",
  "Structured JSON outputs",
  "Confidence tagging",
  "Human review flags",
  "Prompt versioning",
];
export const LEARN = [
  "Markov transition weighting",
  "Graph versioning",
  "Rule feedback loop",
  "Reviewer-confirmed corrections",
];
export const DEPLOY = [
  "On-premise compatible",
  "Government cloud ready",
  "API + CLI + Dashboard modes",
  "Designed for CREA federation scale",
  "8 systemd services in production",
  "Cloudflare Tunnel (zero-config TLS)",
];

