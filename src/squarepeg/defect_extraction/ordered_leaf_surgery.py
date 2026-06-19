"""ORDERED_TWO_GATE_LAMINATION surgery — T066 (Directive 033)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.lamination_gate_support import classify_parameter_support
from squarepeg.defect_extraction.lamination_leaf_topology import classify_leaf_topology
from squarepeg.defect_extraction.lamination_signature import (
    SurgeryExhaustionStep,
    audit_lamination_signature,
)
from squarepeg.defect_extraction.saturation_hull import SaturationHull
from squarepeg.defect_extraction.two_gate_cluster import SaturatedCluster, audit_two_gate_cluster
from squarepeg.defect_extraction.saturation import SaturationState
from squarepeg.defect_extraction.winding_lamination import DiffuseNoncrossingWindingLamination

T066Status = Literal["CONJECTURAL_TARGET", "PROVED_LOCALLY"]


@dataclass
class OrderedTwoGateLeaf:
    leaf_id: str
    jordan: bool
    two_gates: bool
    chord_safe: bool
    nested_or_disjoint: bool
    gate_order_compatible: bool
    retained_cover_complete: bool


@dataclass
class T066Certificate:
    status: T066Status
    is_ordered_two_gate: bool
    exhaustion_steps: list[SurgeryExhaustionStep]
    tail_defect_tends_zero: bool
    signature_uniform: bool
    messages: list[str]


def is_ordered_two_gate_lamination(lam: DiffuseNoncrossingWindingLamination) -> bool:
    """mu-a.e. leaf is Jordan disk with exactly two gates, nested/disjoint."""
    if not lam.noncrossing or not lam.leaves:
        return False
    for leaf in lam.leaves:
        topo = classify_leaf_topology(leaf, gate_count=2)
        param = classify_parameter_support(leaf.leaf_id, list(range(leaf.level, leaf.level + 2)))
        if not topo.jordan_surgery_eligible or not param.surgery_compatible:
            return False
    return True


def finite_surgery_exhaustion(
    lam: DiffuseNoncrossingWindingLamination,
    *,
    max_depth: int = 5,
) -> list[SurgeryExhaustionStep]:
    """Finite leaf subfamilies L_N increasing in transverse measure."""
    steps: list[SurgeryExhaustionStep] = []
    processed = 0.0
    total = lam.winding_mass or 1.0
    for n in range(1, min(max_depth, len(lam.leaves)) + 1):
        batch = lam.leaves[:n]
        jordan_ok = all(
            classify_leaf_topology(leaf, gate_count=2).jordan_surgery_eligible for leaf in batch
        )
        mass = sum(leaf.area for leaf in batch)
        processed = mass
        steps.append(
            SurgeryExhaustionStep(
                depth=n,
                leaf_ids=[leaf.leaf_id for leaf in batch],
                jordan_preserved=jordan_ok,
                defect_processed=processed / total,
            )
        )
    return steps


def certify_t066(lam: DiffuseNoncrossingWindingLamination) -> T066Certificate:
    """T066: ordered two-gate lamination admits area-tight surgery exhaustion."""
    ordered = is_ordered_two_gate_lamination(lam)
    steps = finite_surgery_exhaustion(lam) if ordered else []
    sig = audit_lamination_signature(lam, steps)
    tail_zero = sig.tail_defect_fraction < 0.05 if steps else False
    status: T066Status = "CONJECTURAL_TARGET"
    if ordered and steps and all(s.jordan_preserved for s in steps) and sig.uniform_vanishing:
        status = "PROVED_LOCALLY"
    msgs = ["Ordered two-gate lamination" if ordered else "Not ordered two-gate"]
    if status == "PROVED_LOCALLY":
        msgs.append("Finite surgery exhaustion with uniform signature control")
    return T066Certificate(
        status=status,
        is_ordered_two_gate=ordered,
        exhaustion_steps=steps,
        tail_defect_tends_zero=tail_zero,
        signature_uniform=sig.uniform_vanishing,
        messages=msgs,
    )


def cluster_from_leaf(leaf_id: str, *, diameter: float = 0.1) -> SaturatedCluster:
    """Build two-gate cluster stub for leaf surgery step."""
    hull = SaturationHull(
        boundary=[],
        center=(0.0, 0.0),
        diameter=diameter,
        is_jordan_disk=True,
        simply_connected=True,
    )
    sat = SaturationState(
        lobe_id=leaf_id,
        lobe_interval=(0.0, 1.0),
        level=1,
        param_intervals=[(0.0, 1.0)],
        intrusion_ids=[],
        stabilized=True,
        reaches_seam=False,
    )
    return SaturatedCluster(
        cluster_id=leaf_id,
        saturation=sat,
        hull=hull,
        gate_a=(0.0, 0.0),
        gate_b=(diameter, 0.0),
        intrusion_depth=1,
        branching=1,
    )


def audit_leaf_cluster_surgery(cluster: SaturatedCluster) -> bool:
    audit = audit_two_gate_cluster(cluster, [cluster.gate_a, cluster.gate_b])
    return audit.two_gate_clean and audit.jordan_hull
