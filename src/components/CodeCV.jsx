import { desc } from "framer-motion/client";
import React, { useMemo } from "react";
import "./code-cv.css";

// Versão final estilizada — igual às imagens 3 e 4 (cards, dark UI, botões bem visíveis)
export default function CodeCVUser() {
  const headline =
    "Full Stack Software Engineer | DevSecOps | AI & Blockchain | Legacy Modernization | Data & Analytics (Streamlit, PostgreSQL, ML)";

  const about = useMemo(
    () =>
      `Sou engenheiro de software com foco em inovação, automação e segurança. Desde 2016, atuo no desenvolvimento de sistemas corporativos e analíticos, com ênfase em escalabilidade, robustez e modernização tecnológica.\n\nAtualmente, lidero projetos de dashboards inteligentes e interativos utilizando Streamlit, PostgreSQL e Machine Learning — aplicando IA para otimizar auditoria, ARTs, boletos, inadimplência e processos fiscais.\n\nMinha trajetória combina a sustentação de sistemas críticos em Java EE com soluções modernas em IA aplicada, Blockchain e DevOps, conectando legado + inovação de forma segura e eficiente.`,
    []
  );

  const contatos = {
    nome: "Silas Vasconcelos Cruz",
    area: "Web · Infra · Data · AI",
    github: "github.com/s-v7",
    linkedin: "linkedin.com/in/s-v7",
    local: "Brasil",
  };

  const especializacoes = [
    {
      titulo: "Backend & Arquitetura",
      itens: [
        "Java EE (JPA, JSF, EJB)",
        "Python (Flask/FastApi, Django, Streamlit)",
        "Node.js",
      ],
    },
    {
      titulo: "Data & Analytics",
      itens: [
        "Streamlit, PostgreSQL, ETL/OCR",
        "IA preditiva e classificação (redes neurais)",
      ],
    },
    {
      titulo: "DevOps & Automação",
      itens: [
        "Git, Gitea, Docker, Kubernetes",
        "Terraform, Ansible",
        "Monitoramento e rollback seguro",
      ],
    },
    {
      titulo: "Segurança & Blockchain",
      itens: [
        "Pentest, OWASP, auditoria de logs",
        "Hyperledger/Ethereum (Solidity)",
      ],
    },
    {
      titulo: "Inteligência Artificial",
      itens: [
        "Previsão de tempo de análise",
        "Inadimplência",
        "Detecção de anomalias",
      ],
    },
    {
      titulo: "Frontend Moderno",
      itens: ["React", "Angular", "PrimeFaces", "TypeScript", "Streamlit"],
    },
  ];

  const contribuicoes = [
    {
      titulo: "Dashboards Inteligentes (Streamlit + PostgreSQL)",
      desc: "Painéis para ARTs, boletos, inadimplência e auditoria, com IA preditiva (redes neurais) e visualização interativa.",
    },
    {
      titulo: "Automação de Insights",
      desc: "Alertas em tempo real e relatórios automáticos com dados financeiros e operacionais.",
    },
    {
      titulo: "Modernização de Legados",
      desc: [
        "JDK 6/8 → 11/17, otimização SQL/JPA e ganho > 40% de performance.",
        "\n",
        "PrimeFaces-3.1 para 4.x -> 5.y -> 7.z, 10.t, 11.u, 13.v.0",
      ],
    },
    {
      titulo: "DevOps & CI/CD",
      desc: "Pipelines com Gitea Webhooks, Docker e Kubernetes (deploy automatizado e rollback seguro).",
    },
    {
      titulo: "Cibersegurança",
      desc: "Modelo neural para anomalias em logs + hardening de servidores.",
    },
    {
      titulo: "Blockchain",
      desc: "Smart contracts (Hyperledger/Ethereum) para rastreabilidade de documentos.",
    },
  ];

  async function copy(text) {
    try {
      await navigator.clipboard.writeText(text);
    } catch {}
  }

  function downloadPDF() {
    window.print();
  }

  return (
    <div className="mx-auto max-w-6xl p-6 text-slate-200">
      {/* Header */}
      <section className="rounded-2xl bg-slate-900 shadow-xl ring-1 ring-white/10">
        <div className="flex flex-col md:flex-row items-center gap-6 p-6">
          <div className="h-24 w-24 rounded-full overflow-hidden ring-4 ring-indigo-500">
            <div className="flex h-full w-full items-center justify-center bg-gradient-to-br from-indigo-400 to-cyan-400 text-3xl font-bold text-slate-900">
              SC
            </div>
          </div>
          <div className="flex-1">
            <h1 className="text-3xl font-extrabold text-white">
              {contatos.nome}
            </h1>
            <p className="mt-1 text-base text-slate-300">
              Software Engineer — {contatos.area}
            </p>

            <div className="mt-3 flex flex-wrap gap-3 text-sm">
              <a
                href={`https://${contatos.github}`}
                target="_blank"
                rel="noreferrer"
                className="rounded-full bg-slate-800 px-3 py-1 hover:bg-slate-700"
              >
                {contatos.github}
              </a>
              <a
                href={`https://${contatos.linkedin}`}
                target="_blank"
                rel="noreferrer"
                className="rounded-full bg-slate-800 px-3 py-1 hover:bg-slate-700"
              >
                {contatos.linkedin}
              </a>
              <span className="rounded-full bg-slate-800 px-3 py-1">
                {contatos.local}
              </span>
            </div>

            <div className="mt-4 flex flex-wrap gap-2 text-xs">
              {[
                "Python",
                "PostgreSQL",
                "Streamlit",
                "Docker",
                "Kubernetes",
                "React",
                "ML",
              ].map((tag) => (
                <span
                  key={tag}
                  className="rounded-full bg-indigo-500/15 px-2.5 py-1 text-indigo-300 ring-1 ring-inset ring-indigo-500/20"
                >
                  {tag}
                </span>
              ))}
            </div>
          </div>
          <div className="flex flex-col gap-2 w-full md:w-auto">
            <button
              onClick={() => copy(headline)}
              className="rounded-xl bg-indigo-600 px-4 py-2 text-sm font-semibold text-white hover:bg-indigo-500"
            >
              Copiar Headline
            </button>
            <button
              onClick={downloadPDF}
              className="rounded-xl bg-slate-800 px-4 py-2 text-sm font-semibold text-slate-200 ring-1 ring-white/10 hover:bg-slate-700"
            >
              Salvar PDF
            </button>
          </div>
        </div>
      </section>

      {/* About + Headline */}
      <section className="mt-6 grid gap-6 md:grid-cols-3">
        <div className="md:col-span-2 rounded-2xl bg-slate-900 p-6 shadow ring-1 ring-white/10">
          <h2 className="text-xl font-bold text-white">Sobre</h2>
          <p className="mt-3 whitespace-pre-line text-slate-300 leading-relaxed">
            {about}
          </p>
          <button
            onClick={() => copy(about)}
            className="mt-4 rounded-lg bg-slate-800 px-3 py-2 text-xs font-semibold text-slate-200 ring-1 ring-white/10 hover:bg-slate-700"
          >
            Copiar Resumo
          </button>
        </div>
        <div className="rounded-2xl bg-slate-900 p-6 shadow ring-1 ring-white/10">
          <h3 className="text-sm font-semibold uppercase tracking-wide text-slate-400">
            Headline
          </h3>
          <p className="mt-2 text-slate-200">{headline}</p>
        </div>
      </section>

      {/* Especializações */}
      <section className="mt-6 rounded-2xl bg-slate-900 p-6 shadow ring-1 ring-white/10">
        <h2 className="text-xl font-bold text-white">Especializações</h2>
        <div className="mt-4 grid gap-4 md:grid-cols-2">
          {especializacoes.map((bloco) => (
            <div
              key={bloco.titulo}
              className="rounded-xl bg-slate-800/50 p-4 ring-1 ring-white/10"
            >
              <h4 className="font-semibold text-slate-100">{bloco.titulo}</h4>
              <ul className="mt-2 list-disc pl-5 text-slate-300">
                {bloco.itens.map((it) => (
                  <li key={it}>{it}</li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </section>

      {/* Experiência */}
      <section className="mt-6 rounded-2xl bg-slate-900 p-6 shadow ring-1 ring-white/10">
        <div className="flex items-center justify-between">
          <h2 className="text-xl font-bold text-white">
            Experiência Atual — CREA‑PI
          </h2>
          <span className="text-sm text-slate-400">
            Teresina, PI • 2024 – Atual
          </span>
        </div>
        <div className="mt-3 grid gap-3 md:grid-cols-2">
          {contribuicoes.map((c) => (
            <div
              key={c.titulo}
              className="rounded-xl bg-slate-800/50 p-4 ring-1 ring-white/10"
            >
              <h4 className="font-semibold text-slate-100">{c.titulo}</h4>
              <p className="mt-1 text-slate-300">{c.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Stack */}
      <section className="mt-6 rounded-2xl bg-slate-900 p-6 shadow ring-1 ring-white/10">
        <h2 className="text-xl font-bold text-white">Stack Utilizada</h2>
        <div className="mt-4 grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {[
            {
              k: "Backend",
              v: [
                "Java EE (JPA, JSF, EJB)",
                "Python (Flask, Streamlit, Django)",
                "Node.js",
              ],
            },
            {
              k: "Data & AI",
              v: [
                "PostgreSQL",
                "Pandas",
                "TensorFlow",
                "Scikit‑Learn",
                "PyTorch",
                "Numpy",
              ],
            },
            {
              k: "DevOps",
              v: [
                "Docker",
                "Kubernetes",
                "CI/CD (Gitea, Jenkins, GitHub Actions)",
                "Terraform",
                "Ansible",
              ],
            },
            {
              k: "Frontend",
              v: [
                "Streamlit",
                "React",
                "Angular",
                "PrimeFaces",
                "TypeScript",
                "Bootstrap",
              ],
            },
            {
              k: "Segurança & Blockchain",
              v: [
                "OWASP Top 10",
                "Pentest",
                "API Hardening",
                "Hyperledger",
                "Ethereum (Solidity)",
              ],
            },
          ].map((grp) => (
            <div
              key={grp.k}
              className="rounded-xl bg-slate-800/50 p-4 ring-1 ring-white/10"
            >
              <h4 className="font-semibold text-slate-100">{grp.k}</h4>
              <ul className="mt-2 list-disc pl-5 text-slate-300">
                {grp.v.map((item) => (
                  <li key={item}>{item}</li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </section>

      <footer className="mt-8 pb-4 text-center text-xs text-slate-500">
        Layout final inspirado nas imagens (cards escuros, grid responsivo,
        botões destacados).
      </footer>
    </div>
  );
}

// import React, { useMemo } from "react";

// /**
//  * Componente de apresentação para usuário final (sem cara de código).
//  * - Layout em cartões, tipografia clara, foco no conteúdo.
//  * - Botões para copiar Headline e Resumo, e para gerar PDF (window.print()).
//  * - Sem dependências externas além de Tailwind (classes utilitárias).
//  */
// export default function CodeCVUser() {
//   const headline =
//     "Full Stack Software Engineer | DevSecOps | AI & Blockchain | Legacy Modernization | Data & Analytics (Streamlit, PostgreSQL, ML)";

//   const about = useMemo(
//     () =>
//       `Sou engenheiro de software com foco em inovação, automação e segurança. Desde 2016, atuo no desenvolvimento de sistemas corporativos e analíticos, com ênfase em escalabilidade, robustez e modernização tecnológica.\n\nAtualmente, lidero projetos de dashboards inteligentes e interativos utilizando Streamlit, PostgreSQL e Machine Learning — aplicando IA para otimizar auditoria, ARTs, boletos, inadimplência e processos fiscais.\n\nMinha trajetória combina a sustentação de sistemas críticos em Java EE com soluções modernas em IA aplicada, Blockchain e DevOps, conectando legado + inovação de forma segura e eficiente.`,
//     []
//   );

//   const contatos = {
//     nome: "Silas Vasconcelos Cruz",
//     area: "Web · Infra · Data · AI",
//     email: "silas@email.com",
//     github: "github.com/s-v7",
//     linkedin: "linkedin.com/in/s-v7",
//     local: "Brasil",
//   };

//   const especializacoes = [
//     {
//       titulo: "Backend & Arquitetura",
//       itens: [
//         "Java EE (JPA, JSF, EJB)",
//         "Python (Flask, Django, Streamlit)",
//         "Node.js",
//       ],
//     },
//     {
//       titulo: "Data & Analytics",
//       itens: [
//         "Streamlit, PostgreSQL, ETL",
//         "IA preditiva e classificação (redes neurais)",
//       ],
//     },
//     {
//       titulo: "DevOps & Automação",
//       itens: [
//         "Git, Gitea, Docker, Kubernetes",
//         "Terraform, Ansible",
//         "Monitoramento e rollback seguro",
//       ],
//     },
//     {
//       titulo: "Segurança & Blockchain",
//       itens: [
//         "Pentest, OWASP, auditoria de logs",
//         "Hyperledger/Ethereum (Solidity)",
//       ],
//     },
//     {
//       titulo: "Inteligência Artificial",
//       itens: [
//         "Previsão de tempo de análise",
//         "Inadimplência",
//         "Detecção de anomalias",
//       ],
//     },
//     {
//       titulo: "Frontend Moderno",
//       itens: ["React", "Angular", "PrimeFaces", "TypeScript", "Streamlit"],
//     },
//   ];

//   const contribuicoes = [
//     {
//       titulo: "Dashboards Inteligentes (Streamlit + PostgreSQL)",
//       desc: "Painéis para ARTs, boletos, inadimplência e auditoria, com IA preditiva (redes neurais) e visualização interativa.",
//     },
//     {
//       titulo: "Automação de Insights",
//       desc: "Alertas em tempo real e relatórios automáticos com dados financeiros e operacionais.",
//     },
//     {
//       titulo: "Modernização de Legados",
//       desc: "JDK 6/8 → 11/17, otimização SQL/JPA e ganho > 40% de performance.",
//     },
//     {
//       titulo: "DevOps & CI/CD",
//       desc: "Pipelines com Gitea Webhooks, Docker e Kubernetes (deploy automatizado e rollback seguro).",
//     },
//     {
//       titulo: "Cibersegurança",
//       desc: "Modelo neural para anomalias em logs + hardening de servidores.",
//     },
//     {
//       titulo: "Blockchain",
//       desc: "Smart contracts (Hyperledger/Ethereum) para rastreabilidade de documentos.",
//     },
//   ];

//   async function copy(text) {
//     try {
//       await navigator.clipboard.writeText(text);
//     } catch (e) {
//       console.warn("Falha ao copiar", e);
//     }
//   }

//   function downloadPDF() {
//     window.print();
//   }

//   return (
//     <div className="mx-auto max-w-5xl p-4 md:p-8 text-slate-200">
//       {/* Header */}
//       <section className="rounded-2xl bg-slate-900/60 backdrop-blur shadow-xl ring-1 ring-white/10">
//         <div className="flex flex-col md:flex-row items-center gap-6 p-6">
//           <div className="h-24 w-24 rounded-full bg-gradient-to-br from-indigo-400 to-cyan-400 ring-4 ring-slate-800 overflow-hidden">
//             {/* Se tiver avatar, substitua por <img src=... className="h-full w-full object-cover"/> */}
//             <div className="flex h-full w-full items-center justify-center text-3xl font-bold text-slate-900">
//               SC
//             </div>
//           </div>
//           <div className="flex-1">
//             <h1 className="text-2xl md:text-3xl font-extrabold tracking-tight text-white">
//               {contatos.nome}
//             </h1>
//             <p className="mt-1 text-sm md:text-base text-slate-300">
//               Software Engineer — {contatos.area}
//             </p>

//             <div className="mt-3 flex flex-wrap gap-3 text-sm">
//               <a
//                 href={`https://${contatos.github}`}
//                 className="rounded-full bg-slate-800 px-3 py-1 hover:bg-slate-700 transition"
//                 target="_blank"
//                 rel="noreferrer"
//               >
//                 {contatos.github}
//               </a>
//               <a
//                 href={`https://${contatos.linkedin}`}
//                 className="rounded-full bg-slate-800 px-3 py-1 hover:bg-slate-700 transition"
//                 target="_blank"
//                 rel="noreferrer"
//               >
//                 {contatos.linkedin}
//               </a>
//               <span className="rounded-full bg-slate-800 px-3 py-1">
//                 {contatos.local}
//               </span>
//             </div>

//             <div className="mt-4 flex flex-wrap gap-2 text-xs">
//               {[
//                 "Python",
//                 "PostgreSQL",
//                 "Streamlit",
//                 "Docker",
//                 "Kubernetes",
//                 "React",
//                 "ML",
//               ].map((tag) => (
//                 <span
//                   key={tag}
//                   className="rounded-full bg-indigo-500/15 px-2.5 py-1 text-indigo-300 ring-1 ring-inset ring-indigo-500/20"
//                 >
//                   {tag}
//                 </span>
//               ))}
//             </div>
//           </div>

//           <div className="flex flex-col gap-2 w-full md:w-auto">
//             <button
//               onClick={() => copy(headline)}
//               className="rounded-xl bg-indigo-500/90 px-4 py-2 text-sm font-semibold text-white hover:bg-indigo-500"
//             >
//               Copiar Headline
//             </button>
//             <button
//               onClick={downloadPDF}
//               className="rounded-xl bg-slate-800 px-4 py-2 text-sm font-semibold text-slate-200 ring-1 ring-white/10 hover:bg-slate-700"
//             >
//               Salvar PDF
//             </button>
//           </div>
//         </div>
//       </section>

//       {/* About */}
//       <section className="mt-6 grid gap-6 md:grid-cols-3">
//         <div className="md:col-span-2 rounded-2xl bg-slate-900/60 p-6 shadow ring-1 ring-white/10">
//           <h2 className="text-xl font-bold text-white">Sobre</h2>
//           <p className="mt-3 whitespace-pre-line leading-relaxed text-slate-300">
//             {about}
//           </p>
//           <div className="mt-4">
//             <button
//               onClick={() => copy(about)}
//               className="rounded-lg bg-slate-800 px-3 py-2 text-xs font-semibold text-slate-200 ring-1 ring-white/10 hover:bg-slate-700"
//             >
//               Copiar Resumo
//             </button>
//           </div>
//         </div>

//         <div className="rounded-2xl bg-slate-900/60 p-6 shadow ring-1 ring-white/10">
//           <h3 className="text-sm font-semibold uppercase tracking-wide text-slate-400">
//             Headline
//           </h3>
//           <p className="mt-2 text-slate-200">{headline}</p>
//         </div>
//       </section>

//       {/* Especializações */}
//       <section className="mt-6 rounded-2xl bg-slate-900/60 p-6 shadow ring-1 ring-white/10">
//         <h2 className="text-xl font-bold text-white">Especializações</h2>
//         <div className="mt-4 grid gap-4 md:grid-cols-2">
//           {especializacoes.map((bloco) => (
//             <div
//               key={bloco.titulo}
//               className="rounded-xl bg-slate-800/50 p-4 ring-1 ring-white/10"
//             >
//               <h4 className="font-semibold text-slate-100">{bloco.titulo}</h4>
//               <ul className="mt-2 list-disc pl-5 text-slate-300">
//                 {bloco.itens.map((it) => (
//                   <li key={it}>{it}</li>
//                 ))}
//               </ul>
//             </div>
//           ))}
//         </div>
//       </section>

//       {/* Experiência Atual */}
//       <section className="mt-6 rounded-2xl bg-slate-900/60 p-6 shadow ring-1 ring-white/10">
//         <div className="flex items-center justify-between">
//           <h2 className="text-xl font-bold text-white">
//             Experiência Atual — CREA‑PI
//           </h2>
//           <span className="text-sm text-slate-400">
//             Teresina, PI • 2024 – Atual
//           </span>
//         </div>
//         <div className="mt-3 grid gap-3 md:grid-cols-2">
//           {contribuicoes.map((c) => (
//             <div
//               key={c.titulo}
//               className="rounded-xl bg-slate-800/50 p-4 ring-1 ring-white/10"
//             >
//               <h4 className="font-semibold text-slate-100">{c.titulo}</h4>
//               <p className="mt-1 text-slate-300">{c.desc}</p>
//             </div>
//           ))}
//         </div>
//       </section>

//       {/* Stack */}
//       <section className="mt-6 rounded-2xl bg-slate-900/60 p-6 shadow ring-1 ring-white/10">
//         <h2 className="text-xl font-bold text-white">Stack Utilizada</h2>
//         <div className="mt-4 grid gap-4 md:grid-cols-2 lg:grid-cols-3">
//           {[
//             {
//               k: "Backend",
//               v: [
//                 "Java EE (JPA, JSF, EJB)",
//                 "Python (Flask, Streamlit, Django)",
//                 "Node.js",
//               ],
//             },
//             {
//               k: "Data & AI",
//               v: [
//                 "PostgreSQL",
//                 "Pandas",
//                 "TensorFlow",
//                 "Scikit‑Learn",
//                 "PyTorch",
//               ],
//             },
//             {
//               k: "DevOps",
//               v: [
//                 "Docker",
//                 "Kubernetes",
//                 "CI/CD (Gitea, Jenkins, GitHub Actions)",
//                 "Terraform",
//                 "Ansible",
//               ],
//             },
//             {
//               k: "Frontend",
//               v: [
//                 "Streamlit",
//                 "React",
//                 "Angular",
//                 "PrimeFaces",
//                 "TypeScript",
//                 "Bootstrap",
//               ],
//             },
//             {
//               k: "Segurança & Blockchain",
//               v: [
//                 "OWASP Top 10",
//                 "Pentest",
//                 "API Hardening",
//                 "Hyperledger",
//                 "Ethereum (Solidity)",
//               ],
//             },
//           ].map((grp) => (
//             <div
//               key={grp.k}
//               className="rounded-xl bg-slate-800/50 p-4 ring-1 ring-white/10"
//             >
//               <h4 className="font-semibold text-slate-100">{grp.k}</h4>
//               <ul className="mt-2 list-disc pl-5 text-slate-300">
//                 {grp.v.map((item) => (
//                   <li key={item}>{item}</li>
//                 ))}
//               </ul>
//             </div>
//           ))}
//         </div>
//       </section>

//       <footer className="mt-8 pb-4 text-center text-xs text-slate-500">
//         Atualizado para apresentação amigável — sem abas e sem visual de editor
//         de código.
//       </footer>
//     </div>
//   );
// }
