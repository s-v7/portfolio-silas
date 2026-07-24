import type { AnalyticsResponse } from "../analytics.types";

const API_BASE_URL = import.meta.env.VITE_API_URL || "";

export async function fetchLearningAnalytics(
  adminToken: string
): Promise<AnalyticsResponse> {
  if (!API_BASE_URL) {
    throw new Error("VITE_API_URL não configurada.");
  }

  const response = await fetch(`${API_BASE_URL}/api/analytics`, {
    method: "GET",
    headers: {
      Authorization: `Bearer ${adminToken}`,
    },
  });

  const contentType = response.headers.get("content-type") || "";

  if (!contentType.includes("application/json")) {
    throw new Error("Resposta inválida do AI Gateway.");
  }

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.details || data.error || "Falha ao carregar analytics.");
  }

  return data as AnalyticsResponse;
}
