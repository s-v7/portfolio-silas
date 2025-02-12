import React from "react";
import "./Skills.css"; // Certifique-se de importar os estilos corretamente

const Skills = () => {
  return (
    <div className="skills-container">
      <h1 className="skills-title">Habilidades</h1>
      <ul className="skills-list">
        <li>✔️ Backend: Java(JDK(s) 8,11,17),(EJB, JPA, JSF, PrimeFaces), Python(Flask, Django), Node.js</li>
        <li>✔️ Frontend: React, Angular, JavaScript</li>
        <li>✔️ Banco de Dados: PostgreSQL, MySQL, SQLite, MongoDB</li>
        <li>✔️ DevOps e Automação: Gitea, CI/CD, Webhooks, Docker, Kubernetes, Terraform, Ansible</li>
        <li>✔️ Segurança: OWASP, Hardening de APIs, Pentest, Blockchain, Auditoria e Logs</li>
        <li>✔️ IA e Machine Learning: TensorFlow, Scikit-Learn, Pandas, PyTorch, Anomalias... </li>
        <li>✔️ Governança e Gestão de TI: ITIL 4, COBIT 2019, BPMN, Arquitetura de Sistemas</li>
      </ul>
    </div>
  );
};

export default Skills;

