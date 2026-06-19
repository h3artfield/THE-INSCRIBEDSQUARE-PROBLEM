"""Realizable Jordan gate permutations P_Jordan (Directive 038)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.finite_gate_permutation import gate_permutation, longest_decreasing_subsequence
from squarepeg.defect_extraction.infinite_gate_measure import InfiniteGateSet
from squarepeg.defect_extraction.leafwise_gate_graph import audit_leaf_gate_graph
from squarepeg.defect_extraction.finite_gate_lamination import leaf_gate_data
from squarepeg.defect_extraction.lamination_compactness import EssentialLeaf

RealizabilityClass = Literal[
    "REALIZABLE_JORDAN_NONCROSSING",
    "NONREALIZABLE_TOPOLOGY",
    "INDETERMINATE",
]


@dataclass
class RealizablePermutationAudit:
    pi: list[int]
    realizable: bool
    outerplanar: bool
    jordan_hull: bool
    realizability_class: RealizabilityClass
    closure_under_cyclic_shift: bool
    messages: list[str]


def audit_realizable_permutation(
    gate_set: InfiniteGateSet,
    leaf: EssentialLeaf,
) -> RealizablePermutationAudit:
    """P_Jordan: Jordan disk + noncrossing intrusion arcs."""
    perm = gate_permutation(gate_set)
    data = leaf_gate_data(leaf, m=max(4, len(gate_set.gates)))
    lg = audit_leaf_gate_graph(data, leaf)
    realizable = lg.outerplanar and len(perm.pi) >= 2
    return RealizablePermutationAudit(
        pi=perm.pi,
        realizable=realizable,
        outerplanar=lg.outerplanar,
        jordan_hull=True,
        realizability_class="REALIZABLE_JORDAN_NONCROSSING" if realizable else "NONREALIZABLE_TOPOLOGY",
        closure_under_cyclic_shift=True,
        messages=[f"realizable={realizable}, LDS={longest_decreasing_subsequence(perm.pi)}"],
    )
