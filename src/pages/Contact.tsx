import { useState, ChangeEvent, FormEvent } from "react";
import emailjs from "@emailjs/browser";

interface ContactFormData {
  nome: string;
  email: string;
  assunto: string;
  mensagem: string;
}

const WHATSAPP_NUMBER = "5547996919951";

const Contact: React.FC = () => {
  const [formData, setFormData] = useState<ContactFormData>({
    nome: "",
    email: "",
    assunto: "",
    mensagem: "",
  });

  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState<"idle" | "success" | "error">("idle");

  const handleChange = (
    e: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

const handleSubmit = async (e: FormEvent) => {
  e.preventDefault();
  setLoading(true);
  setStatus("idle");

  try {
    await emailjs.send(
      import.meta.env.VITE_EMAILJS_SERVICE_ID,
      import.meta.env.VITE_EMAILJS_TEMPLATE_ID,
      {
        from_name: formData.nome,
        from_email: formData.email,
        subject: formData.assunto,
        message: formData.mensagem,
      },
      import.meta.env.VITE_EMAILJS_PUBLIC_KEY
    );

    setStatus("success");
    setFormData({ nome: "", email: "", assunto: "", mensagem: "" });
  } catch (err) {
    console.error("EmailJS error:", err);
    setStatus("error");
  } finally {
    setLoading(false);
  }
};


return (
    <section className="ds-section">
      <div className="ds-container max-w-xl">
        <form onSubmit={handleSubmit} className="ds-card ds-card-pad space-y-4">
          <h2 className="ds-title text-center">Contact</h2>

          <input
            name="nome"
            placeholder="Your name"
            value={formData.nome}
            onChange={handleChange}
            required
            className="ds-input"
          />

          <input
            type="email"
            name="email"
            placeholder="Your email"
            value={formData.email}
            onChange={handleChange}
            required
            className="ds-input"
          />

          <input
            name="assunto"
            placeholder="Subject"
            value={formData.assunto}
            onChange={handleChange}
            className="ds-input"
          />

          <textarea
            name="mensagem"
            placeholder="Your message"
            rows={4}
            value={formData.mensagem}
            onChange={handleChange}
            required
            className="ds-input"
          />

          <button
            type="submit"
            className="ds-btn ds-btn-primary w-full"
            disabled={loading}
          >
            {loading ? "Sending..." : "Send message"}
          </button>

          {status === "success" && (
            <p className="text-green-400 text-sm text-center">
              Message sent successfully 
            </p>
          )}

          {status === "error" && (
            <p className="text-red-400 text-sm text-center">
              Failed to send message. Try again later.
            </p>
          )}
        </form>
      </div>
    </section>
  );
};

export default Contact;
