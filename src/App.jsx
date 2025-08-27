import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import Navbar from "./components/Navbar.jsx";
import Footer from "./components/Footer.jsx";
import Contact from "./pages/Contact.jsx";
import Home from "./pages/Home.jsx";
import Projects from "./pages/Projects.jsx";
import CVInit from "./pages/CVInit.jsx";

import "./styles/global.css";
import ScrollToTop from "./components/ScrollToTop.jsx";

export default function App() {
  return (
    <Router basename={import.meta.env.BASE_URL}>
      {" "}
      {/* "/" no dev; "/portfolio-silas/" no preview/prod */}
      <ScrollToTop />
      <Navbar />
      <main>
        <Routes>
          <Route index element={<Home />} /> {/* em vez de path="/" */}
          <Route path="cvinit" element={<CVInit />} />
          <Route path="projects" element={<Projects />} />
          <Route path="contact" element={<Contact />} />
          <Route path="*" element={<Home />} /> {/* fallback simples */}
        </Routes>
      </main>
      <Footer />
    </Router>
  );
}
