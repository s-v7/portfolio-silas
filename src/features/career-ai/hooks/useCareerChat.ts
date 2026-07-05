import { useState } from "react";
import { askCareerAssistant } from "../services/api";
import type { CareerMessage, ProviderId } from "../types";

const INITIAL_MESSAGE: CareerMessage = {
  id: crypto.randomUUID(),
  role: "assistant",
  content:
    "Olá! Sou o AI Career Assistant do Silas.\n\nPosso responder perguntas sobre trajetória, projetos, tecnologias, experiência profissional, e também posso fornecer sugestões de prompts para você interagir comigo. Sinta-se à vontade para perguntar qualquer coisa!",
  provider: "openai",
};

export function useCareerChat() {
  const [provider, setProvider] = useState<ProviderId>("openai");
  const [messages, setMessages] = useState<CareerMessage[]>([INITIAL_MESSAGE]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  // sourcery skip: avoid-function-declarations-in-blocks
  async function sendMessage(customText?: string) {
    const text = (customText ?? input).trim();

    if (!text || loading) return;

    const userMessage: CareerMessage = {
      id: crypto.randomUUID(),
      role: "user",
      content: text,
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const data = await askCareerAssistant(provider, text);

      const assistantMessage: CareerMessage = {
        id: crypto.randomUUID(),
        role: "assistant",
        content: data.answer || "Sem resposta.",
        provider,
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      const err = error instanceof Error ? error.message : "Erro desconhecido";

      setMessages((prev) => [
        ...prev,
        {
          id: crypto.randomUUID(),
          role: "assistant",
          content: `Não foi possível obter resposta agora. ${err}`,
          provider,
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  function clearConversation() {
    setMessages([INITIAL_MESSAGE]);
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
    clearConversation,
  };
}
