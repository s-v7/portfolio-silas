import type { ProviderId } from "@/features/career-ai/types";

export type Props = {
  provider: ProviderId;
  loading: boolean;
  onProviderChange: (provider: ProviderId) => void;
  onPrompt: (prompt: string) => void;
};
