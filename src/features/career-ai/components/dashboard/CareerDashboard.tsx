import { useEffect, useState } from "react";

import { OperationalTicker } from "../../../../components/ui/OperationalTicker";
import { ProviderSelector } from "../ProviderSelector";
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
      <OperationalTicker />
      <p className="career-hero__eyebrow">AI-first professional portfolio</p>

      <section className="career-dashboard__workspace">
        <div className={`career-sidebar-shell ${sidebarOpen ? "career-sidebar-shell--open" : ""}`}>
          <button
            type="button"
            className="career-sidebar-backdrop"
            aria-label="Close professional profile"
            onClick={() => setSidebarOpen(false)}
          />

          <aside
            id="career-profile-drawer"
            className="career-sidebar-drawer"
            role="dialog"
            aria-modal={sidebarOpen ? "true" : undefined}
            aria-label="Explore Silas's professional profile"
          >
            <div className="career-drawer-provider">
              <ProviderSelector provider={props.provider} onChange={props.onProviderChange} />
            </div>

            <CareerSidebar
              loading={props.loading}
              onPrompt={handlePrompt}
              provider={props.provider}
              onProviderChange={props.onProviderChange}
            />
          </aside>
        </div>

        <ChatWindow
          provider={props.provider}
          messages={props.messages}
          input={props.input}
          loading={props.loading}
          onInputChange={props.onInputCHange}
          onPrompt={handlePrompt}
          onSend={props.onSend}
          onClear={props.onClear}
          onFeedback={props.onFeedback}
          onExploreProfile={() => setSidebarOpen(true)}
        />
      </section>
    </main>
  );
}
