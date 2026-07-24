import { useEffect, useState } from "react";

import { ProviderSelector } from "../ProviderSelector";
import { RecruiterToolkit } from "../RecruiterToolkit";
import { ChatWindow } from "../ChatWindow";
import { CareerSidebar } from "../CareerSidebar";
import type { Props } from "../../../../data/careerDashboard";

export function CareerDashboard(props: Readonly<Props>) {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  useEffect(() => {
    if (!sidebarOpen) return;

    const previousOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";

    function handleEscape(event: KeyboardEvent) {
      if (event.key === "Escape") {
        setSidebarOpen(false);
      }
    }

    document.addEventListener("keydown", handleEscape);

    return () => {
      document.body.style.overflow = previousOverflow;
      document.removeEventListener("keydown", handleEscape);
    };
  }, [sidebarOpen]);

  function handlePrompt(prompt: string) {
    props.onPrompt(prompt);
    setSidebarOpen(false);
  }

  return (
    <main className="career-dashboard">
      <header className="career-dashboard__header">
        <div>
          <p>AI Career Assistant</p>
          <h2>Portfólio do Silas Vasconcelos Cruz (s-v7)</h2>
        </div>

        <RecruiterToolkit />
      </header>

      <div className="career-mobile-toolbar">
        <div>
          <strong>AI Career</strong>
          <span>Assistente profissional</span>
        </div>

        <button
          type="button"
          className="career-sidebar-toggle"
          aria-expanded={sidebarOpen}
          aria-controls="career-sidebar-drawer"
          onClick={() => setSidebarOpen(true)}
        >
          <span aria-hidden="true">☰</span>
          Base
        </button>
      </div>

      <ProviderSelector
        provider={props.provider}
        onChange={props.onProviderChange}
      />

      <section className="career-dashboard__grid">
        <div
          className={`career-sidebar-shell ${
            sidebarOpen ? "career-sidebar-shell--open" : ""
          }`}
        >
          <button
            type="button"
            className="career-sidebar-backdrop"
            aria-label="Fechar base profissional"
            onClick={() => setSidebarOpen(false)}
          />

          <div
            id="career-sidebar-drawer"
            className="career-sidebar-drawer"
            role="dialog"
            aria-modal={sidebarOpen ? "true" : undefined}
            aria-label="Base profissional"
          >
            <header className="career-sidebar-drawer__header">
              <div>
                <strong>Base profissional</strong>
                <span>CV, experiência, projetos e ferramentas</span>
              </div>

              <button
                type="button"
                aria-label="Fechar"
                onClick={() => setSidebarOpen(false)}
              >
                ×
              </button>
            </header>

            <CareerSidebar
              loading={props.loading}
              onPrompt={handlePrompt}
              provider={props.provider}
              onProviderChange={props.onProviderChange}
            />
          </div>
        </div>

        <ChatWindow
          provider={props.provider}
          messages={props.messages}
          input={props.input}
          loading={props.loading}
          onInputChange={props.onInputCHange}
          onSend={props.onSend}
          onClear={props.onClear}
          onFeedback={props.onFeedback}
        />
      </section>
    </main>
  );
}
