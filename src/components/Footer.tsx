import { useTheme } from "../context/ThemeContext";
import "./Footer.css";
export default function Footer() {
  const { theme } = useTheme();
  const isAdmin = theme === "admin";
  const year = new Date().getFullYear();
  return (
    <footer className="footer">
      <div className="container footer__inner">
        <span className="footer__copy">
          © {year} Silas Vasconcelos Cruz · Teresina, PI
        </span>
        <div className="footer__links">
          <a href="https://github.com/s-v7" target="_blank" rel="noreferrer">
            GitHub
          </a>
          <a
            href="https://linkedin.com/in/s-v7"
            target="_blank"
            rel="noreferrer"
          >
            LinkedIn
          </a>
          <a href="mailto:svasconceloscruz7@gmail.com">
            {isAdmin ? "Email" : "Email"}
          </a>
        </div>
        <span className="footer__sig">{isAdmin ? "s▪v7" : "Silas Cruz"}</span>
      </div>
    </footer>
  );
}
