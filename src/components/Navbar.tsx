import { Link, useLocation } from "react-router-dom";

const Navbar: React.FC = () => {
  const location = useLocation();

  const isActive = (path: string): boolean => {
    if (
      path === "/" &&
      (location.pathname === "/" || location.pathname === "")
    ) {
      return true;
    }

    return location.pathname.startsWith(path);
  };

  return (
    <nav
      className="navbar sticky-navbar"
      role="navigation"
      aria-label="Main Navigation"
    >
      <ul className="navbar-links">
        <li>
          <Link
            to="/"
            className={`navbar-link ${isActive("/") ? "active" : ""}`}
          >
            Home
          </Link>
        </li>

        <li>
          <Link
            to="/cvinit"
            className={`navbar-link ${isActive("/cvinit") ? "active" : ""}`}
          >
            Profile / CV
          </Link>
        </li>
        <li>
          <Link
            to="/education"
            className={`navbar-link ${isActive("/education") ? "actice": ""}`}
          >
            Education
          </Link>
        </li>
        <li>
          <Link
            to="/projects"
            className={`navbar-link ${isActive("/projects") ? "active" : ""}`}
          >
            Projects
          </Link>
        </li>

        <li>
          <Link
            to="/contact"
            className={`navbar-link ${isActive("/contact") ? "active" : ""}`}
          >
            Contact
          </Link>
        </li>
      </ul>
    </nav>
  );
};

export default Navbar;
