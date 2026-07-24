export const KNOWLEDGE_ITEMS = [
  {
    label: "CV",
    description: "Resumo profissional",
    prompt:
      "Apresente um resumo executivo do CV do Silas, destacando perfil, trajetória, competências, formação e principais diferenciais.",
  },
  {
    label: "Experiência",
    description: "CREA-PI, EDM, MEGi9",
    prompt:
      "Explique somente a experiência profissional do Silas. Organize por empresa e período, destacando responsabilidades, tecnologias utilizadas e impacto. Não liste projetos independentes nem apresente uma lista geral de competências.",
  },
  {
    label: "Projetos",
    description: "Portfólio e laboratórios",
    prompt:
      "Liste somente os projetos mais relevantes do Silas. Para cada projeto, apresente problema, solução, stack, status e evidência disponível. Não repita todo o histórico profissional.",
  },
  {
    label: "Skills",
    description: "Stack técnica",
    prompt:
      "Apresente somente as principais competências técnicas do Silas, organizadas por categorias e relacionadas a evidências reais da experiência e dos projetos.",
  },
  {
    label: "Formação",
    description: "Graduação e certificações",
    prompt:
      "Resuma somente a formação acadêmica e as certificações do Silas, sem listar projetos ou repetir toda a experiência profissional.",
  },
];

export type Props = {
  loading: boolean;
  onSelect: (prompt: string) => void;
};
