"""Signature-weighted occupation measures on neutral states (Directive 051)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_extraction.augmented_neutral_state import audit_augmented_neutral_state
from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.neutral_transfer_operator import audit_neutral_transfer_operator


@dataclass
class OccupationAtom:
    node_id: str
    weight: float
    X_hat: tuple[float, ...]
    scale_ratio: float


@dataclass
class NeutralOccupationMeasure:
    atoms: list[OccupationAtom]
    total_mass: float
    boundary_leakage: float
    normalized: bool


@dataclass
class NeutralOccupationAudit:
    measure: NeutralOccupationMeasure
    corona_depth: int
    messages: list[str]


def audit_neutral_occupation_measure(tree: CanonicalIntrusionTree) -> NeutralOccupationAudit:
    states = audit_augmented_neutral_state(tree)
    transfer = audit_neutral_transfer_operator(tree)
    ratio_map = {t.child_id: t.scale_ratio for t in transfer.transfers}
    total = sum(s.Phi for s in states.states) or 1.0
    atoms: list[OccupationAtom] = []
    for s in states.states:
        w = s.Phi / total
        atoms.append(OccupationAtom(s.node_id, w, s.X_hat, ratio_map.get(s.node_id, 0.0)))
    boundary = sum(s.B for s in states.states) / total
    depth = 0
    if atoms:
        from squarepeg.defect_extraction.noncarleson_end_density import cylinder_density
        depth = max(cylinder_density(tree, a.node_id).depth for a in atoms)
    return NeutralOccupationAudit(
        measure=NeutralOccupationMeasure(atoms, 1.0, boundary, True),
        corona_depth=depth,
        messages=[f"atoms={len(atoms)}, boundary={boundary:.3f}"],
    )
