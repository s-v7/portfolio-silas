
export type ProviderId = "anthropic" | "nvidia" | "openai";

export type CareerMessage = {
  id: string;
  role: ChatRole;
  content: string;
  provider?: ProviderId;
};

export type ProviderOption = {
  id: ProviderId;
  label: string;
  status: "online" | "offline" | "disabled";
  description: string;
};

export type ChatResponse = {
  provider: ProviderId;
  answer: string;
};

