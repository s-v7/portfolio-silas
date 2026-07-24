import { useState } from "react";

import type {
  FeedbackPayload,
  FeedbackReason,
} from "../types";

type Props = {
  open: boolean;
  submitting: boolean;
  onClose: () => void;
  onSubmit: (feedback: FeedbackPayload) => Promise<void>;
};

const REASONS: Array<{
  value: FeedbackReason;
  label: string;
}> = [
  { value: "incomplete", label: "Resposta incompleta" },
  { value: "incorrect", label: "Informação incorreta" },
  { value: "too_generic", label: "Resposta muito genérica" },
  { value: "not_answered", label: "Não respondeu à pergunta" },
  { value: "other", label: "Outro motivo" },
];

export function NegativeFeedbackModal({
  open,
  submitting,
  onClose,
  onSubmit,
}: Readonly<Props>) {
  const [reason, setReason] =
    useState<FeedbackReason>("incomplete");
  const [comment, setComment] = useState("");

  if (!open) return null;

  function close() {
    if (submitting) return;

    setReason("incomplete");
    setComment("");
    onClose();
  }

  async function submit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();

    await onSubmit({
      rating: -1,
      reason,
      comment: comment.trim() || undefined,
    });

    setReason("incomplete");
    setComment("");
  }

  return (
    <div className="feedback-modal-backdrop" role="presentation">
      <form
        className="feedback-modal"
        onSubmit={submit}
        role="dialog"
        aria-modal="true"
        aria-labelledby="feedback-modal-title"
      >
        <header>
          <div>
            <p>Feedback da resposta</p>
            <h2 id="feedback-modal-title">
              Como podemos melhorar?
            </h2>
          </div>

          <button
            type="button"
            onClick={close}
            aria-label="Fechar"
          >
            ×
          </button>
        </header>

        <div className="feedback-modal__reasons">
          {REASONS.map((item) => (
            <label key={item.value}>
              <input
                type="radio"
                name="feedback-reason"
                value={item.value}
                checked={reason === item.value}
                onChange={() => setReason(item.value)}
              />
              <span>{item.label}</span>
            </label>
          ))}
        </div>

        <label className="feedback-modal__comment">
          <span>Comentário opcional</span>
          <textarea
            value={comment}
            maxLength={500}
            rows={4}
            placeholder="Explique brevemente o que faltou na resposta."
            onChange={(event) => setComment(event.target.value)}
          />
          <small>{comment.length}/500</small>
        </label>

        <footer>
          <button
            type="button"
            onClick={close}
            disabled={submitting}
          >
            Cancelar
          </button>

          <button type="submit" disabled={submitting}>
            {submitting ? "Enviando..." : "Enviar feedback"}
          </button>
        </footer>
      </form>
    </div>
  );
}
