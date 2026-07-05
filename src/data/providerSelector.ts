import type { ProviderId, ProviderOption } from "@/features/career-ai/types";

export const PROVIDERS: ProviderOption[] = [
  {
    id: "openai",
    label: "OpenAI",
    status: "online",
    description: "GPT model",
  },
  {
    id: "nvidia",
    label: "NVIDIA",
    status: "online",
    description: "Llama / NIM",
  },
  {
    id: "anthropic",
    label: "Claude",
    status: "disabled",
    description: "Sem créditos",
  },
];

export type Props = {
  provider: ProviderId;
  onChange: (provider: ProviderId) => void;
};
