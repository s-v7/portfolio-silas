
export const CAREER_AI = {
  providers: [
    { id: "anthropic", label: "Anthropic", description: "Sem Créditos", status: "disabled" },
    { id: "nvidia", label: "NVIDIA", description: "Llama / NIM", status: "online" },
    { id: "openai", label: "OpenAI", description: "GPT Model", status: "online" }
  ],
  knowledge: [
    { label: " CV", prompt: "Resuma o CV do Silas." },
    { label: " Experience", prompt: "Explique a experiência profissional do Silas." },
    { label: " Projetos", prompt: "Quais projetos do Silas são mais relevantes?" },
    { label: " Skills", prompt: "Quais são as principais competências técnicas do Silas?" },
    { label: " Education", prompt: "Resuma a formação e certificações do Silas." }
  ],
  tools: [
    "Resume Analyzer",
    "ATS Score",
    "Interview Simulator",
    "Github Analyzer",
    "Portfolio Review",
    "Career Roadmap",
    "Salary Estimator"
  ],

  toolkit: {
    cvUrl: "https://s-v7.github.io/portfolio-silas/curriculo.pdf",
    portfolioUrl: "https://s-v7.github.io/portfolio-silas/"
  },
} as const;

