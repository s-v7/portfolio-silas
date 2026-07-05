import { PROVIDERS, Props } from "../../../data/providerSelector";

export function ProviderSelector({ provider, onChange }: Readonly<Props>) {
  return (
    <section>
      <h2>Providers</h2>
      <div className="provider-list">
        {PROVIDERS.map((p) => (
          <button
            key={p.id}
            className={`provider-card ${provider === p.id ? "provider-card--active" : ""}`}
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
