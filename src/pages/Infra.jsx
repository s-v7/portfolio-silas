import React from "react";
import {
  FaServer,
  FaNetworkWired,
  FaShieldAlt,
  FaCodeBranch,
  FaCogs,
  FaCloud,
} from "react-icons/fa";

const Infra = () => {
  return (
    <div className="min-h-screen p-6 bg-gradient-to-b from-gray-900 via-gray-800 to-gray-700 text-white">
      <h1 className="text-4xl font-bold text-center text-teal-400 mb-8">
        🔧 Infraestrutura DevOps
      </h1>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 text-base leading-relaxed">
        <div className="p-4 bg-gray-800 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-2 flex items-center text-blue-400">
            <FaServer className="mr-2" /> Provisionamento e Automação
          </h2>
          <ul className="list-disc list-inside text-gray-300">
            <li>
              <strong>Ansible:</strong> Inventários separados por ambiente (dev,
              homolog, prod)
            </li>
            <li>
              Playbooks declarativos com roles específicas: Docker, Payara,
              FastAPI, PostgreSQL
            </li>
            <li>
              Script cloud-init para provisionamento rápido em cloud ou VM local
            </li>
          </ul>
        </div>

        <div className="p-4 bg-gray-800 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-2 flex items-center text-yellow-400">
            <FaNetworkWired className="mr-2" /> Containers e Orquestração
          </h2>
          <ul className="list-disc list-inside text-gray-300">
            <li>Dockerfile customizado para GlassFish</li>
            <li>Docker Compose para ambiente local e testes rápidos</li>
            <li>
              Kubernetes com suporte a PostgreSQL, ELK Stack, serviços EJB e web
            </li>
          </ul>
        </div>

        <div className="p-4 bg-gray-800 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-2 flex items-center text-red-400">
            <FaShieldAlt className="mr-2" /> Segurança e Testes
          </h2>
          <ul className="list-disc list-inside text-gray-300">
            <li>OWASP ZAP e Burp Suite com relatórios de segurança</li>
            <li>SonarQube para análise estática de código</li>
            <li>
              Checklists e scripts shell para segurança e certificados SSL
            </li>
          </ul>
        </div>

        <div className="p-4 bg-gray-800 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-2 flex items-center text-green-400">
            <FaCodeBranch className="mr-2" /> CI/CD e Automação
          </h2>
          <ul className="list-disc list-inside text-gray-300">
            <li>Deploy automatizado com Gitea, Webhooks e scripts Bash</li>
            <li>Suporte a rollback, compilações SCSS e autodeploy EAR/WAR</li>
            <li>Scripts para restore, teste e deploy de certificados</li>
          </ul>
        </div>

        <div className="p-4 bg-gray-800 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-2 flex items-center text-purple-400">
            <FaCloud className="mr-2" /> Infraestrutura como Código (IaC)
          </h2>
          <ul className="list-disc list-inside text-gray-300">
            <li>
              Terraform estruturado com `main.tf`, `outputs.tf`, `variables.tf`
            </li>
            <li>Base preparada para cloud pública ou ambiente local</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default Infra;
