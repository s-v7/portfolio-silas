import React, { useState } from "react";
import { FaCode, FaServer, FaDatabase } from "react-icons/fa";

const About = () => {
  const [currentPage, setCurrentPage] = useState(1);

  const changePage = (page) => {
    setCurrentPage(page);
  };

  return (
    <div className="min-h-screen p-6 bg-gradient-to-b from-gray-900 via-gray-800 to-gray-700 text-white">
      {/* Conteúdo da Página */}
      <div className="max-w-4xl">
        {currentPage === 1 && (
          <section>
            <h1 className="text-4xl font-bold mb-6 text-teal-400">About Me</h1>
            <p className="mb-6 leading-relaxed text-gray-300">
              I am a Full Stack Java programmer with experience in developing
              web and mobile systems, focusing on information security,
              artificial intelligence and integration with external APIs such as
              SEFAZ. Passionate about learning new languages ​​and frameworks, I
              am always up to date with market trends and constantly evolving
              professionally.
            </p>
            <p className="mb-6 leading-relaxed text-gray-300">
              With more than 5 years of experience in software development, I
              have extensive experience in systems implementation and
              maintenance, requirements analysis, development of new features
              and improvements, in addition to working with infrastructure and
              systems security. My focus is always on optimization and
              technological innovation.
            </p>
            <p className="mb-6 leading-relaxed text-gray-300">
              During my experience at{" "}
              <a
                href="https://handpdv.com.br/"
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue hover:underline"
              >
                HANDpdv
              </a>
              , a company specialized in retail software, I developed and
              improved web and mobile functionalities for issuing electronic
              invoices and integration with SEFAZ. My work involved technologies
              such as XHTML, HTML, JSF, CSS, JavaScript, Ajax, JQuery, Java,
              SQL, JPA, Hibernate, IBExperts, TomCat, WebServices (SOAP, REST),
              XML and SVN. Furthermore, I have knowledge of C and cryptography
              to ensure data security.
            </p>
          </section>
        )}

        {currentPage === 2 && (
          <section>
            <p className="mb-6 leading-relaxed text-gray-300">
              Currently, I work as a
              <strong>Technology and Information Security Advisor</strong> at{" "}
              <a
                href="https://crea-pi.org.br/"
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue hover:underline"
              >
                CREA-PI
              </a>
            </p>
            <p className="mb-6 leading-relaxed text-gray-300">
              where I work as a <strong>Full Stack Development Analyst</strong>.
              My role involves maintaining and evolving legacy systems, in
              addition to implementing new functionalities, resolving critical
              bugs and exploring new technologies to modernize the corporate
              environment.
            </p>
            <p className="mb-6 leading-relaxed text-gray-300">
              Working on the front line in modernization and evolution, from
              infrastructure to support for professionals and companies!
              Actively participated in the migration from JDK-6 EE to JDK-7 EE
              and later JDK-8, Glassfish-3.1 to 4.1/5.1, PrimeFaces-3.5 to
              5.0/10 Implementation of Automations for database backup, using
              Shell(.sh); Implementation of SSL/TLS Certificate Renewal
              Automations for various use cases, CI/CD for Glassfish-4.1.1,
              using the best development and Security practices!
            </p>
            <p className="mb-6 leading-relaxed text-gray-300">
              Automation implementation for build and deploy/autodeploy/rollback
              on a dedicated server, using best practices and security!
              <br />
              Developed and Implemented a System, based on AI | Blockchain |
              Python | Angular, for Registration and Tracking of works in Civil
              Construction! AI model for analyzing logs/anomalies, on servers
              and depending on use cases and needs! The intention is to change
              the entire Infrastructure from Product to Service! Implement means
              of Digitization, Automation, among others, always in compliance
              with environmental areas and other areas!
            </p>
            <h2 className="text-2xl mt-6 mb-4">Technologies Used</h2>
            <div>
              <ul className="space-y-2">
                <li>
                  <FaCode className="inline mr-2 text-teal-400 hover:scale-110 transition-transform duration-300" />
                  Frontend Development: JSF, PrimeFaces-5.0, JQuery, Ajax,
                  JavaScript, XHtml, css
                </li>
                <li>
                  <FaServer className="inline mr-2" /> Backend Development: Java
                  EE 6, Java EE 7 com JDk-8, JasperReport, Server:
                  Glassfish-4.1.1, Hibernate, Jpa
                </li>
                <li>
                  <FaDatabase className="inline mr-2" /> Database: PostgreSQL,
                  SQLite
                </li>
              </ul>
            </div>
          </section>
        )}

        {currentPage === 3 && (
          <section>
            <h2 className="text-2xl font-bold text-teal-400 mb-4">
              Sistema CREA-PI
            </h2>
            <p className="mb-4 text-gray-300">
              <strong>Descrição:</strong> Sistema de gestão institucional
              legado, originalmente desenvolvido em JSF 2.0 com PrimeFaces 3.1,
              EJBs e GlassFish 3.1. Ao longo de 1 ano e 3 meses, liderei a
              modernização do projeto, mantendo compatibilidade com os fluxos
              críticos e estrutura modular EAR.
            </p>
            <p className="mb-4 text-gray-300">
              <strong>Minhas Contribuições:</strong>
            </p>
            <ul className="list-disc pl-6 text-gray-300 mb-4">
              <li>Atualização de stack: PrimeFaces 3.1 → PrimeFaces 13</li>
              <li>
                Migração visual para Poseidon Template (com customizações)
              </li>
              <li>Refatoração de Beans e integração com CDI</li>
              <li>Reestruturação de JS/CSS, correção de layout quebrado</li>
              <li>Compatibilidade com FastAPI para integração REST</li>
            </ul>
            <p className="mb-4 text-gray-300">
              <strong>Desafios Técnicos:</strong>
            </p>
            <ul className="list-disc pl-6 text-gray-300 mb-4">
              <li>Corrigir o comportamento da engrenagem de configuração</li>
              <li>Ajustar menu responsivo (layout-overlay / layout-static)</li>
              <li>Compatibilidade entre guestPreferences e o JS do Poseidon</li>
              <li>
                Conflitos entre ID de componentes JSF e scripts vanilla JS
              </li>
            </ul>
            <p className="mb-4 text-gray-300">
              <strong>Tecnologias utilizadas:</strong> Java 8, PrimeFaces 13,
              Poseidon, JSF 2.3, EJB, Maven, GlassFish, PostgreSQL, Git,
              SonarQube
            </p>
          </section>
        )}
      </div>

      {/* Controles de Paginação */}
      <div className="flex justify-center space-x-4 mt-6">
        <button
          disabled={currentPage === 1}
          onClick={() => changePage(1)}
          className={`px-4 py-2 rounded transition-all duration-300 ${
            currentPage === 1
              ? "bg-gray-600 text-white cursor-default"
              : "bg-blue-500 text-white hover:bg-teal-600"
          }`}
        >
          Página 1
        </button>
        <button
          disabled={currentPage === 2}
          onClick={() => changePage(2)}
          className={`px-4 py-2 rounded transition-all duration-300 ${
            currentPage === 2
              ? "bg-gray-600 text-white cursor-default"
              : "bg-blue-500 text-white hover:bg-teal-600"
          }`}
        >
          Página 2
        </button>
        <button
          disabled={currentPage === 3}
          onClick={() => changePage(3)}
          className={`px-4 py-2 rounded transition-all duration-300 ${
            currentPage === 3
              ? "bg-gray-600 text-white cursor-default"
              : "bg-blue-500 text-white hover:bg-teal-600"
          }`}
        >
          Página 3
        </button>
      </div>
    </div>
  );
};

export default About;
