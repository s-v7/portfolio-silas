import { motion } from "framer-motion";

const projects = [
  {
    nome: "Audit System",
    descricao: "Application for auditing using Flask and Angular.",
    tecnologias: "Python, Angular, SQLite",
    link: "https://github.com/s-v7/sistema-auditoria",
  },
  {
    nome: "Blockchain CREA-PI",
    descricao: "Blockchain network for CREA-PI data integration.",
    tecnologias: "Blockchain, Node.js",
    link: "https://github.com/s-v7/blockchain-crea-pi",
  },
  {
    nome: "RegistrationTrackingWorks",
    descricao:
      "Robust and modular system for managing information related to civil construction works..",
    tecnologias: "Python, Angular, PostreSQL/SQLite",
    link: "https://github.com/s-v7/CadastroRastreamentoObras",
  },
  {
    nome: "Sistema CREA-PI",
    descricao:
      "Institutional system originally built with PrimeFaces 3.1, Java EE 6, and GlassFish 3.1. Migrated to PrimeFaces 13 with Poseidon Layout, layout fixes, dynamic config panel (engrenagem), and legacy compatibility.",
    tecnologias: "Java 8, JSF 2.3, PrimeFaces 13, Poseidon, EJB, EAR, Maven",
    link: "https://github.com/s-v7",
  },
];

const Projects = () => {
  return (
    <section id="projetos" className="p-6 bg-coffee text-white">
      <h2 className="text-3xl font-bold mb-6 text-center">Projects</h2>
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
                <strong>Technologies:</strong> {project.tecnologias}
              </p>
              <a
                href={project.link}
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-400 hover:underline mt-4 inline-block"
              >
                View on GitHub
              </a>
            </motion.div>
          ))}
        </motion.div>
      </div>
    </section>
  );
};

export default Projects;
