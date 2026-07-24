import { useState } from "react";
import {
  askCareerAssistant,
  sendCareerFeedback,
} from "../services/api";
import type {
  CareerMessage,
  FeedbackPayload,
  ProviderId,
} from "../types";

const createInitialMessage = (): CareerMessage => ({
  id: crypto.randomUUID(),
  role: "assistant",
  content:
    "Olá! Sou o AI Career Assistant do Silas.\n\nPosso responder perguntas sobre trajetória, projetos, tecnologias, experiência profissional e formação.",
  provider: "openai",
});

export function useCareerChat() {
  const [provider, setProvider] = useState<ProviderId>("openai");
  const [messages, setMessages] = useState<CareerMessage[]>([
    createInitialMessage(),
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

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
