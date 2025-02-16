import React from "react";
import "./Skills.css";

const Skills = () => {
  return (
    <div className="skills-container">
      <h1 className="skills-title">Skills</h1>
      <ul className="skills-list">
        <li>✔️ Backend: Java(JDK(s) 8,11,17),(EJB, JPA, JSF, PrimeFaces), Python(Flask, Django), Node.js</li>
        <li>✔️ Frontend: React, Angular, JavaScript...</li>
        <li>✔️ Database: PostgreSQL, MySQL, SQLite, MongoDB</li>
        <li>✔️ DevOps and Automation: Gitea, CI/CD, Webhooks, Docker, Kubernetes, Terraform, Ansible</li>
        <li>✔️ Security: OWASP, API Hardening, Pentest, Blockchain, Audit and Logs</li>
        <li>✔️ AI and Machine Learning: TensorFlow, Scikit-Learn, Pandas, PyTorch, Anomalies... </li>
        <li>✔️ IT Governance and Management: ITIL 4, COBIT 2019, BPMN, Systems Architecture</li>
      </ul>
    </div>
  );
};

export default Skills;

