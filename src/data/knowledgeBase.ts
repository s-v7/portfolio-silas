export const KNOWLEDGE_ITEMS = [
  { label: "CV", description: "Resumo profissional", prompt: "Resuma o CV do Silas." },
  {
    label: "Experiência",
    description: "CREA-PI, EDM, MEGi9",
    prompt: "Explique a experiência profissional do Silas.",
  },
  {
    label: "Projetos",
    description: "Portfólio e laboratórios",
    prompt: "Quais projetos do Silas são mais relevantes?",
  },
  {
    label: "Skills",
    description: "Stack técnica",
    prompt: "Quais são as principais competências técnicas do Silas?",
  },
  {
    label: "Formação",
    description: "Graduação e certificações",
    prompt: "Resuma a formação e certificações do Silas.",
  },
];

export type Props = {
  loading: boolean;
  onSelect: (prompt: string) => void;
};
