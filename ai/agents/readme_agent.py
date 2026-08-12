from __future__ import annotations

from dataclasses import dataclass

from ai.agents.base import Agent, AgentResult
from ai.agents.metadata import AgentMetadata
from ai.context.models import PortfolioContext
from ai.core.contracts import (
    GenerationOptions,
    LLMProvider,
    Message,
    ProviderRequest,
    TaskType,
)
from ai.core.exceptions import AgentExecutionError


def _strip_markdown_fence(content: str) -> str:
    normalized = content.strip()

    if not normalized.startswith("```"):
        return normalized

    lines = normalized.splitlines()
    if lines and lines[0].strip().lower() in {
        "```",
        "```markdown",
        "```md",
    }:
        lines = lines[1:]

    if lines and lines[-1].strip() == "```":
        lines = lines[:-1]

    return "\n".join(lines).strip()


@dataclass(frozen=True, slots=True)
class ReadmeAgentInput:
    language: str = "pt-BR"
    audience: str = "technical recruiters"
    title: str = "Silas Vasconcelos Cruz"


@dataclass(frozen=True, slots=True)
class ReadmeDraft:
    content: str
    provider: str
    model: str


class ReadmeAgent(Agent[ReadmeAgentInput, ReadmeDraft]):
    def __init__(self,provider: LLMProvider) -> None:
        self.name = "readme-agent"
        self._provider = provider

    @property
    def metadata(self) -> AgentMetadata:
        return AgentMetadata(
            name="readme-agent",
            responsibility="Generate evidence-grounded README content.",
            inputs=("ReadmeAgentInput", "PortfolioContext"),
            outputs=("ReadmeDraft",),
            capabilities=(
                "markdown",
                "generation",
                "portfolio",
                "github",
            ),
        )

    def execute(
        self,
        agent_input: ReadmeAgentInput,
        context: PortfolioContext,
    ) -> AgentResult[ReadmeDraft]:
        prompt_context = context.as_prompt_context()

        if not prompt_context.strip():
            raise AgentExecutionError(
                "README generation requires verified evidence."
            )

        request = ProviderRequest(
            task=TaskType.LONG_MARKDOWN,
            messages=(
                Message(
                    role="system",
                    content=(
                        "You are a strict technical portfolio editor. "
                        "Use exclusively the verified evidence provided. "
                        "Every factual claim must be directly supported "
                        "by the evidence. Do not infer personality, "
                        "motivation, seniority, job title, years of "
                        "experience, results, metrics, contact details, "
                        "links or technologies. Do not create "
                        "placeholders. Omit sections for which there is "
                        "no evidence. Return raw Markdown without "
                        "Markdown code fences."
                    ),
                ),
                Message(
                    role="user",
                    content=(
                        "Create a GitHub profile README in "
                        f"{agent_input.language}.\n"
                        f"Title: {agent_input.title}\n"
                        f"Audience: {agent_input.audience}\n\n"
                        "Verified evidence:\n"
                        f"{prompt_context}\n\n"
                        "Do not add contact information, biography claims, "
                        "generic enthusiasm statements or "
                        "placeholder links.\n"
                        "Do not wrap the response in triple "
                        "backticks.\n"
                        "Return only the final README Markdown."
                    ),
                ),
            ),
            options=GenerationOptions(
                temperature=0.2,
                max_tokens=1800,
            ),
        )

        response = self._provider.generate(request)
        content = _strip_markdown_fence(response.content)
        if not content:
            raise AgentExecutionError("README provider returned empty content.")

        return AgentResult(
            agent=self.name,
            output=ReadmeDraft(
                content=content,
                provider=response.provider,
                model=response.model,
            ),
            metadata={"evidence_count": len(context.verified_evidences)},
        )
