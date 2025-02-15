import React, { useEffect, useState, useMemo } from "react";
import UserImagePro from "../components/UserImagePro";
import profilePic from "../assets/images/profile.jpg"; 

const Home = () => {

  const [currentText, setCurrentText] = useState("");
  const [currentIndex, setCurrentIndex] = useState(0);
  const [charIndex, setCharIndex] = useState(0);
  const [isDeleting, setIsDeleting] = useState(false);

  const textToType = useMemo(() => [
    "Bem-vindo ao meu Portfólio",
    "Analista Programador Full Stack | CIO | Arquiteto de Sistemas",
    "Segurança | DevOps | IA | C/C++ | Java | Python | JavaScript | SQL",
    "Sou um programador Full Stack com experiência em desenvolvimento de sistemas web, com foco em segurança da informação, inteligência artificial e integração com APIs externas como SEFAZ e conforme as necessidades. Apaixonado por aprender novas linguagens e frameworks, estou sempre atualizado com as tendências do mercado e em constante evolução profissional."	  
  ], []);


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
    <div className="flex flex-col md:flex-row items-center justify-center min-h-screen bg-gray-900 text-white px-8">
      <div className="flex flex-col items-center md:items-start md:flex-row space-x-6">
        <UserImagePro src={profilePic} alt="Minha Foto" className="w-32 h-32 rounded-full border-4 border-teal-400" />
        <div>
          <h1 className="text-3xl md:text-4xl font-bold mb-4 animate-pulse">{currentText}</h1>
          <p className="text-lg text-gray-300">Portfólio de projetos e habilidades técnicas</p>
        </div>
      </div>
    </div>
  );

};

export default Home;

