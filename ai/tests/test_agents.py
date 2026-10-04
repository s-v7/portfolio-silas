from unittest.mock import MagicMock
import pytest

from ai.agents.evidence_validator import EvidenceValidatorAgent
from ai.agents.readme_agent import ReadmeAgent, ReadmeAgentInput
from ai.context.models import Evidence, PortfolioContext
from ai.core.contracts import EvidenceStatus, LLMProvider, ProviderResponse


@pytest.fixture
def sample_context() -> PortfolioContext:
    verified_ev = Evidence(
        identifier="exp_1",
        content="Desenvolvimento de APIs em Python e Go.",
        status=EvidenceStatus.VERIFIED,
        source="linkedin",
    )
    unverified_ev = Evidence(
        identifier="exp_2",
        content="Conteúdo não validado",
        status=EvidenceStatus.UNVERIFIED,
        source="draft",
    )
    return PortfolioContext(evidences=(verified_ev, unverified_ev))


def test_evidence_validator_agent(sample_context: PortfolioContext) -> None:
    agent = EvidenceValidatorAgent[None]()
    result = agent.execute(agent_input=None, context=sample_context)

    assert result.agent == "evidence-validator"
    assert result.output.valid is True
    assert len(result.output.verified) == 1
    assert result.output.verified[0].identifier == "exp_1"
    assert len(result.output.rejected) == 1
    assert any("exp_2" in warning for warning in result.output.warnings)


def test_readme_agent_execution(sample_context: PortfolioContext) -> None:
    mock_provider = MagicMock(spec=LLMProvider)
    mock_provider.generate.return_value = ProviderResponse(
        content="# Silas Vasconcelos\nDesenvolvedor de Software",
        provider="openai",
        model="gpt-4o-mini",
    )

    agent = ReadmeAgent(provider=mock_provider)
    input_data = ReadmeAgentInput(language="pt-BR")

    result = agent.execute(agent_input=input_data, context=sample_context)

    assert result.agent == "readme-agent"
    assert result.output.content.startswith("# Silas Vasconcelos")
    assert result.output.provider == "openai"
    assert result.output.model == "gpt-4o-mini"
    mock_provider.generate.assert_called_once()
