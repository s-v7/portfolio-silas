import React from "react";
import {
  FaServer,
  FaNetworkWired,
  FaShieldAlt,
  FaCodeBranch,
  FaCloud,
} from "react-icons/fa";

const sections = [
  {
    title: "Provisionamento e Automação",
    icon: <FaServer className="text-blue-400 text-2xl mr-3" />,
    items: [
      "Ansible: Inventários separados por ambiente (dev, homolog, prod)",
      "Playbooks com roles específicas: Docker, Payara, FastAPI, PostgreSQL",
      "Script cloud-init para provisionamento em cloud ou VM local",
    ],
  },
  {
    title: "Containers e Orquestração",
    icon: <FaNetworkWired className="text-yellow-400 text-2xl mr-3" />,
    items: [
      "Dockerfile customizado para GlassFish",
      "Docker Compose para testes e ambiente local",
      "Kubernetes com PostgreSQL, ELK Stack, serviços EJB e web",
    ],
  },
  {
    title: "Segurança e Testes",
    icon: <FaShieldAlt className="text-red-400 text-2xl mr-3" />,
    items: [
      "OWASP ZAP e Burp Suite com relatórios de segurança",
      "SonarQube para análise estática de código",
      "Checklists e scripts shell para certificados SSL",
    ],
  },
  {
    title: "CI/CD e Automação",
    icon: <FaCodeBranch className="text-green-400 text-2xl mr-3" />,
    items: [
      "Deploy automatizado com Gitea, Webhooks e Bash",
      "Rollback, SCSS build e autodeploy EAR/WAR",
      "Scripts de restore, teste e deploy de certificados",
    ],
  },
  {
    title: "Infraestrutura como Código (IaC)",
    icon: <FaCloud className="text-purple-400 text-2xl mr-3" />,
    items: [
      "Terraform com `main.tf`, `outputs.tf`, `variables.tf`",
      "Base preparada para cloud pública ou ambiente local",
    ],
  },
];

const Infra = () => {
  return (
    <div className="min-h-screen p-6 bg-gray-900 text-white">
      <h1 className="text-4xl font-bold text-center text-teal-400 mb-16">
        Infraestrutura DevOps
      </h1>

      <div className="space-y-10 max-w-4xl mx-auto">
        {sections.map((section, index) => (
          <div
            key={index}
            className="bg-gray-800 p-6 rounded-xl shadow hover:shadow-lg transition"
          >
            <h2 className="text-xl font-bold flex items-center mb-4">
              {section.icon}
              {section.title}
            </h2>
            <ul className="list-disc list-inside pl-2 space-y-1 text-gray-300 text-base leading-relaxed">
              {section.items.map((item, idx) => (
                <li key={idx}>{item}</li>
              ))}
            </ul>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Infra;
