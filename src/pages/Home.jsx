import React, { useEffect, useState, useMemo, useRef } from "react";
import UserImagePro from "../components/UserImagePro";
import profilePic from "../logo.svg";
import "./Home.css";

const Home = () => {
  const mainSectionRef = useRef(null);
  const [currentText, setCurrentText] = useState("");
  const [currentIndex, setCurrentIndex] = useState(0);
  const [charIndex, setCharIndex] = useState(0);
  const [isDeleting, setIsDeleting] = useState(false);

  const textToType = useMemo(
    () => [
      "Welcome to my Portfolio",
      "Full Stack Programmer Analyst | Systems Architect",
      "Security | DevOps | AI | C/C++ | Java | Python | JavaScript | SQL",
      "I am a Full Stack Developer and Technology Consultant with extensive experience in developing and optimizing web systems, focusing on information security, artificial intelligence (AI), and blockchain integration. My expertise spans backend and frontend development, system architecture, automation, and DevOps, enabling me to build robust, scalable, and secure solutions.",
      "Passionate about software architecture and cloud computing, I specialize in Java EE (JSF, PrimeFaces, Hibernate), Python (Flask, TensorFlow), and JavaScript frameworks like Angular and Node.js. I have deep knowledge of databases (PostgreSQL, MySQL, MongoDB) and work with Docker, Kubernetes, and CI/CD pipelines to optimize deployment and scalability.",
      "I have hands-on experience integrating with external APIs such as SEFAZ, implementing audit logs, cryptographic security measures, and compliance solutions for regulatory systems. My work also involves machine learning and neural networks for anomaly detection and predictive analytics, applying AI to enhance security and automation.",
      "In addition to development, I focus on cybersecurity best practices, penetration testing, and secure system design, ensuring data integrity and protection against vulnerabilities. I am currently expanding my expertise in cloud security, distributed architectures, and blockchain-based smart contracts to enhance system resilience and trust.",
      "I thrive on continuous learning and technology leadership, staying updated with the latest trends in software engineering, AI, and cybersecurity. My goal is to drive innovation through automation, AI-driven insights, and secure, scalable architectures, contributing to cutting-edge technology solutions on a global scale.",
      "\u2699\ufe0f Engenheiro de Software Fullstack com Foco em Sustenta\u00e7\u00e3o e Moderniza\u00e7\u00e3o",
      "\u2728 \u00c1reas de Especializa\u00e7\u00e3o:",
      "Back-end Java EE: Herdou um sistema legado com GlassFish, EJB, EAR e PrimeFaces 3.1, atualizou com sucesso para PrimeFaces 13.",
      "Migra\u00e7\u00e3o de Legado: Experi\u00eancia consolidada na transi\u00e7\u00e3o de JDK 6 para 8, PF 3 para 13, mantendo fluxo de trabalho intacto.",
      "Dom\u00ednio de JSF + PrimeFaces + Poseidon: Dom\u00ednio de componentiza\u00e7\u00e3o, escopos e integra\u00e7\u00e3o com template.",
      "Frontend Estruturado: Forte compreens\u00e3o de JavaScript nativo, DOM, comportamento din\u00e2mico, layout responsivo.",
      "Mentalidade Estruturada e Limpa: C\u00f3digo claro, comentado e objetivo, com foco real no problema t\u00e9cnico.",
      "\ud83d\udcbc Fun\u00e7\u00e3o Atual ou Potencial:",
      "Analista Desenvolvedor Pleno/S\u00eanior com foco em sistemas legados e arquitetura JSF corporativa.",
      "Manuten\u00e7\u00e3o e moderniza\u00e7\u00e3o de sistemas de \u00f3rg\u00e3os p\u00fablicos com ciclo longo.",
      "Atualiza\u00e7\u00e3o segura de sistemas sem quebrar fluxos de trabalho cr\u00edticos.",
      "Comunica\u00e7\u00e3o t\u00e9cnica clara com times de infra, an\u00e1lise e DevOps.",
    ],
    []
  );

  useEffect(() => {
    // Aguarda a renderização antes de rolar
    setTimeout(() => {
      if (mainSectionRef.current) {
        mainSectionRef.current.scrollIntoView({
          behavior: "smooth",
          block: "start",
        });
      }
    }, 500);
  }, []);

  useEffect(() => {
    const handleTyping = () => {
      const currentString = textToType[currentIndex];

      if (!isDeleting && charIndex < currentString.length) {
        setCurrentText(currentString.slice(0, charIndex + 1));
        setCharIndex((prev) => prev + 1);
      } else if (isDeleting && charIndex > 0) {
        setCurrentText(currentString.slice(0, charIndex - 1));
        setCharIndex((prev) => prev - 1);
      } else if (!isDeleting && charIndex === currentString.length) {
        setIsDeleting(true);
        setTimeout(() => {}, 1000);
      } else if (isDeleting && charIndex === 0) {
        setIsDeleting(false);
        setCurrentIndex((prevIndex) => (prevIndex + 1) % textToType.length);
      }
    };

    const typingSpeed = isDeleting ? 5 : 30;
    const timer = setTimeout(handleTyping, typingSpeed);

    return () => clearTimeout(timer);
  }, [charIndex, isDeleting, currentIndex, textToType]);

  return (
    <div ref={mainSectionRef} id="main-section" className="home-container">
      <div className="flex flex-col md:flex-row items-center justify-center min-h-screen bg-gray-900 text-white px-8">
        <div className="flex flex-col items-center md:items-start md:flex-row space-x-6">
          <UserImagePro
            src={profilePic}
            alt="Minha Foto"
            className="w-32 h-32 rounded-full border-4 border-teal-400"
          />
          <div>
            <h1 className="text-3xl md:text-4xl font-bold mb-4 animate-pulse">
              {currentText}
            </h1>
            <p className="text-lg text-gray-300">
              Project portfolio and technical skills
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;
