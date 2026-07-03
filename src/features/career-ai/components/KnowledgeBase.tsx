const KNOWLEDGE_ITEMS = [
  { label: "CV", description: "Resumo profissional" },
  { label: "Experiência", description: "CREA-PI, EDM, MEGi9" },
  { label: "Projetos", description: "Portfólio e laboratórios" },
  { label: "Skills", description: "Stack técnica" },
  { label: "Formação", description: "Graduação e certificações" },
];

export function KnowledgeBase() {
  return (
    <section className="knowledge-base">
      <h2>Knowledge Base</h2>

      <div className="knowledge-list">
        {KNOWLEDGE_ITEMS.map((item) => (
          <button key={item.label} type="button" className="knowledge-card">
            <strong>{item.label}</strong>
            <small>{item.description}</small>
          </button>
        ))}
      </div>
    </section>
  );
}
