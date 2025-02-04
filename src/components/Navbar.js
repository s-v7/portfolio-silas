import React from "react";
import { Link } from "react-router-dom";
import styled from "styled-components";

const NavbarContainer = styled.nav`
  display: flex;
  justify-content: space-between;
  padding: 1rem 2rem;
  background: #1f1f1f;
`;

const Navbar = () => {
  return (
    <nav className="bg-blue-700 text-white p-4">
      <div className="container mx-auto flex justify-between">
        <h1 className="text-xl font-bold">Portfólio de Silas</h1>
        <div className="space-x-4">
          <Link to="/" className="hover:underline">Home</Link>
          <Link to="/about" className="hover:underline">Sobre Mim</Link>
          <Link to="/projects" className="hover:underline">Projetos</Link>
          <Link to="/contact" className="hover:underline">Contato</Link>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
