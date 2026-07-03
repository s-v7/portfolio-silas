import type { ChatResponse, ProviderId } from "../types";

const API_URL = "/api/chat";

export async function askCareerAssistant(
  provider: ProviderId,
  message: string
): Promise<ChatResponse> {
  const response = await fetch(API_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({provider, mode: "career", message}),
  });
  const data = await response.json();

  if(!response.ok) { throw new Error(data.details || data.error || "Erro na API"); }

  return data;
}
