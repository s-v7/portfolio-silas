import React, { useEffect, useState } from "react";

const Home = () => {
  const textToType = [
    "Bem-vindo ao meu Portfólio",
    "Desenvolvedor Full Stack",
    "Segurança | DevOps | IA",
    "Sou um programador Full Stack Java com experiência em desenvolvimento de sistemas web e mobile, com foco em segurança da informação, inteligência artificial e integração com APIs externas como SEFAZ. Apaixonado por aprender novas linguagens e frameworks, estou sempre atualizado com as tendências do mercado e em constante evolução profissional."	  
  ];

  const [currentText, setCurrentText] = useState("");
  const [currentIndex, setCurrentIndex] = useState(0);
  const [charIndex, setCharIndex] = useState(0);
  const [isDeleting, setIsDeleting] = useState(false);

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

    const typingSpeed = isDeleting ? 7 : 30;
    const timer = setTimeout(handleTyping, typingSpeed);

    return () => clearTimeout(timer);
  }, [charIndex, isDeleting, currentIndex, textToType]);

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-900 text-white">
      <h1 className="text-4xl font-bold mb-4 animate-pulse">{currentText}</h1>
      <p className="text-lg">Portfólio de projetos e habilidades técnicas</p>
    </div>
  );
};

export default Home;

