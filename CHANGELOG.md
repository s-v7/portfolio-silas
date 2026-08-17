# Changelog

All notable technical changes to this project are documented here.

## [Unreleased]

- Planned: Full UI redesign (Legacy → Modern)
- Planned: Design system and visual identity update
- Planned: Accessibility and performance improvements

### Added

- `PlannerAgent` in `ai/planner/`: discovers agents by capability via `AgentRegistry` and produces typed `ExecutionPlan` objects (does not execute agents itself)
- `AgentGraph.execution_levels()` and `AgentGraph.get_node()` in `ai/graph/graph.py`, grouping the topological order into waves of mutually-independent nodes
- `ParallelExecutor` in `ai/executor/`: executes `AgentGraph` instances level-by-level, running independent nodes concurrently via `ThreadPoolExecutor`; drop-in compatible with `AgentGraph.execute()`'s report format
- `WorkflowBuilder.add(..., input_factory=...)`: allows a workflow node to supply a typed `agent_input` (e.g. `ReadmeAgentInput`) instead of always passing `None`
- Minimal `Memory` contract (`ai/memory/`) with `InMemoryMemory` implementation: `get`/`set`/`has`/`delete`, no namespacing/TTL/persistence yet

### Changed

- `AgentGraph._topological_order()` now derives from `execution_levels()` instead of duplicating Kahn's algorithm, eliminating redundant cycle-detection logic

### Fixed

- `WorkflowBuilder.build()` read `graph_context.context`, an attribute that does not exist on `GraphExecutionContext` (correct field is `.portfolio`); this caused any executed workflow to fail with `AttributeError` before reaching an agent

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