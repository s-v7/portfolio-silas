import type { Role } from "../types/experience";

export const ROLES: Role[] = [
  {
    id: "crea",
    org: "CREA-PI",
    title: {
      en: "Technology & Information Security Advisor",
      pt: "Assessor de Tecnologia e Segurança da Informação",
    },
    location: { en: "Teresina, Brazil", pt: "Teresina, Brasil" },
    period: { en: "05/2024 – Present", pt: "05/2024 – Atual" },
    current: true,
    bullets: [
      {
        en: "Led the technical modernization of a mission-critical enterprise system with ~250k lines of code and 2,300+ classes, evolving from Java EE / GlassFish to Jakarta EE 10 / JDK 17 while keeping production operations running.",
        pt: "Liderança técnica da modernização de um sistema corporativo crítico com ~250 mil linhas de código e 2.300+ classes, evoluindo de Java EE / GlassFish para Jakarta EE 10 / JDK 17 sem interromper a operação em produção.",
      },
      {
        en: "Built APIs and services with NestJS integrated into the Java transactional core, supporting dashboards and business intelligence layers in Angular.",
        pt: "Desenvolvimento de APIs e serviços em NestJS integrados ao núcleo transacional Java, apoiando dashboards e camadas de inteligência de negócio em Angular.",
      },
      {
        en: "Implemented financial integrations involving PIX, dynamic QR Code generation, bank-confirmation webhooks, HMAC signature validation and idempotency controls.",
        pt: "Implementação de integrações financeiras envolvendo PIX, geração de QR Code dinâmico, webhooks bancários, validação de assinatura HMAC e controles de idempotência.",
      },
      {
        en: "Decoupled SOAP integrations using WSDL/wsimport clients into dedicated modules, reducing coupling with the web layer and improving maintainability.",
        pt: "Desacoplamento de integrações SOAP utilizando clientes WSDL/wsimport em módulos dedicados, reduzindo o acoplamento com a camada web e melhorando a manutenibilidade.",
      },
      {
        en: "Worked on requirements gathering, security analysis, vulnerability assessment, process automation and high-volume data routines using Linux and Shell Script.",
        pt: "Atuação em levantamento de requisitos, análise de segurança, avaliação de vulnerabilidades, automação de processos e rotinas de alto volume com Linux e Shell Script.",
      },
    ],
    stack: [
      "Java EE 6+",
      "Jakarta EE 10",
      "JDK 6/7/8/17+",
      "Payara/GlassFish",
      "Spring Boot",
      "NestJS",
      "Angular",
      "PostgreSQL",
      "Linux",
    ],
  },
  {
    id: "edm",
    org: "EDM Software",
    title: {
      en: "Java Full Stack Developer",
      pt: "Desenvolvedor Java Full Stack",
    },
    location: { en: "Florianópolis, Brazil", pt: "Florianópolis, Brasil" },
    period: { en: "05/2022 – 09/2022", pt: "05/2022 – 09/2022" },
    bullets: [
      {
        en: "Developed, maintained and improved Java full stack systems, handling internal support tickets, bug fixes and business-driven enhancements.",
        pt: "Desenvolvimento, manutenção e evolução de sistemas Java full stack, atuando em chamados internos, correções de bugs e melhorias orientadas ao negócio.",
      },
      {
        en: "Integrated systems with SOAP/REST web services and Brazilian fiscal documents such as NF-e and NFC-e.",
        pt: "Integração de sistemas com web services SOAP/REST e documentos fiscais brasileiros como NF-e e NFC-e.",
      },
    ],
    stack: [
      "Java 7/8",
      "JSF/PrimeFaces",
      "JPA",
      "Hibernate",
      "Tomcat",
      "SQL",
      "SOAP/REST",
    ],
  },
  {
    id: "megi9",
    org: "MEGi9 Soluções",
    title: {
      en: "Java Full Stack Developer",
      pt: "Desenvolvedor Java Full Stack",
    },
    location: {
      en: "Jaraguá do Sul, Brazil",
      pt: "Jaraguá do Sul, Brasil",
    },
    period: { en: "07/2017 – 12/2021", pt: "07/2017 – 12/2021" },
    bullets: [
      {
        en: "Developed and maintained enterprise systems for the textile and industrial sector in partnership with Systextil.",
        pt: "Desenvolvimento e manutenção de sistemas corporativos para o setor têxtil e industrial em parceria com a Systextil.",
      },
      {
        en: "Worked on Java business applications using JSF/PrimeFaces, JavaScript, XHTML/CSS and relational databases.",
        pt: "Atuação em aplicações corporativas Java utilizando JSF/PrimeFaces, JavaScript, XHTML/CSS e bancos de dados relacionais.",
      },
      {
        en: "Supported systems integrated with Oracle and MySQL, focusing on stability, bug fixing and continuous improvement of business processes.",
        pt: "Suporte a sistemas integrados com Oracle e MySQL, com foco em estabilidade, correção de bugs e melhoria contínua de processos de negócio.",
      },
    ],
    stack: [
      "Java",
      "JSF/PrimeFaces",
      "JavaScript",
      "XHTML/CSS",
      "Oracle",
      "MySQL",
    ],
  },
];
