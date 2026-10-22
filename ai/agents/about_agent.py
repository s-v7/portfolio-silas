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
class AboutAgentInput:
    language: str = "en"
    name: str = "Silas Vasconcelos Cruz"


@dataclass(frozen=True, slots=True)
class AboutDraft:
    content: str
    provider: str
    model: str


class AboutAgent(Agent[AboutAgentInput, AboutDraft]):
    name = "about-agent"
    responsibility = "Generate an evidence-grounded About section."

    def __init__(self, provider: LLMProvider) -> None:
        super().__init__(provider)
        self._provider = provider

    @property
    def metadata(self) -> AgentMetadata:
        return AgentMetadata(
            name=self.name,
            responsibility=self.responsibility,
            inputs=("AboutAgentInput", "PortfolioContext"),
            outputs=("AboutDraft",),
            capabilities=(
                "markdown",
                "generation",
                "portfolio",
                "about",
            ),
        )

    def execute(
        self,
        agent_input: AboutAgentInput,
        context: PortfolioContext,
    ) -> AgentResult[AboutDraft]:
        prompt_context = context.as_prompt_context()

        if not prompt_context.strip():
            raise AgentExecutionError("About generation requires verified evidence.")

        request = ProviderRequest(
            task=TaskType.SHORT_TEXT,
            messages=(
                Message(
                    role="system",
                    content=(
                        "You are a strict technical profile editor. "
                        "Use exclusively the verified evidence provided. "
                        "Every factual claim, number, technology and project "
                        "name must be directly supported by the evidence. "
                        "Do not infer seniority, motivation, years of "
                        "experience or a current job title; mention an "
                        "employer or role only as the evidence states it, "
                        "with its dates when given. Do not invent links or "
                        "contact details. Avoid empty adjectives such as "
                        "seasoned, passionate, dedicated, innovative or "
                        "results-driven. Return raw Markdown prose without "
                        "code fences."
                    ),
                ),
                Message(
                    role="user",
                    content=(
                        f"Write an About section about {agent_input.name} "
                        f"in {agent_input.language}.\n"
                        "Format: exactly 2 paragraphs of prose, 4 sentences in the "
                        "first and 3 in the second (7 in total), no lists, no headers. "
                        "Merge related facts into one sentence instead of "
                        "adding sentences. Write numbers exactly as "
                        "they appear in the evidence.\n"
                        "Tone: direct technical prose that states what was "
                        "built and what it does.\n"
                        "Prefer concrete numbers and project names found in "
                        "the evidence.\n\n"
                        "Verified evidence:\n"
                        f"{prompt_context}\n\n"
                        "Rules: do not claim leadership or ownership (led, "
                        "architected, managed) unless the evidence uses those "
                        "words. Name technologies exactly as the evidence does; "
                        "do not group them into categories. If the evidence "
                        "mentions a role or employer, mention it, including that "
                        "it ended when the evidence says so.\n"
                        "Return only the two paragraphs."
                    ),
                ),
            ),
            options=GenerationOptions(
                temperature=0.2,
                max_tokens=600,
            ),
        )

        response = self._provider.generate(request)
        content = _strip_markdown_fence(response.content)

        if not content:
            raise AgentExecutionError("About provider returned empty content.")

        return AgentResult(
            agent=self.name,
            output=AboutDraft(
                content=content,
                provider=response.provider,
                model=response.model,
            ),
            metadata={"evidence_count": len(context.verified_evidences)},
        )
