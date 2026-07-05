import { AI_TOOLS, Props } from "../../../data/aiTools";
import { PromptCards } from "../components/PromptCards";

export function AITools({ loading, onSelect }: Readonly<Props>) {
  return (
    <section className="ai-tools">
      <h2>AI Tools</h2>
      <div className="ai-tools-list">
        {AI_TOOLS.map((tool) => (
          <button
            key={tool}
            type="button"
            disabled={loading}
            onClick={() =>
              onSelect(`Explique como funcionaria o módulo ${tool} no AI Career do Silas.`)
            }
          >
            {tool}
          </button>
        ))}
        <PromptCards loading={loading} onSelect={onSelect} />
      </div>
    </section>
  );
}
