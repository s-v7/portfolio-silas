import "../features/career-ai/styles/career-dashboard.css";

import { useCareerChat } from "../features/career-ai/hooks/useCareerChat";
import { CareerDashboard } from "../features/career-ai/components/dashboard/CareerDashboard";

export default function Chat() {
  const {
    provider,
    setProvider,
    messages,
    input,
    setInput,
    loading,
    sendMessage,
    clearConversation,
  } = useCareerChat();

  return (
    <CareerDashboard
      provider={provider}
      messages={messages}
      input={input}
      loading={loading}
      onProviderChange={setProvider}
      onPrompt={sendMessage}
      onInputCHange={setInput}
      onSend={() => sendMessage()}
      onClear={clearConversation}
    />
  );
}
