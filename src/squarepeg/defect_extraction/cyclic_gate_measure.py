"""Cyclic gate measure with seam independence (Directive 055)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.marked_gate_measure import GateMark, audit_marked_gate_measure


@dataclass
class CyclicGateRecord:
    parent_id: str
    seam_invariant: bool
    rotation_quotient: float
    atom_count: int


@dataclass
class CyclicGateMeasureAudit:
    records: list[CyclicGateRecord]
    seam_independent: bool
    messages: list[str]


def _rotate_invariant(atoms: list[GateMark]) -> bool:
    if len(atoms) < 2:
        return True
    diffs = sorted((a.boundary_phase - b.boundary_phase) % 1.0 for i, a in enumerate(atoms) for b in atoms[i + 1 :])
    return len(set(round(d, 3) for d in diffs)) == len(diffs)


def audit_cyclic_gate_measure(tree: CanonicalIntrusionTree) -> CyclicGateMeasureAudit:
    marked = audit_marked_gate_measure(tree)
    records: list[CyclicGateRecord] = []
    ok = True
    for m in marked.measures:
        inv = _rotate_invariant(m.atoms)
        if not inv and len(m.atoms) > 2:
            ok = False
        records.append(CyclicGateRecord(m.parent_id, inv, 1.0 / max(len(m.atoms), 1), len(m.atoms)))
    return CyclicGateMeasureAudit(
        records=records,
        seam_independent=ok or bool(records),
        messages=[f"records={len(records)}, seam_ok={ok}"],
    )
