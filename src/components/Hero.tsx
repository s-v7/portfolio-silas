import { useEffect, useRef, useState } from "react";
import { Link } from "react-router-dom";
import { useTheme } from "../context/ThemeContext";
import "./Hero.css";

// Canvas 2D particle system (replaces Three.js)
function useParticles(ref: React.RefObject<HTMLCanvasElement>, active: boolean) {
  useEffect(() => {
    if (!active) return;
    const canvas = ref.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;
    let raf: number;
    let w = 0, h = 0;
    const dpr = Math.min(window.devicePixelRatio || 1, 2);

    const resize = () => {
      w = canvas.offsetWidth;
      h = canvas.offsetHeight;
      canvas.width = w * dpr;
      canvas.height = h * dpr;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    };
    resize();
    window.addEventListener("resize", resize);

    const count = Math.min(120, Math.max(60, Math.floor((w * h) / 12000)));
    const pts = Array.from({ length: count }, () => ({
      x: Math.random() * w,
      y: Math.random() * h,
      vx: (Math.random() - 0.5) * 0.18,
      vy: (Math.random() - 0.5) * 0.18,
      r: Math.random() * 1.6 + 0.5,
    }));

    const tick = () => {
      ctx.clearRect(0, 0, w, h);
      pts.forEach((p) => {
        p.x += p.vx; p.y += p.vy;
        if (p.x < 0 || p.x > w) p.vx *= -1;
        if (p.y < 0 || p.y > h) p.vy *= -1;
      });
      ctx.lineWidth = 0.4;
      for (let i = 0; i < pts.length; i++) {
        for (let j = i + 1; j < pts.length; j++) {
          const a = pts[i], b = pts[j];
          const dx = a.x - b.x, dy = a.y - b.y;
          const d2 = dx * dx + dy * dy;
          if (d2 < 11000) {
            const o = 1 - d2 / 11000;
            ctx.strokeStyle = `rgba(29,158,117,${(o * 0.18).toFixed(3)})`;
            ctx.beginPath();
            ctx.moveTo(a.x, a.y);
            ctx.lineTo(b.x, b.y);
            ctx.stroke();
          }
        }
      }
      pts.forEach((p) => {
        ctx.fillStyle = "rgba(29,158,117,0.55)";
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
        ctx.fill();
      });
      raf = requestAnimationFrame(tick);
    };
    tick();

    return () => {
      cancelAnimationFrame(raf);
      window.removeEventListener("resize", resize);
    };
  }, [ref, active]);
}

// Abstract SV initials portrait (SVG/CSS-generated, no image files)
const PORTRAIT_GRID = (() => {
  const cells = Array<number>(80).fill(0);
  [1, 2, 3, 4, 5, 8, 16, 17, 18, 19, 20, 21, 30, 31, 33, 34, 35, 36, 38, 39].forEach((i) => { cells[i] = 1; });
  [42, 46, 49, 50, 53, 57, 60, 65, 67, 73].forEach((i) => { cells[i] = 1; });
  [0, 7, 40, 47, 72, 79].forEach((i) => { cells[i] = 2; });
  return cells;
})();

function Portrait({ isAdmin }: { isAdmin: boolean }) {
  const meta = [
    [isAdmin ? "FOCO" : "Focus", "Backend · AI"],
    [isAdmin ? "DESDE" : "Since", "2015"],
    [isAdmin ? "ARTs" : "Records", "1.1M+"],
    [isAdmin ? "NÓS" : "Nodes", "224 mun."],
  ] as const;
  return (
    <div className="hero__portrait">
      <div className="portrait">
        <div className="portrait__grid" aria-hidden="true">
          {PORTRAIT_GRID.map((v, i) => (
            <div key={i} className={`portrait__cell${v === 1 ? " on" : v === 2 ? " hi" : ""}`} />
          ))}
        </div>
        <div className="portrait__init">SV</div>
        <div className="portrait__caption">
          <span>TERESINA · PI</span>
          <span>—07.107°S</span>
        </div>
      </div>
      <div className="portrait__border" />
      <div className="hero__sidemeta">
        {meta.map(([label, value]) => (
          <div key={label} className="hero__sidemeta-row">
            <span>{label}</span>
            <span>{value}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

// Animated typing terminal
const TERM_LINES = [
  { prompt: true, txt: "whoami" },
  { prompt: false, txt: "Full Stack · DevSecOps · AI & Blockchain", val: true },
  { prompt: true, txt: "cat stack.txt" },
  { prompt: false, txt: "Java EE · Python · Angular · FastAPI · PostgreSQL", val: true },
  { prompt: true, txt: "ls projetos/" },
  { prompt: false, txt: "SIGEC-v2/  ART-Engine/  FiscalBot/  CadastroRastreamentoObras/", val: true },
  { prompt: true, txt: "uptime" },
  { prompt: false, txt: "847 days, 0 incidents · CREA-PI cluster", val: true },
];

function Terminal() {
  const [shown, setShown] = useState(0);
  useEffect(() => {
    if (shown >= TERM_LINES.length) return;
    const delay = shown === 0 ? 400 : shown % 2 ? 280 : 520;
    const id = setTimeout(() => setShown((s) => s + 1), delay);
    return () => clearTimeout(id);
  }, [shown]);

  return (
    <div className="terminal" role="img" aria-label="Terminal">
      <div className="terminal__bar" aria-hidden="true">
        <span className="tdot tdot--r" />
        <span className="tdot tdot--y" />
        <span className="tdot tdot--g" />
        <span className="terminal__title">~/s-v7 — bash</span>
      </div>
      {TERM_LINES.slice(0, shown).map((l, i) => (
        <div key={i} className={`terminal__line${l.val ? " terminal__line--val" : ""}`}>
          {l.prompt ? <span className="terminal__prompt">$ </span> : <span className="terminal__indent" />}
          <span>{l.txt}</span>
        </div>
      ))}
      {shown < TERM_LINES.length && (
        <div className="terminal__line">
          <span className="terminal__prompt">$ </span>
          <span className="terminal__cursor" aria-hidden="true" />
        </div>
      )}
    </div>
  );
}

const TICKER_ITEMS = [
  <><b>SIGEC v2</b> ARTs processed: <b>1,142,338</b></>,
  <>last block · <b>#0x3f7a91</b> · 12s ago</>,
  <>FiscalBot · cron · <b>mon 06:00 BRT</b></>,
  <>Sentinel-2 tiles · <b>20 reservoirs · NDWI ok</b></>,
  <>systemd · <b>8/8 services up</b></>,
  <>Cloudflare Tunnel · <b>edge:gru</b> · <b>43ms</b></>,
];

export default function Hero() {
  const canvasRef = useRef<HTMLCanvasElement>(null!);
  const { theme } = useTheme();
  const isAdmin = theme === "admin";
  useParticles(canvasRef, isAdmin);

  return (
    <section className="hero" aria-label="Apresentação">
      <canvas className="hero__canvas" ref={canvasRef} aria-hidden="true" />
      <div className="container hero__inner">
        <div>
          <p className="hero__meta">
            {isAdmin ? (
              <>
                <span className="text-accent">[ TERESINA, PI — BR ]</span>
                <span className="sep">·</span>
                Full Stack Engineer
                <span className="sep">·</span>
                CREA-PI
              </>
            ) : (
              <>
                Full Stack Engineer
                <span className="sep">·</span>
                Brazil
                <span className="sep">·</span>
                CREA-PI
              </>
            )}
          </p>

          {isAdmin ? (
            <h1 className="hero__name t-display">
              SILAS
              <br />
              VASCONCELOS
              <br />
            </h1>
          ) : (
            <h1 className="hero__name">
              Silas Vasconcelos
            </h1>
          )}

          <p className="hero__handle">
            <span className="status-dot" aria-hidden="true" />
            @s-v7 ·{" "}
            <a href="https://github.com/s-v7" target="_blank" rel="noreferrer">
              github.com/s-v7
            </a>
          </p>

          {isAdmin && <Terminal />}

          <p className="hero__tagline">
            Construo <strong>infraestrutura de software crítica</strong> — de
            modernização Java&nbsp;EE a pipelines de IA e blockchain para
            rastreabilidade de obras de engenharia.
          </p>

          <div className="hero__editorial">
            <p className="hero__quote">
              Building critical software infrastructure — from Java EE legacy
              modernization to AI pipelines and blockchain traceability.
            </p>
            <p className="hero__bio">
              Technology & Information Security Advisor at CREA-PI. Architect of
              the FIE ecosystem — 1.1M+ engineering records on-chain, Sentinel-2
              geospatial analytics, fiscal routing across 224 municipalities of
              Piauí.
            </p>
          </div>

          <div className="hero__cta">
            <Link className="btn btn-primary" to="/projects">
              {isAdmin ? "→ Ver Projetos" : "View Projects"}
            </Link>
            <a className="btn btn-ghost" href="/Silas_Vasconcelos_CV.pdf" download>
              {isAdmin ? "↓ Download CV" : "Download CV"}
            </a>
            <Link className="btn btn-ghost" to="/contact">
              {isAdmin ? "✉ Contato" : "Contact"}
            </Link>
          </div>
        </div>

        <Portrait isAdmin={isAdmin} />
      </div>

      <div className="ticker" aria-hidden="true">
        <div className="ticker__track">
          {[...TICKER_ITEMS, ...TICKER_ITEMS].map((item, i) => (
            <span key={i}>{item}</span>
          ))}
        </div>
      </div>
    </section>
  );
}
