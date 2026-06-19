"""Multi-gate saturated clusters T054 (Directive 028)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_surgery.annular_attachment_order import GatePair, endpoints_interleave

T054Status = Literal["CONJECTURAL_MULTIGATE_TARGET", "PROVED_LOCALLY_SUBCLUSTER"]

T054Outcome = Literal[
    "TWO_GATE_SUBCLUSTER",
    "PROTECTED_SQUARE",
    "MULTICENTER_RESIDUAL",
]


@dataclass
class GateWord:
    boundary_order: list[str]
    parameter_order: list[str]
    pairing: Literal["ALTERNATING", "NESTED", "MIXED"]


@dataclass
class MultiGateCluster:
    gate_count: int
    gates: list[GatePair]
    gate_word: GateWord
    winding_same_sign: bool


@dataclass
class T054Audit:
    status: T054Status
    outcome: T054Outcome
    interleaving_unprotected: bool
    messages: list[str]


def classify_gate_pairing(gates: list[GatePair]) -> Literal["ALTERNATING", "NESTED", "MIXED"]:
    if len(gates) < 2:
        return "NESTED"
    interleaved = any(endpoints_interleave(gates[i], gates[j]) for i in range(len(gates)) for j in range(i + 1, len(gates)))
    if interleaved:
        return "ALTERNATING"
    return "NESTED"


def audit_multigate_cluster(cluster: MultiGateCluster) -> T054Audit:
    """
    T054: >=4 gates => two-gate subcluster, protected square, or multicenter residual.

    Interleaving alone does NOT imply T039 protection (Directive 027 / T049).
    """
    msgs = ["Multi-gate cluster not auto-assigned to protected-square branch"]
    if cluster.gate_count < 4:
        return T054Audit(
            status="CONJECTURAL_MULTIGATE_TARGET",
            outcome="TWO_GATE_SUBCLUSTER",
            interleaving_unprotected=False,
            messages=["Fewer than four gates"],
        )
    if cluster.gate_word.pairing == "NESTED" and cluster.winding_same_sign:
        return T054Audit(
            status="CONJECTURAL_MULTIGATE_TARGET",
            outcome="TWO_GATE_SUBCLUSTER",
            interleaving_unprotected=False,
            messages=["Nested pairing may yield two-gate subcluster with definite defect"],
        )
    return T054Audit(
        status="CONJECTURAL_MULTIGATE_TARGET",
        outcome="MULTICENTER_RESIDUAL",
        interleaving_unprotected=cluster.gate_word.pairing == "ALTERNATING",
        messages=msgs + ["No protected-square theorem without additional structure"],
    )


def _gate(i0: int, i1: int, pa: tuple[float, float], pb: tuple[float, float]) -> GatePair:
    cx = (pa[0] + pb[0]) / 2
    cy = (pa[1] + pb[1]) / 2
    r = max(abs(pa[0] - pb[0]), abs(pa[1] - pb[1]), 0.05) / 2
    return GatePair(i0, i1, pa, pb, (cx, cy), r)


def example_four_gate_cluster() -> MultiGateCluster:
    gates = [
        _gate(0, 1, (0.0, 0.0), (0.5, 0.0)),
        _gate(2, 3, (0.5, 0.5), (1.0, 0.5)),
        _gate(4, 5, (1.0, 1.0), (0.5, 1.0)),
        _gate(6, 7, (0.0, 0.5), (0.0, 1.0)),
    ]
    return MultiGateCluster(
        gate_count=4,
        gates=gates,
        gate_word=GateWord(
            boundary_order=["G1", "G2", "G3", "G4"],
            parameter_order=["G1", "G3", "G2", "G4"],
            pairing=classify_gate_pairing(gates),
        ),
        winding_same_sign=True,
    )


def example_six_gate_nested() -> MultiGateCluster:
    gates = [_gate(2 * i, 2 * i + 1, (i * 0.2, 0.0), (i * 0.2 + 0.1, 0.0)) for i in range(6)]
    return MultiGateCluster(
        gate_count=6,
        gates=gates,
        gate_word=GateWord(
            boundary_order=[f"G{i}" for i in range(6)],
            parameter_order=[f"G{i}" for i in range(6)],
            pairing="NESTED",
        ),
        winding_same_sign=True,
    )
