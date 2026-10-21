from __future__ import annotations

from ai.scripts.evidence_dataset import (
    majority_baseline,
    record_kind,
    stratified_split,
)


def test_record_kind_follows_the_identifier() -> None:
    assert record_kind("local-x-readme") == "readme"
    assert record_kind("local-x-changelog (1)") == "changelog"
    assert record_kind("local-x-struct") == "struct"


def test_split_is_a_partition_and_is_deterministic() -> None:
    lbls = [0] * 10 + [1] * 10 + [2] * 5

    trn, tst = stratified_split(lbls)

    assert sorted(trn + tst) == list(range(25))
    assert not set(trn) & set(tst)
    assert stratified_split(lbls) == (trn, tst)


def test_every_class_with_two_examples_reaches_the_test_set() -> None:
    lbls = [0] * 10 + [1] * 2

    _, tst = stratified_split(lbls)

    assert {lbls[idx] for idx in tst} == {0, 1}


def test_a_single_example_class_stays_in_training() -> None:
    lbls = [0] * 10 + [1]

    trn, tst = stratified_split(lbls)

    assert 10 in trn
    assert 10 not in tst


def test_the_seed_changes_the_split() -> None:
    lbls = [0] * 20

    tsts = {tuple(stratified_split(lbls, seed=sed)[1]) for sed in range(5)}

    assert len(tsts) > 1


def test_majority_baseline() -> None:
    assert majority_baseline([0, 0, 1], [0, 1, 0, 0]) == 0.75
    assert majority_baseline([0], []) is None
