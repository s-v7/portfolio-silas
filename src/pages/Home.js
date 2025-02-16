import React, { useEffect, useState, useMemo, useRef } from "react";
import UserImagePro from "../components/UserImagePro";
import profilePic from "../assets/images/profile.jpg"; 
import "./Home.css";

const Home = () => {
  const mainSectionRef = useRef(null);
  const [currentText, setCurrentText] = useState("");
  const [currentIndex, setCurrentIndex] = useState(0);
  const [charIndex, setCharIndex] = useState(0);
  const [isDeleting, setIsDeleting] = useState(false);

  const textToType = useMemo(() => [
    "Welcome to my Portfolio",
    "Full Stack Programmer Analyst | CIO | Systems Architect",
    "Security | DevOps | AI | C/C++ | Java | Python | JavaScript | SQL",
    "I am a Full Stack Developer and Technology Consultant with extensive experience in developing and optimizing web systems, focusing on information security, artificial intelligence (AI), and blockchain integration. My expertise spans backend and frontend development, system architecture, automation, and DevOps, enabling me to build robust, scalable, and secure solutions.",
    "Passionate about software architecture and cloud computing, I specialize in Java EE (JSF, PrimeFaces, Hibernate), Python (Flask, TensorFlow), and JavaScript frameworks like Angular and Node.js. I have deep knowledge of databases (PostgreSQL, MySQL, MongoDB) and work with Docker, Kubernetes, and CI/CD pipelines to optimize deployment and scalability.",
    "I have hands-on experience integrating with external APIs such as SEFAZ, implementing audit logs, cryptographic security measures, and compliance solutions for regulatory systems. My work also involves machine learning and neural networks for anomaly detection and predictive analytics, applying AI to enhance security and automation.",
    "In addition to development, I focus on cybersecurity best practices, penetration testing, and secure system design, ensuring data integrity and protection against vulnerabilities. I am currently expanding my expertise in cloud security, distributed architectures, and blockchain-based smart contracts to enhance system resilience and trust.",
    "I thrive on continuous learning and technology leadership, staying updated with the latest trends in software engineering, AI, and cybersecurity. My goal is to drive innovation through automation, AI-driven insights, and secure, scalable architectures, contributing to cutting-edge technology solutions on a global scale."
  ], []);

  useEffect(() => {
  // Aguarda a renderização antes de rolar
    setTimeout(() => {
     if (mainSectionRef.current) {
       mainSectionRef.current.scrollIntoView({ behavior: "smooth", block: "start" });
     }
    }, 500); // Pequeno delay para garantir que tudo carregou
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
        <UserImagePro src={profilePic} alt="Minha Foto" className="w-32 h-32 rounded-full border-4 border-teal-400" />
        <div>
          <h1 className="text-3xl md:text-4xl font-bold mb-4 animate-pulse">{currentText}</h1>
          <p className="text-lg text-gray-300">Project portfolio and technical skills</p>
        </div>
      </div>
    </div>
   </div>	  
  );

};

export default Home;

