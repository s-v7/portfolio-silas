from __future__ import annotations

import argparse

import pytest

from ai.scripts import generate_readme


def parse(*extra: str) -> argparse.Namespace:
    return generate_readme.build_parser().parse_args(
        ["--evidence-file", "evidence.json", *extra]
    )


@pytest.mark.parametrize(
    "provider",
    ("proxy", "openai", "anthropic", "nvidia"),
)
def test_accepts_every_supported_provider(provider: str) -> None:
    args = parse("--provider", provider)

    assert args.provider == provider


def test_provider_defaults_to_none_so_factory_decides() -> None:
    assert parse().provider is None


def test_rejects_unknown_provider() -> None:
    with pytest.raises(SystemExit):
        parse("--provider", "does-not-exist")


def test_help_describes_the_real_default() -> None:
    help_text = generate_readme.build_parser().format_help()

    assert "or proxy" in help_text
    assert "or openai" not in help_text
