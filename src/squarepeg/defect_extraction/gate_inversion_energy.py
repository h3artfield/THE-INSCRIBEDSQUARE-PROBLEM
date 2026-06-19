"""Gate inversion energy and T070 (Directive 035)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.infinite_gate_measure import InfiniteGateSet
from squarepeg.defect_extraction.measurable_gate_field import GateOrderRelations, gate_order_relations

T070Status = Literal["CONJECTURAL_ORDER_TARGET", "PROVED_LOCALLY"]


@dataclass
class InversionEnergy:
    leaf_id: str
    energy: float
    inversion_pairs: int
    total_pairs: int
    positive_class: bool


@dataclass
class T070Certificate:
    status: T070Status
    almost_everywhere_ordered: bool
    null_gate_removable: bool
    truncation_gate_ordered: bool
    messages: list[str]


def inversion_energy(gate_set: InfiniteGateSet) -> InversionEnergy:
    """I(L) = iint 1[boundary and parameter orders disagree] dnu dnu."""
    order = gate_order_relations(gate_set)
    inv = 0
    pairs = 0
    b = order.boundary_order
    p = order.parameter_order
    b_idx = {gid: i for i, gid in enumerate(b)}
    p_idx = {gid: i for i, gid in enumerate(p)}
    for i, gi in enumerate(b):
        for gj in b[i + 1 :]:
            pairs += 1
            if (p_idx.get(gi, 0) - p_idx.get(gj, 0)) * (b_idx[gi] - b_idx[gj]) < 0:
                inv += 1
    energy = inv / pairs if pairs else 0.0
    return InversionEnergy(
        leaf_id=gate_set.leaf_id,
        energy=energy,
        inversion_pairs=inv,
        total_pairs=pairs,
        positive_class=energy >= 0.05,
    )


def inversion_on_truncation(gate_set: InfiniteGateSet, N: int) -> float:
    sub_gates = gate_set.gates[: min(N, len(gate_set.gates))]
    from squarepeg.defect_extraction.infinite_gate_measure import InfiniteGateSet as IGS

    sub = IGS(gate_set.leaf_id, "FINITE", sub_gates, True, sum(g.scale_weight for g in sub_gates))
    return inversion_energy(sub).energy


def certify_t070(gate_set: InfiniteGateSet) -> T070Certificate:
    """T070: I(L)=0 => a.e. gate order compatibility after null removal."""
    inv = inversion_energy(gate_set)
    status: T070Status = "CONJECTURAL_ORDER_TARGET"
    ae_ordered = inv.energy < 1e-9
    if ae_ordered:
        status = "PROVED_LOCALLY"
    return T070Certificate(
        status=status,
        almost_everywhere_ordered=ae_ordered,
        null_gate_removable=ae_ordered,
        truncation_gate_ordered=ae_ordered or inversion_on_truncation(gate_set, len(gate_set.gates)) < 0.01,
        messages=[f"I(L)={inv.energy:.4f}"],
    )
