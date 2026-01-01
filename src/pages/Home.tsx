import CodeCVUser from "../components/CodeCVUser";
import photo from "../assets/react.svg";

const Home: React.FC = () => {
  return (
    <>
      {/* Skip navigation for accessibility */}
      <a href="#main" className="skip-link">
        Pular para o conteúdo
      </a>

      <section className="cv-wrap">
        <header className="cv-header" role="banner">
          <img
            className="cv-photo"
            src={photo}
            alt="Silas Vasconcelos Cruz"
            width={110}
            height={110}
            loading="lazy"
          />

          <div className="cv-head-text">
            <h1>Silas Vasconcelos Cruz</h1>
            <p className="cv-sub">
              Software Engineer · Web · Infra · AI & Blockchain
            </p>

            <ul className="cv-links" aria-label="Links and location">
              <li className="sep">•</li>

              <li>
                <a
                  href="https://github.com/s-v7"
                  target="_blank"
                  rel="noopener noreferrer"
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
                >
                  linkedin.com/in/s-v7
                </a>
              </li>

              <li className="sep">•</li>

              <li>
                <span role="img" aria-label="Brazil">
                  🇧🇷
                </span>{" "}
                Brazil
              </li>
            </ul>

            <ul
              className="cv-chips"
              role="list"
              aria-label="Core technologies"
            >
              {[
                "Java",
                "Python",
                "TypeScript",
                "PostgreSQL",
                "Streamlit",
                "Docker",
                "Kubernetes",
                "React",
                "Machine Learning",
              ].map((tech) => (
                <li key={tech}>{tech}</li>
              ))}
            </ul>
          </div>
        </header>

        <main id="main" role="main">
          <CodeCVUser />
        </main>
      </section>
    </>
  );
};

export default Home;

