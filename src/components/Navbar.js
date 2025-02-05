import React from "react";
import { Link } from "react-router-dom";


const Navbar = () => {
  return (
    <nav className="navbar">
      <ul className="flex space-x-4">
        <h1 className="text-xl font-bold">Portfólio de Silas</h1>
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
      </ul>
    </nav>
  );
};

export default Navbar;
