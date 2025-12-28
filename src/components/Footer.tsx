import { FaGithub, FaLinkedin, FaEnvelope } from "react-icons/fa";

const Footer: React.FC = () => {
  return (
    <footer className="footer fade-in">
      <div className="container mx-auto text-center">
        <p>
          © {new Date().getFullYear()} Silas Vasconcelos Cruz portfolio. All rights
          reserved.
        </p>

        <div className="social-icons">
          <a
            href="https://github.com/s-v7"
            target="_blank"
            rel="noopener noreferrer"
            aria-label="GitHub profile"
          >
            <FaGithub />
          </a>

          <a
            href="https://www.linkedin.com/in/silas-v-053293255/"
            target="_blank"
            rel="noopener noreferrer"
            aria-label="LinkedIn profile"
          >
            <FaLinkedin />
          </a>

          <a
            href="mailto:svasconceloscruz7@gmail.com"
            aria-label="Send email"
          >
            <FaEnvelope />
          </a>
        </div>
      </div>
    </footer>
  );
};

export default Footer;

