import "../styles/pages/Chat.css";

import { useCareerChat } from "../features/career-ai/hooks/useCareerChat";
import { ProviderSelector } from "../features/career-ai/components/ProviderSelector";
import { PromptCards } from "../features/career-ai/components/PromptCards";
import { CareerInsights } from "../features/career-ai/components/CareerInsights";
import { ChatWindow } from "../features/career-ai/components/ChatWindow";

import { KnowledgeBase } from "../features/career-ai/components/KnowledgeBase";

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
    <main className="career-chat-page">
      <section className="career-chat-hero">
        <p className="career-chat-label">AI Career Assistant</p>
        <h1>Converse com o portfólio do Silas</h1>
        <p>
          Pergunte sobre experiência profissional, tecnologias, projetos,
          arquitetura, IA Generativa, modernização de sistemas e objetivos de
          carreira.
        </p>
      </section>

      <section className="career-chat-layout">
        <aside className="career-chat-sidebar">
          <ProviderSelector provider={provider} onChange={setProvider} />
          <PromptCards loading={loading} onSelect={sendMessage} />
          <KnowledgeBase />
          <CareerInsights />
        </aside>

        <ChatWindow
          provider={provider}
          messages={messages}
          input={input}
          loading={loading}
          onInputChange={setInput}
          onSend={() => sendMessage()}
          onClear={clearConversation}
        />
      </section>
    </main>
  );
}
