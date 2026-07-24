import type {
  CareerMessage,
  FeedbackPayload,
  ProviderId,
} from "../features/career-ai/types";

export type Props = {
  provider: ProviderId;
  messages: CareerMessage[];
  input: string;
  loading: boolean;
  onProviderChange: (provider: ProviderId) => void;
  onPrompt: (prompt: string) => void;
  onInputCHange: (value: string) => void;
  onSend: () => void;
  onClear: () => void;
  onFeedback: (
    messageId: string,
    interactionId: string,
    feedback: FeedbackPayload
  ) => Promise<void>;
};
