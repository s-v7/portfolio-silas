import { useEffect, useMemo, useState } from "react";

import type { AnalyticsResponse } from "../features/career-ai/analytics.types";
import { fetchLearningAnalytics } from "../features/career-ai/services/analyticsApi";

import "../styles/pages/LearningDashboard.css";

const TOKEN_KEY = "ai-career-admin-token";

function formatDate(value: string | null) {
  if (!value) return "Nenhuma interação";

  return new Intl.DateTimeFormat("pt-BR", {
    dateStyle: "short",
    timeStyle: "short",
  }).format(new Date(value));
}

export default function LearningDashboard() {
  const [token, setToken] = useState(
    () => sessionStorage.getItem(TOKEN_KEY) || ""
  );
  const [tokenInput, setTokenInput] = useState(token);
  const [analytics, setAnalytics] = useState<AnalyticsResponse | null>(null);
  const [loading, setLoading] = useState(Boolean(token));
  const [error, setError] = useState("");

  async function loadAnalytics(currentToken = token) {
    if (!currentToken) return;

    setLoading(true);
    setError("");

    try {
      const data = await fetchLearningAnalytics(currentToken);
      setAnalytics(data);
    } catch (caughtError) {
      setAnalytics(null);
      setError(
        caughtError instanceof Error
          ? caughtError.message
          : "Erro ao carregar analytics."
      );
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    if (token) void loadAnalytics(token);
  }, [token]);

  const maxIntent = useMemo(
    () => Math.max(1, ...(analytics?.intents.map((item) => item.total) || [1])),
    [analytics]
  );

  const maxTimeline = useMemo(
    () => Math.max(1, ...(analytics?.timeline.map((item) => item.total) || [1])),
    [analytics]
  );

  function authenticate(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const normalizedToken = tokenInput.trim();

    if (!normalizedToken) return;

    sessionStorage.setItem(TOKEN_KEY, normalizedToken);
    setToken(normalizedToken);
  }

  function logout() {
    sessionStorage.removeItem(TOKEN_KEY);
    setToken("");
    setTokenInput("");
    setAnalytics(null);
    setError("");
  }

  if (!token) {
    return (
      <main className="learning-login">
        <form className="learning-login__card" onSubmit={authenticate}>
          <p>Área administrativa</p>
          <h1>AI Learning Dashboard</h1>
          <span>Informe o token administrativo do AI Gateway.</span>

          <input
            type="password"
            value={tokenInput}
            onChange={(event) => setTokenInput(event.target.value)}
            placeholder="ADMIN_API_TOKEN"
            autoComplete="off"
          />

          <button type="submit">Entrar</button>
        </form>
      </main>
    );
  }

  return (
    <main className="learning-dashboard">
      <header className="learning-dashboard__header">
        <div>
          <p>Privado · AI Career</p>
          <h1>AI Learning Dashboard</h1>
          <span>
            Telemetria, feedback e padrões de uso do Career Assistant.
          </span>
        </div>

        <div className="learning-dashboard__actions">
          <button type="button" onClick={() => void loadAnalytics()}>
            Atualizar
          </button>
          <button type="button" onClick={logout}>
            Sair
          </button>
        </div>
      </header>

      {loading && <p className="learning-state">Carregando analytics...</p>}

      {error && (
        <div className="learning-error">
          <strong>Não foi possível carregar os dados.</strong>
          <span>{error}</span>
        </div>
      )}

      {analytics && (
        <>
          <section className="learning-summary">
            <article>
              <span>Total de perguntas</span>
              <strong>{analytics.summary.totalInteractions}</strong>
            </article>

            <article>
              <span>Feedback positivo</span>
              <strong>{analytics.summary.positiveRate}%</strong>
            </article>

            <article>
              <span>Intenções detectadas</span>
              <strong>{analytics.summary.totalIntents}</strong>
            </article>

            <article>
              <span>Total de feedbacks</span>
              <strong>{analytics.summary.totalFeedback}</strong>
            </article>
          </section>

          <section className="learning-grid">
            <article className="learning-panel">
              <div className="learning-panel__header">
                <h2>Intenções</h2>
                <span>Temas mais consultados</span>
              </div>

              <div className="learning-bars">
                {analytics.intents.map((item) => (
                  <div key={item.intent} className="learning-bar">
                    <div>
                      <span>{item.intent}</span>
                      <strong>{item.total}</strong>
                    </div>
                    <progress value={item.total} max={maxIntent} />
                  </div>
                ))}
              </div>
            </article>

            <article className="learning-panel">
              <div className="learning-panel__header">
                <h2>Providers</h2>
                <span>Distribuição das respostas</span>
              </div>

              <div className="learning-provider-list">
                {analytics.providers.map((item) => (
                  <div key={item.provider}>
                    <span>{item.provider}</span>
                    <strong>{item.total}</strong>
                  </div>
                ))}
              </div>
            </article>

            <article className="learning-panel learning-panel--wide">
              <div className="learning-panel__header">
                <h2>Perguntas por dia</h2>
                <span>Últimos 14 dias</span>
              </div>

              <div className="learning-timeline">
                {analytics.timeline.map((item) => (
                  <div key={item.day}>
                    <span>{item.day.slice(5)}</span>
                    <i
                      style={{
                        height: `${Math.max(
                          8,
                          (item.total / maxTimeline) * 100
                        )}%`,
                      }}
                    />
                    <strong>{item.total}</strong>
                  </div>
                ))}
              </div>
            </article>

            <article className="learning-panel learning-panel--wide">
              <div className="learning-panel__header">
                <h2>Knowledge Gaps</h2>
                <span>Respostas avaliadas negativamente</span>
              </div>

              {analytics.knowledgeGaps.length === 0 ? (
                <p className="learning-empty">
                  Nenhum knowledge gap registrado.
                </p>
              ) : (
                <div className="learning-gap-list">
                  {analytics.knowledgeGaps.map((gap) => (
                    <div key={gap.id}>
                      <span>{gap.intent}</span>
                      <p>{gap.question}</p>
                      <small>{formatDate(gap.created_at)}</small>
                    </div>
                  ))}
                </div>
              )}
            </article>
          </section>

          <footer className="learning-dashboard__footer">
            Última interação:{" "}
            <strong>{formatDate(analytics.summary.lastInteraction)}</strong>
          </footer>
        </>
      )}
    </main>
  );
}
