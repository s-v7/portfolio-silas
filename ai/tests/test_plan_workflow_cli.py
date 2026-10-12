from __future__ import annotations

from pytest import CaptureFixture

from ai.scripts import plan_workflow


def test_selects_agents_by_capability(
    capsys: CaptureFixture[str],
) -> None:
    exit_code = plan_workflow.main(
        ["--objective", "Generate README", "--capability", "markdown"]
    )

    output = capsys.readouterr().out

    assert exit_code == 0
    assert "Objective: Generate README" in output
    assert "readme-agent" in output
    assert "evidence-validator" not in output


def test_requires_every_capability_flag(
    capsys: CaptureFixture[str],
) -> None:
    exit_code = plan_workflow.main(
        [
            "--objective",
            "Validate evidence",
            "--capability",
            "evidence-validation",
            "--capability",
            "verification",
        ]
    )

    output = capsys.readouterr().out

    assert exit_code == 0
    assert "evidence-validator" in output
    assert "readme-agent" not in output


def test_without_capabilities_lists_every_agent(
    capsys: CaptureFixture[str],
) -> None:
    exit_code = plan_workflow.main(["--objective", "Inspect"])

    output = capsys.readouterr().out

    assert exit_code == 0
    assert "readme-agent" in output
    assert "evidence-validator" in output


def test_fails_when_no_agent_matches(
    capsys: CaptureFixture[str],
) -> None:
    exit_code = plan_workflow.main(
        ["--objective", "Anything", "--capability", "does-not-exist"]
    )

    assert exit_code == 1
    assert "No registered agent" in capsys.readouterr().err


def test_fails_for_empty_objective(
    capsys: CaptureFixture[str],
) -> None:
    exit_code = plan_workflow.main(["--objective", " "])

    assert exit_code == 1
    assert "cannot be empty" in capsys.readouterr().err
