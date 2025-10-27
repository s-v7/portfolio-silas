import React, { useMemo, useState, memo } from "react";

// High-level positioning headline under "Summary"
const HEADLINE =
  "Full Stack Software | DevSecOps | AI | Legacy Modernization | Data & Analytics (Streamlit, PostgreSQL, ML)";

// Current role contributions / impact
const CONTRIBS_CURRENT = [
  [
    "Intelligent Dashboards (Streamlit + PostgreSQL)",
    "Operational panels for ART review, invoice control, default risk, and auditing — using predictive AI (neural networks) and interactive visual analytics.",
  ],
  [
    "Automated Insights",
    "Real-time alerts and automated reporting for financial and compliance data.",
  ],
  [
    "Legacy Modernization",
    "JDK 6 → 7 → 8 → 11 → 17, SQL/JPA optimization and +40% performance gains in critical systems.",
  ],
  [
    "DevOps & CI/CD",
    "Pipelines with Gitea webhooks, Docker, and Kubernetes for automated deployment and safe rollback.",
  ],
  [
    "Cybersecurity",
    "Anomaly detection in logs using neural models, plus hardening of internal services and infrastructure.",
  ],
  [
    "Blockchain",
    "Smart contracts (Hyperledger / Ethereum) for document and process traceability.",
  ],
];

// Previous role contributions / impact
const CONTRIBS_HANDPDV = [
  [
    "Feature Development",
    "Delivered new features for issuing NF-e and NFC-e with SEFAZ integration.",
  ],
  [
    "Performance Optimization",
    "Improved SQL queries and Hibernate usage, reducing response time and load.",
  ],
  [
    "Security and Cryptography",
    "Applied encryption and data protection to ensure integrity of fiscal transactions.",
  ],
  [
    "Integration and APIs",
    "Worked with SOAP and REST WebServices to connect external services and internal modules.",
  ],
  [
    "Maintenance and Support",
    "Resolved internal tickets and delivered production stability improvements.",
  ],
];

// High-level capability buckets
const SPECIALIZATIONS = [
  [
    "Backend & Architecture",
    ["Java EE (JPA, JSF, EJB)", "Python ([...])", "Node.js"],
  ],
  [
    "Data & Analytics",
    [
      "Streamlit, PostgreSQL, ETL/OCR",
      "Predictive AI and automated classification (neural networks)",
    ],
  ],
  [
    "DevOps & Automation",
    [
      "Git, Gitea, Docker, Kubernetes",
      "Terraform, Ansible",
      "Monitoring and safe rollback",
    ],
  ],
  [
    "Security & Blockchain",
    ["Pentest, OWASP, log auditing", "Hyperledger / Ethereum (Solidity)"],
  ],
  [
    "Applied AI",
    [
      "Analysis time prediction",
      "Default / delinquency risk scoring",
      "Anomaly detection in operational data",
    ],
  ],
  [
    "Modern Frontend",
    ["React", "Angular", "PrimeFaces", "TypeScript", "Streamlit"],
  ],
];

// Stack list, tech-oriented, not pitch
const STACKS = [
  [
    "Backend",
    [
      "Java EE (JPA, JSF, EJB)",
      "Python (FastAPI, Flask, Streamlit)",
      "Node.js",
    ],
  ],
  [
    "Data & AI",
    [
      "PostgreSQL / SQLite",
      "MongoDB",
      "Pandas",
      "TensorFlow",
      "Scikit-Learn",
      "PyTorch",
      "NumPy",
    ],
  ],
  [
    "DevOps",
    [
      "Ansible",
      "CI/CD (Gitea, GitHub Actions)",
      "Docker",
      "N8n",
      "Makefile",
      "Terraform",
      "Kubernetes",
    ],
  ],
  [
    "Frontend / UI",
    ["React", "Angular", "PrimeFaces", "TypeScript", "Bootstrap", "Streamlit"],
  ],
  [
    "Security & Blockchain",
    [
      "Linux",
      "OWASP Top 10",
      "Pentest",
      "API Hardening",
      "Hyperledger",
      "Ethereum (Solidity)",
    ],
  ],
];

// Small presentational component that renders a 2-col list of titled cards
const CVPillList = memo(function CVPillList({ items }) {
  return (
    <div className="cv-cols">
      {items.map(([title, desc]) => (
        <div className="cv-pill-card" key={title}>
          <h4>{title}</h4>
          {Array.isArray(desc) ? (
            <ul>
              {desc.map((it) => (
                <li key={it}>{it}</li>
              ))}
            </ul>
          ) : (
            <p>{desc}</p>
          )}
        </div>
      ))}
    </div>
  );
});

// One experience block (title, location/date meta + bullet cards)
function ExperienceSection({ title, meta, contribs }) {
  return (
    <section className="cv-card">
      <div className="cv-row">
        <h2>{title}</h2>
        <span className="cv-meta">{meta}</span>
      </div>
      <CVPillList items={contribs} />
    </section>
  );
}

export default function CodeCVUser() {
  const [tab, setTab] = useState(0);

  const about = useMemo(
    () =>
      `I am a Software Engineer specialized in automation, applied AI, and secure modernization of mission-critical systems. Since 2016, I have been delivering and evolving corporate and analytical platforms, always prioritizing scalability, robustness, and governance.

I design and deliver intelligent operational dashboards using Streamlit, PostgreSQL, and Machine Learning — applying AI directly inside corporate environments to optimize auditing, ART analysis, invoice management, default-risk scoring, inspection prioritization, and decision-making support.

My work spans two fronts: (1) sustaining and improving critical Java EE systems (JDK 8, PrimeFaces 13, JSF 2.3), and (2) building modern solutions with applied AI, Blockchain, and DevOps — bridging legacy and innovation in a secure, auditable, and efficient way.

Main Specializations

• Development of APIs and corporate applications in Java EE (JPA, JSF, EJB), Python (Flask, Django, Streamlit), and Node.js.
• Interactive analytical dashboards in Streamlit, integrated with PostgreSQL, data ETL, predictive AI, and automated classification using neural networks.
• CI/CD pipelines with Git / Gitea, Docker, Kubernetes, Terraform, and Ansible — automated deployments, monitoring, and safe rollback.
• Security and compliance: pentesting, OWASP, log auditing, and smart contracts (Hyperledger / Ethereum) for traceability and process integrity.
• Predictive models and neural networks for analysis time prediction, default risk, document classification, and anomaly detection in internal systems.
• Responsive dashboards and interfaces built with React, Angular, PrimeFaces, and TypeScript.

Technical Differentials

• Specialist in modernizing corporate JSF systems and embedding AI capabilities (forecasting, classification, anomaly detection) without breaking legacy code.
• Proven experience integrating legacy systems + Streamlit + PostgreSQL + Machine Learning in production with full traceability and governance.
• End-to-end mindset: I can work with Dev, Infra, QA, Audit, and Management and translate operational pain into actionable software.
• Driven by automation, clarity, and measurable impact — especially in auditing, billing, compliance, and risk.`,
    []
  );

  const onTabKeyDown = (e) => {
    if (e.key === "ArrowRight") setTab((t) => (t + 1) % 2);
    if (e.key === "ArrowLeft") setTab((t) => (t + 1 + 1) % 2);
  };

  return (
    <section className="cv-wrap">
      {/* SUMMARY / HEADLINE */}
      <header className="cv-header cv-block" aria-labelledby="headline">
        <h2
          id="headline"
          className="cv-small-title"
          style={{ marginBottom: 6 }}
        >
          Summary
        </h2>
        <p className="cv-headline">{HEADLINE}</p>
      </header>

      {/* ABOUT */}
      <article className="cv-card cv-span-2">
        <h2>About</h2>
        <p className="cv-pre">{about}</p>
      </article>

      {/* SPECIALIZATIONS */}
      <section className="cv-card">
        <h2>Specializations</h2>
        <CVPillList items={SPECIALIZATIONS} />
      </section>

      {/* EXPERIENCE TABS */}
      <nav
        className="cv-tabs"
        role="tablist"
        aria-label="Experience timeline"
        onKeyDown={onTabKeyDown}
      >
        <button
          role="tab"
          id="tab-current"
          aria-controls="panel-current"
          aria-selected={tab === 0}
          className={`cv-tab ${tab === 0 ? "is-active" : ""}`}
          onClick={() => setTab(0)}
          type="button"
        >
          Current
        </button>

        <button
          role="tab"
          id="tab-previous"
          aria-controls="panel-previous"
          aria-selected={tab === 1}
          className={`cv-tab ${tab === 1 ? "is-active" : ""}`}
          onClick={() => setTab(1)}
          type="button"
        >
          Previous
        </button>
      </nav>

      {/* CURRENT EXPERIENCE */}
      <div
        role="tabpanel"
        id="panel-current"
        aria-labelledby="tab-current"
        hidden={tab !== 0}
        className="cv-container"
      >
        <ExperienceSection
          title="Current Experience — CREA-PI"
          meta="Teresina, PI • 2024 – Present"
          contribs={CONTRIBS_CURRENT}
        />
      </div>

      {/* PREVIOUS EXPERIENCE */}
      <div
        role="tabpanel"
        id="panel-previous"
        aria-labelledby="tab-previous"
        hidden={tab !== 1}
        className="cv-container"
      >
        <ExperienceSection
          title="Previous Experience — HANDpdv"
          meta="Florianópolis, SC • May 2022 – Sep 2022"
          contribs={CONTRIBS_HANDPDV}
        />
      </div>

      {/* STACK */}
      <section className="cv-card">
        <h2>Technology Stack</h2>
        <CVPillList items={STACKS} />
      </section>
    </section>
  );
}
