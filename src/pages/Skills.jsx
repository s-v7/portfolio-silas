import React, { useState } from "react";

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
          <li>✔️ Databases: PostgreSQL, MySQL, SQLite, MongoDB</li>
          <li>
            ✔️ DevOps & Automation: Gitea, CI/CD, Webhooks, Docker, Kubernetes,
            Terraform, Ansible
          </li>
          <li>
            ✔️ Security: OWASP, API Hardening, Pentesting, Blockchain,
            Compliance & Audit Logging
          </li>
          <li>
            ✔️ AI & Machine Learning: TensorFlow, Scikit-Learn, Pandas, PyTorch,
            Anomaly Detection
          </li>
          <li>
            ✔️ IT Governance & Management: ITIL 4, COBIT 2019, BPMN, Systems
            Architecture
          </li>
        </ul>
      )}

      {currentPage === 2 && (
        <div className="skills-differentials">
          <h2 className="skills-subtitle">Technical Differentials</h2>
          <ul className="skills-list">
            <li>Specialist in modernizing large JSF-based corporate systems</li>
            <li>
              Able to read, refactor and evolve systems that are 10+ years old
              without breaking mission-critical flows
            </li>
            <li>
              Deep understanding of layout, DOM behavior, and dynamic/custom JS
            </li>
            <li>
              Hands-on experience with production systems under high compliance
              and public/financial accountability
            </li>
            <li>
              Strong balance between maintaining stability in legacy platforms
              and introducing modern best practices (automation, observability,
              security, AI augmentation)
            </li>
          </ul>
        </div>
      )}

      {/* Pagination */}
      <div className="skills-pagination">
        <button
          onClick={() => changePage(1)}
          className={`skills-page-btn ${currentPage === 1 ? "active" : ""}`}
          disabled={currentPage === 1}
        >
          Page 1
        </button>
        <button
          onClick={() => changePage(2)}
          className={`skills-page-btn ${currentPage === 2 ? "active" : ""}`}
          disabled={currentPage === 2}
        >
          Page 2
        </button>
      </div>
    </div>
  );
};

export default Skills;
