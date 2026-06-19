"""Forbidden pattern audit for P_Jordan (Directive 038)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.finite_gate_permutation import gate_permutation, longest_decreasing_subsequence
from squarepeg.defect_extraction.infinite_gate_measure import InfiniteGateSet

ForbiddenPatternVerdict = Literal[
    "SEPARABLE_PERMUTATIONS_ONLY",
    "FINITE_BASIS_BROADER_CLASS",
    "INFINITE_BASIS_CLASS",
    "ARBITRARY_PERMUTATIONS_REALIZABLE",
    "UNRESOLVED",
]


@dataclass
class ForbiddenPatternAudit:
    verdict: ForbiddenPatternVerdict
    contains_2413: bool
    contains_3142: bool
    lds_length: int
    width: int
    messages: list[str]


def _pattern_subpermutation(pi: list[int], pattern: list[int]) -> bool:
    m = len(pattern)
    n = len(pi)
    if m > n:
        return False
    p_sorted = sorted(pattern)
    for start in range(n - m + 1):
        sub = pi[start : start + m]
        if sorted(sub) != p_sorted:
            continue
        rel = [sub.index(x) for x in sorted(sub, key=lambda v: pattern.index(v) if v in pattern else 0)]
        if rel == list(range(m)):
            return True
    return False


def audit_forbidden_patterns(gate_set: InfiniteGateSet) -> ForbiddenPatternAudit:
    """Reconnaissance audit for 2413 and 3142 — not a proof."""
    perm = gate_permutation(gate_set)
    pi = perm.pi
    has_2413 = _contains_pattern_simple(pi, [2, 4, 1, 3])
    has_3142 = _contains_pattern_simple(pi, [3, 1, 4, 2])
    lds = longest_decreasing_subsequence(pi)
    width = lds
    verdict: ForbiddenPatternVerdict = "UNRESOLVED"
    if lds <= 2 and not has_2413 and not has_3142:
        verdict = "SEPARABLE_PERMUTATIONS_ONLY"
    elif has_2413 or has_3142:
        verdict = "FINITE_BASIS_BROADER_CLASS"
    elif lds >= len(pi) // 2:
        verdict = "ARBITRARY_PERMUTATIONS_REALIZABLE"
    elif lds > 4:
        verdict = "INFINITE_BASIS_CLASS"
    return ForbiddenPatternAudit(
        verdict=verdict,
        contains_2413=has_2413,
        contains_3142=has_3142,
        lds_length=lds,
        width=width,
        messages=[f"verdict={verdict}, LDS={lds}"],
    )


def _contains_pattern_simple(pi: list[int], pattern: list[int]) -> bool:
    m = len(pattern)
    for i in range(len(pi) - m + 1):
        sub = pi[i : i + m]
        if sorted(sub) == sorted(pattern):
            order_sub = sorted(range(m), key=lambda k: sub[k])
            order_pat = sorted(range(m), key=lambda k: pattern[k])
            if order_sub == order_pat:
                return True
    return False
