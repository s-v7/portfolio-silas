import type {
  ChatResponse,
  FeedbackPayload,
  FeedbackResponse,
  ProviderId,
} from "../types";

const API_BASE_URL = import.meta.env.VITE_API_URL || "";

function getApiUrl(path: string) {
  if (import.meta.env.PROD && !API_BASE_URL) {
    throw new Error("AI Gateway não configurado no ambiente publicado.");
  }

  return `${API_BASE_URL}${path}`;
}

async function readJson<T>(response: Response): Promise<T> {
  const contentType = response.headers.get("content-type") || "";

  if (!contentType.includes("application/json")) {
    throw new Error("AI Gateway indisponível.");
  }

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.details || data.error || "Erro na API");
  }

  return data as T;
}

export async function askCareerAssistant(
  provider: ProviderId,
  message: string
): Promise<ChatResponse> {
  const response = await fetch(getApiUrl("/api/chat"), {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ provider, mode: "career", message }),
  });

  return readJson<ChatResponse>(response);
}

export async function sendCareerFeedback(
  interactionId: string,
  feedback: FeedbackPayload
): Promise<FeedbackResponse> {
  const response = await fetch(getApiUrl("/api/feedback"), {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      interactionId,
      rating: feedback.rating,
      reason: feedback.reason,
      comment: feedback.comment,
    }),
  });

  return readJson<FeedbackResponse>(response);
}
