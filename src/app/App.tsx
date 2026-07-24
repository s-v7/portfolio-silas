import { BrowserRouter, Routes, Route } from "react-router-dom";

import { ThemeProvider } from "../context/ThemeContext";
import Navbar from "../components/layout/Navbar";
import Footer from "../components/layout/Footer";
import ScrollToTop from "../components/layout/ScrollToTop";

import Home from "../pages/Home";
import Education from "../pages/Education";
import Projects from "../pages/Projects";
import ArtEngine from "../pages/ArtEngine";
import Contact from "../pages/Contact";
import CVInit from "../pages/CVInit";
import Chat from "../pages/Chat";
import LearningDashboard from "../pages/LearningDashboard";

import "../styles/components/Navbar.css";
import "../styles/components/Footer.css";
import "../styles/components.css";

const routerBase =
  import.meta.env.BASE_URL === "/"
    ? "/"
    : import.meta.env.BASE_URL.replace(/\/$/, "");

export default function App() {
  return (
    <ThemeProvider>
      <BrowserRouter basename={routerBase}>
        <ScrollToTop />
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/profile" element={<CVInit />} />
          <Route path="/education" element={<Education />} />
          <Route path="/projects" element={<Projects />} />
          <Route path="/art-engine" element={<ArtEngine />} />
          <Route path="/chat" element={<Chat />} />
          <Route path="/ai-career" element={<Chat />} />
          <Route path="/contact" element={<Contact />} />
          {import.meta.env.DEV && (
            <Route path="/admin/learning" element={<LearningDashboard />} />
          )}
        </Routes>
        <Footer />
      </BrowserRouter>
    </ThemeProvider>
  );
}
