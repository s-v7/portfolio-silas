import { useMemo, useState, memo } from "react";


type PillItem =
  | [title: string, description: string]
  | [title: string, description: string[]];

interface CVPillListProps {
  items: PillItem[];
}

interface ExperienceSectionProps {
  title: string;
  meta: string;
  contribs: PillItem[];
}

const HEADLINE =
  "Full Stack Software | DevSecOps | AI | Legacy Modernization | Data & Analytics (Streamlit, PostgreSQL, ML)";

const CONTRIBS_CURRENT: PillItem[] = [
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

const CONTRIBS_HANDPDV: PillItem[] = [
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

const SPECIALIZATIONS: PillItem[] = [
  ["Backend & Architecture", ["Java EE (JPA, JSF, EJB)", "Python", "Node.js"]],
  [
    "Data & Analytics",
    [
      "Streamlit, PostgreSQL, ETL/OCR",
      "Predictive AI and automated classification",
    ],
  ],
  [
    "DevOps & Automation",
    ["Git, Gitea, Docker, Kubernetes", "Terraform, Ansible"],
  ],
  [
    "Security & Blockchain",
    ["Pentest, OWASP, log auditing", "Hyperledger / Ethereum"],
  ],
  [
    "Applied AI",
    [
      "Analysis time prediction",
      "Default-risk scoring",
      "Anomaly detection",
    ],
  ],
  [
    "Modern Frontend",
    ["React", "Angular", "PrimeFaces", "TypeScript", "Streamlit"],
  ],
];

const STACKS: PillItem[] = [
  [
    "Backend",
    ["Java EE", "Python (FastAPI, Flask, Streamlit)", "Node.js"],
  ],
  [
    "Data & AI",
    [
      "PostgreSQL",
      "MongoDB",
      "Pandas",
      "TensorFlow",
      "Scikit-Learn",
      "PyTorch",
    ],
  ],
  [
    "DevOps",
    ["Docker", "Kubernetes", "Terraform", "CI/CD", "Ansible"],
  ],
  [
    "Frontend / UI",
    ["React", "Angular", "PrimeFaces", "TypeScript"],
  ],
  [
    "Security & Blockchain",
    ["OWASP", "Pentest", "API Hardening", "Hyperledger", "Ethereum"],
  ],
];


const CVPillList = memo<CVPillListProps>(({ items }) => {
  return (
    <div className="cv-cols">
      {items.map(([title, desc]) => (
        <div className="cv-pill-card" key={title}>
          <h4>{title}</h4>
          {Array.isArray(desc) ? (
            <ul>
              {desc.map((item) => (
                <li key={item}>{item}</li>
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

const ExperienceSection: React.FC<ExperienceSectionProps> = ({
  title,
  meta,
  contribs,
}) => {
  return (
    <section className="cv-card">
      <div className="cv-row">
        <h2>{title}</h2>
        <span className="cv-meta">{meta}</span>
      </div>
      <CVPillList items={contribs} />
    </section>
  );
};


const CodeCVUser: React.FC = () => {
  const [tab, setTab] = useState<number>(0);

  const about = useMemo(
    () =>
      `I am a Software Engineer specialized in automation, applied AI, and secure modernization of mission-critical systems.

I bridge legacy Java EE platforms with modern AI-driven analytics, DevOps, and Blockchain — always with governance, traceability, and measurable impact.`,
    []
  );

  const onTabKeyDown = (e: React.KeyboardEvent<HTMLDivElement>) => {
    if (e.key === "ArrowRight") setTab((t) => (t + 1) % 2);
    if (e.key === "ArrowLeft") setTab((t) => (t + 1 + 1) % 2);
  };

  return (
    <section className="cv-wrap">
      <header className="cv-header cv-block">
        <h2 className="cv-small-title">Summary</h2>
        <p className="cv-headline">{HEADLINE}</p>
      </header>

      <article className="cv-card cv-span-2">
        <h2>About</h2>
        <p className="cv-pre">{about}</p>
      </article>

      <section className="cv-card">
        <h2>Specializations</h2>
        <CVPillList items={SPECIALIZATIONS} />
      </section>

      <nav
        className="cv-tabs"
        role="tablist"
        aria-label="Experience timeline"
        onKeyDown={onTabKeyDown}
      >
        <button
          type="button"
          className={`cv-tab ${tab === 0 ? "is-active" : ""}`}
          onClick={() => setTab(0)}
        >
          Current
        </button>

        <button
          type="button"
          className={`cv-tab ${tab === 1 ? "is-active" : ""}`}
          onClick={() => setTab(1)}
        >
          Previous
        </button>
      </nav>

      {tab === 0 && (
        <ExperienceSection
          title="Current Experience — CREA-PI"
          meta="Teresina, PI • 2024 – Present"
          contribs={CONTRIBS_CURRENT}
        />
      )}

      {tab === 1 && (
        <ExperienceSection
          title="Previous Experience — HANDpdv"
          meta="Florianópolis, SC • 2022"
          contribs={CONTRIBS_HANDPDV}
        />
      )}

      <section className="cv-card">
        <h2>Technology Stack</h2>
        <CVPillList items={STACKS} />
      </section>
    </section>
  );
};

export default CodeCVUser;

