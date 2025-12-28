import { useState } from "react";
import { FaCode, FaServer, FaDatabase } from "react-icons/fa";

type PageIndex = 1 | 2 | 3;

const About: React.FC = () => {
  const [currentPage, setCurrentPage] = useState<PageIndex>(1);

  const changePage = (page: PageIndex): void => {
    setCurrentPage(page);
  };

  return (
    <div className="min-h-screen p-6 bg-gradient-to-b from-gray-900 via-gray-800 to-gray-700 text-white">
      <div className="max-w-4xl">
        {/* PAGE 1 */}
        {currentPage === 1 && (
          <section>
            <h1 className="text-4xl font-bold mb-6 text-teal-400">About Me</h1>

            <p className="mb-6 leading-relaxed text-gray-300">
              I am a Full Stack Software Engineer with experience in developing
              web and enterprise systems, focused on information security,
              applied artificial intelligence, and integration with external
              APIs such as SEFAZ.
            </p>

            <p className="mb-6 leading-relaxed text-gray-300">
              With more than 5 years of experience, I have worked on system
              implementation and maintenance, requirements analysis, feature
              development, infrastructure, and security — always focused on
              optimization and technological evolution.
            </p>

            <p className="mb-6 leading-relaxed text-gray-300">
              During my time at{" "}
              <a
                href="https://handpdv.com.br/"
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue hover:underline"
              >
                HANDpdv
              </a>
              , I developed and improved web and mobile systems for issuing
              electronic invoices and integrating with SEFAZ, working with Java,
              JSF, PrimeFaces, Hibernate, WebServices (SOAP/REST), and database
              optimization.
            </p>
          </section>
        )}

        {/* PAGE 2 */}
        {currentPage === 2 && (
          <section>
            <p className="mb-6 leading-relaxed text-gray-300">
              Currently, I work as a{" "}
              <strong>Technology and Information Security Advisor</strong> at{" "}
              <a
                href="https://crea-pi.org.br/"
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue hover:underline"
              >
                CREA-PI
              </a>
              , acting as a <strong>Full Stack Development Analyst</strong>.
            </p>

            <p className="mb-6 leading-relaxed text-gray-300">
              My responsibilities include maintaining and modernizing legacy
              systems, implementing new features, resolving critical issues, and
              introducing new technologies into the corporate environment.
            </p>

            <p className="mb-6 leading-relaxed text-gray-300">
              I actively participated in migrations from JDK 6 → 7 → 8, upgrades
              of GlassFish and PrimeFaces, and the implementation of CI/CD,
              automation, SSL/TLS renewal, database backup strategies, and secure
              deployment pipelines.
            </p>

            <h2 className="text-2xl mt-6 mb-4">Technologies Used</h2>
            <ul className="space-y-2 text-gray-300">
              <li>
                <FaCode className="inline mr-2 text-teal-400" />
                Frontend: JSF, PrimeFaces, JavaScript, Ajax, XHTML, CSS
              </li>
              <li>
                <FaServer className="inline mr-2 text-teal-400" />
                Backend: Java EE, EJB, Hibernate, JPA, GlassFish
              </li>
              <li>
                <FaDatabase className="inline mr-2 text-teal-400" />
                Databases: PostgreSQL, SQLite
              </li>
            </ul>
          </section>
        )}

        {/* PAGE 3 */}
        {currentPage === 3 && (
          <section>
            <h2 className="text-2xl font-bold text-teal-400 mb-4">
              CREA-PI Legacy System Modernization
            </h2>

            <p className="mb-4 text-gray-300">
              <strong>Description:</strong> Institutional legacy management
              system originally developed with JSF 2.0, PrimeFaces 3.1, EJB, and
              GlassFish 3.1. I led a full modernization effort while preserving
              critical workflows and EAR modular structure.
            </p>

            <ul className="list-disc pl-6 text-gray-300 mb-4">
              <li>PrimeFaces upgrade: 3.1 → 13</li>
              <li>Visual migration to Poseidon template</li>
              <li>JSF/CDI refactoring and layout fixes</li>
              <li>REST integration with FastAPI services</li>
              <li>Improved performance and maintainability</li>
            </ul>

            <p className="mb-4 text-gray-300">
              <strong>Technologies:</strong> Java 8, JSF 2.3, PrimeFaces 13,
              GlassFish, PostgreSQL, Maven, Git, SonarQube
            </p>
          </section>
        )}
      </div>

      {/* PAGINATION */}
      <div className="flex justify-center space-x-4 mt-8">
        {[1, 2, 3].map((page) => (
          <button
            key={page}
            disabled={currentPage === page}
            onClick={() => changePage(page as PageIndex)}
            className={`px-4 py-2 rounded transition ${
              currentPage === page
                ? "bg-gray-600 cursor-default"
                : "bg-blue-500 hover:bg-teal-600"
            }`}
          >
            Page {page}
          </button>
        ))}
      </div>
    </div>
  );
};

export default About;

