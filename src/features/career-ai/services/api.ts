import type { ChatResponse, ProviderId } from "../types";

const API_BASE_URL = import.meta.env.VITE_API_URL || "";

function getApiUrl() {
  if (import.meta.env.PROD && !API_BASE_URL) {
    throw new Error(
      "AI Gateway não configurado no ambiente publicado. A interface está online, mas as LLMs funcionam apenas localmente até o backend ser publicado."
    );
  }

  return `${API_BASE_URL}/api/chat`;
}

export async function askCareerAssistant(
  provider: ProviderId,
  message: string
): Promise<ChatResponse> {
  const response = await fetch(getApiUrl(), {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ provider, mode: "career", message }),
  });

  const contentType = response.headers.get("content-type") || "";

  if (!contentType.includes("application/json")) {
    throw new Error(
      "AI Gateway indisponível. No GitHub Pages, o backend de IA precisa estar publicado separadamente."
    );
  }

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.details || data.error || "Erro na API");
  }

  return data;
}
