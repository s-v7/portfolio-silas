import React from "react";
import { Link } from "react-router-dom";

const Navbar = () => {
  return (
    <nav className="navbar sticky-navbar">
      {/* Links da Navbar */}
      <ul className="navbar-links flex space-x-4">
        <li>
          <Link to="/" className="hover:underline">
            Home
          </Link>
        </li>
        <li>
          <Link to="/about" className="hover:underline">
            About Me
          </Link>
        </li>
        <li>
          <Link to="/projects" className="hover:underline">
            Projects
          </Link>
        </li>
        <li>
          <Link to="/skills" className="hover:underline">
            Skills
          </Link>
        </li>
        <li>
          <Link to="/infra" className="hover:underline">
            Infra
          </Link>
        </li>

        <li>
          <Link to="/AI" className="hover:underline">
            AI
          </Link>
        </li>
        <li>
          <Link to="/contact" className="hover:underline">
            Contact
          </Link>
        </li>
      </ul>
    </nav>
  );
};

export default Navbar;
