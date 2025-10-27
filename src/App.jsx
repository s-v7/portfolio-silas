import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import Navbar from "./components/Navbar.jsx";
import Footer from "./components/Footer.jsx";
import Contact from "./pages/Contact.jsx";
import Home from "./pages/Home.jsx";
import Projects from "./pages/Projects.jsx";
import CVInit from "./pages/CVInit.jsx";
import ScrollToTop from "./components/ScrollToTop.jsx";

import "./styles/global.css";
import "./styles/layout.css";
import "./styles/components.css";

// import { HelmetProvider } from "react-helmet-async";

export default function App() {
  return (
    // <HelmetProvider>
    <Router basename={import.meta.env.BASE_URL}>
      {" "}
      <ScrollToTop />
      <Navbar />
      <main>
        <Routes>
          <Route index element={<Home />} />
          <Route path="cvinit" element={<CVInit />} />
          <Route path="projects" element={<Projects />} />
          <Route path="contact" element={<Contact />} />
          <Route path="*" element={<Home />} />
        </Routes>
      </main>
      <Footer />
    </Router>
    // </HelmetProvider>
  );
}
