import { ProviderSelector } from "../ProviderSelector";
import { RecruiterToolkit } from "../RecruiterToolkit";
import { ChatWindow } from "../ChatWindow";
import { CareerSidebar } from "../CareerSidebar";
import { Props } from "../../../../data/careerDashboard";

export function CareerDashboard(props: Readonly<Props>) {
  return (
    <main className="career-dashboard">
      <header className="career-dashboard__header">
        <div>
          <p>AI Career Assistant</p>
          <h2>Portfólio do Silas Vasconcelos Cruz(s-v7)</h2>
        </div>
        <RecruiterToolkit />
      </header>

      <ProviderSelector provider={props.provider} onChange={props.onProviderChange} />

      <section className="career-dashboard__grid">
        <CareerSidebar
          loading={props.loading}
          onPrompt={props.onPrompt}
          provider={"anthropic"}
          onProviderChange={function (): void {
            throw new Error("Function not implemented.");
          }}
        />

        <ChatWindow
          provider={props.provider}
          messages={props.messages}
          input={props.input}
          loading={props.loading}
          onInputChange={props.onInputCHange}
          onSend={props.onSend}
          onClear={props.onClear}
        />
      </section>
    </main>
  );
}
