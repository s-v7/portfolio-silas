import { useEffect, useRef, useState } from "react";

import {
  clearStoredConversation,
  loadConversation,
  saveConversation,
} from "../services/conversationStorage";
import { askCareerAssistant, sendCareerFeedback } from "../services/api";
import type { CareerMessage, FeedbackPayload, ProviderId } from "../types";

const DEFAULT_PROVIDER: ProviderId = "openai";

const createInitialMessage = (): CareerMessage => ({
  id: crypto.randomUUID(),
  role: "assistant",
  content:
    "Hello! I am Silas's AI Career Assistant.\n\nI can answer questions about his professional background, projects, technologies, enterprise modernization, applied AI, and education.",
  provider: DEFAULT_PROVIDER,
});

function createInitialConversation() {
  return (
    loadConversation() ?? {
      provider: DEFAULT_PROVIDER,
      messages: [createInitialMessage()],
    }
  );
}

export function useCareerChat() {
  const [initialConversation] = useState(createInitialConversation);

  const [provider, setProvider] = useState<ProviderId>(
    initialConversation.provider
  );
  const [messages, setMessages] = useState<CareerMessage[]>(
    initialConversation.messages
  );
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const skipNextPersistenceRef = useRef(false);

  useEffect(() => {
    if (skipNextPersistenceRef.current) {
      skipNextPersistenceRef.current = false;
      return;
    }

    saveConversation(provider, messages);
  }, [provider, messages]);

  async function sendMessage(customText?: string) {
    const text = (customText ?? input).trim();

    if (!text || loading) return;

    setMessages((previous) => [
      ...previous,
      {
        id: crypto.randomUUID(),
        role: "user",
        content: text,
      },
    ]);

    setInput("");
    setLoading(true);

    try {
      const data = await askCareerAssistant(provider, text);

      setMessages((previous) => [
        ...previous,
        {
          id: crypto.randomUUID(),
          role: "assistant",
          content: data.answer || "Sem resposta.",
          provider: data.provider,
          intent: data.intent,
          interactionId: data.interactionId,
        },
      ]);
    } catch (error) {
      const message =
        error instanceof Error ? error.message : "Erro desconhecido";

      setMessages((previous) => [
        ...previous,
        {
          id: crypto.randomUUID(),
          role: "assistant",
          content: `Não foi possível obter resposta agora. ${message}`,
          provider,
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  async function rateMessage(
    messageId: string,
    interactionId: string,
    feedback: FeedbackPayload
  ) {
    await sendCareerFeedback(interactionId, feedback);

    setMessages((previous) =>
      previous.map((message) =>
        message.id === messageId
          ? { ...message, feedback: feedback.rating }
          : message
      )
    );
  }

  function clearConversation() {
    skipNextPersistenceRef.current = true;
    clearStoredConversation();

    setMessages([createInitialMessage()]);
    setInput("");
  }

  return {
    provider,
    setProvider,
    messages,
    input,
    setInput,
    loading,
    sendMessage,
    rateMessage,
    clearConversation,
  };
}
