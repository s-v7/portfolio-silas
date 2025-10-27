import { desc } from "framer-motion/client";
import React, { useMemo } from "react";

export default function CodeCVUser() {
  const headline =
    "Full Stack Software Engineer | DevSecOps | AI & Blockchain | Legacy Modernization | Data & Analytics (Streamlit, PostgreSQL, ML)";

  const about = useMemo(
    () =>
      `I am a software engineer focused on innovation, automation, and security. Since 2016, I have been working on corporate and analytical systems with emphasis on scalability, robustness, and technological modernization.

Currently, I lead intelligent and interactive dashboard projects using Streamlit, PostgreSQL, and Machine Learning — applying AI to optimize auditing, ART review, invoice tracking, default risk, and fiscal/compliance workflows.

My background bridges the maintenance of critical Java EE systems with modern solutions in applied AI, Blockchain, and DevOps, securely connecting legacy systems with innovation.`,
    []
  );

  const contacts = {
    name: "Silas Vasconcelos Cruz",
    area: "Web · Infra · Data · AI",
    github: "github.com/s-v7",
    linkedin: "linkedin.com/in/s-v7",
    location: "Brazil",
  };

  const specializations = [
    {
      title: "Backend & Architecture",
      items: [
        "Java EE (JPA, JSF, EJB)",
        "Python (Flask/FastAPI, Django, Streamlit)",
        "Node.js",
      ],
    },
    {
      title: "Data & Analytics",
      items: [
        "Streamlit, PostgreSQL, ETL/OCR",
        "Predictive AI and classification (neural networks)",
      ],
    },
    {
      title: "DevOps & Automation",
      items: [
        "Git, Gitea, Docker, Kubernetes",
        "Terraform, Ansible",
        "Monitoring and safe rollback",
      ],
    },
    {
      title: "Security & Blockchain",
      items: [
        "Pentest, OWASP, log auditing",
        "Hyperledger / Ethereum (Solidity)",
      ],
    },
    {
      title: "Applied AI",
      items: [
        "Analysis time prediction",
        "Delinquency / default scoring",
        "Anomaly detection",
      ],
    },
    {
      title: "Modern Frontend",
      items: ["React", "Angular", "PrimeFaces", "TypeScript", "Streamlit"],
    },
  ];

  const contributions = [
    {
      title: "Intelligent Dashboards (Streamlit + PostgreSQL)",
      desc: "Operational panels for ART review, invoices, default prediction and auditing, powered by predictive AI (neural networks) and interactive visual analytics.",
    },
    {
      title: "Automated Insights",
      desc: "Real-time alerts and automated reporting for financial and operational data.",
    },
    {
      title: "Legacy Modernization",
      desc: [
        "JDK 6/8 → 11/17, SQL/JPA tuning and >40% performance gain.",
        "\n",
        "PrimeFaces 3.x → 4.x → 5.x → 7.x → 10.x → 11.x → 13.x",
      ],
    },
    {
      title: "DevOps & CI/CD",
      desc: "Pipelines with Gitea webhooks, Docker and Kubernetes (automated deploy and safe rollback).",
    },
    {
      title: "Cybersecurity",
      desc: "Neural anomaly detection on logs + server hardening.",
    },
    {
      title: "Blockchain",
      desc: "Smart contracts (Hyperledger / Ethereum) for document traceability.",
    },
  ];

  async function copy(text) {
    try {
      await navigator.clipboard.writeText(text);
    } catch {}
  }

  function downloadPDF() {
    window.print();
  }

  return (
    <div className="mx-auto max-w-6xl p-6 text-slate-200">
      {/* HEADER / CONTACT */}
      <section className="rounded-2xl bg-slate-900 shadow-xl ring-1 ring-white/10">
        <div className="flex flex-col md:flex-row items-center gap-6 p-6">
          <div className="h-24 w-24 rounded-full overflow-hidden ring-4 ring-indigo-500">
            <div className="flex h-full w-full items-center justify-center bg-gradient-to-br from-indigo-400 to-cyan-400 text-3xl font-bold text-slate-900">
              SC
            </div>
          </div>

          <div className="flex-1">
            <h1 className="text-3xl font-extrabold text-white">
              {contacts.name}
            </h1>
            <p className="mt-1 text-base text-slate-300">
              Software Engineer — {contacts.area}
            </p>

            <div className="mt-3 flex flex-wrap gap-3 text-sm">
              <a
                href={`https://${contacts.github}`}
                target="_blank"
                rel="noreferrer"
                className="rounded-full bg-slate-800 px-3 py-1 hover:bg-slate-700"
              >
                {contacts.github}
              </a>
              <a
                href={`https://${contacts.linkedin}`}
                target="_blank"
                rel="noreferrer"
                className="rounded-full bg-slate-800 px-3 py-1 hover:bg-slate-700"
              >
                {contacts.linkedin}
              </a>
              <span className="rounded-full bg-slate-800 px-3 py-1">
                {contacts.location}
              </span>
            </div>

            <div className="mt-4 flex flex-wrap gap-2 text-xs">
              {[
                "Python",
                "PostgreSQL",
                "Streamlit",
                "Docker",
                "Kubernetes",
                "React",
                "ML",
              ].map((tag) => (
                <span
                  key={tag}
                  className="rounded-full bg-indigo-500/15 px-2.5 py-1 text-indigo-300 ring-1 ring-inset ring-indigo-500/20"
                >
                  {tag}
                </span>
              ))}
            </div>
          </div>

          <div className="flex flex-col gap-2 w-full md:w-auto">
            <button
              onClick={() => copy(headline)}
              className="rounded-xl bg-indigo-600 px-4 py-2 text-sm font-semibold text-white hover:bg-indigo-500"
            >
              Copy Headline
            </button>
            <button
              onClick={downloadPDF}
              className="rounded-xl bg-slate-800 px-4 py-2 text-sm font-semibold text-slate-200 ring-1 ring-white/10 hover:bg-slate-700"
            >
              Save as PDF
            </button>
          </div>
        </div>
      </section>

      {/* ABOUT + HEADLINE */}
      <section className="mt-6 grid gap-6 md:grid-cols-3">
        <div className="md:col-span-2 rounded-2xl bg-slate-900 p-6 shadow ring-1 ring-white/10">
          <h2 className="text-xl font-bold text-white">About</h2>
          <p className="mt-3 whitespace-pre-line text-slate-300 leading-relaxed">
            {about}
          </p>
          <button
            onClick={() => copy(about)}
            className="mt-4 rounded-lg bg-slate-800 px-3 py-2 text-xs font-semibold text-slate-200 ring-1 ring-white/10 hover:bg-slate-700"
          >
            Copy Summary
          </button>
        </div>

        <div className="rounded-2xl bg-slate-900 p-6 shadow ring-1 ring-white/10">
          <h3 className="text-sm font-semibold uppercase tracking-wide text-slate-400">
            Headline
          </h3>
          <p className="mt-2 text-slate-200">{headline}</p>
        </div>
      </section>

      {/* SPECIALIZATIONS */}
      <section className="mt-6 rounded-2xl bg-slate-900 p-6 shadow ring-1 ring-white/10">
        <h2 className="text-xl font-bold text-white">Specializations</h2>
        <div className="mt-4 grid gap-4 md:grid-cols-2">
          {specializations.map((block) => (
            <div
              key={block.title}
              className="rounded-xl bg-slate-800/50 p-4 ring-1 ring-white/10"
            >
              <h4 className="font-semibold text-slate-100">{block.title}</h4>
              <ul className="mt-2 list-disc pl-5 text-slate-300">
                {block.items.map((it) => (
                  <li key={it}>{it}</li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </section>

      {/* EXPERIENCE */}
      <section className="mt-6 rounded-2xl bg-slate-900 p-6 shadow ring-1 ring-white/10">
        <div className="flex items-center justify-between">
          <h2 className="text-xl font-bold text-white">
            Current Experience — CREA-PI
          </h2>
          <span className="text-sm text-slate-400">
            Teresina, PI • 2024 – Present
          </span>
        </div>

        <div className="mt-3 grid gap-3 md:grid-cols-2">
          {contributions.map((c) => (
            <div
              key={c.title}
              className="rounded-xl bg-slate-800/50 p-4 ring-1 ring-white/10"
            >
              <h4 className="font-semibold text-slate-100">{c.title}</h4>
              <p className="mt-1 text-slate-300">{c.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* STACK */}
      <section className="mt-6 rounded-2xl bg-slate-900 p-6 shadow ring-1 ring-white/10">
        <h2 className="text-xl font-bold text-white">Tech Stack</h2>
        <div className="mt-4 grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {[
            {
              k: "Backend",
              v: [
                "Java EE (JPA, JSF, EJB)",
                "Python (Flask, Streamlit, Django)",
                "Node.js",
              ],
            },
            {
              k: "Data & AI",
              v: [
                "PostgreSQL",
                "Pandas",
                "TensorFlow",
                "Scikit-Learn",
                "PyTorch",
                "NumPy",
              ],
            },
            {
              k: "DevOps",
              v: [
                "Docker",
                "Kubernetes",
                "CI/CD (Gitea, Jenkins, GitHub Actions)",
                "Terraform",
                "Ansible",
              ],
            },
            {
              k: "Frontend",
              v: [
                "Streamlit",
                "React",
                "Angular",
                "PrimeFaces",
                "TypeScript",
                "Bootstrap",
              ],
            },
            {
              k: "Security & Blockchain",
              v: [
                "OWASP Top 10",
                "Pentest",
                "API Hardening",
                "Hyperledger",
                "Ethereum (Solidity)",
              ],
            },
          ].map((grp) => (
            <div
              key={grp.k}
              className="rounded-xl bg-slate-800/50 p-4 ring-1 ring-white/10"
            >
              <h4 className="font-semibold text-slate-100">{grp.k}</h4>
              <ul className="mt-2 list-disc pl-5 text-slate-300">
                {grp.v.map((item) => (
                  <li key={item}>{item}</li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </section>

      <footer className="mt-8 pb-4 text-center text-xs text-slate-500">
        Final layout inspired by production dashboards (dark cards, responsive
        grid, actionable CTAs).
      </footer>
    </div>
  );
}
