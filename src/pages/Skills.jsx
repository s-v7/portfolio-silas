import React, { useState } from "react";
import "./Skills.css";

const Skills = () => {
  const [currentPage, setCurrentPage] = useState(1);

  const changePage = (page) => {
    setCurrentPage(page);
  };

  return (
    <div className="skills-container">
      <h1 className="skills-title">Skills</h1>

      {currentPage === 1 && (
        <ul className="skills-list">
          <li>
            ✔️ Backend: Java (JDK 8, 11, 17), EJB, JPA, JSF, PrimeFaces; Python
            (Flask, Django); Node.js
          </li>
          <li>
            ✔️ Frontend: React, Angular, JavaScript, HTML, CSS/SCSS, Bootstrap
          </li>
          <li>✔️ Database: PostgreSQL, MySQL, SQLite, MongoDB</li>
          <li>
            ✔️ DevOps and Automation: Gitea, CI/CD, Webhooks, Docker,
            Kubernetes, Terraform, Ansible
          </li>
          <li>
            ✔️ Security: OWASP, API Hardening, Pentest, Blockchain, Audit and
            Logs
          </li>
          <li>
            ✔️ AI and Machine Learning: TensorFlow, Scikit-Learn, Pandas,
            PyTorch, Anomalies Detection
          </li>
          <li>
            ✔️ IT Governance and Management: ITIL 4, COBIT 2019, BPMN, Systems
            Architecture
          </li>
        </ul>
      )}

      {currentPage === 2 && (
        <div className="skills-differentials">
          <h2 className="skills-subtitle">Diferenciais Técnicos</h2>
          <ul className="skills-list">
            <li>
              Especialista em sistemas JSF corporativos e sua modernização
            </li>
            <li>
              Capacidade de leitura e reestruturação de sistemas com mais de 10
              anos
            </li>
            <li>
              Entendimento profundo de layout, DOM, comportamento JS dinâmico
            </li>
            <li>Experiência prática com projetos de missão crítica</li>
            <li>
              Equilíbrio entre manutenção do legado e uso de boas práticas
              modernas
            </li>
          </ul>
        </div>
      )}

      {/* Paginação */}
      <div className="skills-pagination">
        <button
          onClick={() => changePage(1)}
          className={`skills-page-btn ${currentPage === 1 ? "active" : ""}`}
          disabled={currentPage === 1}
        >
          Página 1
        </button>
        <button
          onClick={() => changePage(2)}
          className={`skills-page-btn ${currentPage === 2 ? "active" : ""}`}
          disabled={currentPage === 2}
        >
          Página 2
        </button>
      </div>
    </div>
  );
};

export default Skills;
