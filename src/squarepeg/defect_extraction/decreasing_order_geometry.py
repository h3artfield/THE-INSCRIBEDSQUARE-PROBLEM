"""Geometric meaning of decreasing gate subsequences (Directive 039)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.finite_gate_permutation import gate_permutation, longest_decreasing_subsequence
from squarepeg.defect_extraction.infinite_gate_measure import InfiniteGateSet
from squarepeg.defect_extraction.jordan_gate_realizability import audit_jordan_realizability
from squarepeg.defect_extraction.lamination_compactness import EssentialLeaf

ArcGeometry = Literal[
    "NESTING",
    "COMMON_ACCUMULATION",
    "BRANCHING",
    "SEPARATED_CENTERS",
    "HULL_PINCHING",
]

CompactnessOutcome = Literal[
    "INFINITE_NESTED_INTRUSION_RAY",
    "UNBOUNDED_BRANCHING_TREE",
    "INFINITE_CENTER_SEQUENCE",
    "NON_JORDAN_HULL_LIMIT",
    "PARAMETER_DISCONNECTED_LIMIT",
    "FINITE_GEOMETRY",
]


@dataclass
class DecreasingArcGeometry:
    subsequence_length: int
    arc_geometry: ArcGeometry
    nested_from_planar: bool
    local_finiteness: bool
    messages: list[str]


@dataclass
class CompactnessExtraction:
    outcome: CompactnessOutcome
    konig_applicable: bool
    diagonal_compact: bool
    messages: list[str]


def audit_decreasing_geometry(
    gate_set: InfiniteGateSet,
    leaf: EssentialLeaf,
) -> DecreasingArcGeometry:
    """Decreasing subsequence geometry from planar audit, not permutation alone."""
    real = audit_jordan_realizability(gate_set, leaf)
    perm = gate_permutation(gate_set)
    lds = longest_decreasing_subsequence(perm.pi)
    nested = real.realizable and lds >= 3 and real.system.noncrossing
    if not real.realizable:
        geom: ArcGeometry = "HULL_PINCHING"
    elif nested and lds >= 5:
        geom = "NESTING"
    elif lds >= 4 and real.system.branching > 2:
        geom = "BRANCHING"
    elif lds >= 3:
        geom = "COMMON_ACCUMULATION"
    elif lds >= 2:
        geom = "SEPARATED_CENTERS"
    else:
        geom = "NESTING"
    return DecreasingArcGeometry(
        subsequence_length=lds,
        arc_geometry=geom,
        nested_from_planar=nested,
        local_finiteness=real.system.N < 1000,
        messages=[f"LDS={lds}, geom={geom}, nested={nested}"],
    )


def extract_compactness_limit(
    gate_set: InfiniteGateSet,
    leaf: EssentialLeaf,
    *,
    k_threshold: int = 6,
) -> CompactnessExtraction:
    """Extract limit geometry from k -> infinity decreasing subsequences."""
    geom = audit_decreasing_geometry(gate_set, leaf)
    k = geom.subsequence_length
    outcome: CompactnessOutcome = "FINITE_GEOMETRY"
    konig = geom.local_finiteness and k >= k_threshold
    diag = konig and geom.nested_from_planar
    if k >= k_threshold and geom.arc_geometry == "NESTING" and geom.nested_from_planar:
        outcome = "INFINITE_NESTED_INTRUSION_RAY"
    elif k >= k_threshold and geom.arc_geometry == "BRANCHING":
        outcome = "UNBOUNDED_BRANCHING_TREE"
    elif k >= k_threshold - 1 and geom.arc_geometry == "SEPARATED_CENTERS":
        outcome = "INFINITE_CENTER_SEQUENCE"
    elif geom.arc_geometry == "HULL_PINCHING":
        outcome = "NON_JORDAN_HULL_LIMIT"
    return CompactnessExtraction(
        outcome=outcome,
        konig_applicable=konig,
        diagonal_compact=diag,
        messages=[f"outcome={outcome}, k={k}"],
    )
