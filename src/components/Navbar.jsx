import React from "react";
import { Link } from "react-router-dom";

const Navbar = () => {
  return (
    <nav className="navbar sticky-navbar">
      <ul className="navbar-links flex space-x-4">
        <li>
          <Link to="" className="hover:underline">
            Home
          </Link>
        </li>
        <li>
          <Link to="cvinit" className="hover:underline">
            AboutMe
          </Link>
        </li>
        <li>
          <Link to="projects" className="hover:underline">
            Projects
          </Link>
        </li>
      </ul>
    </nav>
  );
};

export default Navbar;
