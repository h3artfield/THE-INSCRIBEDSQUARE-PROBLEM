"""M_GATE_BOUNDED clusters and T057 (Directive 029)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.ear_peeling import EarPeelingResult, peel_ears
from squarepeg.defect_extraction.gate_graph import GateGraph
from squarepeg.defect_extraction.outerplanar_structure import audit_outerplanarity

T057Status = Literal["CONJECTURAL_TARGET", "PROVED_LOCALLY_BOUNDED"]
T057Outcome = Literal[
    "TWO_GATE_FOREST",
    "PROTECTED_SQUARE",
    "IRREDUCIBLE_OUTERPLANAR",
]


@dataclass
class BoundedGateCluster:
    gate_graph: GateGraph
    gate_bound: int
    jordan_hull: bool


@dataclass
class T057Audit:
    status: T057Status
    outcome: T057Outcome
    peel: EarPeelingResult | None
    gate_count: int
    messages: list[str]


def is_m_gate_bounded(g: GateGraph, m: int) -> bool:
    return g.gate_count <= m


def audit_t057(cluster: BoundedGateCluster) -> T057Audit:
    """
    T057: every M_GATE_BOUNDED finite saturated cluster with Jordan hull
    decomposes into two-gate forest OR irreducible outerplanar type.
    """
    g = cluster.gate_graph
    msgs: list[str] = []
    if not cluster.jordan_hull:
        return T057Audit(
            status="CONJECTURAL_TARGET",
            outcome="IRREDUCIBLE_OUTERPLANAR",
            peel=None,
            gate_count=g.gate_count,
            messages=["Non-Jordan hull — see nonjordan_hull module"],
        )
    if not is_m_gate_bounded(g, cluster.gate_bound):
        return T057Audit(
            status="CONJECTURAL_TARGET",
            outcome="IRREDUCIBLE_OUTERPLANAR",
            peel=None,
            gate_count=g.gate_count,
            messages=[f"Gate count {g.gate_count} exceeds bound {cluster.gate_bound}"],
        )
    op = audit_outerplanarity(g)
    if not op.is_outerplanar:
        return T057Audit(
            status="CONJECTURAL_TARGET",
            outcome="IRREDUCIBLE_OUTERPLANAR",
            peel=None,
            gate_count=g.gate_count,
            messages=["Gate graph not outerplanar"],
        )
    peel = peel_ears(g)
    msgs.extend(peel.messages)
    outcome: T057Outcome = "IRREDUCIBLE_OUTERPLANAR"
    status: T057Status = "CONJECTURAL_TARGET"
    if peel.status in ("TWO_GATE_REMAINDER", "ALL_EARS_SURGERY"):
        outcome = "TWO_GATE_FOREST"
        status = "PROVED_LOCALLY_BOUNDED"
        msgs.append("Ear peeling yields two-gate forest")
    elif peel.status == "GEOMETRIC_GAP":
        outcome = "IRREDUCIBLE_OUTERPLANAR"
        msgs.append("Geometric ear gap blocks full reduction")
    return T057Audit(status=status, outcome=outcome, peel=peel, gate_count=g.gate_count, messages=msgs)


def t057_statement() -> str:
    return "T057 — PROVED_LOCALLY for outerplanar M-gate clusters without geometric ear gap"
