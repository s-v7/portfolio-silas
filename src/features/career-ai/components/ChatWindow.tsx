import type { CareerMessage, ProviderId } from "../types";

type Props = {
  provider: ProviderId;
  messages: CareerMessage[];
  input: string;
  loading: boolean;
  onInputChange: (value: string) => void;
  onSend: () => void;
  onClear: () => void;
};

export function ChatWindow({
  provider,
  messages,
  input,
  loading,
  onInputChange,
  onSend,
  onClear,
}: Props) {
  const providerLabel = provider === "nvidia" ? "NVIDIA" : "OpenAI";

  return (
    <section className="career-chat-card">
      <div className="career-chat-header">
        <div className="career-chat-title">
          <strong>Career Assistant</strong>
          <span>Baseado no CV, projetos e experiência do Silas</span>
        </div>

        <div className="career-chat-actions">
          <span className="career-chat-status">{providerLabel}</span>
          <button type="button" onClick={onClear} className="chat-clear-btn">
            Limpar
          </button>
        </div>
      </div>

      <div className="career-chat-messages">
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`career-message ${
              msg.role === "user"
                ? "career-message--user"
                : "career-message--assistant"
            }`}
          >
            <div className="career-message-author">
              {msg.role === "user" ? "Você" : "AI Assistant"}
            </div>
            <p>{msg.content}</p>
          </div>
        ))}

        {loading && (
          <div className="career-message career-message--assistant">
            <div className="career-message-author">AI Assistant</div>
            <p>Consultando a base profissional...</p>
          </div>
        )}
      </div>

      <div className="career-chat-input">
        <input
          type="text"
          placeholder="Pergunte algo sobre a trajetória do Silas..."
          value={input}
          onChange={(e) => onInputChange(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && onSend()}
        />

        <button onClick={onSend} disabled={loading} type="button">
          {loading ? "Enviando..." : "Enviar"}
        </button>
      </div>
    </section>
  );
}
