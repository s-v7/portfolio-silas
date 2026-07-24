import React from "react";
import {
  FaCloud,
  FaCodeBranch,
  FaNetworkWired,
  FaServer,
  FaShieldAlt,
} from "react-icons/fa";

const sections = [
  {
    title: "Infraestrutura e servidores",
    icon: <FaServer className="mr-3 text-teal-400" />,
    items: [
      "Linux, administração de serviços e automação operacional",
      "Docker, containers e ambientes reproduzíveis",
      "Payara Server e aplicações Jakarta EE corporativas",
    ],
  },
  {
    title: "Redes e integração",
    icon: <FaNetworkWired className="mr-3 text-teal-400" />,
    items: [
      "Nginx como proxy reverso e gateway de aplicações",
      "Integração entre APIs, serviços internos e sistemas legados",
      "Diagnóstico de conectividade, rotas e disponibilidade",
    ],
  },
  {
    title: "Segurança",
    icon: <FaShieldAlt className="mr-3 text-teal-400" />,
    items: [
      "Autenticação, autorização e controle de acesso",
      "Gestão de segredos e proteção de credenciais",
      "Auditoria, hardening e práticas DevSecOps",
    ],
  },
  {
    title: "Entrega e versionamento",
    icon: <FaCodeBranch className="mr-3 text-teal-400" />,
    items: [
      "Git, GitHub e estratégias de branches",
      "CI/CD e validações automatizadas",
      "Builds, testes e implantação controlada",
    ],
  },
  {
    title: "Cloud e observabilidade",
    icon: <FaCloud className="mr-3 text-teal-400" />,
    items: [
      "Cloudflare Workers, Pages e serviços distribuídos",
      "Monitoramento, métricas, logs e rastreabilidade",
      "Arquiteturas preparadas para nuvem e escalabilidade",
    ],
  },
];

const Infra = () => {
  return (
    <div className="min-h-screen p-6 bg-gray-900 text-white">
      <h1 className="text-4xl font-bold text-center text-teal-400 mb-16">Infraestrutura DevOps</h1>

      <div className="space-y-10 max-w-4xl mx-auto">
        {sections.map((section) => (
          <div key={section.title} className="bg-gray-800 p-6 rounded-xl shadow hover:shadow-lg transition">
            <h2 className="text-xl font-bold flex items-center mb-4">
              {section.icon}
              {section.title}
            </h2>
            <ul className="list-disc list-inside pl-2 space-y-1 text-gray-300 text-base leading-relaxed">
              {section.items.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Infra;
