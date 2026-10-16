from __future__ import annotations

from dataclasses import dataclass

from ai.agents.base import Agent, AgentResult
from ai.agents.metadata import AgentMetadata
from ai.agents.readme_agent import _strip_markdown_fence
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
class BioAgentInput:
    language: str = "en"
    name: str = "Silas Vasconcelos Cruz"


@dataclass(frozen=True, slots=True)
class BioDraft:
    content: str
    provider: str
    model: str


class BioAgent(Agent[BioAgentInput, BioDraft]):
    name = "bio-agent"
    responsibility = "Generate an evidence-grounded short professional bio."

    def __init__(self, provider: LLMProvider) -> None:
        super().__init__(provider)
        self._provider = provider

    @property
    def metadata(self) -> AgentMetadata:
        return AgentMetadata(
            name=self.name,
            responsibility=self.responsibility,
            inputs=("BioAgentInput", "PortfolioContext"),
            outputs=("BioDraft",),
            capabilities=("generation", "bio"),
        )

    def execute(
        self,
        agent_input: BioAgentInput,
        context: PortfolioContext,
    ) -> AgentResult[BioDraft]:
        prompt_context = context.as_prompt_context()

        if not prompt_context.strip():
            raise AgentExecutionError("Bio generation requires verified evidence.")

        request = ProviderRequest(
            task=TaskType.SHORT_TEXT,
            messages=(
                Message(
                    role="system",
                    content=(
                        "You are a strict technical profile editor. "
                        "Use exclusively the verified evidence provided. "
                        "Every fact, number and project name must be "
                        "directly supported by it. Do not infer seniority, "
                        "years of experience or a current job title; "
                        "mention a role only as the evidence states it. "
                        "Avoid empty adjectives such as seasoned, "
                        "passionate, dedicated or innovative. Return plain "
                        "text only: no Markdown, no bullets, no headers."
                    ),
                ),
                Message(
                    role="user",
                    content=(
                        f"Write a short professional bio of {agent_input.name} "
                        f"in {agent_input.language}, suitable for a LinkedIn "
                        "headline and a GitHub profile.\n"
                        "Format: plain text, 2 or 3 lines, one sentence per "
                        "line.\n"
                        "Include at least one concrete number from the "
                        "evidence. State facts, not adjectives.\n\n"
                        "Verified evidence:\n"
                        f"{prompt_context}\n\n"
                        "Return only the bio."
                    ),
                ),
            ),
            options=GenerationOptions(
                temperature=0.2,
                max_tokens=200,
            ),
        )

        response = self._provider.generate(request)
        content = _strip_markdown_fence(response.content)

        if not content:
            raise AgentExecutionError("Bio provider returned empty content.")

        return AgentResult(
            agent=self.name,
            output=BioDraft(
                content=content,
                provider=response.provider,
                model=response.model,
            ),
            metadata={"evidence_count": len(context.verified_evidences)},
        )
