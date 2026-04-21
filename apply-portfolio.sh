#!/usr/bin/env bash
set -e
ROOT="$(pwd)/src"
echo "→ s▪v7 Portfolio — aplicando modernização dual-theme"
echo "  Destino: $ROOT"
echo ""

mkdir -p "$ROOT/styles" "$ROOT/components" "$ROOT/pages" "$ROOT/context"

# ════════════════════════════════════════════════════════════
# 1. DESIGN SYSTEM — DUAL THEME
# ════════════════════════════════════════════════════════════
cat > "$ROOT/styles/design-system.css" << 'EOF'
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@700;800&family=DM+Serif+Display:ital@0;1&family=Inter:wght@400;500;600&display=swap');

/* ── ADMIN THEME (default) ── */
[data-theme="admin"], :root {
  --g: #1D9E75;
  --g2: #0d6b50;
  --bg: #0a0d0b;
  --bg2: #0f1510;
  --bg3: #141a14;
  --line: rgba(29,158,117,0.15);
  --line2: rgba(29,158,117,0.08);
  --line-hi: rgba(29,158,117,0.35);
  --text: #e8ede8;
  --text-dim: #9aaa9a;
  --muted: #5c6e5c;
  --display: 'Syne', system-ui, sans-serif;
  --body: 'Space Mono', monospace;
  --mono: 'Space Mono', monospace;
  --nav-h: 52px;
  --max-w: 960px;
  --radius: 0px;
  --btn-radius: 0px;
}

/* ── RECRUITER THEME ── */
[data-theme="recruiter"] {
  --g: #E8890C;
  --g2: #d4780a;
  --bg: #141210;
  --bg2: #1c1915;
  --bg3: #221f1a;
  --line: rgba(232,137,12,0.14);
  --line2: rgba(232,137,12,0.07);
  --line-hi: rgba(232,137,12,0.35);
  --text: #f0ebe3;
  --text-dim: #a89880;
  --muted: #7a6f5e;
  --display: 'DM Serif Display', serif;
  --body: 'Inter', sans-serif;
  --mono: 'Space Mono', monospace;
  --radius: 3px;
  --btn-radius: 3px;
}

/* ── RESET ── */
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0;}
html{scroll-behavior:smooth;}
body{
  font-family:var(--body);
  background:var(--bg);
  color:var(--text);
  font-size:13px;
  line-height:1.6;
  -webkit-font-smoothing:antialiased;
  overflow-x:hidden;
  transition:background .3s ease, color .3s ease;
}

/* blueprint grid — admin only */
[data-theme="admin"] body::before{
  content:'';position:fixed;inset:0;
  background-image:
    linear-gradient(var(--line2) 1px,transparent 1px),
    linear-gradient(90deg,var(--line2) 1px,transparent 1px);
  background-size:40px 40px;
  pointer-events:none;z-index:0;
}

/* warm glow — recruiter only */
[data-theme="recruiter"] body::before{
  content:'';position:fixed;inset:0;
  background-image:radial-gradient(ellipse at 75% 10%,rgba(232,137,12,0.06) 0%,transparent 55%);
  pointer-events:none;z-index:0;
}

img{display:block;max-width:100%;}
a{color:var(--g);text-decoration:none;transition:color .15s;}
a:hover{color:var(--text);}
#root{min-height:100vh;display:flex;flex-direction:column;}
main{flex:1;position:relative;z-index:1;}
::-webkit-scrollbar{width:4px;}
::-webkit-scrollbar-track{background:var(--bg);}
::-webkit-scrollbar-thumb{background:var(--line-hi);}
::selection{background:rgba(29,158,117,.22);color:var(--text);}
[data-theme="recruiter"] ::selection{background:rgba(232,137,12,.18);}
:focus-visible{outline:2px solid var(--g);outline-offset:2px;}

/* ── TYPOGRAPHY ── */
.t-display{
  font-family:var(--display);
  font-weight:800;
  line-height:.92;
  letter-spacing:-2px;
}
[data-theme="recruiter"] .t-display{
  font-weight:400;
  line-height:1.05;
  letter-spacing:0;
  font-style:normal;
}
.t-heading{font-family:var(--display);font-weight:700;letter-spacing:-.8px;}
[data-theme="recruiter"] .t-heading{font-family:var(--display);font-weight:400;letter-spacing:0;}
.t-label{font-family:var(--mono);font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);}
[data-theme="recruiter"] .t-label{font-family:var(--body);font-size:10px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);}

/* ── LAYOUT ── */
.container{max-width:var(--max-w);margin:0 auto;padding:0 2rem;position:relative;z-index:1;}
.section{border-top:1px solid var(--line2);padding:3rem 0;}
.section-header{display:flex;align-items:baseline;gap:1rem;margin-bottom:2rem;}
.section-num{font-family:var(--mono);font-size:11px;color:var(--g);letter-spacing:.1em;flex-shrink:0;}
.section-title{font-family:var(--display);font-size:1.7rem;font-weight:700;letter-spacing:-1px;color:var(--text);}
[data-theme="recruiter"] .section-title{font-size:1.8rem;font-weight:400;letter-spacing:0;}
.section-rule{flex:1;height:1px;background:var(--line);}

/* ── BUTTONS ── */
.btn{
  display:inline-flex;align-items:center;gap:8px;
  padding:10px 22px;font-family:var(--mono);font-size:11px;
  letter-spacing:.08em;text-transform:uppercase;
  border-radius:var(--btn-radius);border:1px solid transparent;
  cursor:pointer;transition:all .2s;text-decoration:none;font-weight:700;
}
[data-theme="recruiter"] .btn{
  font-family:var(--body);font-size:12px;font-weight:600;
  letter-spacing:.02em;text-transform:none;
}
.btn-primary{background:var(--g);color:var(--bg);border-color:var(--g);}
.btn-primary:hover{background:transparent;color:var(--g);}
.btn-ghost{background:transparent;color:var(--text);border-color:rgba(255,255,255,.15);}
.btn-ghost:hover{border-color:var(--g);color:var(--g);}

/* ── TAGS ── */
.tag{
  display:inline-block;font-family:var(--mono);font-size:10px;
  padding:3px 8px;border:1px solid var(--line);color:var(--muted);
  letter-spacing:.05em;transition:all .15s;border-radius:var(--radius);
}
[data-theme="recruiter"] .tag{font-family:var(--body);font-size:10px;font-weight:500;}
.tag:hover,.tag-active{border-color:var(--g);color:var(--g);background:rgba(29,158,117,.06);}
[data-theme="recruiter"] .tag:hover,[data-theme="recruiter"] .tag-active{background:rgba(232,137,12,.06);}

/* ── STATUS DOT ── */
.status-dot{display:inline-block;width:6px;height:6px;border-radius:50%;background:var(--g);animation:pulse 2s ease-in-out infinite;}
@keyframes pulse{0%,100%{opacity:1;}50%{opacity:.35;}}
@keyframes blink{0%,100%{opacity:1;}50%{opacity:0;}}

/* ── REVEAL ── */
.reveal{opacity:0;transform:translateY(20px);transition:opacity .5s ease,transform .5s ease;}
.reveal.visible{opacity:1;transform:none;}

.sr-only{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0;}
.text-accent{color:var(--g);}
.text-muted{color:var(--muted);}
EOF

cat > "$ROOT/styles/global.css" << 'EOF'
@import './design-system.css';
EOF

cat > "$ROOT/index.css" << 'EOF'
@import './styles/global.css';
EOF

echo "  ✓ design-system.css (dual theme)"

# ════════════════════════════════════════════════════════════
# 2. THEME CONTEXT
# ════════════════════════════════════════════════════════════
cat > "$ROOT/context/ThemeContext.tsx" << 'EOF'
import { createContext, useContext, useEffect, useState } from 'react';

type Theme = 'admin' | 'recruiter';

interface ThemeCtx { theme: Theme; toggle: () => void; }

const Ctx = createContext<ThemeCtx>({ theme: 'admin', toggle: () => {} });

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setTheme] = useState<Theme>(() => {
    const saved = localStorage.getItem('sv7-theme') as Theme | null;
    return saved === 'recruiter' ? 'recruiter' : 'admin';
  });

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('sv7-theme', theme);
  }, [theme]);

  const toggle = () => setTheme(t => t === 'admin' ? 'recruiter' : 'admin');

  return <Ctx.Provider value={{ theme, toggle }}>{children}</Ctx.Provider>;
}

export const useTheme = () => useContext(Ctx);
EOF

echo "  ✓ ThemeContext.tsx"

# ════════════════════════════════════════════════════════════
# 3. NAVBAR + THEME TOGGLE
# ════════════════════════════════════════════════════════════
cat > "$ROOT/components/Navbar.css" << 'EOF'
.nav{
  position:sticky;top:0;z-index:200;height:var(--nav-h);
  background:rgba(10,13,11,.88);
  backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px);
  border-bottom:1px solid var(--line);
  transition:background .3s;
}
[data-theme="recruiter"] .nav{background:rgba(20,18,16,.9);}
.nav-inner{height:100%;display:flex;align-items:center;justify-content:space-between;gap:1.5rem;}
.nav-brand{text-decoration:none;flex-shrink:0;}
.nav-brand-admin{font-family:'Syne',sans-serif;font-weight:800;font-size:16px;color:var(--g);letter-spacing:-.5px;}
.nav-brand-admin span{color:var(--text);opacity:.35;}
.nav-brand-rec{font-family:'DM Serif Display',serif;font-size:18px;color:var(--text);}
.nav-brand-rec em{color:var(--g);font-style:italic;}
.nav-links{display:flex;list-style:none;height:var(--nav-h);margin:0;padding:0;}
.nav-link{
  display:flex;align-items:center;height:100%;padding:0 14px;
  font-family:var(--mono);font-size:10px;letter-spacing:.08em;text-transform:uppercase;
  color:var(--muted);text-decoration:none;
  border-bottom:2px solid transparent;
  transition:color .15s,border-color .15s;white-space:nowrap;
}
[data-theme="recruiter"] .nav-link{font-family:'Inter',sans-serif;text-transform:none;font-size:11px;font-weight:500;letter-spacing:.02em;}
.nav-link:hover{color:var(--text-dim);}
.nav-link--active{color:var(--g);border-bottom-color:var(--g);}
.nav-right{display:flex;align-items:center;gap:10px;flex-shrink:0;}
.nav-status{display:flex;align-items:center;gap:5px;font-family:var(--mono);font-size:10px;color:var(--muted);}
[data-theme="recruiter"] .nav-status{font-family:'Inter',sans-serif;}
.theme-toggle{
  width:28px;height:28px;border:1px solid var(--line);background:var(--bg3);
  display:flex;align-items:center;justify-content:center;
  cursor:pointer;transition:border-color .2s,background .2s;flex-shrink:0;
  border-radius:var(--radius);
}
.theme-toggle:hover{border-color:var(--g);background:var(--bg2);}
.theme-toggle svg{width:14px;height:14px;stroke:var(--muted);fill:none;stroke-width:1.5;stroke-linecap:round;}
@media(max-width:768px){.nav-links{display:none;}.nav-status{display:none;}}
EOF

cat > "$ROOT/components/Navbar.tsx" << 'EOF'
import { NavLink } from 'react-router-dom';
import { useTheme } from '../context/ThemeContext';
import './Navbar.css';

const LINKS_ADMIN = [
  {to:'/',          label:'Home'},
  {to:'/profile',   label:'Profile / CV'},
  {to:'/education', label:'Education'},
  {to:'/projects',  label:'Projects'},
  {to:'/art-engine',label:'ART Engine'},
  {to:'/contact',   label:'Contact'},
];
const LINKS_REC = [
  {to:'/',          label:'Home'},
  {to:'/profile',   label:'Profile'},
  {to:'/education', label:'Education'},
  {to:'/projects',  label:'Projects'},
  {to:'/art-engine',label:'ART Engine'},
  {to:'/contact',   label:'Contact'},
];

function IconAdmin() {
  return (
    <svg viewBox="0 0 16 16" aria-hidden="true">
      <circle cx="8" cy="8" r="3.5" stroke="currentColor"/>
      <line x1="8" y1="1" x2="8" y2="3"/><line x1="8" y1="13" x2="8" y2="15"/>
      <line x1="1" y1="8" x2="3" y2="8"/><line x1="13" y1="8" x2="15" y2="8"/>
      <line x1="3.4" y1="3.4" x2="4.8" y2="4.8"/><line x1="11.2" y1="11.2" x2="12.6" y2="12.6"/>
      <line x1="3.4" y1="12.6" x2="4.8" y2="11.2"/><line x1="11.2" y1="4.8" x2="12.6" y2="3.4"/>
    </svg>
  );
}
function IconRec() {
  return (
    <svg viewBox="0 0 16 16" aria-hidden="true">
      <path d="M8 2a6 6 0 1 0 0 12A6 6 0 0 0 8 2zm0 1.5v9A4.5 4.5 0 0 1 8 3.5z" stroke="currentColor" fill="none"/>
    </svg>
  );
}

export default function Navbar() {
  const { theme, toggle } = useTheme();
  const isRec = theme === 'recruiter';
  const links = isRec ? LINKS_REC : LINKS_ADMIN;

  return (
    <header className="nav">
      <div className="nav-inner container">
        <a href="/" className="nav-brand" aria-label="home">
          {isRec
            ? <span className="nav-brand-rec">Silas <em>Cruz</em></span>
            : <span className="nav-brand-admin">s<span>▪</span>v7</span>
          }
        </a>
        <nav aria-label="Main navigation">
          <ul className="nav-links">
            {links.map(({to,label}) => (
              <li key={to}>
                <NavLink to={to} end={to==='/'} className={({isActive})=>`nav-link${isActive?' nav-link--active':''}`}>
                  {label}
                </NavLink>
              </li>
            ))}
          </ul>
        </nav>
        <div className="nav-right">
          <div className="nav-status" aria-label="Available for work">
            <span className="status-dot" aria-hidden="true"/>
            <span>{isRec ? 'open to work' : 'available'}</span>
          </div>
          <button
            className="theme-toggle"
            onClick={toggle}
            aria-label={`Switch to ${isRec ? 'admin' : 'recruiter'} theme`}
            title={isRec ? 'Switch to Admin theme' : 'Switch to Recruiter theme'}
          >
            {isRec ? <IconAdmin/> : <IconRec/>}
          </button>
        </div>
      </div>
    </header>
  );
}
EOF

echo "  ✓ Navbar + ThemeToggle"

# ════════════════════════════════════════════════════════════
# 4. HERO
# ════════════════════════════════════════════════════════════
cat > "$ROOT/components/Hero.css" << 'EOF'
.hero{position:relative;overflow:hidden;padding:4rem 0 3rem;min-height:calc(100vh - var(--nav-h));display:flex;align-items:center;}
.hero__canvas{position:absolute;inset:0;width:100%;height:100%;pointer-events:none;z-index:0;opacity:.7;}
[data-theme="recruiter"] .hero__canvas{display:none;}
.hero__inner{position:relative;z-index:1;display:grid;grid-template-columns:1fr 200px;gap:3rem;align-items:start;}
.hero__meta{font-family:var(--mono);font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);margin-bottom:1rem;}
[data-theme="recruiter"] .hero__meta{font-family:'Inter',sans-serif;font-weight:500;letter-spacing:.04em;text-transform:none;font-size:11px;}
.hero__name{color:var(--text);margin-bottom:.5rem;}
[data-theme="admin"] .hero__name{font-family:'Syne',sans-serif;font-size:clamp(2.8rem,6vw,4.5rem);font-weight:800;line-height:.92;letter-spacing:-2px;}
[data-theme="recruiter"] .hero__name{font-family:'DM Serif Display',serif;font-size:clamp(2.4rem,5vw,3.8rem);font-weight:400;line-height:1.05;letter-spacing:0;}
[data-theme="recruiter"] .hero__name em{color:var(--g);font-style:italic;}
.hero__handle{font-family:var(--mono);font-size:12px;color:var(--g);margin-bottom:1.5rem;letter-spacing:.04em;}
[data-theme="recruiter"] .hero__handle{font-family:'Inter',sans-serif;font-size:12px;font-weight:500;}
.hero__handle a{color:var(--g);}
.hero__handle a:hover{color:var(--text);}
.terminal{background:var(--bg2);border:1px solid var(--line);padding:1rem;margin-bottom:1.5rem;max-width:520px;}
[data-theme="recruiter"] .terminal{display:none;}
.terminal__bar{display:flex;align-items:center;gap:5px;margin-bottom:10px;}
.dot{width:8px;height:8px;border-radius:50%;flex-shrink:0;}
.dot--red{background:#ff5f57;}.dot--amber{background:#febc2e;}.dot--green{background:#28c840;}
.terminal__title{font-size:10px;color:var(--muted);margin-left:6px;}
.terminal__line{font-family:var(--mono);font-size:11px;color:var(--muted);line-height:1.9;display:flex;align-items:center;}
.terminal__line--val{color:#5dd8a3;}
.terminal__prompt{color:var(--g);flex-shrink:0;}
.terminal__indent{display:inline-block;width:1.1em;flex-shrink:0;}
.terminal__cursor{display:inline-block;width:7px;height:13px;background:var(--g);vertical-align:middle;margin-left:1px;animation:blink 1s step-end infinite;}
.hero__editorial{display:none;}
[data-theme="recruiter"] .hero__editorial{display:block;margin-bottom:1.5rem;}
.hero__quote{font-family:'DM Serif Display',serif;font-size:1.1rem;color:var(--text);line-height:1.5;border-left:2px solid var(--g);padding-left:1rem;font-style:italic;margin-bottom:.75rem;}
.hero__bio{font-family:'Inter',sans-serif;font-size:13px;color:var(--text-dim);line-height:1.7;padding-left:1rem;}
.hero__tagline{font-family:'Syne',sans-serif;font-size:1rem;color:var(--muted);max-width:500px;line-height:1.65;border-left:2px solid var(--g);padding-left:1rem;margin-bottom:1.5rem;}
[data-theme="recruiter"] .hero__tagline{display:none;}
.hero__tagline strong{color:var(--text);font-weight:600;}
.hero__cta{display:flex;gap:12px;flex-wrap:wrap;}
.hero__photo-wrap{position:relative;padding-top:1.5rem;}
.hero__photo{width:180px;height:220px;object-fit:cover;object-position:top center;filter:grayscale(15%) contrast(1.05);border:1px solid var(--line);}
[data-theme="recruiter"] .hero__photo{filter:sepia(10%) contrast(1.02);border-color:var(--line);}
.hero__photo-border{position:absolute;bottom:-10px;right:-10px;width:180px;height:220px;border:1px solid var(--g);pointer-events:none;top:calc(1.5rem + 10px);}
.hero__photo-label{position:absolute;bottom:-28px;left:0;font-family:var(--mono);font-size:10px;color:var(--g);letter-spacing:.1em;text-transform:uppercase;}
[data-theme="recruiter"] .hero__photo-label{font-family:'Inter',sans-serif;text-transform:none;letter-spacing:.02em;}
@media(max-width:640px){.hero__inner{grid-template-columns:1fr;}.hero__photo-wrap{display:none;}.hero{min-height:auto;padding:3rem 0;}}
EOF

cat > "$ROOT/components/Hero.tsx" << 'EOF'
import { useEffect, useRef } from 'react';
import { Link } from 'react-router-dom';
import { useTheme } from '../context/ThemeContext';
import './Hero.css';

const LINES = [
  {prompt:true, text:'whoami',                                            color:''},
  {prompt:false,text:'Full Stack · DevSecOps · AI & Blockchain',         color:'val'},
  {prompt:true, text:'cat stack.txt',                                     color:''},
  {prompt:false,text:'Java EE · Python · Angular · FastAPI · PostgreSQL', color:'val'},
  {prompt:true, text:'ls projetos/',                                      color:''},
  {prompt:false,text:'SIGEC-v2/  SertLedger/  FiscalBot/  VoxPiaui/',    color:'val'},
];

function useParticles(ref: React.RefObject<HTMLCanvasElement>, active: boolean) {
  useEffect(() => {
    if (!active) return;
    const canvas = ref.current;
    if (!canvas) return;
    let THREE: any;
    let animId: number;
    import('three').then(mod => {
      THREE = mod;
      const renderer = new THREE.WebGLRenderer({canvas, alpha:true, antialias:false});
      renderer.setPixelRatio(Math.min(window.devicePixelRatio,2));
      renderer.setSize(canvas.offsetWidth, canvas.offsetHeight);
      const scene = new THREE.Scene();
      const cam = new THREE.PerspectiveCamera(60, canvas.offsetWidth/canvas.offsetHeight, .1, 1000);
      cam.position.z = 5;
      const pos = new Float32Array(600*3);
      for (let i=0;i<600;i++){pos[i*3]=(Math.random()-.5)*20;pos[i*3+1]=(Math.random()-.5)*14;pos[i*3+2]=(Math.random()-.5)*10;}
      const geo = new THREE.BufferGeometry();
      geo.setAttribute('position',new THREE.BufferAttribute(pos,3));
      const mat = new THREE.PointsMaterial({color:0x1D9E75,size:.04,transparent:true,opacity:.45,sizeAttenuation:true});
      const pts = new THREE.Points(geo,mat);
      scene.add(pts);
      const lp:number[]=[];
      for(let i=0;i<80;i++){const x=(Math.random()-.5)*20,y=(Math.random()-.5)*14,z=(Math.random()-.5)*5;lp.push(x,y,z,x+(Math.random()-.5)*3,y+(Math.random()-.5)*3,z);}
      const lg=new THREE.BufferGeometry();
      lg.setAttribute('position',new THREE.BufferAttribute(new Float32Array(lp),3));
      scene.add(new THREE.LineSegments(lg,new THREE.LineBasicMaterial({color:0x1D9E75,transparent:true,opacity:.06})));
      const tick=()=>{animId=requestAnimationFrame(tick);pts.rotation.y+=.0004;pts.rotation.x+=.0001;renderer.render(scene,cam);};
      tick();
      const onResize=()=>{if(!canvas)return;renderer.setSize(canvas.offsetWidth,canvas.offsetHeight);cam.aspect=canvas.offsetWidth/canvas.offsetHeight;cam.updateProjectionMatrix();};
      window.addEventListener('resize',onResize);
      return ()=>{cancelAnimationFrame(animId);window.removeEventListener('resize',onResize);renderer.dispose();};
    });
    return ()=>cancelAnimationFrame(animId);
  },[ref,active]);
}

export default function Hero() {
  const canvasRef = useRef<HTMLCanvasElement>(null!);
  const {theme} = useTheme();
  const isAdmin = theme === 'admin';
  useParticles(canvasRef, isAdmin);

  return (
    <section className="hero" aria-label="Apresentação">
      <canvas className="hero__canvas" ref={canvasRef} aria-hidden="true"/>
      <div className="container hero__inner">
        <div>
          <p className="hero__meta">
            {isAdmin
              ? <><span className="text-accent">[ TERESINA, PI — BR ]</span> · Full Stack Engineer</>
              : <>Full Stack Engineer · Teresina, Brazil</>
            }
          </p>

          {isAdmin ? (
            <h1 className="hero__name t-display">
              SILAS<br/>VASCONCELOS<br/><span className="text-accent">CRUZ</span>
            </h1>
          ) : (
            <h1 className="hero__name">
              Silas Vasconcelos<br/><em>Cruz</em>
            </h1>
          )}

          <p className="hero__handle">
            @s-v7 · <a href="https://github.com/s-v7" target="_blank" rel="noreferrer">github.com/s-v7</a>
          </p>

          {/* Admin: terminal */}
          <div className="terminal" role="img" aria-label="Terminal">
            <div className="terminal__bar" aria-hidden="true">
              <span className="dot dot--red"/><span className="dot dot--amber"/><span className="dot dot--green"/>
              <span className="terminal__title">~/s-v7 — bash</span>
            </div>
            {LINES.map((l,i)=>(
              <div key={i} className={`terminal__line${l.color?` terminal__line--${l.color}`:''}`}>
                {l.prompt?<span className="terminal__prompt">$ </span>:<span className="terminal__indent"/>}
                <span>{l.text}</span>
              </div>
            ))}
            <div className="terminal__line"><span className="terminal__prompt">$ </span><span className="terminal__cursor" aria-hidden="true"/></div>
          </div>

          {/* Admin: tagline */}
          <p className="hero__tagline">
            Construo <strong>infraestrutura de software crítica</strong> — de modernização Java&nbsp;EE a pipelines de IA e blockchain para rastreabilidade de obras de engenharia.
          </p>

          {/* Recruiter: editorial */}
          <div className="hero__editorial">
            <p className="hero__quote">Building critical software infrastructure — from Java EE legacy modernization to AI pipelines and blockchain traceability.</p>
            <p className="hero__bio">Technology & Information Security Advisor at CREA-PI. Architect of the FIE ecosystem — 1.1M+ engineering records on-chain, Sentinel-2 geospatial analytics, fiscal routing across 224 municipalities of Piauí.</p>
          </div>

          <div className="hero__cta">
            <Link className="btn btn-primary" to="/projects">{isAdmin?'→ Ver Projetos':'View Projects'}</Link>
            <a className="btn btn-ghost" href="/Silas_Vasconcelos_CV.pdf" download>{isAdmin?'↓ Download CV':'Download CV'}</a>
            <Link className="btn btn-ghost" to="/contact">{isAdmin?'✉ Contato':'Contact'}</Link>
          </div>
        </div>

        <div className="hero__photo-wrap" aria-hidden="true">
          <img src="/assets/images/profile.jpg" alt="Silas Vasconcelos Cruz" className="hero__photo" width={180} height={220}/>
          <div className="hero__photo-border"/>
          <span className="hero__photo-label">Teresina · PI</span>
        </div>
      </div>
    </section>
  );
}
EOF

echo "  ✓ Hero (dual-theme)"

# ════════════════════════════════════════════════════════════
# 5. SKILL CARDS
# ════════════════════════════════════════════════════════════
cat > "$ROOT/components/SkillCards.css" << 'EOF'
.skills-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:1px;background:var(--line);border:1px solid var(--line);}
.skill-card{background:var(--bg);padding:1.25rem;transition:background .2s;}
.skill-card:hover{background:var(--bg3);}
.skill-cat{margin-bottom:10px;}
.skill-items{display:flex;flex-wrap:wrap;gap:6px;list-style:none;padding:0;margin:0;}
@media(max-width:600px){.skills-grid{grid-template-columns:1fr;}}
EOF

cat > "$ROOT/components/SkillCards.tsx" << 'EOF'
import { useTheme } from '../context/ThemeContext';
import './SkillCards.css';

const SKILLS = [
  {cat:'Backend & Architecture', items:['Java EE 8','JSF / PrimeFaces','Spring Boot','FastAPI','Python','Node.js']},
  {cat:'Frontend',               items:['Angular 17+','React','TypeScript','Three.js','Leaflet','XHTML / CSS']},
  {cat:'DevOps & Infra',         items:['Docker','Kubernetes','Nginx','Cloudflare Tunnel','Linux / systemd','CI/CD']},
  {cat:'Data, AI & Security',    items:['PostgreSQL','PostGIS','Sentinel-2','NumPy / Pandas','OpenAI API','Pentest / OWASP']},
  {cat:'Blockchain & Distributed',items:['SHA-256 chains','Hyperledger','Smart Contracts','ReportLab PDF','QR traceability']},
  {cat:'Languages',              items:['Portuguese (native)','English (intermediate)','Java','Python','TypeScript','C']},
];

export default function SkillCards() {
  const {theme} = useTheme();
  const isAdmin = theme === 'admin';
  return (
    <section className="section reveal" id="skills" aria-labelledby="skills-title">
      <div className="container">
        <header className="section-header">
          <span className="section-num">01.</span>
          <h2 className="section-title" id="skills-title">{isAdmin?'Stack':'Skills'}</h2>
          <div className="section-rule"/>
        </header>
        <div className="skills-grid">
          {SKILLS.map(({cat,items})=>(
            <div className="skill-card" key={cat}>
              <p className="skill-cat t-label">{cat}</p>
              <ul className="skill-items">{items.map(i=><li key={i} className="tag">{i}</li>)}</ul>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
EOF

echo "  ✓ SkillCards"

# ════════════════════════════════════════════════════════════
# 6. WHATIDO
# ════════════════════════════════════════════════════════════
cat > "$ROOT/components/WhatIDo.css" << 'EOF'
.projects-list{display:flex;flex-direction:column;gap:1px;background:var(--line);border:1px solid var(--line);margin-bottom:1rem;}
.project-card{display:grid;grid-template-columns:1fr auto;gap:1.5rem;align-items:start;padding:1.5rem;background:var(--bg);text-decoration:none;color:inherit;transition:background .2s;border-left:2px solid transparent;}
.project-card:hover{background:var(--bg3);border-left-color:var(--g);}
.project-card--featured{border-left:2px solid var(--g);background:var(--bg2);}
.project-card__tag{margin-bottom:6px;}
.project-card__title{font-size:1.05rem;color:var(--text);margin-bottom:8px;letter-spacing:-.3px;}
[data-theme="recruiter"] .project-card__title{font-family:'DM Serif Display',serif;font-size:1.1rem;letter-spacing:0;}
.project-card__desc{font-size:12px;color:var(--muted);line-height:1.65;max-width:520px;}
.project-card__meta{display:flex;flex-direction:column;align-items:flex-end;gap:6px;}
.project-card__stack{display:flex;flex-direction:column;align-items:flex-end;gap:4px;list-style:none;padding:0;margin:0;}
.project-card__arrow{font-size:18px;color:var(--g);margin-top:4px;}
.projects-footer{display:flex;justify-content:flex-end;margin-top:.75rem;}
@media(max-width:600px){.project-card{grid-template-columns:1fr;}.project-card__meta{flex-direction:row;flex-wrap:wrap;}.project-card__stack{flex-direction:row;}}
EOF

cat > "$ROOT/components/WhatIDo.tsx" << 'EOF'
import { Link } from 'react-router-dom';
import { useTheme } from '../context/ThemeContext';
import './WhatIDo.css';

const PROJECTS = [
  {tag:'Fiscal Intelligence · CREA-PI',  title:'SIGEC v2 — Fiscal Intelligence Engine',  desc:'1.1M+ ARTs em blockchain SHA-256, pipeline Sentinel-2→PostGIS para monitoramento hídrico, FiscalBot Telegram e roteamento NetworkX/TSP nos 224 municípios do Piauí.',stack:['Flask + FastAPI','Angular 17','PostgreSQL','Blockchain','PostGIS'],href:'/projects#sigec',featured:true},
  {tag:'Energy · Fintech · Piauí',       title:'SertLedgerToken',                          desc:'Marketplace para tokenização de energia solar sob Lei 14.300/2022. Tokens SHA-256 encadeados, certificados PDF + QR, R$0,65/kWh.',stack:['Flask','Angular 19','SHA-256','ReportLab'],href:'/projects#sertledger',featured:false},
  {tag:'Legacy Modernization',            title:'SistemaCrea — Jakarta EE',                 desc:'Modernização de ERP institucional: Maven EAR, integração e-MEC (4.328 IES), JSF/PrimeFaces 13 com design system CSS variables.',stack:['Java EE 8','JSF/PrimeFaces','Payara 6','PostgreSQL'],href:'/projects#sistemacrea',featured:false},
  {tag:'AI · Telegram',                  title:'FiscalBot & ART Engine',                   desc:'Bot Telegram operacional com alertas automáticos (cron seg 06:00 BRT), processamento de ARTs em massa e motor OpenAI + Claude.',stack:['FastAPI','Telegram API','OpenAI','Claude API'],href:'/art-engine',featured:false},
];

export default function WhatIDo() {
  const {theme} = useTheme();
  const isAdmin = theme === 'admin';
  return (
    <section className="section reveal" id="projects" aria-labelledby="whatido-title">
      <div className="container">
        <header className="section-header">
          <span className="section-num">02.</span>
          <h2 className="section-title" id="whatido-title">{isAdmin?'Projetos':'Projects'}</h2>
          <div className="section-rule"/>
        </header>
        <div className="projects-list">
          {PROJECTS.map(p=>(
            <Link key={p.title} to={p.href} className={`project-card${p.featured?' project-card--featured':''}`}>
              <div>
                <p className="project-card__tag t-label">{p.tag}</p>
                <h3 className="project-card__title t-heading">{p.title}</h3>
                <p className="project-card__desc">{p.desc}</p>
              </div>
              <div className="project-card__meta">
                <ul className="project-card__stack">{p.stack.map(t=><li key={t} className="tag">{t}</li>)}</ul>
                <span className="project-card__arrow" aria-hidden="true">→</span>
              </div>
            </Link>
          ))}
        </div>
        <div className="projects-footer">
          <Link className="btn btn-ghost" to="/projects">{isAdmin?'Ver todos →':'All projects →'}</Link>
        </div>
      </div>
    </section>
  );
}
EOF

echo "  ✓ WhatIDo"

# ════════════════════════════════════════════════════════════
# 7. CTA SECTION
# ════════════════════════════════════════════════════════════
cat > "$ROOT/components/CTASection.css" << 'EOF'
.exp-list{margin-bottom:3rem;}
.exp-item{display:grid;grid-template-columns:160px 1fr;gap:2rem;padding:1.5rem 0;border-bottom:1px solid var(--line2);}
.exp-item:last-child{border-bottom:none;}
.exp-date{padding-top:3px;line-height:1.5;}
.exp-role{font-size:.95rem;color:var(--text);margin-bottom:4px;}
[data-theme="recruiter"] .exp-role{font-family:'DM Serif Display',serif;font-size:1.05rem;}
.exp-org{font-family:var(--mono);font-size:11px;color:var(--g);letter-spacing:.04em;margin-bottom:10px;}
[data-theme="recruiter"] .exp-org{font-family:'Inter',sans-serif;font-weight:600;}
.exp-desc{font-size:12px;color:var(--muted);line-height:1.7;}
.cta-banner{border:1px solid var(--line);background:var(--bg2);padding:2rem;display:flex;align-items:center;justify-content:space-between;gap:1.5rem;flex-wrap:wrap;}
.cta-banner__headline{font-size:1.05rem;color:var(--text);max-width:380px;}
[data-theme="recruiter"] .cta-banner__headline{font-family:'DM Serif Display',serif;font-size:1.2rem;}
.cta-banner__actions{display:flex;gap:12px;flex-wrap:wrap;}
@media(max-width:640px){.exp-item{grid-template-columns:1fr;gap:4px;}.cta-banner{flex-direction:column;align-items:flex-start;}}
EOF

cat > "$ROOT/components/CTASection.tsx" << 'EOF'
import { Link } from 'react-router-dom';
import { useTheme } from '../context/ThemeContext';
import './CTASection.css';

const EXP = [
  {date:'May 2024 — Present',role:'Technology & Information Security Advisor',org:'CREA-PI · Teresina, Brasil',desc:'Arquiteto solo do ecossistema FIE — SIGEC v2, FiscalBot, ART Engine, SistemaCrea. Modernização Java EE, análise de segurança e pipeline Sentinel-2 para monitoramento hídrico piauiense.'},
  {date:'May 2022 — Sep 2022',role:'Java Full Stack Developer',org:'EDM Software · Florianópolis, Brasil',desc:'Desenvolvimento e manutenção de aplicações enterprise JSF/PrimeFaces, correção de bugs e suporte a melhorias contínuas no produto principal.'},
];

export default function CTASection() {
  const {theme} = useTheme();
  const isAdmin = theme==='admin';
  return (
    <section className="section reveal" id="experience" aria-labelledby="exp-title">
      <div className="container">
        <header className="section-header">
          <span className="section-num">03.</span>
          <h2 className="section-title" id="exp-title">{isAdmin?'Experiência':'Experience'}</h2>
          <div className="section-rule"/>
        </header>
        <div className="exp-list">
          {EXP.map(e=>(
            <article key={e.role} className="exp-item">
              <time className="exp-date t-label">{e.date}</time>
              <div>
                <h3 className="exp-role t-heading">{e.role}</h3>
                <p className="exp-org">{e.org}</p>
                <p className="exp-desc">{e.desc}</p>
              </div>
            </article>
          ))}
        </div>
        <div className="cta-banner">
          <div>
            <p className="t-label" style={{marginBottom:'6px'}}>{isAdmin?'Próximos passos':'Next steps'}</p>
            <p className="cta-banner__headline t-heading">{isAdmin?'Disponível para projetos e colaborações em 2026':'Open to senior engineering roles and consulting in 2026'}</p>
          </div>
          <div className="cta-banner__actions">
            <Link className="btn btn-primary" to="/contact">{isAdmin?'✉ Entre em Contato':'Get in touch'}</Link>
            <a className="btn btn-ghost" href="/Silas_Vasconcelos_CV.pdf" download>{isAdmin?'↓ Download CV':'Download CV'}</a>
          </div>
        </div>
      </div>
    </section>
  );
}
EOF

echo "  ✓ CTASection"

# ════════════════════════════════════════════════════════════
# 8. FOOTER
# ════════════════════════════════════════════════════════════
cat > "$ROOT/components/Footer.css" << 'EOF'
.footer{position:relative;z-index:1;border-top:1px solid var(--line);padding:1.5rem 0;}
.footer__inner{display:flex;align-items:center;justify-content:space-between;gap:1.5rem;flex-wrap:wrap;}
.footer__copy{font-size:11px;color:var(--muted);}
[data-theme="recruiter"] .footer__copy{font-family:'Inter',sans-serif;}
.footer__links{display:flex;gap:1.5rem;}
.footer__links a{font-family:var(--mono);font-size:11px;color:var(--muted);text-decoration:none;letter-spacing:.06em;text-transform:uppercase;transition:color .15s;}
[data-theme="recruiter"] .footer__links a{font-family:'Inter',sans-serif;text-transform:none;letter-spacing:.02em;}
.footer__links a:hover{color:var(--g);}
.footer__sig{font-family:'Syne',sans-serif;font-size:14px;font-weight:800;color:var(--g);letter-spacing:-.5px;}
[data-theme="recruiter"] .footer__sig{font-family:'DM Serif Display',serif;font-size:16px;font-weight:400;font-style:italic;}
EOF

cat > "$ROOT/components/Footer.tsx" << 'EOF'
import { useTheme } from '../context/ThemeContext';
import './Footer.css';
export default function Footer() {
  const {theme} = useTheme();
  const isAdmin = theme==='admin';
  const year = new Date().getFullYear();
  return (
    <footer className="footer">
      <div className="container footer__inner">
        <span className="footer__copy">© {year} Silas Vasconcelos Cruz · Teresina, PI</span>
        <div className="footer__links">
          <a href="https://github.com/s-v7" target="_blank" rel="noreferrer">GitHub</a>
          <a href="https://linkedin.com/in/s-v7" target="_blank" rel="noreferrer">LinkedIn</a>
          <a href="mailto:svasconceloscruz7@gmail.com">{isAdmin?'Email':'Email'}</a>
        </div>
        <span className="footer__sig">{isAdmin?'s▪v7':'Silas Cruz'}</span>
      </div>
    </footer>
  );
}
EOF

echo "  ✓ Footer"

# ════════════════════════════════════════════════════════════
# 9. SCROLL TO TOP
# ════════════════════════════════════════════════════════════
cat > "$ROOT/components/ScrollToTop.tsx" << 'EOF'
import { useEffect } from 'react';
import { useLocation } from 'react-router-dom';
export default function ScrollToTop() {
  const { pathname } = useLocation();
  useEffect(() => { window.scrollTo({ top: 0, behavior: 'instant' }); }, [pathname]);
  return null;
}
EOF

echo "  ✓ ScrollToTop"

# ════════════════════════════════════════════════════════════
# 10. HOME PAGE
# ════════════════════════════════════════════════════════════
cat > "$ROOT/pages/Home.tsx" << 'EOF'
import { useEffect } from 'react';
import Hero from '../components/Hero';
import SkillCards from '../components/SkillCards';
import WhatIDo from '../components/WhatIDo';
import CTASection from '../components/CTASection';

export default function Home() {
  useEffect(() => {
    const obs = new IntersectionObserver(
      entries => entries.forEach(e => { if(e.isIntersecting) e.target.classList.add('visible'); }),
      { threshold: 0.08, rootMargin: '0px 0px -40px 0px' }
    );
    document.querySelectorAll('.reveal').forEach(el => obs.observe(el));
    return () => obs.disconnect();
  }, []);
  return (
    <main>
      <Hero />
      <SkillCards />
      <WhatIDo />
      <CTASection />
    </main>
  );
}
EOF

echo "  ✓ Home"

# ════════════════════════════════════════════════════════════
# 11. PROJECTS PAGE (todos os projetos, existentes + novos)
# ════════════════════════════════════════════════════════════
cat > "$ROOT/pages/Projects.css" << 'EOF'
.projects-page{padding-bottom:4rem;}
.filter-bar{display:flex;gap:1px;background:var(--line);border:1px solid var(--line);width:fit-content;margin-bottom:2rem;border-radius:var(--radius);}
.filter-btn{background:var(--bg);border:none;padding:8px 16px;font-family:var(--mono);font-size:10px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);cursor:pointer;transition:all .15s;}
[data-theme="recruiter"] .filter-btn{font-family:'Inter',sans-serif;text-transform:none;font-size:11px;font-weight:500;letter-spacing:.02em;}
.filter-btn:hover{background:var(--bg3);color:var(--text);}
.filter-btn--active{background:var(--g);color:var(--bg);font-weight:700;}
.projects-full-list{display:flex;flex-direction:column;gap:1px;background:var(--line);border:1px solid var(--line);}
.proj-full-card{background:var(--bg);padding:2rem;border-left:2px solid transparent;transition:background .2s;}
.proj-full-card:hover{background:var(--bg3);}
.proj-full-card--featured{border-left-color:var(--g);background:var(--bg2);}
.proj-full-header{display:flex;align-items:flex-start;justify-content:space-between;gap:1.5rem;margin-bottom:1rem;flex-wrap:wrap;}
.proj-full-tag{margin-bottom:4px;}
.proj-full-title{font-size:1.1rem;color:var(--text);letter-spacing:-.3px;}
[data-theme="recruiter"] .proj-full-title{font-family:'DM Serif Display',serif;font-size:1.2rem;letter-spacing:0;}
.proj-full-badges{display:flex;flex-direction:column;align-items:flex-end;gap:6px;flex-shrink:0;}
.proj-status{display:flex;align-items:center;gap:5px;font-family:var(--mono);font-size:10px;letter-spacing:.08em;}
[data-theme="recruiter"] .proj-status{font-family:'Inter',sans-serif;font-weight:500;}
.proj-status__dot{display:inline-block;width:5px;height:5px;border-radius:50%;}
.proj-full-desc{font-size:12px;color:var(--muted);line-height:1.75;max-width:700px;margin-bottom:1.5rem;}
.proj-full-footer{display:flex;align-items:center;justify-content:space-between;gap:1.5rem;flex-wrap:wrap;}
.proj-full-stack{display:flex;flex-wrap:wrap;gap:6px;list-style:none;padding:0;margin:0;}
@media(max-width:640px){.proj-full-card{padding:1.25rem;}.proj-full-header{flex-direction:column;}.proj-full-badges{align-items:flex-start;}}
EOF

cat > "$ROOT/pages/Projects.tsx" << 'EOF'
import { useState } from 'react';
import { useTheme } from '../context/ThemeContext';
import './Projects.css';

const PROJECTS = [
  {id:'sigec',       tag:'Fiscal Intelligence',    title:'SIGEC v2 — Fiscal Intelligence Engine',      desc:'Plataforma de rastreamento de obras com 1.1M+ ARTs em blockchain SHA-256, pipeline Sentinel-2→PostGIS para 20 açudes piauienses (NDWI), FiscalBot Telegram com alertas automáticos (cron seg 06:00 BRT), roteamento NetworkX/TSP nos 224 municípios, orchestrator OpenAI + Claude.', stack:['Flask / Gunicorn','FastAPI','Angular 17','PostgreSQL 17','PostGIS','Blockchain','Sentinel-2','NetworkX','Telegram API','Claude API'],category:'Gov',     link:'https://github.com/s-v7/CadastroRastreamentoObras',status:'Production', year:'2024–2025',featured:true},
  {id:'sertledger',  tag:'Energy · Fintech',        title:'SertLedgerToken',                             desc:'Marketplace para tokenização de energia solar de prosumidores sob Lei 14.300/2022. Tokens SHA-256 encadeados com certificados ReportLab + QR, tarifa R$0,65/kWh (24% abaixo da Equatorial PI). Registro INPI planejado.',            stack:['Flask','Angular 19','PostgreSQL','SHA-256','ReportLab','QR Code'],        category:'Research',link:'https://github.com/s-v7/SertLedgerToken',             status:'MVP',        year:'2025–2026',featured:false},
  {id:'voxpiaui',    tag:'Civic Tech · Geospatial', title:'Vox Piauí',                                   desc:'Plataforma de inteligência territorial para os 224 municípios do Piauí. FastAPI + Angular 21, Leaflet dark-mode com CircleMarker animado por criticidade, 10 tabelas vx_, 4 funções PL/pgSQL. Município de Teresina = id 216.',           stack:['FastAPI','Angular 21','PostgreSQL','PostGIS','Leaflet'],                  category:'Gov',     link:null,                                                       status:'Development',year:'2026',    featured:false},
  {id:'creapi-ai',   tag:'AI · Analytics',          title:'CREAPI — Intelligent Analytics Platform',     desc:'Plataforma de analytics preditivo para CREA-PI, integrando modelos ML, pipelines OCR + NLP e monitoramento estatístico de ARTs.',                                                                                                         stack:['FastAPI','PostgreSQL','OCR','NLP','DVC'],                                 category:'AI',      link:null,                                                       status:'Private',    year:'2024',    featured:false},
  {id:'fiscalbot',   tag:'AI · Telegram',           title:'FiscalBot & ART Engine',                      desc:'Bot Telegram operacional com pipeline de alertas automáticos, processamento de 1.1M+ ARTs com ON CONFLICT DO NOTHING e motor de IA OpenAI + Claude para análise e classificação fiscal.',                                                stack:['FastAPI','Telegram Bot API','OpenAI','Claude API','PostgreSQL'],          category:'AI',      link:null,                                                       status:'Production', year:'2025',    featured:false},
  {id:'ru-confea',   tag:'Government · Integration',title:'RU ↔ CONFEA Integration Platform',           desc:'Plataforma oficial de integração automatizando fluxos SRP entre CONFEA e CREAs usando APIs e webhooks. Comunicação bidirecional com garantias de entrega.',                                                                               stack:['Jakarta EE','Webhooks','OpenAPI','PostgreSQL'],                           category:'Gov',     link:null,                                                       status:'Private',    year:'2024',    featured:false},
  {id:'sistemacrea', tag:'Legacy Modernization',    title:'SistemaCrea — Jakarta EE',                    desc:'Modernização de ERP institucional legacy: Maven multi-module EAR, integração e-MEC (4.328 IES via Dados Abertos MEC), JSF/PrimeFaces 13 com design system vd-* e CSS variables light/dark/dim.',                                       stack:['Java EE 8','JSF / PrimeFaces','EJB','JPA','Payara 6','PostgreSQL'],       category:'Enterprise',link:null,                                                 status:'Active',     year:'2024–Now',featured:false},
  {id:'blockchain',  tag:'Research · Blockchain',   title:'Blockchain CREA-PI',                          desc:'Rede blockchain para integração e rastreabilidade segura de dados do CREA-PI. Fundação do pipeline de 1.1M ARTs do SIGEC v2.',                                                                                                           stack:['Blockchain','Node.js','SHA-256'],                                         category:'Research',link:'https://github.com/s-v7/blockchain-crea-pi',           status:'Research',   year:'2023',    featured:false},
  {id:'audit',       tag:'Enterprise · Full Stack', title:'Audit System',                                desc:'Sistema full-stack de auditoria construído com Flask e Angular, com foco em rastreabilidade e arquitetura modular.',                                                                                                                     stack:['Python','Flask','Angular','SQLite'],                                      category:'Enterprise',link:'https://github.com/s-v7/sistema-auditoria',          status:'Public',     year:'2023',    featured:false},
  {id:'tracking',    tag:'Enterprise',              title:'Registration Tracking Works',                  desc:'Sistema para gestão de dados de obras de construção civil com backend modular e banco de dados relacional. Precursor do SIGEC v2.',                                                                                                      stack:['Python','Angular','PostgreSQL','SQLite'],                                 category:'Enterprise',link:'https://github.com/s-v7/CadastroRastreamentoObras', status:'Public',     year:'2022',    featured:false},
];

const CATS = ['All','Gov','AI','Enterprise','Research'];
const S_COLOR: Record<string,string> = {
  Production:'var(--g)',Active:'var(--g)',Public:'var(--g)',
  MVP:'#EF9F27',Development:'#EF9F27',
  Private:'var(--text-dim)',Research:'var(--text-dim)',
};

export default function Projects() {
  const {theme} = useTheme();
  const isAdmin = theme==='admin';
  const [f, setF] = useState('All');
  const visible = f==='All' ? PROJECTS : PROJECTS.filter(p=>p.category===f);

  return (
    <main className="projects-page">
      <div className="container">
        <header className="section-header" style={{paddingTop:'3rem'}}>
          <span className="section-num">02.</span>
          <h1 className="section-title">{isAdmin?'Projetos':'Projects'}</h1>
          <div className="section-rule"/>
        </header>
        <div className="filter-bar" role="group">
          {CATS.map(c=>(
            <button key={c} onClick={()=>setF(c)} className={`filter-btn${f===c?' filter-btn--active':''}`} aria-pressed={f===c}>{c}</button>
          ))}
        </div>
        <div className="projects-full-list">
          {visible.map(p=>(
            <article key={p.id} id={p.id} className={`proj-full-card${p.featured?' proj-full-card--featured':''}`}>
              <div className="proj-full-header">
                <div>
                  <p className="proj-full-tag t-label">{p.tag}</p>
                  <h2 className="proj-full-title t-heading">{p.title}</h2>
                </div>
                <div className="proj-full-badges">
                  <span className="proj-status" style={{'--c':S_COLOR[p.status]} as any}>
                    <span className="proj-status__dot" style={{background:S_COLOR[p.status]}}/>
                    <span style={{color:S_COLOR[p.status]}}>{p.status}</span>
                  </span>
                  <span className="t-label">{p.year}</span>
                </div>
              </div>
              <p className="proj-full-desc">{p.desc}</p>
              <div className="proj-full-footer">
                <ul className="proj-full-stack">{p.stack.map(t=><li key={t} className="tag">{t}</li>)}</ul>
                {p.link&&<a className="btn btn-ghost" href={p.link} target="_blank" rel="noreferrer">GitHub →</a>}
              </div>
            </article>
          ))}
        </div>
      </div>
    </main>
  );
}
EOF

echo "  ✓ Projects (10 projetos)"

# ════════════════════════════════════════════════════════════
# 12. ART ENGINE
# ════════════════════════════════════════════════════════════
cat > "$ROOT/pages/ArtEngine.css" << 'EOF'
.art-page{padding-bottom:4rem;}
.art-stats{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:var(--line);border:1px solid var(--line);margin-bottom:2rem;}
.art-stat{background:var(--bg2);padding:1rem;text-align:center;}
.art-stat__n{font-family:var(--display);font-size:1.6rem;font-weight:700;color:var(--g);}
[data-theme="recruiter"] .art-stat__n{font-weight:400;}
.art-stat__l{font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin-top:4px;font-family:var(--mono);}
[data-theme="recruiter"] .art-stat__l{font-family:'Inter',sans-serif;font-weight:500;}
.art-caps{display:grid;grid-template-columns:repeat(2,1fr);gap:1px;background:var(--line);border:1px solid var(--line);margin-bottom:2rem;}
.art-cap{background:var(--bg);padding:1rem 1.25rem;display:flex;align-items:flex-start;gap:.75rem;}
.art-cap__check{color:var(--g);font-size:14px;flex-shrink:0;margin-top:1px;}
.art-cap__title{font-size:12px;color:var(--text);font-family:var(--body);margin-bottom:2px;}
[data-theme="recruiter"] .art-cap__title{font-family:'Inter',sans-serif;font-weight:600;}
.art-cap__sub{font-size:11px;color:var(--muted);line-height:1.5;}
.pipeline{display:flex;align-items:center;gap:0;margin-bottom:2rem;overflow-x:auto;padding-bottom:.5rem;}
.pipe-step{background:var(--bg2);border:1px solid var(--line);padding:.6rem .9rem;font-size:10px;font-family:var(--mono);color:var(--text-dim);white-space:nowrap;flex-shrink:0;}
[data-theme="recruiter"] .pipe-step{font-family:'Inter',sans-serif;font-size:11px;font-weight:500;}
.pipe-step--accent{border-color:var(--g);color:var(--g);}
.pipe-arrow{font-size:12px;color:var(--line-hi);padding:0 4px;flex-shrink:0;}
.art-blocks{display:grid;grid-template-columns:1fr 1fr;gap:1px;background:var(--line);border:1px solid var(--line);}
.art-block{background:var(--bg);padding:1.25rem;}
.art-block__label{margin-bottom:.75rem;}
.art-block__list{list-style:none;padding:0;display:flex;flex-direction:column;gap:4px;}
.art-block__list li{font-size:12px;color:var(--muted);display:flex;align-items:baseline;gap:6px;line-height:1.6;}
.art-block__list li::before{content:"·";color:var(--g);flex-shrink:0;}
.art-deploy{border:1px solid var(--line);background:var(--bg2);padding:1.5rem;margin-top:2rem;display:flex;gap:2rem;flex-wrap:wrap;}
.art-deploy__col{flex:1;min-width:200px;}
.art-deploy__label{margin-bottom:.75rem;}
.art-deploy__items{display:flex;flex-wrap:wrap;gap:6px;}
@media(max-width:640px){.art-stats{grid-template-columns:repeat(2,1fr);}.art-caps{grid-template-columns:1fr;}.art-blocks{grid-template-columns:1fr;}}
EOF

cat > "$ROOT/pages/ArtEngine.tsx" << 'EOF'
import { useTheme } from '../context/ThemeContext';
import './ArtEngine.css';

const CAPS = [
  {title:'Deterministic audit rules',    sub:'Reproducible, no LLM drift on rule decisions'},
  {title:'DB × PDF divergence detection',sub:'Cross-validates database records against PDF documents'},
  {title:'Sensitive data masking',       sub:'PII stripped before any LLM call'},
  {title:'DAG execution pipeline',       sub:'Directed acyclic graph — full audit traceability'},
  {title:'LLM semantic enrichment',      sub:'OpenAI + Claude with strict governance guardrails'},
  {title:'Human-in-the-loop learning',   sub:'Auditor feedback improves classification over time'},
  {title:'Multi-CREA scalable model',    sub:'Designed for CONFEA federation — 27 regional councils'},
  {title:'Blockchain traceability',      sub:'SHA-256 chained records, 1.1M+ ARTs stored on-chain'},
];

const PIPELINE = ['DB Extraction','PDF Parsing','Cross-check','Rule Scoring','Guard Filters','LLM Enrichment','Traceable Storage'];

const GOV = ['Masked inputs only','No legal conclusions generated','Structured JSON outputs','Confidence tagging','Human review flags','Prompt versioning'];
const LEARN = ['Markov transition weighting','Graph versioning','Rule feedback loop','Reviewer-confirmed corrections'];
const DEPLOY = ['On-premise compatible','Government cloud ready','API + CLI + Dashboard modes','Designed for CREA federation scale','8 systemd services in production','Cloudflare Tunnel (zero-config TLS)'];

export default function ArtEngine() {
  const {theme} = useTheme();
  const isAdmin = theme==='admin';
  return (
    <main className="art-page">
      <div className="container">
        <header className="section-header" style={{paddingTop:'3rem'}}>
          <span className="section-num">AI.</span>
          <h1 className="section-title">ART Intelligence Engine</h1>
          <div className="section-rule"/>
        </header>

        <p style={{fontFamily:isAdmin?'var(--mono)':'Inter, sans-serif',fontSize:'13px',color:'var(--text-dim)',maxWidth:'680px',lineHeight:'1.7',marginBottom:'2rem'}}>
          {isAdmin
            ? 'Motor de IA institucional para auditoria de ARTs (Anotações de Responsabilidade Técnica). Combina regras determinísticas, cross-check DB×PDF, normalização semântica e enriquecimento LLM com governança estrita.'
            : 'Institutional AI engine for auditing Engineering Responsibility Records (ARTs). Combines deterministic rules, DB×PDF cross-validation, semantic normalization and LLM enrichment under strict governance guardrails.'
          }
        </p>

        {/* Stats */}
        <div className="art-stats">
          {[['1.1M+','ARTs on-chain'],['224','Municípios PI'],['8','Serviços systemd'],['2,045','ARTs/second']].map(([n,l])=>(
            <div className="art-stat" key={l}>
              <div className="art-stat__n">{n}</div>
              <div className="art-stat__l">{l}</div>
            </div>
          ))}
        </div>

        {/* Pipeline */}
        <div className="section-header" style={{marginBottom:'1rem'}}>
          <span className="section-num">—</span>
          <h2 className="section-title" style={{fontSize:'1.1rem'}}>{isAdmin?'Pipeline de execução':'Execution pipeline'}</h2>
        </div>
        <div className="pipeline">
          {PIPELINE.map((s,i)=>(
            <>
              <div key={s} className={`pipe-step${i===4||i===5?' pipe-step--accent':''}`}>{s}</div>
              {i<PIPELINE.length-1&&<span className="pipe-arrow" key={`a${i}`}>→</span>}
            </>
          ))}
        </div>

        {/* Capabilities */}
        <div className="section-header" style={{marginBottom:'1rem'}}>
          <span className="section-num">—</span>
          <h2 className="section-title" style={{fontSize:'1.1rem'}}>{isAdmin?'Capacidades':'Core capabilities'}</h2>
        </div>
        <div className="art-caps">
          {CAPS.map(c=>(
            <div className="art-cap" key={c.title}>
              <span className="art-cap__check" aria-hidden="true">✔</span>
              <div><div className="art-cap__title">{c.title}</div><div className="art-cap__sub">{c.sub}</div></div>
            </div>
          ))}
        </div>

        {/* Governance + Learning */}
        <div className="art-blocks">
          <div className="art-block">
            <p className="art-block__label t-label">// LLM Governance Model</p>
            <ul className="art-block__list">{GOV.map(g=><li key={g}>{g}</li>)}</ul>
          </div>
          <div className="art-block">
            <p className="art-block__label t-label">// Continuous Learning</p>
            <ul className="art-block__list">{LEARN.map(l=><li key={l}>{l}</li>)}</ul>
          </div>
        </div>

        {/* Deployment */}
        <div className="art-deploy">
          <div className="art-deploy__col">
            <p className="art-deploy__label t-label">// Deployment model</p>
            <div className="art-deploy__items">{DEPLOY.map(d=><span key={d} className="tag">{d}</span>)}</div>
          </div>
          <div className="art-deploy__col">
            <p className="art-deploy__label t-label">// Stack</p>
            <div className="art-deploy__items">{['FastAPI','LangGraph','OpenAI','Claude API','PostgreSQL','PostGIS','Cloudflare','systemd'].map(t=><span key={t} className="tag tag-active">{t}</span>)}</div>
          </div>
        </div>
      </div>
    </main>
  );
}
EOF

echo "  ✓ ArtEngine"

# ════════════════════════════════════════════════════════════
# 13. EDUCATION, CONTACT, CVINIT (shared CSS pattern)
# ════════════════════════════════════════════════════════════
cat > "$ROOT/pages/Education.tsx" << 'EOF'
import { useTheme } from '../context/ThemeContext';
import './Education.css';
const EDU=[{degree:'Tecnólogo em Segurança da Informação',inst:'Universidade Paulista (UNIP)',period:'Aug 2024 — Dec 2026 (expected)',mode:'Distance Learning',status:'In progress',topics:['Cryptography','Pentesting','Networks','LGPD','Application Security','Vulnerability Analysis']}];
const CERTS=[{name:'Docker & Kubernetes — Fundamentals',issuer:'Udemy',year:'2023'},{name:'Java EE — Enterprise Applications',issuer:'Alura',year:'2022'},{name:'Advanced PostgreSQL',issuer:'Dio',year:'2022'},{name:'Machine Learning with Python',issuer:'Coursera',year:'2021'},{name:'React — Fundamentals & Hooks',issuer:'Rocketseat',year:'2021'}];
const LANGS=[{lang:'Portuguese',level:'Native',pct:100},{lang:'English',level:'Intermediate (reading) / Basic (writing)',pct:58}];
export default function Education() {
  const {theme}=useTheme(); const isAdmin=theme==='admin';
  return (
    <main className="edu-page">
      <div className="container">
        <header className="section-header" style={{paddingTop:'3rem'}}>
          <span className="section-num">ED.</span>
          <h1 className="section-title">Education</h1>
          <div className="section-rule"/>
        </header>
        <section className="edu-block"><p className="block-label t-label">// Academic</p>
          {EDU.map(e=>(
            <div key={e.degree} className="edu-card">
              <div className="edu-card__header">
                <div><h2 className="edu-card__degree t-heading">{e.degree}</h2><p className="edu-card__inst">{e.inst}</p></div>
                <div className="edu-card__meta"><span className="tag tag-active">{e.status}</span><span className="t-label">{e.mode} · {e.period}</span></div>
              </div>
              <div className="edu-card__topics">{e.topics.map(t=><span key={t} className="tag">{t}</span>)}</div>
            </div>
          ))}
        </section>
        <section className="edu-block"><p className="block-label t-label">// Certifications</p>
          <div className="certs-list">{CERTS.map(c=><div key={c.name} className="cert-row"><span className="cert-name">{c.name}</span><span className="t-label">{c.issuer}</span><span className="t-label cert-year">{c.year}</span></div>)}</div>
        </section>
        <section className="edu-block"><p className="block-label t-label">// Languages</p>
          <div className="lang-list">{LANGS.map(l=>(
            <div key={l.lang} className="lang-row">
              <div className="lang-info"><span className="lang-name t-heading">{l.lang}</span><span className="t-label">{l.level}</span></div>
              <div className="lang-bar"><div className="lang-bar__fill" style={{width:`${l.pct}%`}}/></div>
              <span className="t-label lang-pct">{l.pct}%</span>
            </div>
          ))}</div>
        </section>
      </div>
    </main>
  );
}
EOF

cat > "$ROOT/pages/Education.css" << 'EOF'
.edu-page{padding-bottom:4rem;}
.edu-block{margin-bottom:3rem;}
.block-label{margin-bottom:1rem;}
.edu-card{border:1px solid var(--line);background:var(--bg2);padding:1.5rem;border-left:2px solid var(--g);}
.edu-card__header{display:flex;justify-content:space-between;align-items:flex-start;gap:1.5rem;margin-bottom:1rem;flex-wrap:wrap;}
.edu-card__degree{font-size:1rem;color:var(--text);margin-bottom:4px;}
[data-theme="recruiter"] .edu-card__degree{font-family:'DM Serif Display',serif;font-size:1.1rem;}
.edu-card__inst{font-family:var(--mono);font-size:11px;color:var(--g);}
[data-theme="recruiter"] .edu-card__inst{font-family:'Inter',sans-serif;font-weight:600;}
.edu-card__meta{display:flex;flex-direction:column;align-items:flex-end;gap:6px;}
.edu-card__topics{display:flex;flex-wrap:wrap;gap:6px;padding-top:1rem;border-top:1px solid var(--line2);}
.certs-list{border:1px solid var(--line);background:var(--bg);}
.cert-row{display:grid;grid-template-columns:1fr auto auto;align-items:center;gap:1.5rem;padding:.85rem 1.25rem;border-bottom:1px solid var(--line2);transition:background .15s;}
.cert-row:last-child{border-bottom:none;}
.cert-row:hover{background:var(--bg3);}
.cert-name{font-size:12px;color:var(--text);}
[data-theme="recruiter"] .cert-name{font-family:'Inter',sans-serif;}
.lang-list{display:flex;flex-direction:column;gap:1rem;}
.lang-row{display:grid;grid-template-columns:220px 1fr 40px;align-items:center;gap:1.5rem;}
.lang-info{display:flex;flex-direction:column;gap:2px;}
.lang-name{font-size:.9rem;color:var(--text);}
.lang-bar{height:3px;background:var(--line);overflow:hidden;}
.lang-bar__fill{height:100%;background:var(--g);transition:width 1s ease;}
.lang-pct{text-align:right;}
@media(max-width:600px){.edu-card__header{flex-direction:column;}.edu-card__meta{align-items:flex-start;}.cert-row{grid-template-columns:1fr auto;}.cert-year{display:none;}.lang-row{grid-template-columns:150px 1fr 36px;gap:.75rem;}}
EOF

cat > "$ROOT/pages/Contact.tsx" << 'EOF'
import { useTheme } from '../context/ThemeContext';
import './Contact.css';
const LINKS=[{label:'Email',value:'svasconceloscruz7@gmail.com',href:'mailto:svasconceloscruz7@gmail.com'},{label:'GitHub',value:'github.com/s-v7',href:'https://github.com/s-v7'},{label:'LinkedIn',value:'linkedin.com/in/s-v7',href:'https://www.linkedin.com/in/silas-v-053293255/'},{label:'Phone',value:'+55 (47) 99691-9951',href:'tel:+5547996919951'},{label:'Location',value:'Teresina, Piauí — Brasil',href:null}];
export default function Contact() {
  const {theme}=useTheme(); const isAdmin=theme==='admin';
  return (
    <main className="contact-page">
      <div className="container">
        <header className="section-header" style={{paddingTop:'3rem'}}>
          <span className="section-num">04.</span>
          <h1 className="section-title">{isAdmin?'Contato':'Contact'}</h1>
          <div className="section-rule"/>
        </header>
        <div className="contact-grid">
          {LINKS.map(({label,value,href})=>
            href ? <a key={label} href={href} className="contact-cell" target={href.startsWith('http')?'_blank':undefined} rel="noreferrer"><p className="contact-label t-label">{label}</p><p className="contact-value">{value}</p></a>
                 : <div key={label} className="contact-cell"><p className="contact-label t-label">{label}</p><p className="contact-value">{value}</p></div>
          )}
        </div>
        <div className="contact-message">
          <p className="t-label" style={{marginBottom:'1rem'}}>{isAdmin?'// Mensagem rápida':'// Quick message'}</p>
          <form action="https://formspree.io/f/YOUR_FORM_ID" method="POST" className="contact-form">
            <div className="form-row">
              <div className="form-field"><label htmlFor="name" className="t-label">{isAdmin?'Nome':'Name'}</label><input id="name" type="text" name="name" placeholder={isAdmin?'Seu nome':'Your name'} required/></div>
              <div className="form-field"><label htmlFor="email" className="t-label">Email</label><input id="email" type="email" name="email" placeholder="your@email.com" required/></div>
            </div>
            <div className="form-field"><label htmlFor="message" className="t-label">{isAdmin?'Mensagem':'Message'}</label><textarea id="message" name="message" rows={5} placeholder={isAdmin?'Descreva o projeto...':'Describe the project or role...'} required/></div>
            <button type="submit" className="btn btn-primary">{isAdmin?'→ Enviar':'Send message'}</button>
          </form>
        </div>
      </div>
    </main>
  );
}
EOF

cat > "$ROOT/pages/Contact.css" << 'EOF'
.contact-page{padding-bottom:4rem;}
.contact-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:var(--line);border:1px solid var(--line);margin-bottom:3rem;}
.contact-cell{background:var(--bg);padding:1.25rem;text-decoration:none;color:inherit;transition:background .2s;}
a.contact-cell:hover{background:var(--bg3);}
.contact-label{margin-bottom:6px;}
.contact-value{font-size:12px;color:var(--text);word-break:break-all;}
[data-theme="recruiter"] .contact-value{font-family:'Inter',sans-serif;}
.contact-message{max-width:640px;padding-bottom:3rem;}
.contact-form{display:flex;flex-direction:column;gap:1rem;}
.form-row{display:grid;grid-template-columns:1fr 1fr;gap:1rem;}
.form-field{display:flex;flex-direction:column;gap:6px;}
.form-field input,.form-field textarea{background:var(--bg2);border:1px solid var(--line);color:var(--text);font-family:var(--mono);font-size:12px;padding:10px 12px;border-radius:var(--radius);resize:vertical;outline:none;transition:border-color .15s;}
[data-theme="recruiter"] .form-field input,[data-theme="recruiter"] .form-field textarea{font-family:'Inter',sans-serif;}
.form-field input:focus,.form-field textarea:focus{border-color:var(--g);}
.form-field input::placeholder,.form-field textarea::placeholder{color:var(--muted);}
@media(max-width:640px){.contact-grid{grid-template-columns:1fr;}.form-row{grid-template-columns:1fr;}}
EOF

echo "  ✓ Education + Contact"

# ════════════════════════════════════════════════════════════
# 14. CVINIT — perfil/CV com typewriter preservado como easter egg
# ════════════════════════════════════════════════════════════
cat > "$ROOT/pages/CVInit.css" << 'EOF'
.cv-page{padding-bottom:4rem;}
.cv-header{padding-top:3rem;padding-bottom:2rem;border-bottom:1px solid var(--line);margin-bottom:2rem;display:flex;justify-content:space-between;align-items:flex-start;gap:1.5rem;flex-wrap:wrap;}
.cv-name{font-size:clamp(2rem,4vw,3rem);color:var(--text);margin-bottom:8px;}
[data-theme="recruiter"] .cv-name{font-family:'DM Serif Display',serif;font-size:clamp(2.2rem,4vw,3.2rem);}
.cv-subtitle{font-size:12px;color:var(--muted);margin-bottom:12px;}
[data-theme="recruiter"] .cv-subtitle{font-family:'Inter',sans-serif;font-size:13px;}
.cv-contacts{display:flex;flex-wrap:wrap;gap:8px;align-items:center;font-size:11px;color:var(--muted);}
.cv-contacts a{color:var(--g);}
.cv-block{margin-bottom:2rem;padding-bottom:2rem;border-bottom:1px solid var(--line2);}
.cv-block__label{margin-bottom:1rem;}
.cv-block__text{font-size:.95rem;color:var(--text-dim);line-height:1.7;max-width:680px;}
[data-theme="recruiter"] .cv-block__text{font-family:'Inter',sans-serif;font-size:14px;}
.cv-skills{border:1px solid var(--line);background:var(--bg);}
.cv-skill-row{display:grid;grid-template-columns:160px 1fr;gap:1rem;padding:.75rem 1.25rem;border-bottom:1px solid var(--line2);align-items:baseline;}
.cv-skill-row:last-child{border-bottom:none;}
.cv-skill-group{font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:var(--g);font-family:var(--mono);}
[data-theme="recruiter"] .cv-skill-group{font-family:'Inter',sans-serif;font-weight:700;letter-spacing:.04em;}
.cv-skill-items{font-size:11px;color:var(--text-dim);font-family:var(--mono);}
[data-theme="recruiter"] .cv-skill-items{font-family:'Inter',sans-serif;font-size:12px;}
.cv-exp-item{margin-bottom:1.5rem;padding-left:1rem;border-left:1px solid var(--line);}
.cv-exp-header{display:flex;justify-content:space-between;align-items:flex-start;gap:1.5rem;margin-bottom:10px;flex-wrap:wrap;}
.cv-exp-role{font-size:.95rem;color:var(--text);margin-bottom:3px;}
[data-theme="recruiter"] .cv-exp-role{font-family:'DM Serif Display',serif;font-size:1.05rem;}
.cv-exp-org{font-size:11px;color:var(--g);font-family:var(--mono);}
[data-theme="recruiter"] .cv-exp-org{font-family:'Inter',sans-serif;font-weight:600;}
.cv-exp-bullets{padding-left:1rem;margin:0;display:flex;flex-direction:column;gap:6px;}
.cv-exp-bullets li{font-size:12px;color:var(--muted);line-height:1.65;}
[data-theme="recruiter"] .cv-exp-bullets li{font-family:'Inter',sans-serif;}
@media(max-width:600px){.cv-header{flex-direction:column;}.cv-skill-row{grid-template-columns:1fr;gap:2px;}.cv-exp-header{flex-direction:column;}}
EOF

cat > "$ROOT/pages/CVInit.tsx" << 'EOF'
import { useTheme } from '../context/ThemeContext';
import './CVInit.css';

const SKILLS=[
  {group:'Languages',    items:'Java · Python · TypeScript · JavaScript (ES6+) · C'},
  {group:'Web',          items:'Angular 17+ · React · JSF (PrimeFaces) · Spring Boot · FastAPI · Node.js'},
  {group:'Databases',    items:'PostgreSQL · PostGIS · MySQL · MongoDB'},
  {group:'DevOps',       items:'Git · Docker · Kubernetes · CI/CD · Nginx · Cloudflare · Linux / systemd'},
  {group:'Data & AI',    items:'Pandas · NumPy · TensorFlow · Scikit-learn · OpenAI API · Claude API · Sentinel-2'},
  {group:'Security',     items:'Pentest · OWASP · Log auditing · Cryptography · LGPD compliance'},
];

const EXP=[
  {role:'Technology & Information Security Advisor',org:'CREA-PI — Teresina, Brasil',period:'May 2024 — Present',bullets:[
    'Sole architect of the FIE ecosystem: SIGEC v2, FiscalBot, ART Engine, SistemaCrea and SertLedgerToken.',
    'Java EE 8 systems development and enhancement (GlassFish, JSF/PrimeFaces, Hibernate, PostgreSQL, Linux).',
    'Sentinel-2→PostgreSQL pipeline for water resource monitoring of Piauí reservoirs via NDWI spectral analysis.',
    'Shell script automation and Telegram bot integration for institutional alerts.',
    'Security analysis, vulnerability mitigation and compliance reviews for government systems.',
  ]},
  {role:'Java Full Stack Developer',org:'EDM Software — Florianópolis, Brasil',period:'May 2022 — Sep 2022',bullets:[
    'Developed and maintained enterprise web application features using JSF (PrimeFaces), JavaScript, XHTML/CSS.',
    'Bug fixes and continuous improvement support for the main product.',
  ]},
];

export default function CVInit() {
  const {theme}=useTheme(); const isAdmin=theme==='admin';
  return (
    <main className="cv-page">
      <div className="container">
        <header className="cv-header">
          <div>
            <h1 className="cv-name t-display">Silas Vasconcelos Cruz</h1>
            <p className="cv-subtitle">Full Stack Developer — Java / Python / React + DevOps & Distributed Systems</p>
            <div className="cv-contacts">
              <a href="mailto:svasconceloscruz7@gmail.com">svasconceloscruz7@gmail.com</a>
              <span>·</span><a href="https://github.com/s-v7" target="_blank" rel="noreferrer">github.com/s-v7</a>
              <span>·</span><a href="https://www.linkedin.com/in/silas-v-053293255/" target="_blank" rel="noreferrer">linkedin.com/in/s-v7</a>
              <span>·</span><span>Teresina, PI — Brasil</span>
            </div>
          </div>
          <a className="btn btn-primary" href="/Silas_Vasconcelos_CV.pdf" download>↓ Download PDF</a>
        </header>

        <section className="cv-block">
          <p className="cv-block__label t-label">{isAdmin?'// Resumo':'// Summary'}</p>
          <p className="cv-block__text">Full Stack Developer with experience building distributed web applications in Java and Python. Skilled in front-end development (React, Angular) and back-end frameworks (Spring Boot, FastAPI), with hands-on DevOps experience (Docker, Kubernetes, CI/CD). Sole architect of the FIE ecosystem at CREA-PI — 1.1M+ engineering records on-chain, Sentinel-2 geospatial analytics, fiscal AI orchestration across 224 municipalities of Piauí. Designed for national adoption by CONFEA across 27 regional councils.</p>
        </section>

        <section className="cv-block">
          <p className="cv-block__label t-label">{isAdmin?'// Competências':'// Skills'}</p>
          <div className="cv-skills">{SKILLS.map(({group,items})=>(
            <div key={group} className="cv-skill-row"><span className="cv-skill-group">{group}</span><span className="cv-skill-items">{items}</span></div>
          ))}</div>
        </section>

        <section className="cv-block">
          <p className="cv-block__label t-label">{isAdmin?'// Experiência':'// Experience'}</p>
          {EXP.map(e=>(
            <div key={e.role} className="cv-exp-item">
              <div className="cv-exp-header">
                <div><h2 className="cv-exp-role t-heading">{e.role}</h2><p className="cv-exp-org">{e.org}</p></div>
                <time className="t-label">{e.period}</time>
              </div>
              <ul className="cv-exp-bullets">{e.bullets.map(b=><li key={b}>{b}</li>)}</ul>
            </div>
          ))}
        </section>

        <section className="cv-block">
          <p className="cv-block__label t-label">{isAdmin?'// Formação':'// Education'}</p>
          <div className="cv-exp-item">
            <div className="cv-exp-header">
              <div><h2 className="cv-exp-role t-heading">Technologist in Information Security (Distance Learning)</h2><p className="cv-exp-org">Universidade Paulista (UNIP) — Brasil</p></div>
              <time className="t-label">Aug 2024 — Dec 2026 (expected)</time>
            </div>
          </div>
        </section>
      </div>
    </main>
  );
}
EOF

echo "  ✓ CVInit"

# ════════════════════════════════════════════════════════════
# 15. APP.TSX — wrap com ThemeProvider
# ════════════════════════════════════════════════════════════
cat > "$ROOT/App.tsx" << 'EOF'
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { ThemeProvider } from './context/ThemeContext';
import Navbar      from './components/Navbar';
import Footer      from './components/Footer';
import ScrollToTop from './components/ScrollToTop';
import Home        from './pages/Home';
import Contact     from './pages/Contact';
import Projects    from './pages/Projects';
import Education   from './pages/Education';
import CVInit      from './pages/CVInit';
import ArtEngine   from './pages/ArtEngine';
import './styles/global.css';

export default function App() {
  return (
    <ThemeProvider>
      <BrowserRouter>
        <ScrollToTop />
        <Navbar />
        <Routes>
          <Route path="/"           element={<Home />}      />
          <Route path="/profile"    element={<CVInit />}    />
          <Route path="/education"  element={<Education />} />
          <Route path="/projects"   element={<Projects />}  />
          <Route path="/art-engine" element={<ArtEngine />} />
          <Route path="/contact"    element={<Contact />}   />
        </Routes>
        <Footer />
      </BrowserRouter>
    </ThemeProvider>
  );
}
EOF

echo "  ✓ App.tsx (ThemeProvider)"

# ════════════════════════════════════════════════════════════
# 16. INDEX.CSS
# ════════════════════════════════════════════════════════════
cat > "$ROOT/index.css" << 'EOF'
@import './styles/global.css';
EOF

echo ""
echo "════════════════════════════════════════════"
echo "✅  Modernização aplicada com sucesso!"
echo "════════════════════════════════════════════"
echo ""
echo "  Próximo passo:"
echo "  npm install three @types/three"
echo "  npm run dev"
echo ""
echo "  Toggle de tema: ícone na navbar (direita)"
echo "  Admin  → #1D9E75  Space Mono + Syne"
echo "  Recruiter → #E8890C  Inter + DM Serif Display"
echo "════════════════════════════════════════════"
