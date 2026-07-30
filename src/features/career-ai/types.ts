export type ProviderId = "anthropic" | "nvidia" | "openai";

export type ChatRole = "user" | "assistant" | "system";

export type FeedbackRating = -1 | 1;

export type FeedbackReason =
  | "incomplete"
  | "incorrect"
  | "too_generic"
  | "not_answered"
  | "other";

export type FeedbackPayload = {
  rating: FeedbackRating;
  reason?: FeedbackReason;
  comment?: string;
};

export type CareerMessage = {
  id: string;
  role: ChatRole;
  content: string;
  provider?: ProviderId;
  intent?: string;
  interactionId?: string;
  feedback?: FeedbackRating;
};

export type ProviderOption = {
  id: ProviderId;
  label: string;
  status: "online" | "offline" | "disabled";
  description: string;
};

export type ChatResponse = {
  interactionId: string;
  provider: ProviderId;
  intent: string;
  answer: string;
};

export type FeedbackResponse = {
  ok: boolean;
};
