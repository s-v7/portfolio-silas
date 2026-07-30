import { KNOWLEDGE_ITEMS, Props } from "../../../data/knowledgeBase";

export function KnowledgeBase({ loading, onSelect }: Readonly<Props>) {
  return (
    <section className="knowledge-base">
      <h2>Knowledge Base</h2>
      <div className="knowledge-list">
        {KNOWLEDGE_ITEMS.map((item) => (
          <button
            key={item.label}
            type="button"
            className="knowledge-card"
            disabled={loading}
            onClick={() => onSelect(item.prompt)}
          >
            <strong>{item.label}</strong>
            <small>{item.description}</small>
          </button>
        ))}
      </div>
    </section>
  );
}
