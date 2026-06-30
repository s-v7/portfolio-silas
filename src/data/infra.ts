
export const sections = [
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

