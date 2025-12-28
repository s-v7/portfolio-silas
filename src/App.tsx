import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
import ScrollToTop from "./components/ScrollToTop";

import Home from "./pages/Home";
import Projects from "./pages/Projects";
import Contact from "./pages/Contact";
import CVInit from "./pages/CVInit";
import Education from "./pages/Education";
import Experience from "./pages/Experience";


import "./styles/global.css";
import "./styles/layout.css";
import "./styles/components.css";

const App: React.FC = () => {
  return (
    <Router basename={import.meta.env.BASE_URL}>
      <ScrollToTop />
      <Navbar />

      <main>
        <Routes>
          <Route index element={<Home />} />
          <Route path="cvinit" element={<CVInit />} />
          <Route path="projects" element={<Projects />} />
          <Route path="education" element={<Education />} />
          <Route path="experience" element={<Experience />} />	  
          <Route path="contact" element={<Contact />} />
          <Route path="*" element={<Home />} />
        </Routes>
      </main>

      <Footer />
    </Router>
  );
};

export default App;

