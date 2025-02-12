import React, { useState } from "react";
import "./Contact.css";


const Contact = () => {
  const [formData, setFormData] = useState({
    nome: "",
    email: "",
    assunto: "",
    mensagem: "",
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Formulário enviado:", formData);
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white p-6 flex items-center justify-center">
      <form
        onSubmit={handleSubmit}
        className="bg-gray-800 p-6 rounded-lg shadow-lg w-full max-w-lg"
      >
        <h2 className="text-3xl font-bold mb-4 text-center">Contato</h2>
        <div className="mb-4">
          <input
            type="text"
            name="nome"
            placeholder="Seu Nome"
            value={formData.nome}
            onChange={handleChange}
            className="w-full p-2 rounded bg-gray-700 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <div className="mb-4">
          <input
            type="email"
            name="email"
            placeholder="Seu E-mail"
            value={formData.email}
            onChange={handleChange}
            className="w-full p-2 rounded bg-gray-700 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <div className="mb-4">
          <input
            type="text"
            name="assunto"
            placeholder="Assunto"
            value={formData.assunto}
            onChange={handleChange}
            className="w-full p-2 rounded bg-gray-700 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <div className="mb-4">
          <textarea
            name="mensagem"
            placeholder="Sua Mensagem"
            value={formData.mensagem}
            onChange={handleChange}
            className="w-full p-2 rounded bg-gray-700 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
            rows="4"
          ></textarea>
        </div>
        <button
          type="submit"
          className="w-full py-2 bg-blue-500 text-white font-bold rounded hover:bg-blue-600 transition duration-300"
        >
          Enviar
        </button>
      </form>
    </div>
  );
};

export default Contact;

