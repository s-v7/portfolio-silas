import React from "react";
import { FaFacebook, FaTwitter, FaInstagram, FaGithub } from "react-icons/fa";


const Footer = () => {
  return (
    <footer className="bg-gray-800 text-white py-6">
      <div className="container mx-auto text-center">
        <p className="mb-4">Conecte-se conosco nas redes sociais:</p>
        <div className="flex justify-center space-x-6">
          <a href="https://facebook.com" target="_blank" rel="noopener noreferrer">
            <FaFacebook className="text-blue-500 hover:text-white text-2xl" />
          </a>
          <a href="https://twitter.com" target="_blank" rel="noopener noreferrer">
            <FaTwitter className="text-blue-400 hover:text-white text-2xl" />
          </a>
          <a href="https://instagram.com" target="_blank" rel="noopener noreferrer">
            <FaInstagram className="text-pink-500 hover:text-white text-2xl" />
          </a>
	  <a href="https://github.com/usuario/projeto" target="_blank" rel="noopener noreferrer">
            <FaGithub className="text-white hover:text-gray-300 text-2xl" />
	  </a>	  
        </div>
        <p className="mt-4 text-sm">
          © {new Date().getFullYear()} Sistema de Relatórios. Todos os direitos reservados.
        </p>
      </div>
    </footer>
  );
};

export default Footer;

