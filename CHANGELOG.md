# Changelog

All notable technical changes to this project are documented here.

## [Unreleased]

- Planned: Full UI redesign (Legacy → Modern)
- Planned: Design system and visual identity update
- Planned: Accessibility and performance improvements

### Added

- `Telemetry` contract in `ai/telemetry/` (`TelemetryEvent`, `Telemetry` protocol) with thread-safe `InMemoryTelemetry` and no-op `NullTelemetry` sinks
- `ParallelExecutor` accepts an optional `telemetry` sink and emits `workflow.started/completed/failed` and `node.started/completed/failed/skipped` events; a failing sink never affects execution
- `PlannerAgent` in `ai/planner/`: discovers agents by capability via `AgentRegistry` and produces typed `ExecutionPlan` objects (does not execute agents itself)
- `AgentGraph.execution_levels()` and `AgentGraph.get_node()` in `ai/graph/graph.py`, grouping the topological order into waves of mutually-independent nodes
- `ParallelExecutor` in `ai/executor/`: executes `AgentGraph` instances level-by-level, running independent nodes concurrently via `ThreadPoolExecutor`; drop-in compatible with `AgentGraph.execute()`'s report format
- `WorkflowBuilder.add(..., input_factory=...)`: allows a workflow node to supply a typed `agent_input` (e.g. `ReadmeAgentInput`) instead of always passing `None`
- Minimal `Memory` contract (`ai/memory/`) with `InMemoryMemory` implementation: `get`/`set`/`has`/`delete`, no namespacing/TTL/persistence yet
- `ReadmeGenerationGraph` and `ReadmeGenerationService` accept an optional `ParallelExecutor`; without one, execution stays sequential
- `--trace` flag in `ai/scripts/generate_readme.py` prints telemetry events and per-node durations after the run
- `WorkflowBuilder.from_plan()` creates one workflow node per `ExecutionPlan` step, so a Planner result can become an executable graph; dependencies and agent inputs are still defined by the caller
- `PlannerAgent` accepts an optional `Memory` and reuses a stored plan for a repeated request; the cache key includes the registered agents, so registry changes invalidate it (`cache_hit` is reported in the result metadata)
- `ai/scripts/plan_workflow.py` shows the agents the planner selects for an objective and capabilities, without calling any provider
- `--run` in `ai/scripts/plan_workflow.py` executes the plan through `WorkflowBuilder.from_plan` and `ParallelExecutor` and prints the generated README
- `WorkflowBuilder` nodes accept an optional `output_check` (also via `from_plan(output_checks=...)`) that can reject an agent result; the plan CLI uses it so `--run` stops at the evidence validator before calling any provider
- `AboutAgent` (`ai/agents/about_agent.py`) generates an evidence-grounded About section with the `about` capability and the cheaper `short_text` task
- Grounding and style checks for the About section (`ai/workflows/about_checks.py`): paragraph and sentence count, forbidden phrases, numbers that must exist in verified evidence, and role claims (leadership, authorship) that must be stated by the evidence
- Hand-written profile evidence in `ai/data/profile_evidence.json`, including the end of the CREA-PI role and the author's role in each project
- `--output` in `ai/scripts/plan_workflow.py` writes the generated text to `ai/output/drafts`, only for plans with a single generating agent and only when the checks pass
- `BioAgent` (`ai/agents/bio_agent.py`) generates a short plain-text professional bio with the `bio` capability; it is not part of the `portfolio` bundle, so `--capability portfolio` keeps generating only the README and the About section
- Bio checks (`ai/workflows/bio_checks.py`): 2-3 lines, no Markdown, forbidden phrases, at least one number, every number present in verified evidence, and the same ownership and authorship rules as the About section; the agent puts one sentence per line in code because the model ignored the instruction
- `--capability bio` runs the bio flow through `ai/scripts/plan_workflow.py`
- `ai/scripts/import_evidences.py` imports the extractor dataset as unverified evidence (the extractor's own status is ignored; `source` falls back to `type`) and promotes chosen identifiers to verified; output goes to `ai/output/evidence`, which git ignores
- `--evidence-file` in `ai/scripts/plan_workflow.py` can be repeated to merge sources; a duplicate evidence identifier fails before any provider call
- About checks reject other verb forms of role claims (`contributing`) and impact claims (`enhance`, `efficiency`, `improve`) unless the evidence uses them; About and bio checks now print the rejected text with the reason
- Mermaid diagrams of the framework flow and the portfolio execution graph in `ai/docs`
- `ai/scripts/measure_flows.py` runs the About and bio flows N times (capped at 20 per flow, one provider call per run) and reports how many passed and why the rest were rejected
- `ai/scripts/import_github.py` imports an owner's public GitHub repositories (through the `gh` CLI) as unverified evidence; forks and repositories with neither description nor topics are skipped, and promotion reuses `import_evidences promote`
- `ai/scripts/import_git.py` computes verified evidence from local git history (the author's commits, matched by e-mail): one evidence per repository, or with `--aggregate` a single evidence with totals and main languages that names no repository; commits are identified by hash so a clone counts once, and generated folders are ignored when counting languages
- Evidence can mark facts the About text must state (`must_mention` in its metadata): the prompt lists them and the About check rejects a text that omits one; the aggregate git activity uses it for its commit total
- The About check accepts up to seven sentences (the prompt asks for six, so a seventh still passes) and the prompt asks for numbers written exactly as in the evidence
- `WorkflowBuilder` nodes accept `retry_input` and `retries`: when an output check rejects a result, the agent runs again with the check's reason as feedback; the plan CLI retries the About and bio flows up to twice and sends only the reason, because echoing the rejected text made the model copy it

### Changed

- `AgentGraph._topological_order()` now derives from `execution_levels()` instead of duplicating Kahn's algorithm, eliminating redundant cycle-detection logic
- `ai/scripts/plan_workflow.py` derives execution order and output checks from agent capabilities (`verification` before `generation`; `verification` and `about` map to checks) instead of hardcoded agent names, so the README and About flows share one path

### Fixed

- `WorkflowBuilder.build()` read `graph_context.context`, an attribute that does not exist on `GraphExecutionContext` (correct field is `.portfolio`); this caused any executed workflow to fail with `AttributeError` before reaching an agent
- `ai/scripts/generate_readme.py` now reports `ProviderError` as a clean message with exit code 1 instead of a raw traceback
- `--provider` in `ai/scripts/generate_readme.py` now accepts `proxy` (the factory's real default) and the help text no longer claims `openai` is the default
- Evidence labeling (`ai/scripts/evidence_labeling.py`, previously inline in `train_neural_net.py`) matches `java`, `node`, `db`, `vue`, `.c` and `.sh` as whole tokens, so `javascript`, `.css` and `feedback` no longer land in the wrong category

---

## [0.3.0] – 2026-04-21

### Added

- Anthropic provider support in `ai/scripts/llm_client.py` via `anthropic==0.86.0` SDK
- Automatic fallback to OpenAI when `ANTHROPIC_API_KEY` is absent
- `ai/scripts/test_anthropic.py` smoke test (provider, model, elapsed time, output)
- `get_model(task, provider)` routing function in `ai/core/model_router.py`
- Provider/model logging in `LLMClient.generate()` and `update_bio` agent
- Providers section and environment variable table in `ai/README.md`

### Changed

- `ai/core/model_router.py` refactored to dual-provider `MODEL_BY_TASK` structure
- `LLM_PROVIDER=anthropic` selects `claude-sonnet-4-5` (short/analysis) and `claude-opus-4-5` (long markdown)

---

## [0.2.0] – 2025-01

### Changed

- Full migration from JavaScript (JS/JSX) to TypeScript (TS/TSX)
- Upgrade to React 19 and React Router v7
- Project structure refactored and standardized
- Components and pages rewritten using modern React patterns

### Added

- TypeScript configuration (`tsconfig.json`)
- Improved ESLint configuration
- Docker + Nginx production-ready setup

### Removed

- Legacy JS/JSX files
- Deprecated CSS and unused components

---

## [0.1.0] – Initial

- Initial portfolio implementation
- React + Vite setup
- Basic routing and pages
