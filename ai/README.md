# Atlas AI

Atlas AI is an autonomous LLM-based system that maintains this portfolio by:
- Analyzing the repository context
- Selecting task-specific models
- Regenerating documentation
- Preserving full audit history

Execution:
- GitHub Actions (weekly)
- systemd timer (local fallback)

---

## Providers

Atlas AI supports two LLM providers. The active provider is selected via `LLM_PROVIDER`.

### OpenAI (default)

Uses the OpenAI Chat Completions API.

| Task          | Model        |
|---------------|--------------|
| `short_text`  | gpt-4o-mini  |
| `long_markdown`| gpt-4o-mini |
| `analysis`    | gpt-4o-mini  |

### Anthropic

Uses the Anthropic Messages API via the official SDK (`anthropic==0.86.0`).

| Task           | Model                  |
|----------------|------------------------|
| `short_text`   | claude-sonnet-4-5      |
| `long_markdown`| claude-opus-4-5        |
| `analysis`     | claude-sonnet-4-5      |

If `ANTHROPIC_API_KEY` is not set, the system automatically falls back to OpenAI.

---

## Environment Variables

| Variable            | Required | Description                                                  |
|---------------------|----------|--------------------------------------------------------------|
| `LLM_PROVIDER`      | No       | `openai` (default) or `anthropic`                            |
| `LLM_API_KEY`       | OpenAI   | OpenAI API key                                               |
| `ANTHROPIC_API_KEY` | Anthropic| Anthropic API key; absence triggers fallback to OpenAI       |
| `LLM_MAX_TOKENS`    | No       | Max tokens per response (default: `2000`)                    |
| `LLM_DEFAULT_MODEL` | No       | Fallback model override for OpenAI                           |
