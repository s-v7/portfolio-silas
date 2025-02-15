import { motion } from "framer-motion";

// Implementation for Projects Page with Automated Presentation and Styled Design


const projects = [
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
];

const Projects = () => {
  return (
    <section id="projetos" className="p-6 bg-coffee text-white">	 
      <h2 className="text-3xl font-bold mb-6 text-center">Projetos</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">	  
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 1 }}
        className="grid grid-cols-1 md:grid-cols-2 gap-4"
      >
        {projects.map((project, index) => (
          <motion.div
            key={index}
            initial={{ opacity: 0, y: 50 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.3, duration: 0.6 }}
            className="projeto-card p-4 bg-gray-800 rounded shadow-md hover:shadow-lg transition-shadow"
		
          >
            <h3 className="text-xl font-semibold mb-2">{project.nome}</h3>
            <p className="text-sm mb-2">{project.descricao}</p>
            <p className="text-sm">
              <strong>Tecnologias:</strong> {project.tecnologias}
            </p>
            <a
              href={project.link}
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-400 hover:underline mt-4 inline-block"
            >
              Ver no GitHub
            </a>
          </motion.div>
        ))}
      </motion.div>
    </div>
  </section>
  );
};

export default Projects;

