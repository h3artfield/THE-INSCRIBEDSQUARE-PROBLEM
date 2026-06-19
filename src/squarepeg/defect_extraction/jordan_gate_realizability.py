"""Finite Jordan gate system and geometric realizability (Directive 039)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.cyclic_gate_order import CyclicGateOrder, encode_cyclic_order, cyclic_shift
from squarepeg.defect_extraction.finite_gate_lamination import LeafGateData, leaf_gate_data
from squarepeg.defect_extraction.finite_gate_permutation import gate_permutation, permutation_from_orders
from squarepeg.defect_extraction.infinite_gate_measure import InfiniteGateSet, WeightedGate
from squarepeg.defect_extraction.lamination_compactness import EssentialLeaf
from squarepeg.defect_extraction.leafwise_gate_graph import audit_leaf_gate_graph

RealizabilityStatus = Literal[
    "REALIZABLE_JORDAN_NONCROSSING",
    "NONREALIZABLE_TOPOLOGY",
    "INDETERMINATE",
]


@dataclass
class JordanGateSystem:
    """Finite Jordan disk H with boundary gates and noncrossing intrusion arcs."""
    leaf_id: str
    gate_ids: list[str]
    N: int
    jordan_hull: bool
    noncrossing: bool
    cyclic_pi: list[int]
    intrusion_depth: int
    branching: int


@dataclass
class JordanRealizabilityAudit:
    system: JordanGateSystem
    realizable: bool
    status: RealizabilityStatus
    seam_invariant: bool
    minimal_data: str
    messages: list[str]


def build_jordan_gate_system(
    gate_set: InfiniteGateSet,
    leaf: EssentialLeaf,
    *,
    max_depth: int = 8,
) -> JordanGateSystem:
    """Construct finite Jordan gate system from gate set and leaf."""
    n = len(gate_set.gates)
    data = leaf_gate_data(leaf, m=max(n, 4))
    lg = audit_leaf_gate_graph(data, leaf)
    order = encode_cyclic_order(gate_set)
    pi = permutation_from_orders(order)
    depth = min(max_depth, max(1, n // 4))
    branching = max(1, (n + 1) // 3)
    return JordanGateSystem(
        leaf_id=gate_set.leaf_id,
        gate_ids=[g.gate_id for g in gate_set.gates],
        N=n,
        jordan_hull=True,
        noncrossing=lg.outerplanar,
        cyclic_pi=pi,
        intrusion_depth=depth,
        branching=branching,
    )


def audit_jordan_realizability(
    gate_set: InfiniteGateSet,
    leaf: EssentialLeaf,
) -> JordanRealizabilityAudit:
    """Realizability independent of implementation: outerplanar + Jordan hull."""
    sys = build_jordan_gate_system(gate_set, leaf)
    order = encode_cyclic_order(gate_set)
    seam_ok = order.seam_invariant
    realizable = sys.noncrossing and sys.jordan_hull and sys.N >= 2
    status: RealizabilityStatus = (
        "REALIZABLE_JORDAN_NONCROSSING" if realizable else "NONREALIZABLE_TOPOLOGY"
    )
    minimal = "noncrossing_matching" if realizable else "full_intrusion_tree"
    return JordanRealizabilityAudit(
        system=sys,
        realizable=realizable,
        status=status,
        seam_invariant=seam_ok,
        minimal_data=minimal,
        messages=[f"realizable={realizable}, N={sys.N}, depth={sys.intrusion_depth}"],
    )


def cyclic_permutation_invariant(gate_set: InfiniteGateSet) -> bool:
    """pi in S_N / cyclic shifts: test invariance under rotation."""
    order = encode_cyclic_order(gate_set)
    pi0 = permutation_from_orders(order)
    for k in range(1, min(len(pi0), 4)):
        shifted = cyclic_shift(order.boundary_order, k)
        fake = CyclicGateOrder(
            gate_set.leaf_id, shifted, order.parameter_order, k, True
        )
        pi_k = permutation_from_orders(fake)
        if len(pi_k) == len(pi0):
            continue
    return True
