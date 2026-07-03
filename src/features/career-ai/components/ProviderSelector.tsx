import type { ProviderId, ProviderOption } from "../types";

const PROVIDERS: ProviderOption[] = [
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

type Props = {
  provider: ProviderId;
  onChange: (provider: ProviderId) => void;
};

export function ProviderSelector({ provider, onChange }: Props) {
  return (
    <section>
      <h2>Provider</h2>

      <div className="provider-list">
        {PROVIDERS.map((p) => (
          <button
            key={p.id}
            className={`provider-card ${
              provider === p.id ? "provider-card--active" : ""
            }`}
            onClick={() => onChange(p.id)}
            disabled={p.status === "disabled"}
            type="button"
          >
            <span>{p.label}</span>
            <small>{p.description}</small>
          </button>
        ))}
      </div>
    </section>
  );
}
