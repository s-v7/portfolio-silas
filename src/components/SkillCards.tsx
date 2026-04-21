import { useTheme } from "../context/ThemeContext";
import "./SkillCards.css";

const SKILLS = [
  {
    cat: "Backend & Architecture",
    items: [
      "Java EE 8+, 17",
      "JSF / PrimeFaces",
      "Spring Boot",
      "FastAPI",
      "Python",
      "Node.js",
    ],
  },
  {
    cat: "Frontend",
    items: [
      "Angular 17+",
      "React",
      "TypeScript",
      "Three.js",
      "Leaflet",
      "XHTML / CSS",
    ],
  },
  {
    cat: "DevOps & Infra",
    items: [
      "Docker",
      "Kubernetes",
      "Nginx",
      "Cloudflare Tunnel",
      "Linux / systemd",
      "CI/CD",
    ],
  },
  {
    cat: "Data, AI & Security",
    items: [
      "PostgreSQL",
      "PostGIS",
      "Sentinel-2",
      "NumPy / Pandas",
      "OpenAI API",
      "Pentest / OWASP",
    ],
  },
  {
    cat: "Blockchain & Distributed",
    items: [
      "SHA-256 chains",
      "Hyperledger",
      "Smart Contracts",
      "ReportLab PDF",
      "QR traceability",
    ],
  },
  {
    cat: "Languages",
    items: [
      "Portuguese (native)",
      "English (intermediate)",
      "Java",
      "Python",
      "TypeScript",
      "C",
    ],
  },
];

export default function SkillCards() {
  const { theme } = useTheme();
  const isAdmin = theme === "admin";
  return (
    <section
      className="section reveal"
      id="skills"
      aria-labelledby="skills-title"
    >
      <div className="container">
        <header className="section-header">
          <span className="section-num">01.</span>
          <h2 className="section-title" id="skills-title">
            {isAdmin ? "Stack" : "Skills"}
          </h2>
          <div className="section-rule" />
        </header>
        <div className="skills-grid">
          {SKILLS.map(({ cat, items }) => (
            <div className="skill-card" key={cat}>
              <p className="skill-cat t-label">{cat}</p>
              <ul className="skill-items">
                {items.map((i) => (
                  <li key={i} className="tag">
                    {i}
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
