import { useTheme } from "../context/ThemeContext";
import "../styles/pages/Contact.css";

import { LINKS } from '../data/contact';

export default function Contact() {
  const { theme } = useTheme();
  const isAdmin = theme === "admin";
  return (
    <main className="contact-page">
      <div className="container">
        <header className="section-header" style={{ paddingTop: "3rem" }}>
          <span className="section-num">04.</span>
          <h1 className="section-title">{isAdmin ? "Contato" : "Contact"}</h1>
          <div className="section-rule" />
        </header>
        <div className="contact-grid">
          {LINKS.map(({ label, value, href }) =>
            href ? (
              <a
                key={label}
                href={href}
                className="contact-cell"
                target={href.startsWith("http") ? "_blank" : undefined}
                rel="noreferrer"
              >
                <p className="contact-label t-label">{label}</p>
                <p className="contact-value">{value}</p>
              </a>
            ) : (
              <div key={label} className="contact-cell">
                <p className="contact-label t-label">{label}</p>
                <p className="contact-value">{value}</p>
              </div>
            ),
          )}
        </div>
        <div className="contact-message">
          <p className="t-label" style={{ marginBottom: "1rem" }}>
            {isAdmin ? "// Mensagem rápida" : "// Quick message"}
          </p>
          <form
            action="https://formspree.io/f/YOUR_FORM_ID"
            method="POST"
            className="contact-form"
          >
            <div className="form-row">
              <div className="form-field">
                <label htmlFor="name" className="t-label">
                  {isAdmin ? "Nome" : "Name"}
                </label>
                <input
                  id="name"
                  type="text"
                  name="name"
                  placeholder={isAdmin ? "Seu nome" : "Your name"}
                  required
                />
              </div>
              <div className="form-field">
                <label htmlFor="email" className="t-label">
                  Email
                </label>
                <input
                  id="email"
                  type="email"
                  name="email"
                  placeholder="your@email.com"
                  required
                />
              </div>
            </div>
            <div className="form-field">
              <label htmlFor="message" className="t-label">
                {isAdmin ? "Mensagem" : "Message"}
              </label>
              <textarea
                id="message"
                name="message"
                rows={5}
                placeholder={
                  isAdmin
                    ? "Descreva o projeto..."
                    : "Describe the project or role..."
                }
                required
              />
            </div>
            <button type="submit" className="btn btn-primary">
              {isAdmin ? "→ Enviar" : "Send message"}
            </button>
          </form>
        </div>
      </div>
    </main>
  );
}
