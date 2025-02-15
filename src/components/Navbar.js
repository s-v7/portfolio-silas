import React from "react";
import { Link } from "react-router-dom";

const Navbar = () => {
  return (
    <nav className="navbar">
      {/* Links da Navbar */}
      <ul className="navbar-links flex space-x-4">
        <li>
          <Link to="/" className="hover:underline">Home</Link>
        </li>
        <li>
          <Link to="/about" className="hover:underline">Sobre Mim</Link>
        </li>
        <li>
          <Link to="/projects" className="hover:underline">Projetos</Link>
        </li>
        <li>
          <Link to="/contact" className="hover:underline">Contato</Link>
        </li>
	<li>
        <Link to="/skills" className="hover:underline">Skills</Link>
	</li>
      </ul>
    </nav>
  );
};

export default Navbar;

