import { useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

import type { Props } from "@/data/chatWindow";
import type { FeedbackPayload } from "../types";
import { NegativeFeedbackModal } from "./NegativeFeedbackModal";

const INTENT_LABELS: Record<string, string> = {
  experience: "Experiência",
  ai: "IA",
  java: "Java",
  projects: "Projetos",
  skills: "Competências",
  education: "Formação",
  security: "Segurança",
  "career-tool": "AI Tool",
  general: "Perfil profissional",
};

type FeedbackTarget = {
  messageId: string;
  interactionId: string;
};

export function ChatWindow({
  provider,
  messages,
  input,
  loading,
  onInputChange,
  onSend,
  onClear,
  onFeedback,
}: Readonly<Props>) {
  const [feedbackTarget, setFeedbackTarget] =
    useState<FeedbackTarget | null>(null);
  const [submittingFeedback, setSubmittingFeedback] = useState(false);
  const [feedbackError, setFeedbackError] = useState("");

  const providerLabel = provider === "nvidia" ? "NVIDIA" : "OpenAI";

  async function submitPositiveFeedback(
    messageId: string,
    interactionId: string
  ) {
    setFeedbackError("");

    try {
      await onFeedback(messageId, interactionId, { rating: 1 });
    } catch (error) {
      setFeedbackError(
        error instanceof Error
          ? error.message
          : "Não foi possível registrar o feedback."
      );
    }
  }

  async function submitNegativeFeedback(feedback: FeedbackPayload) {
    if (!feedbackTarget) return;

    setSubmittingFeedback(true);
    setFeedbackError("");

    try {
      await onFeedback(
        feedbackTarget.messageId,
        feedbackTarget.interactionId,
        feedback
      );

      setFeedbackTarget(null);
    } catch (error) {
      setFeedbackError(
        error instanceof Error
          ? error.message
          : "Não foi possível registrar o feedback."
      );
    } finally {
      setSubmittingFeedback(false);
    }
  }

  return (
    <>
      <section className="career-chat-card">
        <div className="career-chat-header">
          <div className="career-chat-title">
            <strong>Career Assistant</strong>
            <span>Baseado no CV, projetos e experiência do Silas</span>
          </div>

          <div className="career-chat-actions">
            <span className="career-chat-status">{providerLabel}</span>

            <button
              type="button"
              onClick={onClear}
              className="chat-clear-btn"
            >
              Limpar
            </button>
          </div>
        </div>

        <div className="career-chat-messages">
          {messages.map((msg) => (
            <article
              key={msg.id}
              className={`career-message career-message--${msg.role}`}
            >
              <div className="career-message-meta">
                <span className="career-message-author">
                  {msg.role === "user" ? "Você" : "AI Assistant"}
                </span>

                {msg.role === "assistant" && msg.intent && (
                  <span className="career-intent-badge">
                    {INTENT_LABELS[msg.intent] ?? msg.intent}
                  </span>
                )}
              </div>

              <div className="career-message-content">
                <ReactMarkdown remarkPlugins={[remarkGfm]}>
                  {msg.content}
                </ReactMarkdown>
              </div>

              {msg.role === "assistant" && msg.interactionId && (
                <div className="career-message-feedback">
                  {msg.feedback ? (
                    <span className="career-feedback-confirmation">
                      Feedback registrado. Obrigado!
                    </span>
                  ) : (
                    <>
                      <span>Esta resposta foi útil?</span>

                      <button
                        type="button"
                        onClick={() =>
                          void submitPositiveFeedback(
                            msg.id,
                            msg.interactionId!
                          )
                        }
                      >
                        👍 Sim
                      </button>

                      <button
                        type="button"
                        onClick={() =>
                          setFeedbackTarget({
                            messageId: msg.id,
                            interactionId: msg.interactionId!,
                          })
                        }
                      >
                        👎 Não
                      </button>
                    </>
                  )}
                </div>
              )}
            </article>
          ))}

          {feedbackError && (
            <p className="career-feedback-error">{feedbackError}</p>
          )}

          {loading && (
            <div className="career-message career-message--assistant">
              <div className="career-message-author">AI Assistant</div>

              <div className="career-message-content">
                <p>Consultando a base profissional...</p>
              </div>
            </div>
          )}
        </div>

        <div className="career-chat-input">
          <input
            type="text"
            placeholder="Pergunte algo sobre a trajetória do Silas..."
            value={input}
            onChange={(event) => onInputChange(event.target.value)}
            onKeyDown={(event) => {
              if (event.key === "Enter" && !loading) onSend();
            }}
          />

          <button onClick={onSend} disabled={loading} type="button">
            {loading ? "Enviando..." : "Enviar"}
          </button>
        </div>
      </section>

      <NegativeFeedbackModal
        open={feedbackTarget !== null}
        submitting={submittingFeedback}
        onClose={() => {
          if (!submittingFeedback) {
            setFeedbackTarget(null);
            setFeedbackError("");
          }
        }}
        onSubmit={submitNegativeFeedback}
      />
    </>
  );
}
