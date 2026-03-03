import Section from "../components/Section";

const ArtEngine: React.FC = () => {
  return (
    <>
      {/* Diagram grid */}
      <div className="art-grid">
        <img src="/docs/art_execution_dag.png" alt="ART Execution DAG" />
        <img src="/docs/art_pipeline.png" alt="ART Pipeline" />
        <img src="/docs/llm_governance.png" alt="LLM Governance" />
      </div>

      <Section
        title="ART Intelligence Engine — LLM + Audit Graph AI"
        subtitle="AI audit platform for Engineering Responsibility Records (ART)"
      >
        <p>
          Institutional AI engine designed for CREA environments. Combines
          deterministic audit rules, DB × PDF cross-check, semantic
          normalization and LLM enrichment with strict governance guardrails.
        </p>
      </Section>

      <Section title="Core Capabilities">
        <ul>
          <li>✔ Deterministic audit rules (reproducible)</li>
          <li>✔ DB × PDF divergence detection</li>
          <li>✔ Sensitive data masking before LLM</li>
          <li>✔ Execution pipeline as DAG (audit graph)</li>
          <li>✔ LLM semantic enrichment with guardrails</li>
          <li>✔ Human-in-the-loop learning</li>
          <li>✔ Multi-CREA scalable model</li>
        </ul>
      </Section>

      <Section title="Execution Architecture (Graph AI)">
        <p>
          The engine runs as a directed acyclic graph (DAG), where each node is
          a deterministic or AI-assisted processing stage:
        </p>

        <ul>
          <li>DB extraction</li>
          <li>PDF parsing</li>
          <li>Cross-check validation</li>
          <li>Rule scoring</li>
          <li>Guard filters</li>
          <li>LLM semantic enrichment</li>
          <li>Traceable storage</li>
        </ul>

        <p>This guarantees traceability, replayability and audit safety.</p>
      </Section>

      <Section title="LLM Governance Model">
        <ul>
          <li>Masked inputs only</li>
          <li>No legal conclusions generated</li>
          <li>Structured JSON outputs</li>
          <li>Confidence tagging</li>
          <li>Human review flags</li>
          <li>Prompt versioning</li>
        </ul>
      </Section>

      <Section title="Continuous Learning">
        <p>
          The platform supports supervised feedback from technical auditors,
          allowing controlled improvement of semantic classification and risk
          signals without breaking reproducibility.
        </p>

        <ul>
          <li>Markov transition weighting</li>
          <li>Graph versioning</li>
          <li>Rule feedback loop</li>
          <li>Reviewer-confirmed corrections</li>
        </ul>
      </Section>

      <Section title="Deployment Model">
        <ul>
          <li>On-premise compatible</li>
          <li>Government cloud ready</li>
          <li>API + CLI + Dashboard modes</li>
          <li>Designed for CREA federation scale</li>
        </ul>
      </Section>
    </>
  );
};

export default ArtEngine;
