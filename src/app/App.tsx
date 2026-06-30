import { BrowserRouter, Routes, Route } from "react-router-dom";

import { ThemeProvider } from "../context/ThemeContext";
import Navbar from "../components/layout/Navbar";
import Footer from "../components/layout/Footer";
import ScrollToTop from "../components/layout/ScrollToTop";

import Home from "../pages/Home";
import About from "../pages/About";
import Skills from "../pages/Skills";
import Experience from "../pages/Experience";
import Education from "../pages/Education";
import Projects from "../pages/Projects";
import ArtEngine from "../pages/ArtEngine";
import Contact from "../pages/Contact";
import CVInit from "../pages/CVInit";

import "../styles/components/Navbar.css";
import "../styles/components/Footer.css";
import "../styles/components.css";

export default function App() {
  return (
    <ThemeProvider>
      <BrowserRouter>
        <ScrollToTop />
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/profile" element={<CVInit />} />
          <Route path="/education" element={<Education />} />
          <Route path="/projects" element={<Projects />} />
          <Route path="/art-engine" element={<ArtEngine />} />
          <Route path="/contact" element={<Contact />} />
        </Routes>
        <Footer />
      </BrowserRouter>
    </ThemeProvider>
  );
}
