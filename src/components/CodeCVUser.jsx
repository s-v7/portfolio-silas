import React, { useMemo, useState, memo } from "react";

const HEADLINE =
  "Full Stack Software | DevSecOps | AI | Legacy Modernization | Data & Analytics (Streamlit, PostgreSQL, ML)";

const CONTRIBS_ATUAL = [
  [
    "Dashboards Inteligentes (Streamlit + PostgreSQL)",
    "Painéis para ARTs, boletos, inadimplência e auditoria, com IA preditiva (redes neurais) e visualização interativa.",
  ],
  [
    "Automação de Insights",
    "Alertas em tempo real e relatórios automáticos com dados financeiros e operacionais.",
  ],
  [
    "Modernização de Legados",
    "JDK 6 → 7 → 8 → 11 → 17, otimização SQL/JPA e ganhos > 40% de performance.",
  ],
  [
    "DevOps & CI/CD",
    "Pipelines com Gitea Webhooks, Docker e Kubernetes (deploy automatizado e rollback seguro).",
  ],
  [
    "Cibersegurança",
    "Detecção de anomalias em logs via modelos neurais + hardening de servidores.",
  ],
  [
    "Blockchain",
    "Smart contracts (Hyperledger/Ethereum) para rastreabilidade de documentos.",
  ],
];

const CONTRIBS_HANDPDV = [
  [
    "Feature Development",
    "Implemented new features for issuing NF-e and NFC-e, integrating with SEFAZ.",
  ],
  [
    "Performance Optimization",
    "Improved SQL queries and Hibernate integration, reducing system response time.",
  ],
  [
    "Security and Cryptography",
    "Applied encryption and data security techniques to ensure integrity of tax transactions.",
  ],
  [
    "Integration and APIs",
    "Worked with SOAP and REST WebServices, enabling efficient system communication.",
  ],
  [
    "Maintenance and Support",
    "Resolved internal calls and delivered stability improvements.",
  ],
];

const ESPECIALIZACOES = [
  [
    "Backend & Arquitetura",
    ["Java EE (JPA, JSF, EJB)", "Python ([ ... ])", "Node.js"],
  ],
  [
    "Data & Analytics",
    [
      "Streamlit, PostgreSQL, ETL/OCR ...",
      "IA preditiva e classificação (redes neurais)",
    ],
  ],
  [
    "DevOps & Automação",
    [
      "Git, Gitea, Docker, Kubernetes",
      "Terraform, Ansible",
      "Monitoramento e rollback seguro",
    ],
  ],
  [
    "Segurança & Blockchain",
    ["Pentest, OWASP, auditoria de logs", "Hyperledger/Ethereum (Solidity)"],
  ],
  [
    "Inteligência Artificial",
    ["Previsão de tempo de análise", "Inadimplência", "Detecção de anomalias"],
  ],
  [
    "Frontend Moderno",
    ["React", "Angular", "PrimeFaces", "TypeScript", "Streamlit"],
  ],
];

const STACKS = [
  [
    "Backend",
    [
      "Java EE (JPA, JSF, EJB)",
      "Python (FastApi, Flask, Streamlit)",
      "Node.js",
    ],
  ],
  [
    "Data & AI",
    [
      "PostgreSQL/SQLite",
      "MongoDB",
      "Pandas",
      "TensorFlow",
      "Scikit-Learn",
      "PyTorch",
      "Numpy",
    ],
  ],
  [
    "DevOps",
    [
      "Ansible",
      "CI/CD (Gitea,GitHub Actions)",
      "Docker",
      "N8n",
      "Makefile",
      "Terraform",
      "Kubernetes",
    ],
  ],
  [
    "Frontend",
    ["React", "Angular", "PrimeFaces", "TypeScript", "Bootstrap", "Streamlit"],
  ],
  [
    "Segurança & Blockchain",
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
  const [tab, setTab] = useState(0); // 0 = Atual, 1 = Anterior

  const about = useMemo(
    () => `Sou Engenheiro de Software(Autodidata) com foco em inovação, automação e segurança. Desde 2016, atuo no desenvolvimento de sistemas corporativos e analíticos, com ênfase em escalabilidade, robustez e modernização tecnológica.

Atualmente, venho liderando projetos de dashboards inteligentes e interativos com Streamlit, PostgreSQL e Machine Learning, integrando IA em sistemas corporativos para otimizar auditoria, análise de ARTs, boletos, inadimplência e processos fiscais e ... .

Faço sustentação de sistemas críticos em Java EE (JDK 8), PrimeFaces 13 e JSF 2.3, além de iniciativas modernas em IA, Blockchain e DevOps, conectando legado e inovação de forma segura e eficiente.

Minha trajetória vai desde a sustentação de sistemas críticos em Java EE até a criação de soluções modernas com IA aplicada, Blockchain e DevOps, conectando legado e inovação de forma segura e eficiente.

Principais Especializações:
APIs robustas com Java EE (JPA, JSF, EJB), Python (Flask, Django, Streamlit) e Node.js.
Painéis analíticos interativos em Streamlit, integração com PostgreSQL, ETL de dados, IA preditiva e classificação automática com redes neurais.
Pipelines CI/CD com Git, Gitea, Docker, Kubernetes, Terraform e Ansible. Deploys automatizados, monitoramento e rollback seguro.
Pentest, OWASP, auditoria de logs e smart contracts com Hyperledger/Ethereum para rastreabilidade.
Modelos preditivos e redes neurais para previsão de tempo de análise, inadimplência e detecção de anomalias em sistemas corporativos.
Dashboards e UIs responsivas com React, Angular, PrimeFaces e TypeScript.

Diferenciais Técnicos
Especialista em modernização de sistemas corporativos JSF com integração de dashboards de IA.
Experiência comprovada em unir sistemas legados + Streamlit + PostgreSQL + Machine Learning.
Comunicação técnica clara entre Dev, Infra, QA e DevOps.
Foco em automação, documentação e resolução de problemas complexos.
Aberto a oportunidades remotas, internacionais ou presenciais em projetos de alto impacto, inovação e modernização tecnológica.`,
    []
  );

  const savePDF = () => window.print();

  // Acessibilidade: navegação por setas nas abas
  const onTabKeyDown = (e) => {
    if (e.key === "ArrowRight") setTab((t) => (t + 1) % 2);
    if (e.key === "ArrowLeft") setTab((t) => (t + 1 + 1) % 2);
  };

  return (
    <section className="cv-wrap">
      {/* <div className="cv-grid"> */}
      <header className="cv-header cv-block" aria-labelledby="headline">
        <h2
          id="headline"
          className="cv-small-title"
          style={{ marginBottom: 6 }}
        >
          Resumo
        </h2>
        <p className="cv-headline">{HEADLINE}</p>
      </header>
      {/* </div> */}

      <article className="cv-card cv-span-2">
        <h2>Sobre</h2>
        <p className="cv-pre">{about}</p>
      </article>

      {/* Especializações */}
      <section className="cv-card">
        <h2>Especializações</h2>
        <CVPillList items={ESPECIALIZACOES} />
      </section>

      {/* Abas: Experiência Atual / Anterior */}
      <nav
        className="cv-tabs"
        role="tablist"
        aria-label="Experiências"
        onKeyDown={onTabKeyDown}
      >
        <button
          role="tab"
          id="tab-atual"
          aria-controls="panel-atual"
          aria-selected={tab === 0}
          className={`cv-tab ${tab === 0 ? "is-active" : ""}`}
          onClick={() => setTab(0)}
          type="button"
        >
          Atual
        </button>
        <button
          role="tab"
          id="tab-anterior"
          aria-controls="panel-anterior"
          aria-selected={tab === 1}
          className={`cv-tab ${tab === 1 ? "is-active" : ""}`}
          onClick={() => setTab(1)}
          type="button"
        >
          Anterior
        </button>
      </nav>

      <div
        role="tabpanel"
        id="panel-atual"
        aria-labelledby="tab-atual"
        hidden={tab !== 0}
        className="cv-container"
      >
        <ExperienceSection
          title="Experiência Atual — CREA-PI"
          meta="Teresina, PI • 2024 – Atual"
          contribs={CONTRIBS_ATUAL}
        />
      </div>

      <div
        role="tabpanel"
        id="panel-anterior"
        aria-labelledby="tab-anterior"
        hidden={tab !== 1}
        className="cv-container"
      >
        <ExperienceSection
          title="Experiência Anterior — HANDpdv"
          meta="Florianópolis, SC • mai 2022 – set 2022"
          contribs={CONTRIBS_HANDPDV}
        />
      </div>

      {/* Stack utilizada */}
      <section className="cv-card">
        <h2>Stack Utilizada</h2>
        <CVPillList items={STACKS} />
      </section>
    </section>
  );
}
