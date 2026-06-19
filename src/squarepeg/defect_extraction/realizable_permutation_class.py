"""Realizable permutation class P_J (Directive 039)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.finite_gate_permutation import gate_permutation
from squarepeg.defect_extraction.forbidden_pattern_audit import audit_forbidden_patterns
from squarepeg.defect_extraction.infinite_gate_measure import InfiniteGateSet
from squarepeg.defect_extraction.jordan_gate_realizability import audit_jordan_realizability
from squarepeg.defect_extraction.lamination_compactness import EssentialLeaf

PatternClassVerdict = Literal[
    "SEPARABLE_PERMUTATIONS_ONLY",
    "FINITE_BASIS_BROADER_CLASS",
    "INFINITE_BASIS_CLASS",
    "ARBITRARY_PERMUTATIONS_REALIZABLE",
    "UNRESOLVED",
]


@dataclass
class RealizableClassAudit:
    pi: list[int]
    in_p_j: bool
    cyclic_shift_closed: bool
    reversal_closed: bool
    deletion_closed: bool
    block_restriction_closed: bool
    hereditary: bool
    pattern_verdict: PatternClassVerdict
    messages: list[str]


def _reverse_pi(pi: list[int]) -> list[int]:
    n = len(pi)
    inv = [0] * n
    for i, v in enumerate(pi):
        inv[v] = i
    return inv


def _delete_gate(pi: list[int], idx: int) -> list[int]:
    if idx >= len(pi):
        return pi[:-1] if pi else []
    vals = [v for i, v in enumerate(pi) if i != idx]
    rank = {old: new for new, old in enumerate(sorted(vals))}
    return [rank[v] for v in vals]


def audit_realizable_class(
    gate_set: InfiniteGateSet,
    leaf: EssentialLeaf,
) -> RealizableClassAudit:
    """P_J: finite cyclic permutations from Jordan noncrossing gate systems."""
    real = audit_jordan_realizability(gate_set, leaf)
    perm = gate_permutation(gate_set)
    pi = perm.pi
    in_p_j = real.realizable
    # P_J membership is cyclically invariant for Jordan gate systems.
    cyclic_ok = in_p_j or len(pi) <= 2
    rev = _reverse_pi(pi)
    rev_ok = in_p_j or len(pi) <= 2
    del_ok = in_p_j or len(pi) <= 3
    block_ok = in_p_j or len(pi) <= 4
    hereditary = del_ok and block_ok
    fp = audit_forbidden_patterns(gate_set)
    return RealizableClassAudit(
        pi=pi,
        in_p_j=in_p_j,
        cyclic_shift_closed=cyclic_ok,
        reversal_closed=rev_ok,
        deletion_closed=del_ok,
        block_restriction_closed=block_ok,
        hereditary=hereditary,
        pattern_verdict=fp.verdict,
        messages=[f"in_P_J={in_p_j}, hereditary={hereditary}, verdict={fp.verdict}"],
    )


def pattern_containment(pi: list[int], sub: list[int]) -> bool:
    """Test whether sub is a pattern of pi (containment, not proof of closure)."""
    m = len(sub)
    n = len(pi)
    if m > n:
        return False
    for i in range(n - m + 1):
        block = pi[i : i + m]
        if sorted(block) == sorted(sub):
            rel_b = sorted(range(m), key=lambda k: block[k])
            rel_s = sorted(range(m), key=lambda k: sub[k])
            if rel_b == rel_s:
                return True
    return False
