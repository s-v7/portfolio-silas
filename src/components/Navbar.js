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
    <NavbarContainer>
      <h2>Silas Vasconcelos</h2>
      <div>
        <Link to="/">Home</Link>
        <Link to="/about">Sobre</Link>
        <Link to="/projects">Projetos</Link>
        <Link to="/contact">Contato</Link>
      </div>
    </NavbarContainer>
  );
};

export default Navbar;

