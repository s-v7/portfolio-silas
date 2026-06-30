
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
        en: "Technical lead for the modernization of an enterprise system (~250k lines, 2,300+ classes) from Java EE 8 / GlassFish to Jakarta EE 10 / JDK 17, keeping the transactional system running in production.",
        pt: "Liderança técnica da modernização de um sistema corporativo (~250 mil linhas, 2.300+ classes) de Java EE 8 / GlassFish para Jakarta EE 10 / JDK 17, mantendo o sistema transacional em produção.",
      },
      {
        en: "Built a modern service layer in NestJS and Angular dashboards, integrated with the Java transactional core (intelligence/analytics layer + transactional layer).",
        pt: "Desenvolvimento de uma camada de serviços moderna em NestJS e dashboards em Angular, integrada ao núcleo transacional Java (camada de inteligência/analytics + camada transacional).",
      },
      {
        en: "Implemented a financial module with PIX: dynamic QR Code generation and a bank-confirmation webhook with signature validation (HMAC) and idempotency.",
        pt: "Implementação de módulo financeiro com PIX: geração de QR Code dinâmico e webhook de confirmação bancária com validação de assinatura (HMAC) e idempotência.",
      },
      {
        en: "Decoupled SOAP integrations (WSDL/wsimport clients) into a dedicated module, reducing coupling with the web layer.",
        pt: "Desacoplamento de integrações SOAP (clientes via WSDL/wsimport) em módulo dedicado, reduzindo o acoplamento com a camada web.",
      },
      {
        en: "Requirements gathering, security analysis, vulnerability assessment and mitigation; process automation and high-volume data routines with Shell Script.",
        pt: "Levantamento de requisitos, análise de segurança, avaliação e mitigação de vulnerabilidades; automação de processos e rotinas de alto volume com Shell Script.",
      },
    ],
    stack: ["Jakarta EE 10", "JDK 17", "Payara", "NestJS", "Angular", "PostgreSQL", "Linux"],
  },
  {
    id: "edm",
    org: "EDM Software",
    title: { en: "Java Full Stack Developer", pt: "Desenvolvedor Java Full Stack" },
    location: { en: "Florianópolis, Brazil", pt: "Florianópolis, Brasil" },
    period: { en: "05/2022 – 09/2022", pt: "05/2022 – 09/2022" },
    bullets: [
      {
        en: "Development, maintenance and bug resolution across Java full stack systems; handled internal support tickets and shipped improvements.",
        pt: "Desenvolvimento, manutenção e resolução de bugs em sistemas Java full stack; atendimento de chamados internos e entrega de melhorias.",
      },
      {
        en: "Integration with web services (SOAP/REST) and fiscal documents (NF-e, NFC-e).",
        pt: "Integração com web services (SOAP/REST) e documentos fiscais (NF-e, NFC-e).",
      },
    ],
    stack: ["Java 7/8", "JSF/PrimeFaces", "JPA", "Hibernate", "Tomcat", "SQL"],
  },
  {
    id: "megi9",
    org: "MEGi9 Soluções",
    title: { en: "Java Full Stack Developer", pt: "Desenvolvedor Java Full Stack" },
    location: {
      en: "Jaraguá do Sul, Santa Catarina, Brazil",
      pt: "Jaraguá do Sul, Santa Catarina, Brasil",
    },
    period: { en: "07/2017 – 12/2021", pt: "07/2017 – 12/2021" },
    bullets: [
      {
        en: "Developed and maintained enterprise systems for the textile/industrial sector in partnership with Systextil.",
        pt: "Desenvolvimento e manutenção de sistemas corporativos para o setor têxtil/industrial em parceria com a Systextil.",
      },
      {
        en: "Worked on Java-based business applications using JSF/PrimeFaces, JavaScript, XHTML/CSS and relational databases.",
        pt: "Atuação em aplicações Java usando JSF/PrimeFaces, JavaScript, XHTML/CSS e bancos relacionais.",
      },
      {
        en: "Supported systems integrated with Oracle and MySQL databases, focusing on stability, bug fixes and business process improvements.",
        pt: "Suporte a sistemas integrados com Oracle e MySQL, com foco em estabilidade, correção de bugs e melhoria de processos.",
      },
    ],
    stack: ["Java", "JSF/PrimeFaces", "JavaScript", "XHTML/CSS", "Oracle", "MySQL"],
  },
];

