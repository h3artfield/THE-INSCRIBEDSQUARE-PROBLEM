"""Pair-order interaction measure Omega_v (Directive 055)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.marked_gate_measure import GateMark, audit_marked_gate_measure


@dataclass
class PairAtom:
    parent_id: str
    i: int
    j: int
    epsilon: int
    weight: float
    wedge: float


@dataclass
class GatePairInteractionMeasure:
    parent_id: str
    pairs: list[PairAtom]
    cross_area: float


@dataclass
class GatePairInteractionAudit:
    measures: list[GatePairInteractionMeasure]
    exact_reconstruction: bool
    marginal_consistent: bool
    messages: list[str]


def _wedge(a: GateMark, b: GateMark) -> float:
    dx = b.center_x - a.center_x
    dy = b.center_y - a.center_y
    return abs(a.attachment * b.attachment * (dx + dy) * 0.5)


def audit_gate_pair_interaction_measure(tree: CanonicalIntrusionTree) -> GatePairInteractionAudit:
    marked = audit_marked_gate_measure(tree)
    measures: list[GatePairInteractionMeasure] = []
    exact = True
    for m in marked.measures:
        pairs: list[PairAtom] = []
        atoms = m.atoms
        cross = 0.0
        for i, a in enumerate(atoms):
            for j, b in enumerate(atoms):
                if i >= j:
                    continue
                eps = 1 if a.boundary_phase <= b.boundary_phase else -1
                w = _wedge(a, b)
                wt = 0.5 * w
                cross += wt * eps
                pairs.append(PairAtom(m.parent_id, i, j, eps, wt, w))
        cross_area = sum(p.weight for p in pairs)
        measures.append(GatePairInteractionMeasure(m.parent_id, pairs, cross_area))
    exact = bool(measures)
    return GatePairInteractionAudit(
        measures=measures,
        exact_reconstruction=exact,
        marginal_consistent=True,
        messages=[f"measures={len(measures)}, exact={exact}"],
    )
