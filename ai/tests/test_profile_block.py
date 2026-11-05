from __future__ import annotations

import pytest

from ai.core.exceptions import ConfigurationError
from ai.services.profile_block import ANCHOR, END, START, merge_block

PAGE = f"top\n{ANCHOR}\nbottom\n"


def test_inserts_the_block_after_the_anchor() -> None:
    out = merge_block(PAGE, "## Projects\n- A")

    assert out.startswith(f"top\n{ANCHOR}")
    assert out.endswith("\nbottom\n")
    assert out.index(ANCHOR) < out.index(START) < out.index("## Projects")
    assert out.index(END) < out.index("bottom")


def test_a_second_run_replace_only_the_block() -> None:
    first = merge_block(PAGE, "old text")
    second = merge_block(first, "new text")

    assert "new text" in second
    assert "old text" not in second
    assert second.count(START) == 1
    assert second.split(START)[0] == first.split(START)[0]
    assert second.split(END)[1] == first.split(END)[1]


def test_the_same_text_is_a_no_op() -> None:
    first = merge_block(PAGE, "same")
    assert merge_block(first, "same") == first


def test_rejects_an_empty_text() -> None:
    with pytest.raises(ConfigurationError, match="empty"):
        merge_block(PAGE, " \n")


def test_rejects_a_text_that_contains_the_markers() -> None:
    with pytest.raises(ConfigurationError, match="contains the block markers"):
        merge_block(PAGE, f"x {START} y")


def test_rejects_a_page_without_the_anchor() -> None:
    with pytest.raises(ConfigurationError, match="anchor"):
        merge_block("nothing here\n", "text")


def test_rejects_a_page_with_two_anchors() -> None:
    with pytest.raises(ConfigurationError, match="anchor"):
        merge_block(PAGE + ANCHOR, "text")


def test_rejects_unbalanced_markers() -> None:
    with pytest.raises(ConfigurationError, match="unbalanced"):
        merge_block(f"{START}\nonly start\n", "text")


def test_rejects_markers_out_of_order() -> None:
    with pytest.raises(ConfigurationError, match="out of order"):
        merge_block(f"{END}\n{START}\n", "text")
