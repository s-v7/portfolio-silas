import React, { useState } from "react";

const About = () => {
  const [currentPage, setCurrentPage] = useState(1);

  const changePage = (page) => {
    setCurrentPage(page);
  };

  return (
    <div className="bg-coffee min-h-screen p-6">
      {/* Conteúdo da Página */}
      <div className="max-w-4xl">
        {currentPage === 1 && (
          <section>
            <h1 className="text-3xl mb-6">Sobre Mim</h1>
            <p className="mb-4">
              Sou um programador Full Stack Java com experiência em desenvolvimento de sistemas web e mobile, com foco em segurança da informação, inteligência artificial e integração com APIs externas como SEFAZ. Apaixonado por aprender novas linguagens e frameworks, estou sempre atualizado com as tendências do mercado e em constante evolução profissional.
            </p>
            <p className="mb-4">
              Com mais de 5 anos de experiência em desenvolvimento de software, tenho ampla prática em implementação e manutenção de sistemas, análise de requisitos, desenvolvimento de novas funcionalidades e melhorias, além de trabalho com infraestrutura e segurança de sistemas. Meu foco está sempre na otimização e inovação tecnológica.
            </p>
            <p className="mb-4">
              Durante minha experiência na{" "}
              <a
                href="https://handpdv.com.br/"
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue hover:underline"
              >
                HANDpdv
              </a>, uma empresa especializada em software para varejo, desenvolvi e aprimorei funcionalidades web e mobile para emissão de notas fiscais eletrônicas e integração com a SEFAZ. Minha atuação envolveu tecnologias como XHTML, HTML, JSF, CSS, JavaScript, Ajax, JQuery, Java, SQL, JPA, Hibernate, IBExperts, TomCat, WebServices (SOAP, REST), XML e SVN. Além disso, possuo conhecimentos em C e criptografia para garantir a segurança dos dados.
            </p>
          </section>
        )}

        {currentPage === 2 && (
          <section>
            <p className="mb-4">
              Atualmente, atuo como <strong>Assessor de Tecnologia e Segurança da Informação</strong> no{" "}
              <a
                href="https://crea-pi.org.br/"
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue hover:underline"
              >
                CREA-PI
              </a>, onde desempenho a função de <strong>Analista Programador Full Stack</strong>. Minha atuação envolve a manutenção e evolução de sistemas legados, além de implementar novas funcionalidades, resolver bugs críticos e explorar novas tecnologias para modernizar o ambiente corporativo.
            </p>
            <h2 className="text-2xl mt-6 mb-4">Tecnologias Utilizadas</h2>
            <ul>
              <li><strong>Back-End:</strong> Java e Python.</li>
              <li><strong>Front-End:</strong> Angular 17, PrimeFaces, Bootstrap.</li>
              <li><strong>Banco de Dados:</strong> PostgreSQL.</li>
              <li><strong>Scripts Shell:</strong> Automação e segurança.</li>
            </ul>
          </section>
        )}

        {currentPage === 3 && (
          <section>
            <p className="mb-4">
              Minha experiência abrange desde a implementação de soluções escaláveis no back-end até a criação de interfaces front-end modernas e responsivas, utilizando tecnologias de ponta.
            </p>
          </section>
        )}
      </div>

      {/* Controles de Paginação */}
      <div className="flex justify-center space-x-4 mt-6">
        <button
          disabled={currentPage === 1}
          onClick={() => changePage(1)}
          className={`px-4 py-2 rounded ${currentPage === 1 ? "bg-gray-300" : "bg-blue-500 text-white hover:bg-blue-600"}`}
        >
          Página 1
        </button>
        <button
          disabled={currentPage === 2}
          onClick={() => changePage(2)}
          className={`px-4 py-2 rounded ${currentPage === 2 ? "bg-gray-300" : "bg-blue-500 text-white hover:bg-blue-600"}`}
        >
          Página 2
        </button>
        <button
          disabled={currentPage === 3}
          onClick={() => changePage(3)}
          className={`px-4 py-2 rounded ${currentPage === 3 ? "bg-gray-300" : "bg-blue-500 text-white hover:bg-blue-600"}`}
        >
          Página 3
        </button>
      </div>
    </div>
  );
};

export default About;

