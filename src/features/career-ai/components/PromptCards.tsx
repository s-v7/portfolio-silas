import { SUGGESTIONS, Props } from "../../../data/promptCards";

export function PromptCards({ loading, onSelect }: Readonly<Props>) {
  return (
    <section>
      <h2>Sugestões</h2>
      <div className="suggestion-list">
        {SUGGESTIONS.map((suggestion) => (
          <button
            key={suggestion}
            onClick={() => onSelect(suggestion)}
            disabled={loading}
            type="button"
          >
            {suggestion}
          </button>
        ))}
      </div>
    </section>
  );
}
