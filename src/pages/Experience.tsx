import { useTheme } from "../context/ThemeContext";

type Lang = "en" | "pt";
type I18n = string | { en: string; pt: string };
const t = (v: I18n, lang: Lang): string =>
  typeof v === "string" ? v : v[lang] ?? v.en;

interface Role {
  id: string;
  org: string;
  title: I18n;
  location: I18n;
  period: I18n;
  current?: boolean;
  bullets: I18n[];
  stack: string[];
}

const ROLES: Role[] = [
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
];

function RoleCard({ r, lang }: { r: Role; lang: Lang }) {
  return (
    <article className="exp-card">
      <div className="exp-card__head">
        <h3 className="exp-card__title">{t(r.title, lang)}</h3>
        {r.current && <span className="exp-card__badge">{lang === "pt" ? "Atual" : "Current"}</span>}
      </div>
      <div className="exp-card__meta">
        <span className="exp-card__org">{r.org}</span>
        <span className="exp-card__dot">·</span>
        <span>{t(r.location, lang)}</span>
        <span className="exp-card__dot">·</span>
        <span>{t(r.period, lang)}</span>
      </div>
      <ul className="exp-card__bullets">
        {r.bullets.map((b, i) => (
          <li key={i}>{t(b, lang)}</li>
        ))}
      </ul>
      <div className="exp-card__stack">
        {r.stack.map((s) => (
          <span key={s} className="tag">{s}</span>
        ))}
      </div>
    </article>
  );
}

export default function Experience() {
  const { theme } = useTheme();
  const isAdmin = theme === "admin";
  const lang: Lang = isAdmin ? "pt" : "en";

  return (
    <main className="exp-page">
      <div className="container">
        <header className="section-header" style={{ paddingTop: "3rem" }}>
          <span className="section-num">03.</span>
          <h1 className="section-title">{isAdmin ? "Experiência" : "Experience"}</h1>
          <div className="section-rule" />
          <span className="t-label">{ROLES.length} {isAdmin ? "cargos" : "roles"}</span>
        </header>
        <div className="exp-list">
          {ROLES.map((r) => (
            <RoleCard key={r.id} r={r} lang={lang} />
          ))}
        </div>
      </div>
    </main>
  );
}
