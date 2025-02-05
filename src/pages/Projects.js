import React from "react";

const Projects = () => {
  const projetos = [
    {
      nome: "Sistema de Auditoria",
      descricao: "Aplicativo para auditoria utilizando Flask e Angular.",
      tecnologias: "Python, Angular, SQLite",
      link: "https://github.com/s-v7/sistema-auditoria",
    },
    {
      nome: "Blockchain CREA-PI",
      descricao: "Rede Blockchain para integração de dados CREA-PI.",
      tecnologias: "Blockchain, Node.js",
      link: "https://github.com/s-v7/blockchain-crea-pi",
    },
    {
      nome: "CadastroRastreamentoObras",
      descricao:
        "Sistema robusto e modular para a gestão de informações relacionadas a obras de construção civil.",
      tecnologias: "Python, Angular, PostreSQL/SQLite",
      link: "https://github.com/s-v7/CadastroRastreamentoObras",
    },
    {
      nome: "Weather Forecast",
      descricao: "Weather forecasts based on a city's climate information.",
      tecnologias: "Python, Scikit-Learn, Pandas, Numpy, Matplotlib",
      link: "https://github.com/s-v7/weather_forecast",
    },
  ];

  return (
    <section id="projetos" className="p-6 bg-coffee text-white">
      <h2 className="text-3xl font-bold mb-6 text-center">Projetos</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {projetos.map((projeto, index) => (
          <div
            key={index}
            className="projeto-card p-4 bg-gray-800 rounded shadow-md hover:shadow-lg transition-shadow"
          >
            <h3 className="text-xl font-semibold mb-2">{projeto.nome}</h3>
            <p className="text-sm mb-2">{projeto.descricao}</p>
            <p className="text-sm">
              <strong>Tecnologias:</strong> {projeto.tecnologias}
            </p>
            <a
              href={projeto.link}
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-400 hover:text-blue-200 mt-2 block"
            >
              Ver no GitHub
            </a>
          </div>
        ))}
      </div>
    </section>
  );
};

export default Projects;

