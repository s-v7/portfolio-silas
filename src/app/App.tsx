import { BrowserRouter, Routes, Route } from "react-router";

import { ThemeProvider } from "../context/ThemeContext";
import Navbar from "../components/layout/Navbar";
import Footer from "../components/layout/Footer";
import ScrollToTop from "../components/layout/ScrollToTop";

import Chat from "../pages/Chat";

const appMeta = import.meta as ImportMeta & { env?: { BASE_URL?: string } };
const routerBase =
  appMeta.env?.BASE_URL === "/" ? "/" : (appMeta.env?.BASE_URL ?? "/").replace(/\/$/, "");

export default function App() {
  return (
    <ThemeProvider>
      <BrowserRouter basename={routerBase}>
        <ScrollToTop />
        <Navbar />
        <Routes>
          <Route path="/" element={<Chat />} />
        </Routes>
        <Footer />
      </BrowserRouter>
    </ThemeProvider>
  );
}
