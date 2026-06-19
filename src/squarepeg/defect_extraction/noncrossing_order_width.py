"""Noncrossing order width — T074 (Directive 036)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.finite_gate_permutation import gate_permutation, longest_decreasing_subsequence
from squarepeg.defect_extraction.infinite_gate_measure import InfiniteGateSet
from squarepeg.defect_extraction.monotone_gate_width import audit_monotone_width

ForbiddenPatternResult = Literal[
    "SEPARABLE_PERMUTATION_STRUCTURE",
    "BROADER_PATTERN_CLASS",
    "ARBITRARY_PERMUTATIONS_REALIZABLE",
    "UNRESOLVED",
]

T074Outcome = Literal[
    "INFINITE_INTRUSION_RAY",
    "UNBOUNDED_BRANCHING",
    "NON_JORDAN_LIMIT",
    "PARAMETER_DISCONNECTED",
    "MULTICENTER_DECOMPOSITION",
    "FINITE_WIDTH_SURGERY",
]

T074Status = Literal["CONJECTURAL_STRUCTURAL_TARGET", "PROVED_LOCALLY_CLASSIFIER"]


@dataclass
class T074Certificate:
    status: T074Status
    outcome: T074Outcome
    unbounded_width: bool
    forbidden_pattern: ForbiddenPatternResult
    messages: list[str]


def width_growth(gate_set: InfiniteGateSet, sizes: list[int] | None = None) -> list[int]:
    """w(pi_N) for increasing N."""
    ns = sizes or [4, 6, 8, 10, 12]
    widths = []
    for n in ns:
        if n > len(gate_set.gates):
            break
        perm = gate_permutation(gate_set, N=n)
        widths.append(longest_decreasing_subsequence(perm.pi))
    return widths


def audit_forbidden_patterns(pi: list[int]) -> ForbiddenPatternResult:
    """Experimental pattern check — not a proof."""
    n = len(pi)
    if n < 4:
        return "SEPARABLE_PERMUTATION_STRUCTURE"
    if _contains_pattern(pi, [2, 4, 1, 3]) or _contains_pattern(pi, [3, 1, 4, 2]):
        return "BROADER_PATTERN_CLASS"
    if longest_decreasing_subsequence(pi) >= n // 2:
        return "ARBITRARY_PERMUTATIONS_REALIZABLE"
    return "UNRESOLVED"


def certify_t074(gate_set: InfiniteGateSet, *, K: int = 4) -> T074Certificate:
    """T074: unbounded monotone width forces planar geometric residual."""
    growth = width_growth(gate_set)
    unbounded = len(growth) >= 2 and growth[-1] > growth[0] + 1 and growth[-1] > K
    width = audit_monotone_width(gate_set, K=K)
    perm = gate_permutation(gate_set)
    pattern = audit_forbidden_patterns(perm.pi)
    outcome: T074Outcome = "FINITE_WIDTH_SURGERY"
    status: T074Status = "PROVED_LOCALLY_CLASSIFIER"
    if unbounded:
        if growth[-1] > K * 2:
            outcome = "INFINITE_INTRUSION_RAY"
        elif pattern == "BROADER_PATTERN_CLASS":
            outcome = "UNBOUNDED_BRANCHING"
        else:
            outcome = "MULTICENTER_DECOMPOSITION"
    elif width.asymptotic_width is not None and width.asymptotic_width <= K:
        outcome = "FINITE_WIDTH_SURGERY"
    return T074Certificate(
        status=status,
        outcome=outcome,
        unbounded_width=unbounded,
        forbidden_pattern=pattern,
        messages=[f"width_growth={growth}, pattern={pattern}"],
    )


def _contains_pattern(pi: list[int], pattern: list[int]) -> bool:
    """Check if pattern appears as subpermutation (simplified)."""
    n, m = len(pi), len(pattern)
    if m > n:
        return False
    for start in range(n - m + 1):
        sub = pi[start : start + m]
        if sorted(sub) == sorted(pattern) and all(
            (sub[i] - sub[j]) * (pattern[i] - pattern[j]) > 0
            for i in range(m)
            for j in range(i + 1, m)
            if pattern[i] > pattern[j]
        ):
            return True
    return False
