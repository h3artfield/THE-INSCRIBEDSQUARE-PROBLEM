"""Marked one-point gate measure Pi_v (Directive 055)."""

from __future__ import annotations

from dataclasses import dataclass, asdict
from math import atan2, pi

from squarepeg.defect_extraction.augmented_neutral_state import audit_augmented_neutral_state
from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree


@dataclass
class GateMark:
    node_id: str
    gate_index: int
    boundary_phase: float
    parameter_phase: float
    scale: float
    center_x: float
    center_y: float
    attachment: float
    sign: float
    multiplicity: int
    param_component: int


@dataclass
class MarkedGateMeasure:
    parent_id: str
    atoms: list[GateMark]
    total_mass: float


@dataclass
class MarkedGateMeasureAudit:
    measures: list[MarkedGateMeasure]
    messages: list[str]


def _phase(x: float, y: float) -> float:
    return (atan2(y, x) + pi) / (2 * pi)


def audit_marked_gate_measure(tree: CanonicalIntrusionTree) -> MarkedGateMeasureAudit:
    states = audit_augmented_neutral_state(tree)
    measures: list[MarkedGateMeasure] = []
    for s in states.states:
        node = tree.nodes.get(s.node_id)
        if not node:
            continue
        atoms: list[GateMark] = []
        gc = max(node.gate_count, 1)
        mass = 0.0
        for i in range(gc):
            bx = _phase(node.center[0] + 0.01 * i, node.center[1])
            py = (node.param_interval[0] + node.param_interval[1]) / 2.0
            att = s.Phi / gc
            q = att
            mass += q
            atoms.append(
                GateMark(
                    s.node_id,
                    i,
                    bx,
                    py,
                    node.diameter,
                    node.center[0],
                    node.center[1],
                    att,
                    1.0 if i % 2 == 0 else -1.0,
                    1,
                    i % 2,
                )
            )
        measures.append(MarkedGateMeasure(s.node_id, atoms, mass))
    return MarkedGateMeasureAudit(measures=measures, messages=[f"measures={len(measures)}"])


def serialize_gate_marks(tree: CanonicalIntrusionTree) -> list[dict]:
    audit = audit_marked_gate_measure(tree)
    out: list[dict] = []
    for m in audit.measures:
        for a in m.atoms:
            out.append(asdict(a))
    return out
