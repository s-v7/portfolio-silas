import { useEffect, useRef, useState, type KeyboardEvent } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

import type { Props } from "@/data/chatWindow";
import type { FeedbackPayload } from "../types";
import { NegativeFeedbackModal } from "./NegativeFeedbackModal";

const INTENT_LABELS: Record<string, string> = {
  experience: "Experience",
  ai: "AI",
  java: "Java",
  projects: "Projects",
  skills: "Skills",
  education: "Education",
  security: "Security",
  "career-tool": "AI Tool",
  general: "Professional profile",
};

const QUICK_QUESTIONS = [
  {
    label: "Tell me about Silas",
    prompt:
      "Give me a concise professional overview of Silas, including his strongest differentiators.",
  },
  {
    label: "Strongest Java skills",
    prompt: "What are Silas's strongest Java, Java EE, and Jakarta EE skills?",
  },
  {
    label: "Enterprise modernization",
    prompt: "Explain Silas's experience modernizing legacy enterprise systems.",
  },
  {
    label: "AI projects",
    prompt: "Which applied AI and LLM projects has Silas built?",
  },
  {
    label: "Why hire Silas?",
    prompt:
      "Why would Silas be a strong candidate for a Full Stack, Backend, DevSecOps, or AI Engineering role?",
  },
] as const;

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
  onPrompt,
  onExploreProfile,
  onSend,
  onClear,
  onFeedback,
}: Readonly<Props>) {
  const [feedbackTarget, setFeedbackTarget] = useState<FeedbackTarget | null>(null);
  const [submittingFeedback, setSubmittingFeedback] = useState(false);
  const [feedbackError, setFeedbackError] = useState("");

  const messagesEndRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const providerLabel = provider === "nvidia" ? "NVIDIA NIM" : "OpenAI";
  const showWelcome = messages.length <= 1;
  const canSend = input.trim().length > 0 && !loading;

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
      block: "end",
    });
  }, [messages, loading]);

  useEffect(() => {
    const textarea = textareaRef.current;
    if (!textarea) return;

    textarea.style.height = "auto";
    textarea.style.height = `${Math.min(textarea.scrollHeight, 180)}px`;
  }, [input]);

  function handleKeyDown(event: KeyboardEvent<HTMLTextAreaElement>) {
    if (event.key === "Enter" && !event.shiftKey && !event.nativeEvent.isComposing) {
      event.preventDefault();

      if (canSend) {
        onSend();
      }
    }
  }

  async function submitPositiveFeedback(messageId: string, interactionId: string) {
    setFeedbackError("");

    try {
      await onFeedback(messageId, interactionId, { rating: 1 });
    } catch (error) {
      setFeedbackError(error instanceof Error ? error.message : "Feedback could not be submitted.");
    }
  }

  async function submitNegativeFeedback(feedback: FeedbackPayload) {
    if (!feedbackTarget) return;

    setSubmittingFeedback(true);
    setFeedbackError("");

    try {
      await onFeedback(feedbackTarget.messageId, feedbackTarget.interactionId, feedback);

      setFeedbackTarget(null);
    } catch (error) {
      setFeedbackError(error instanceof Error ? error.message : "Feedback could not be submitted.");
    } finally {
      setSubmittingFeedback(false);
    }
  }

  return (
    <>
      <section className="career-chat-card">
        <header className="career-chat__header">
          <div className="career-chat__heading">
            <h2>Career Assistant</h2>
            <p>Grounded in Silas&apos;s CV, experience, and projects</p>
          </div>

          <div className="career-chat__header-right">
            <nav className="career-chat__professional-links" aria-label="Professional links">
              <a
                href={`${import.meta.env.BASE_URL}Silas_V_C_EN.pdf`}
                target="_blank"
                rel="noopener noreferrer"
                className="career-chat__link career-chat__link--primary"
              >
                <span aria-hidden="true">↓</span>
                CV
              </a>

              <a
                href="https://github.com/s-v7"
                target="_blank"
                rel="noopener noreferrer"
                className="career-chat__link"
              >
                GitHub
              </a>

              <a
                href="https://www.linkedin.com/in/silas-v-053293255/"
                target="_blank"
                rel="noopener noreferrer"
                className="career-chat__link"
              >
                LinkedIn
              </a>
            </nav>

            <div className="career-chat__actions">
              <span className="career-chat__provider">
                <span aria-hidden="true" className="career-chat__status-dot" />
                {providerLabel}
              </span>

              <button
                type="button"
                className="career-chat__action-button"
                onClick={onExploreProfile}
              >
                <span aria-hidden="true">☰</span>
                Explore profile
              </button>

              <button
                type="button"
                className="career-chat__action-button career-chat__action-button--clear"
                onClick={onClear}
              >
                Clear
              </button>
            </div>
          </div>
        </header>

        <div className="career-chat-messages">
          {showWelcome && (
            <section className="career-chat-welcome">
              <span className="career-chat-welcome__eyebrow">AI Career Assistant</span>

              <h2>How can I help you explore Silas's career?</h2>

              <p>
                Ask about enterprise modernization, Java, backend architecture, DevSecOps, applied
                AI, projects, or professional experience.
              </p>

              <div className="career-quick-questions" aria-label="Suggested questions">
                {QUICK_QUESTIONS.map(({ label, prompt }) => (
                  <button
                    key={label}
                    type="button"
                    disabled={loading}
                    onClick={() => onPrompt(prompt)}
                  >
                    <span>{label}</span>
                    <span aria-hidden="true">↗</span>
                  </button>
                ))}
              </div>
            </section>
          )}

          <div className="career-conversation">
            {messages.map((msg) => (
              <article key={msg.id} className={`career-message career-message--${msg.role}`}>
                <div className="career-message-avatar" aria-hidden="true">
                  {msg.role === "user" ? "Y" : "SV"}
                </div>

                <div className="career-message-body">
                  <div className="career-message-meta">
                    <span className="career-message-author">
                      {msg.role === "user" ? "You" : "Silas AI"}
                    </span>

                    {msg.role === "assistant" && msg.intent && (
                      <span className="career-intent-badge">
                        {INTENT_LABELS[msg.intent] ?? msg.intent}
                      </span>
                    )}
                  </div>

                  <div className="career-message-content">
                    <ReactMarkdown remarkPlugins={[remarkGfm]}>{msg.content}</ReactMarkdown>
                  </div>

                  {msg.role === "assistant" && msg.interactionId && (
                    <div className="career-message-feedback">
                      {msg.feedback ? (
                        <span className="career-feedback-confirmation">
                          Feedback recorded. Thank you.
                        </span>
                      ) : (
                        <>
                          <span>Was this response useful?</span>

                          <button
                            type="button"
                            aria-label="Helpful response"
                            onClick={() => void submitPositiveFeedback(msg.id, msg.interactionId!)}
                          >
                            👍 Yes
                          </button>

                          <button
                            type="button"
                            aria-label="Unhelpful response"
                            onClick={() =>
                              setFeedbackTarget({
                                messageId: msg.id,
                                interactionId: msg.interactionId!,
                              })
                            }
                          >
                            👎 No
                          </button>
                        </>
                      )}
                    </div>
                  )}
                </div>
              </article>
            ))}

            {feedbackError && <p className="career-feedback-error">{feedbackError}</p>}

            {loading && (
              <article className="career-message career-message--assistant">
                <div className="career-message-avatar" aria-hidden="true">
                  SV
                </div>

                <div className="career-message-body">
                  <div className="career-message-author">Silas AI</div>

                  <div className="career-thinking" aria-label="Generating response">
                    <span />
                    <span />
                    <span />
                    <small>Searching the professional knowledge base</small>
                  </div>
                </div>
              </article>
            )}

            <div ref={messagesEndRef} aria-hidden="true" />
          </div>
        </div>

        <div className="career-composer-shell">
          <div className="career-chat-input">
            <textarea
              ref={textareaRef}
              rows={1}
              placeholder="Ask anything about Silas's career..."
              value={input}
              disabled={loading}
              onChange={(event) => onInputChange(event.target.value)}
              onKeyDown={handleKeyDown}
              aria-label="Message"
            />

            <button
              onClick={onSend}
              disabled={!canSend}
              type="button"
              aria-label="Send message"
              title="Send message"
            >
              <span aria-hidden="true">↑</span>
            </button>
          </div>

          <small className="career-composer-hint">
            Press Enter to send · Shift + Enter for a new line
          </small>
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
