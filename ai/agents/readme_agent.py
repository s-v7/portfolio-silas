from __future__ import annotations

from dataclasses import dataclass

from ai.agents.base import Agent, AgentResult
from ai.context.models import PortfolioContext
from ai.core.contracts import (
    GenerationOptions,
    LLMProvider,
    Message,
    ProviderRequest,
    TaskType,
)
from ai.core.exceptions import AgentExecutionError


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


class ReadmeAgent(
    Agent[ReadmeAgentInput, ReadmeDraft]
):
    def __init__(
        self,
        provider: LLMProvider,
    ) -> None:
        self.name = "readme-agent"
        self._provider = provider

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
            task=TaskType.SHORT_TEXT,
            messages=(
                Message(
                    role="system",
                    content=(
                        "You are a technical portfolio editor. "
                        "Use only the verified evidence provided. "
                        "Never invent technologies, results, dates "
                        "or professional experience."
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
                        "Return Markdown only."
                    ),
                ),
            ),
            options=GenerationOptions(
                temperature=0.2,
                max_tokens=1800,
            ),
        )

        response = self._provider.generate(request)
        content = response.content.strip()

        if not content:
            raise AgentExecutionError(
                "README provider returned empty content."
            )

        return AgentResult(
            agent=self.name,
            output=ReadmeDraft(
                content=content,
                provider=response.provider,
                model=response.model,
            ),
            metadata={
                "evidence_count": len(
                    context.verified_evidences
                ),
            },
        )
