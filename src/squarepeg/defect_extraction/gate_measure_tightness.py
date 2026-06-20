"""Tightness for augmented gate measures (Directive 055)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.gate_collision_measure import audit_gate_collision_measure
from squarepeg.defect_extraction.gate_pair_interaction_measure import audit_gate_pair_interaction_measure
from squarepeg.defect_extraction.marked_gate_measure import audit_marked_gate_measure


@dataclass
class GateMeasureTightnessRecord:
    parent_id: str
    psi_moment: float
    tight: bool


@dataclass
class GateMeasureTightnessAudit:
    records: list[GateMeasureTightnessRecord]
    all_tight: bool
    messages: list[str]


def audit_gate_measure_tightness(tree: CanonicalIntrusionTree) -> GateMeasureTightnessAudit:
    pi = audit_marked_gate_measure(tree)
    omega = audit_gate_pair_interaction_measure(tree)
    lam = audit_gate_collision_measure(tree)
    records: list[GateMeasureTightnessRecord] = []
    omap = {m.parent_id: m for m in omega.measures}
    lmap = {m.parent_id: m for m in lam.measures}
    for m in pi.measures:
        o = omap.get(m.parent_id)
        l = lmap.get(m.parent_id)
        psi = m.total_mass + (o.cross_area if o else 0.0) + (l.diagonal_mass if l else 0.0)
        records.append(GateMeasureTightnessRecord(m.parent_id, psi, psi < 100.0))
    tight = all(r.tight for r in records) and bool(records)
    return GateMeasureTightnessAudit(records=records, all_tight=tight, messages=[f"tight={tight}"])
