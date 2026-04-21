import { NavLink } from "react-router-dom";
import { useTheme } from "../context/ThemeContext";
import "./Navbar.css";

const LINKS_ADMIN = [
  { to: "/", label: "Home" },
  { to: "/profile", label: "Profile / CV" },
  { to: "/education", label: "Education" },
  { to: "/projects", label: "Projects" },
  { to: "/art-engine", label: "ART Engine" },
  { to: "/contact", label: "Contact" },
];
const LINKS_REC = [
  { to: "/", label: "Home" },
  { to: "/profile", label: "Profile" },
  { to: "/education", label: "Education" },
  { to: "/projects", label: "Projects" },
  { to: "/art-engine", label: "ART Engine" },
  { to: "/contact", label: "Contact" },
];

function IconAdmin() {
  return (
    <svg viewBox="0 0 16 16" aria-hidden="true">
      <circle cx="8" cy="8" r="3.5" stroke="currentColor" />
      <line x1="8" y1="1" x2="8" y2="3" />
      <line x1="8" y1="13" x2="8" y2="15" />
      <line x1="1" y1="8" x2="3" y2="8" />
      <line x1="13" y1="8" x2="15" y2="8" />
      <line x1="3.4" y1="3.4" x2="4.8" y2="4.8" />
      <line x1="11.2" y1="11.2" x2="12.6" y2="12.6" />
      <line x1="3.4" y1="12.6" x2="4.8" y2="11.2" />
      <line x1="11.2" y1="4.8" x2="12.6" y2="3.4" />
    </svg>
  );
}
function IconRec() {
  return (
    <svg viewBox="0 0 16 16" aria-hidden="true">
      <path
        d="M8 2a6 6 0 1 0 0 12A6 6 0 0 0 8 2zm0 1.5v9A4.5 4.5 0 0 1 8 3.5z"
        stroke="currentColor"
        fill="none"
      />
    </svg>
  );
}

export default function Navbar() {
  const { theme, toggle } = useTheme();
  const isRec = theme === "recruiter";
  const links = isRec ? LINKS_REC : LINKS_ADMIN;

  return (
    <header className="nav">
      <div className="nav-inner container">
        <a href="/" className="nav-brand" aria-label="home">
          {isRec ? (
            <span className="nav-brand-rec">
              Silas <em>Cruz</em>
            </span>
          ) : (
            <span className="nav-brand-admin">
              s<span>▪</span>v7
            </span>
          )}
        </a>
        <nav aria-label="Main navigation">
          <ul className="nav-links">
            {links.map(({ to, label }) => (
              <li key={to}>
                <NavLink
                  to={to}
                  end={to === "/"}
                  className={({ isActive }) =>
                    `nav-link${isActive ? " nav-link--active" : ""}`
                  }
                >
                  {label}
                </NavLink>
              </li>
            ))}
          </ul>
        </nav>
        <div className="nav-right">
          <div className="nav-status" aria-label="Available for work">
            <span className="status-dot" aria-hidden="true" />
            <span>{isRec ? "open to work" : "available"}</span>
          </div>
          <button
            className="theme-toggle"
            onClick={toggle}
            aria-label={`Switch to ${isRec ? "admin" : "recruiter"} theme`}
            title={
              isRec ? "Switch to Admin theme" : "Switch to Recruiter theme"
            }
          >
            {isRec ? <IconAdmin /> : <IconRec />}
          </button>
        </div>
      </div>
    </header>
  );
}
