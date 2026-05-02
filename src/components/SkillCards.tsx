import { useState } from "react";
import { useTheme } from "../context/ThemeContext";
import "./SkillCards.css";

const STACK_RADAR = [
  { axis: "Backend", score: 95, items: ["Java EE 8/17", "Spring Boot", "FastAPI", "Flask", "Node.js"] },
  { axis: "Frontend", score: 78, items: ["Angular 17+", "React", "TypeScript", "JSF/PrimeFaces", "Three.js"] },
  { axis: "DevSecOps", score: 88, items: ["Docker", "K8s", "Nginx", "Cloudflare Tunnel", "systemd", "CI/CD"] },
  { axis: "Data + AI", score: 84, items: ["PostgreSQL", "PostGIS", "Sentinel-2", "OpenAI", "Claude", "LangGraph"] },
  { axis: "Blockchain", score: 72, items: ["SHA-256 chains", "Hyperledger", "Smart Contracts", "QR traceability"] },
  { axis: "Security", score: 80, items: ["OWASP", "Pentest", "LGPD", "Cryptography", "PII masking"] },
];

function Radar({ active, setActive }: { active: number; setActive: (i: number) => void }) {
  const size = 480, cx = size / 2, cy = size / 2, R = 160;
  const N = STACK_RADAR.length;
  const angle = (i: number) => (Math.PI * 2 * i) / N - Math.PI / 2;
  const pt = (i: number, r: number): [number, number] => [
    cx + Math.cos(angle(i)) * r,
    cy + Math.sin(angle(i)) * r,
  ];

  const rings = [0.25, 0.5, 0.75, 1];
  const ringPts = (k: number) => STACK_RADAR.map((_, i) => pt(i, R * k).join(",")).join(" ");
  const polyPts = STACK_RADAR.map((s, i) => pt(i, R * (s.score / 100)).join(",")).join(" ");

  return (
    <svg viewBox={`0 0 ${size} ${size}`} className="radar-svg" aria-hidden="true">
      {rings.map((k, j) => (
        <polygon
          key={j}
          points={ringPts(k)}
          className={`radar__grid${j < rings.length - 1 ? " radar__grid--inner" : ""}`}
        />
      ))}
      {STACK_RADAR.map((_, i) => {
        const [x, y] = pt(i, R);
        return <line key={i} x1={cx} y1={cy} x2={x} y2={y} className="radar__spoke" />;
      })}
      {[25, 50, 75, 100].map((v, j) => (
        <text key={v} x={cx + 4} y={cy - R * rings[j] + 3} className="radar__legend">
          {v}
        </text>
      ))}
      <polygon points={polyPts} className="radar__poly" />
      {STACK_RADAR.map((s, i) => {
        const [x, y] = pt(i, R * (s.score / 100));
        return (
          <circle
            key={i}
            cx={x}
            cy={y}
            r={active === i ? 7 : 5}
            className="radar__dot"
            onMouseEnter={() => setActive(i)}
          />
        );
      })}
      {STACK_RADAR.map((s, i) => {
        const [x, y] = pt(i, R + 34);
        const a = angle(i);
        const anchor = Math.cos(a) > 0.3 ? "start" : Math.cos(a) < -0.3 ? "end" : "middle";
        return (
          <text
            key={i}
            x={x}
            y={y}
            textAnchor={anchor}
            dominantBaseline="middle"
            className="radar__axis-label"
            onMouseEnter={() => setActive(i)}
            style={{ cursor: "pointer", fill: active === i ? "var(--g)" : undefined }}
          >
            {s.axis}
          </text>
        );
      })}
    </svg>
  );
}

export default function SkillCards() {
  const { theme } = useTheme();
  const isAdmin = theme === "admin";
  const [active, setActive] = useState(0);

  return (
    <section className="section reveal" id="skills" aria-labelledby="skills-title">
      <div className="container">
        <header className="section-header">
          <span className="section-num">01.</span>
          <h2 className="section-title" id="skills-title">
            {isAdmin ? "Stack" : "Skills"}
          </h2>
          <div className="section-rule" />
          <span className="t-label">radar/v2</span>
        </header>
        <div className="stack-wrap">
          <div className="radar">
            <Radar active={active} setActive={setActive} />
          </div>
          <div className="stack-detail">
            {STACK_RADAR.map((s, i) => (
              <div
                key={s.axis}
                className={`stack-cat${active === i ? " active" : ""}`}
                onMouseEnter={() => setActive(i)}
                onClick={() => setActive(i)}
              >
                <div className="stack-cat__head">
                  <div className="stack-cat__name">{s.axis}</div>
                  <div className="stack-cat__score">{s.score}/100</div>
                </div>
                <div className="stack-cat__items">
                  {s.items.map((it) => (
                    <span key={it} className="tag">
                      {it}
                    </span>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
