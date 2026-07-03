
const SUGGESTIONS = [
  "Resuma a trajetória do Silas em até 7 linhas.",
  "Qual é a experiência do Silas com Java?",
  "Quais são os principais pontos fortes do Silas?",
  "Como o Silas atua com IA Generativa?",
  "Quais tecnologias o Silas domina?",
  "Por que o Silas seria uma boa escolha para uma vaga Full Stack?"
];

type Props = {
  loading: boolean;
  onSelect: (prompt: string) => void;
};

export function PromptCards({ loading, onSelect }: Props){
  return(
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
