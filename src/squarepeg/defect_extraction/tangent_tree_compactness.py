"""Tangent end-tree compactness (Directive 045)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.bad_end_cylinders import maximal_bad_antichain
from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.normalized_end_tangent import NormalizedEndTangent, normalize_bad_cylinder

CompactnessFailure = Literal[
    "TREE_COMPACTNESS_FAILURE",
    "HULL_COMPACTNESS_FAILURE",
    "END_MAP_GRAPH_FAILURE",
    "PARAMETER_SUPPORT_COMPACTNESS_FAILURE",
    "UNBOUNDED_LOCAL_COMPLEXITY",
    "NONE",
]


@dataclass
class TangentSequence:
    node_ids: list[str]
    tangents: list[NormalizedEndTangent]
    converged: bool


@dataclass
class TangentCompactnessAudit:
    sequence: TangentSequence | None
    tree_compact: bool
    hull_compact: bool
    measure_compact: bool
    failure: CompactnessFailure
    messages: list[str]


def build_tangent_sequence(
    tree: CanonicalIntrusionTree,
    *,
    A: float = 4.0,
    max_steps: int = 4,
) -> TangentSequence:
    bad = maximal_bad_antichain(tree, A=A)
    tangents = [normalize_bad_cylinder(tree, b.node_id) for b in bad[:max_steps]]
    ids = [b.node_id for b in bad[:max_steps]]
    converged = len(tangents) >= 1 and all(t.density_ratio_identity for t in tangents)
    return TangentSequence(ids, tangents, converged)


def audit_tangent_tree_compactness(
    tree: CanonicalIntrusionTree,
    *,
    A: float = 4.0,
) -> TangentCompactnessAudit:
    seq = build_tangent_sequence(tree, A=A)
    if not seq.tangents:
        return TangentCompactnessAudit(
            sequence=seq,
            tree_compact=False,
            hull_compact=False,
            measure_compact=False,
            failure="TREE_COMPACTNESS_FAILURE",
            messages=["no bad cylinders"],
        )
    t = seq.tangents[0]
    radii = [n.hull_radius for n in t.nodes]
    hull_compact = max(radii, default=1.0) <= 2.0 and min(radii, default=0.0) >= 0.0
    mu_sum = sum(n.mu_tilde for n in t.nodes)
    measure_compact = 0.5 <= mu_sum <= 3.0 or mu_sum > 0
    branching = max(len(tree.nodes[n].child_ids) for n in tree.nodes)
    failure: CompactnessFailure = "NONE"
    if branching > 50:
        failure = "UNBOUNDED_LOCAL_COMPLEXITY"
    elif not hull_compact:
        failure = "HULL_COMPACTNESS_FAILURE"
    elif not measure_compact:
        failure = "END_MAP_GRAPH_FAILURE"
    tree_compact = seq.converged and failure == "NONE"
    return TangentCompactnessAudit(
        sequence=seq,
        tree_compact=tree_compact,
        hull_compact=hull_compact,
        measure_compact=measure_compact,
        failure=failure,
        messages=[f"compact={tree_compact}, failure={failure}"],
    )
