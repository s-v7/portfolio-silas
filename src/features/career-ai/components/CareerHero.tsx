import { LINKS } from "../../../data/contact";

const CV_URL = `${import.meta.env.BASE_URL}Silas_V_C_EN.pdf`;

function getLink(label: string) {
  return LINKS.find((item) => item.label === label);
}

export function CareerHero() {
  const github = getLink("GitHub");
  const linkedin = getLink("LinkedIn");
  const email = getLink("Email");

  return (
    <section className="career-hero career-hero--compact" aria-labelledby="career-hero-title">
      <div className="career-hero__content">

        <h1 id="career-hero-title">Silas Vasconcelos Cruz</h1>

        <div className="career-hero__position">
          <strong>Full Stack Software Engineer</strong>

          <span>Enterprise Modernization · DevSecOps · Applied AI</span>
        </div>

        <p className="career-hero__summary">
          I modernize mission-critical enterprise systems, design secure architectures, automate
          infrastructure, and connect legacy platforms with modern Java, Python, Node.js, and AI
          engineering.
        </p>

        <div className="career-hero__actions">
          <a
            className="career-hero__action career-hero__action--primary"
            href={CV_URL}
            target="_blank"
            rel="noreferrer"
          >
            <span aria-hidden="true">↓</span>
            Download CV
          </a>

          {github?.href && (
            <a className="career-hero__action" href={github.href} target="_blank" rel="noreferrer">
              GitHub
            </a>
          )}

          {linkedin?.href && (
            <a
              className="career-hero__action"
              href={linkedin.href}
              target="_blank"
              rel="noreferrer"
            >
              LinkedIn
            </a>
          )}

          {email?.href && (
            <a className="career-hero__action" href={email.href}>
              Contact
            </a>
          )}
        </div>
      </div>

      <div className="career-hero__highlights" aria-label="Professional highlights">
        <span>Java EE → Jakarta EE</span>
        <span>Java · Python · Node.js</span>
        <span>Backend · DevSecOps · AI</span>
        <span>Open to international opportunities</span>
      </div>
    </section>
  );
}
