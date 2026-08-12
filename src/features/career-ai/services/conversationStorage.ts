import type { CareerMessage, ProviderId } from "../types";

const STORAGE_KEY = "portfolio-silas:career-chat:v1";

type StoredConversation = {
  provider: ProviderId;
  messages: CareerMessage[];
};

function isProviderId(value: unknown): value is ProviderId {
  return value === "anthropic" || value === "nvidia" || value === "openai";
}

function isCareerMessage(value: unknown): value is CareerMessage {
  if (!value || typeof value !== "object") {
    return false;
  }

  const message = value as Partial<CareerMessage>;

  return (
    typeof message.id === "string" &&
    (message.role === "user" ||
      message.role === "assistant" ||
      message.role === "system") &&
    typeof message.content === "string"
  );
}

export function loadConversation(): StoredConversation | null {
  if (typeof window === "undefined") {
    return null;
  }

  try {
    const raw = window.localStorage.getItem(STORAGE_KEY);

    if (!raw) {
      return null;
    }

    const parsed = JSON.parse(raw) as Partial<StoredConversation>;

    if (
      !isProviderId(parsed.provider) ||
      !Array.isArray(parsed.messages) ||
      !parsed.messages.every(isCareerMessage)
    ) {
      return null;
    }

    return {
      provider: parsed.provider,
      messages: parsed.messages,
    };
  } catch {
    return null;
  }
}

export function saveConversation(
  provider: ProviderId,
  messages: CareerMessage[]
): void {
  if (typeof window === "undefined") {
    return;
  }

  const payload: StoredConversation = {
    provider,
    messages,
  };

  try {
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(payload));
  } catch {
    // A conversa continua funcionando mesmo se o armazenamento estiver indisponível.
  }
}

export function clearStoredConversation(): void {
  if (typeof window === "undefined") {
    return;
  }

  try {
    window.localStorage.removeItem(STORAGE_KEY);
  } catch {
    // Não interrompe a limpeza da interface.
  }
}
