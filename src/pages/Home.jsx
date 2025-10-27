// src/pages/CVInit.jsx
import React from "react";
import photo from "../assets/react.svg";
import CodeCVUser from "../components/CodeCVUser";

export default function Home() {
  return (
    <>
      <a href="#main" className="skip-link">
        Pular para o conteúdo
      </a>

      <section className="cv-wrap">
        <header className="cv-header" role="banner">
          <img
            className="cv-photo"
            src={photo}
            alt="Foto de perfil de Silas Vasconcelos Cruz"
            width={110}
            height={110}
            loading="lazy"
          />
          <div className="cv-head-text">
            <h1>SILAS VASCONCELOS CRUZ</h1>
            <p className="cv-sub">
              Software Engineer · Web/Infra (IA & Blockchain)
            </p>

            <ul className="cv-links" aria-label="Links e localização">
              <li className="sep">•</li>
              <li>
                <a
                  href="https://github.com/s-v7"
                  target="_blank"
                  rel="noopener noreferrer"
                  aria-label="GitHub de Silas"
                >
                  github.com/s-v7
                </a>
              </li>
              <li className="sep">•</li>
              <li>
                <a
                  href="https://www.linkedin.com/in/silas-v-053293255/"
                  target="_blank"
                  rel="noopener noreferrer"
                  aria-label="LinkedIn de Silas"
                >
                  linkedin.com/in/s-v7
                </a>
              </li>
              <li className="sep">•</li>
              <li>
                <span role="img" aria-label="Brasil">
                  🇧🇷
                </span>{" "}
                Brasil
              </li>
            </ul>

            <ul
              className="cv-chips"
              role="list"
              aria-label="Principais tecnologias"
            >
              {[
                "Java",
                "Python",
                "JavaScript",
                "PostgreSQL",
                "Streamlit",
                "Docker",
                "Kubernetes",
                "React",
                "ML",
              ].map((t) => (
                <li key={t}>{t}</li>
              ))}
            </ul>
          </div>
        </header>

        <div id="main" role="main">
          <CodeCVUser />
        </div>
      </section>
    </>
  );
}
