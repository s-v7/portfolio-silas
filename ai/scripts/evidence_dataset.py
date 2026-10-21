from __future__ import annotations

import random
from collections import Counter
from collections.abc import Sequence

TRAINABLE_KINDS = ("readme", "changelog")


def record_kind(idf: str) -> str:
    """Classify an extractor identifier: readme, changelog or folder summary."""
    if idf.endswith("-struct"):
        return "struct"

    if "-changelog" in idf:
        return "changelog"

    return "readme"


def stratified_split(
    lbls: Sequence[int],
    test_ratio: float = 0.2,
    seed: int = 42,
) -> tuple[list[int], list[int]]:
    """Split indexes keeping every class in both sets when it has 2+ examples."""
    rng = random.Random(seed)
    groups: dict[int, list[int]] = {}

    for idx, lbl in enumerate(lbls):
        groups.setdefault(lbl, []).append(idx)

    trn: list[int] = []
    tst: list[int] = []

    for lbl in sorted(groups):
        idxs = list(groups[lbl])
        rng.shuffle(idxs)
        num = max(1, round(len(idxs) * test_ratio)) if len(idxs) >= 2 else 0
        tst.extend(idxs[:num])
        trn.extend(idxs[num:])

    return sorted(trn), sorted(tst)


def majority_baseline(y_trn: Sequence[int], y_tst: Sequence[int]) -> float | None:
    """Accuracy of always predicting the most common training class."""
    if not y_tst or not y_trn:
        return None

    top = Counter(y_trn).most_common(1)[0][0]

    return sum(1 for val in y_tst if val == top) / len(y_tst)
