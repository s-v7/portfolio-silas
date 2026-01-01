import { HashRouter as Router, Routes, Route } from "react-router-dom";

import Navbar from "./components/Navbar";
import ScrollToTop from "./components/ScrollToTop";

import Home from "./pages/Home";
import CVInit from "./pages/CVInit";  
import Projects from "./pages/Projects";
import Contact from "./pages/Contact";
import Education from "./pages/Education";
import Footer from "./components/Footer";


import "./styles/global.css";
import "./styles/layout.css";
import "./styles/components.css";
import "./styles/design-system.css";

const App: React.FC = () => {
  return (
    <Router>
      <ScrollToTop />
      <Navbar />

      <main>
        <Routes>
          <Route index element={<Home />} />
          <Route path="cvinit" element={<CVInit />} />
          <Route path="projects" element={<Projects />} />
          <Route path="education" element={<Education />} />
          <Route path="contact" element={<Contact />} />
          <Route path="*" element={<Home />} />
        </Routes>
      </main>

      <Footer />
    </Router>
  );
};

export default App;

