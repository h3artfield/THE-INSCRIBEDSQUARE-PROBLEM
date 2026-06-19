"""Unbounded gate accumulation (Directive 029)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

ResidualGateClass = Literal[
    "UNBOUNDED_GATE_DENSITY_CLUSTER",
    "DENSE_BOUNDARY_GATE_ACCUMULATION",
    "UNBOUNDED_OUTERPLANAR_BRANCHING",
    "NONVANISHING_JOIN_SIGNATURE_CLUSTER",
    "NONE",
]


@dataclass
class GateAccumulationRecord:
    cluster_id: str
    gate_count: int
    diameter: float
    param_diameter: float
    gate_spacing_min: float
    defect_per_gate: float
    join_signature: float
    branching_count: int


@dataclass
class GateAccumulationAudit:
    unbounded: bool
    residual_class: ResidualGateClass
    records: list[GateAccumulationRecord]
    alternative: Literal[
        "BOUNDARY_SUBARC_ACCUMULATION",
        "UNBOUNDED_BRANCHING",
        "UNBOUNDED_WINDING",
        "POSITIVE_SCALE",
        "JOIN_SIGNATURE_DOMINANT",
        "NONE",
    ]
    messages: list[str]


def audit_gate_accumulation(records: list[GateAccumulationRecord]) -> GateAccumulationAudit:
    """
    Unbounded gate accumulation: #(Gates(C_n)) -> infty with controlled diameters.

    Classifies gate-density alternatives per Directive 029 Part IX.
    """
    if not records:
        return GateAccumulationAudit(False, "NONE", [], "NONE", ["Empty sequence"])
    gates = [r.gate_count for r in records]
    unbounded = max(gates) > 10 and gates[-1] > gates[0]
    if not unbounded:
        return GateAccumulationAudit(False, "NONE", records, "NONE", ["Gate count bounded"])
    last = records[-1]
    spacing = last.gate_spacing_min
    dpg = last.defect_per_gate
    join = last.join_signature
    alt: GateAccumulationAudit.__annotations__["alternative"] = "NONE"
    residual: ResidualGateClass = "UNBOUNDED_GATE_DENSITY_CLUSTER"
    msgs: list[str] = []
    if spacing < 0.01 and last.diameter < 0.1:
        residual = "DENSE_BOUNDARY_GATE_ACCUMULATION"
        alt = "BOUNDARY_SUBARC_ACCUMULATION"
        msgs.append("Gates accumulate on boundary subarc")
    elif last.branching_count > 4:
        residual = "UNBOUNDED_OUTERPLANAR_BRANCHING"
        alt = "UNBOUNDED_BRANCHING"
    elif join > dpg * last.gate_count:
        residual = "NONVANISHING_JOIN_SIGNATURE_CLUSTER"
        alt = "JOIN_SIGNATURE_DOMINANT"
    elif last.diameter > 0.5:
        alt = "POSITIVE_SCALE"
    return GateAccumulationAudit(
        unbounded=unbounded,
        residual_class=residual,
        records=records,
        alternative=alt,
        messages=msgs or ["Unbounded gate density detected"],
    )


def example_unbounded_gate_sequence(n: int = 12) -> list[GateAccumulationRecord]:
    """Cantor-like gate accumulation candidate."""
    recs: list[GateAccumulationRecord] = []
    for k in range(1, n + 1):
        gc = 2 + k
        d = 0.3 / k
        recs.append(
            GateAccumulationRecord(
                cluster_id=f"C{k}",
                gate_count=gc,
                diameter=d,
                param_diameter=0.2 / k,
                gate_spacing_min=0.05 / k,
                defect_per_gate=0.001 / k,
                join_signature=0.002 * k,
                branching_count=min(k // 2, 6),
            )
        )
    return recs
