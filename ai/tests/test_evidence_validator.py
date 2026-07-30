from ai.agents.evidence_validator import EvidenceValidatorAgent
from ai.context.models import Evidence, PortfolioContext
from ai.core.contracts import EvidenceStatus


def test_accepts_only_verified_evidence() -> None:
    context = PortfolioContext(
        evidences=(
            Evidence(
                identifier="git-001",
                source="git",
                content="Implemented FastAPI health endpoint.",
                status=EvidenceStatus.VERIFIED,
            ),
            Evidence(
                identifier="plan-001",
                source="roadmap",
                content="Planned Kubernetes deployment.",
                status=EvidenceStatus.UNVERIFIED,
            ),
        )
    )

    result = EvidenceValidatorAgent[None]().execute(None, context)

    assert result.output.valid is True
    assert len(result.output.verified) == 1
    assert len(result.output.rejected) == 1
    assert result.output.verified[0].identifier == "git-001"


def test_rejects_empty_verified_evidence() -> None:
    context = PortfolioContext(
        evidences=(
            Evidence(
                identifier="empty",
                source="test",
                content=" ",
                status=EvidenceStatus.VERIFIED,
            ),
        )
    )

    result = EvidenceValidatorAgent[None]().execute(None, context)

    assert result.output.valid is False
    assert not result.output.verified


def test_rejects_conflicting_evidence() -> None:
    context = PortfolioContext(
        evidences=(
            Evidence(
                identifier="conflict-001",
                source="git",
                content="Conflicting claim.",
                status=EvidenceStatus.CONFLICTING,
            ),
        )
    )

    result = EvidenceValidatorAgent[None]().execute(None, context)

    assert result.output.valid is False
    assert not result.output.verified
    assert len(result.output.rejected) == 1
    assert result.output.warnings


def test_builds_prompt_context_only_from_verified_evidence() -> None:
    context = PortfolioContext(
        evidences=(
            Evidence(
                identifier="verified-001",
                source="git",
                content="FastAPI endpoint implemented.",
                status=EvidenceStatus.VERIFIED,
            ),
            Evidence(
                identifier="planned-001",
                source="roadmap",
                content="Kubernetes deployment planned.",
                status=EvidenceStatus.UNVERIFIED,
            ),
        )
    )

    prompt_context = context.as_prompt_context()

    assert "FastAPI endpoint implemented." in prompt_context
    assert "Kubernetes deployment planned." not in prompt_context
    assert "[Evidence: verified-001]" in prompt_context
