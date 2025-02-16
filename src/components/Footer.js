import React from "react";
import { FaGithub, FaLinkedin, FaEnvelope } from "react-icons/fa";

const Footer = () => {
  return (
    <footer className="footer fade-in">
      <div className="container mx-auto text-center">	  
      <p>© 2025 Silas Vasconcelos Cruz portfolio. All rights reserved.</p>
      <div className="social-icons">
        <a href="https://github.com/s-v7" target="_blank" rel="noopener noreferrer">
          <FaGithub />
        </a>
        <a href="https://www.linkedin.com/in/silas-v-053293255/" target="_blank" rel="noopener noreferrer">
          <FaLinkedin />
        </a>
        <a href="mailto:svasconceloscruz7@gmail.com" target="_blank" rel="noopener noreferrer">
          <FaEnvelope />
        </a>
      </div>
     </div>
    </footer>
  );
};

export default Footer;

