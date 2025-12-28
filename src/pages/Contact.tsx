import { useState, ChangeEvent, FormEvent } from "react";


interface ContactFormData {
  nome: string;
  email: string;
  assunto: string;
  mensagem: string;
}


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

    // Placeholder for real integration (API / email service)
    console.log("Contact form submitted:", formData);
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white p-6 flex items-center justify-center">
      <form
        onSubmit={handleSubmit}
        className="bg-gray-800 p-6 rounded-lg shadow-lg w-full max-w-lg"
        noValidate
      >
        <h2 className="text-3xl font-bold mb-6 text-center">Contact</h2>

        <div className="mb-4">
          <label htmlFor="nome" className="sr-only">
            Your name
          </label>
          <input
            id="nome"
            type="text"
            name="nome"
            placeholder="Your name"
            value={formData.nome}
            onChange={handleChange}
            required
            className="w-full p-2 rounded bg-gray-700 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div className="mb-4">
          <label htmlFor="email" className="sr-only">
            Your email
          </label>
          <input
            id="email"
            type="email"
            name="email"
            placeholder="Your email"
            value={formData.email}
            onChange={handleChange}
            required
            className="w-full p-2 rounded bg-gray-700 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div className="mb-4">
          <label htmlFor="assunto" className="sr-only">
            Subject
          </label>
          <input
            id="assunto"
            type="text"
            name="assunto"
            placeholder="Subject"
            value={formData.assunto}
            onChange={handleChange}
            className="w-full p-2 rounded bg-gray-700 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div className="mb-6">
          <label htmlFor="mensagem" className="sr-only">
            Message
          </label>
          <textarea
            id="mensagem"
            name="mensagem"
            placeholder="Your message"
            value={formData.mensagem}
            onChange={handleChange}
            rows={4}
            required
            className="w-full p-2 rounded bg-gray-700 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <button
          type="submit"
          className="w-full py-2 bg-blue-500 text-white font-bold rounded hover:bg-blue-600 transition"
        >
          Send message
        </button>
      </form>
    </div>
  );
};

export default Contact;

