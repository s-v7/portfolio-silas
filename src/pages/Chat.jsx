import React, { useState } from "react";

const Chat = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false); // Indicador de carregamento

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { role: "user", content: input };
    setMessages((prevMessages) => [...prevMessages, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const response = await fetch(
        "https://api.openai.com/v1/chat/completions",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer fajhlasflah`,
          },
          body: JSON.stringify({
            model: "gpt-4",
            messages: [...messages, userMessage],
          }),
        }
      );

      const data = await response.json();
      setLoading(false);

      if (data.choices && data.choices.length > 0) {
        const botMessage = {
          role: "assistant",
          content: data.choices[0].message.content,
        };
        setMessages((prevMessages) => [...prevMessages, botMessage]);
      } else {
        throw new Error("Resposta inválida da API.");
      }
    } catch (error) {
      console.error("Erro ao conectar à OpenAI:", error);
      setLoading(false);
      setMessages((prevMessages) => [
        ...prevMessages,
        { role: "assistant", content: "Erro ao obter resposta." },
      ]);
    }
  };

  return (
    <div className="chat-container">
      <h2>🤖 AI Chat - Pergunte algo!</h2>
      <div className="chat-box">
        {messages.map((msg, index) => (
          <p
            key={index}
            className={msg.role === "user" ? "user-msg" : "bot-msg"}
          >
            <strong>{msg.role === "user" ? "Você" : "AI"}:</strong>{" "}
            {msg.content}
          </p>
        ))}
        {loading && <p className="bot-msg">Carregando...</p>}
      </div>
      <input
        type="text"
        placeholder="Digite sua pergunta..."
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyPress={(e) => e.key === "Enter" && sendMessage()}
      />
      <button onClick={sendMessage} disabled={loading}>
        Enviar
      </button>
    </div>
  );
};

export default Chat;
