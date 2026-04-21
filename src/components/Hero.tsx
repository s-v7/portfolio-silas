import { useEffect, useRef } from "react";
import { Link } from "react-router-dom";
import { useTheme } from "../context/ThemeContext";
import "./Hero.css";

const LINES = [
  { prompt: true, text: "whoami", color: "" },
  {
    prompt: false,
    text: "Full Stack · DevSecOps · AI & Blockchain",
    color: "val",
  },
  { prompt: true, text: "cat stack.txt", color: "" },
  {
    prompt: false,
    text: "Java EE · Python · Angular · FastAPI · PostgreSQL",
    color: "val",
  },
  { prompt: true, text: "ls projetos/", color: "" },
  {
    prompt: false,
    text: "SIGEC-v2/  SertLedger/  FiscalBot/  VoxPiaui/",
    color: "val",
  },
];

function useParticles(
  ref: React.RefObject<HTMLCanvasElement>,
  active: boolean,
) {
  useEffect(() => {
    if (!active) return;
    const canvas = ref.current;
    if (!canvas) return;
    let THREE: any;
    let animId: number;
    import("three").then((mod) => {
      THREE = mod;
      const renderer = new THREE.WebGLRenderer({
        canvas,
        alpha: true,
        antialias: false,
      });
      renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
      renderer.setSize(canvas.offsetWidth, canvas.offsetHeight);
      const scene = new THREE.Scene();
      const cam = new THREE.PerspectiveCamera(
        60,
        canvas.offsetWidth / canvas.offsetHeight,
        0.1,
        1000,
      );
      cam.position.z = 5;
      const pos = new Float32Array(600 * 3);
      for (let i = 0; i < 600; i++) {
        pos[i * 3] = (Math.random() - 0.5) * 20;
        pos[i * 3 + 1] = (Math.random() - 0.5) * 14;
        pos[i * 3 + 2] = (Math.random() - 0.5) * 10;
      }
      const geo = new THREE.BufferGeometry();
      geo.setAttribute("position", new THREE.BufferAttribute(pos, 3));
      const mat = new THREE.PointsMaterial({
        color: 0x1d9e75,
        size: 0.04,
        transparent: true,
        opacity: 0.45,
        sizeAttenuation: true,
      });
      const pts = new THREE.Points(geo, mat);
      scene.add(pts);
      const lp: number[] = [];
      for (let i = 0; i < 80; i++) {
        const x = (Math.random() - 0.5) * 20,
          y = (Math.random() - 0.5) * 14,
          z = (Math.random() - 0.5) * 5;
        lp.push(
          x,
          y,
          z,
          x + (Math.random() - 0.5) * 3,
          y + (Math.random() - 0.5) * 3,
          z,
        );
      }
      const lg = new THREE.BufferGeometry();
      lg.setAttribute(
        "position",
        new THREE.BufferAttribute(new Float32Array(lp), 3),
      );
      scene.add(
        new THREE.LineSegments(
          lg,
          new THREE.LineBasicMaterial({
            color: 0x1d9e75,
            transparent: true,
            opacity: 0.06,
          }),
        ),
      );
      const tick = () => {
        animId = requestAnimationFrame(tick);
        pts.rotation.y += 0.0004;
        pts.rotation.x += 0.0001;
        renderer.render(scene, cam);
      };
      tick();
      const onResize = () => {
        if (!canvas) return;
        renderer.setSize(canvas.offsetWidth, canvas.offsetHeight);
        cam.aspect = canvas.offsetWidth / canvas.offsetHeight;
        cam.updateProjectionMatrix();
      };
      window.addEventListener("resize", onResize);
      return () => {
        cancelAnimationFrame(animId);
        window.removeEventListener("resize", onResize);
        renderer.dispose();
      };
    });
    return () => cancelAnimationFrame(animId);
  }, [ref, active]);
}

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
                <span className="text-accent">[ TERESINA, PI — BR ]</span> ·
                Full Stack Engineer
              </>
            ) : (
              <>Full Stack Engineer · Teresina, Brazil</>
            )}
          </p>

          {isAdmin ? (
            <h1 className="hero__name t-display">
              SILAS
              <br />
              VASCONCELOS
              <br />
              <span className="text-accent">CRUZ</span>
            </h1>
          ) : (
            <h1 className="hero__name">
              Silas Vasconcelos
              <br />
              <em>Cruz</em>
            </h1>
          )}

          <p className="hero__handle">
            @s-v7 ·{" "}
            <a href="https://github.com/s-v7" target="_blank" rel="noreferrer">
              github.com/s-v7
            </a>
          </p>

          {/* Admin: terminal */}
          <div className="terminal" role="img" aria-label="Terminal">
            <div className="terminal__bar" aria-hidden="true">
              <span className="dot dot--red" />
              <span className="dot dot--amber" />
              <span className="dot dot--green" />
              <span className="terminal__title">~/s-v7 — bash</span>
            </div>
            {LINES.map((l, i) => (
              <div
                key={i}
                className={`terminal__line${l.color ? ` terminal__line--${l.color}` : ""}`}
              >
                {l.prompt ? (
                  <span className="terminal__prompt">$ </span>
                ) : (
                  <span className="terminal__indent" />
                )}
                <span>{l.text}</span>
              </div>
            ))}
            <div className="terminal__line">
              <span className="terminal__prompt">$ </span>
              <span className="terminal__cursor" aria-hidden="true" />
            </div>
          </div>

          {/* Admin: tagline */}
          <p className="hero__tagline">
            Construo <strong>infraestrutura de software crítica</strong> — de
            modernização Java&nbsp;EE a pipelines de IA e blockchain para
            rastreabilidade de obras de engenharia.
          </p>

          {/* Recruiter: editorial */}
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
            <a
              className="btn btn-ghost"
              href="/Silas_Vasconcelos_CV.pdf"
              download
            >
              {isAdmin ? "↓ Download CV" : "Download CV"}
            </a>
            <Link className="btn btn-ghost" to="/contact">
              {isAdmin ? "✉ Contato" : "Contact"}
            </Link>
          </div>
        </div>

        <div className="hero__photo-wrap" aria-hidden="true">
          <img
            src="/assets/images/profile.jpg"
            alt="Silas Vasconcelos Cruz"
            className="hero__photo"
            width={180}
            height={220}
          />
          <div className="hero__photo-border" />
          <span className="hero__photo-label">Teresina · PI</span>
        </div>
      </div>
    </section>
  );
}
