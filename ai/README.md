# SV7 AI

SV7 AI is the Python agent framework behind this portfolio. An objective goes through a planner, a workflow and a parallel executor, and each text it generates (profile README, About section, bio) is checked in code against verified evidence before it is accepted.

- Evidence comes from a hand-written profile, the extractor, GitHub and local git history; imported evidence stays unverified until it is promoted
- Output checks reject invented numbers, links, roles and impact claims, and a rejected text is retried with the reason
- Telemetry events and durations are printed by `generate_readme.py --trace`

Execution:

- On demand from the command line (`ai/scripts/plan_workflow.py`, `ai/scripts/generate_readme.py`)

---

## Providers

SV7 AI can use several LLM providers; the active one is selected with `LLM_PROVIDER` or `--provider`. The tables below cover OpenAI and Anthropic.

### OpenAI

Uses the OpenAI Chat Completions API.

| Task            | Model       |
| --------------- | ----------- |
| `short_text`    | gpt-4o-mini |
| `long_markdown` | gpt-4o-mini |
| `analysis`      | gpt-4o-mini |

### Anthropic

Uses the Anthropic Messages API via the official SDK (`anthropic==0.86.0`).

| Task            | Model             |
| --------------- | ----------------- |
| `short_text`    | claude-sonnet-4-5 |
| `long_markdown` | claude-opus-4-5   |
| `analysis`      | claude-sonnet-4-5 |

If `ANTHROPIC_API_KEY` is not set, the system automatically falls back to OpenAI.

---

## Environment Variables

| Variable | Used by | Description |
| --- | --- | --- |
| `LLM_PROVIDER` | all | `proxy`, `openai`, `anthropic` or `nvidia` (the CLIs also take `--provider`). Default: `proxy` in the framework, `openai` in the legacy `llm_client.py` |
| `OPENAI_API_KEY` or `LLM_API_KEY` | `openai` | OpenAI API key |
| `ANTHROPIC_API_KEY` | `anthropic` | Anthropic API key; the legacy client falls back to OpenAI when it is absent |
| `NVIDIA_API_KEY` | `nvidia` | NVIDIA API key |
| `PORTFOLIO_PROXY_URL` | `proxy` | Proxy base URL (default `http://localhost:8080/v1`) |
| `PORTFOLIO_PROXY_API_KEY` or `LLM_API_KEY` | `proxy` | Proxy API key |
| `LLM_MAX_TOKENS` | legacy client | Max tokens per response (default `2000`) |
| `OPENAI_BASE_URL` | legacy client | OpenAI-compatible base URL (default `https://api.openai.com/v1`) |
