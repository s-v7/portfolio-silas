import { useState, ChangeEvent, FormEvent } from "react";

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

  const handleChange = (
    e: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ): void => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e: FormEvent<HTMLFormElement>): void => {
    e.preventDefault();
    console.log("Contact form submitted:", formData);
  };

  const openWhatsApp = () => {
    const text = `
Olá! Gostaria de entrar em contato para saber mais informações.

${formData.mensagem}
    `.trim();

    const url = `https://api.whatsapp.com/send?phone=${WHATSAPP_NUMBER}&text=${encodeURIComponent(
      text
    )}`;

    window.open(url, "_blank");
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white p-6 flex items-center justify-center">
      <form
        onSubmit={handleSubmit}
        className="bg-gray-800 p-6 rounded-lg shadow-lg w-full max-w-lg"
        noValidate
      >
        <h2 className="text-3xl font-bold mb-6 text-center">Contact</h2>

        <input
          name="nome"
          placeholder="Your name"
          value={formData.nome}
          onChange={handleChange}
          className="w-full p-2 mb-4 rounded bg-gray-700 text-white"
        />

        <input
          type="email"
          name="email"
          placeholder="Your email"
          value={formData.email}
          onChange={handleChange}
          className="w-full p-2 mb-4 rounded bg-gray-700 text-white"
        />

        <input
          name="assunto"
          placeholder="Subject"
          value={formData.assunto}
          onChange={handleChange}
          className="w-full p-2 mb-4 rounded bg-gray-700 text-white"
        />

        <textarea
          name="mensagem"
          placeholder="Your message"
          rows={4}
          value={formData.mensagem}
          onChange={handleChange}
          className="w-full p-2 mb-6 rounded bg-gray-700 text-white"
        />

        <button
          type="submit"
          className="w-full py-2 mb-3 bg-blue-500 rounded hover:bg-blue-600 transition"
        >
          Send message
        </button>

        {/* WhatsApp direto */}
        <button
          type="button"
          onClick={openWhatsApp}
          className=" whatsapp-btn w-full py-2 bg-green-500 text-black font-semibold rounded hover:bg-green-600 transition"
        >
          💬 Contact via WhatsApp
        </button>
      </form>
    </div>
  );
};

export default Contact;
