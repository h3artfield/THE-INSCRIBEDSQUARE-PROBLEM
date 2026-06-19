"""T053B bounded-gate finite-intrusion extraction (Directive 029)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from squarepeg.defect_extraction.bounded_gate_cluster import BoundedGateCluster, T057Audit, audit_t057
from squarepeg.defect_extraction.cluster_signature import T052Certificate, certify_t052
from squarepeg.defect_extraction.cluster_forest import ClusterForest
from squarepeg.defect_extraction.ear_peeling import EarPeelingResult
from squarepeg.defect_extraction.retained_skeleton_iteration import iterate_retained_skeleton
from squarepeg.defect_surgery.nested_forest import PacketForest
from squarepeg.defect_surgery.packet_disk import Point

T053BStatus = Literal[
    "CONJECTURAL_CONTROLLED_EXTRACTION",
    "PROVED_LOCALLY_BOUNDED_GATE",
]
T050RStatus = Literal["CONJECTURAL_STRUCTURAL_TARGET", "PROVED_LOCALLY_FINITE"]


@dataclass
class T053BCertificate:
    status: T053BStatus
    t057: T057Audit
    t052: T052Certificate | None
    retained_complete: bool
    messages: list[str] = field(default_factory=list)


@dataclass
class T050RAudit:
    status: T050RStatus
    branch: Literal[
        "TWO_GATE",
        "OUTERPLANAR_MULTI_GATE",
        "NON_JORDAN_HULL",
        "POSITIVE_SCALE",
        "UNBOUNDED_GATE_SEQUENCE",
    ]
    messages: list[str]


def certify_t053b(
    cluster: BoundedGateCluster,
    vertices: list[Point],
    forest: ClusterForest,
    i0: int,
    i1: int,
) -> T053BCertificate:
    """
    T053B: finite intrusion tree + Jordan hull + M gates + ear hypotheses
    => signature-controlled cluster surgery forest => T052 => T043R => T022.
    """
    t057 = audit_t057(cluster)
    msgs = list(t057.messages)
    status: T053BStatus = "CONJECTURAL_CONTROLLED_EXTRACTION"
    t052 = None
    retained_ok = False
    if t057.outcome == "TWO_GATE_FOREST" and t057.peel and t057.peel.jordan_preserved:
        t052 = certify_t052(forest, vertices, i0, i1)
        if vertices:
            iteration = iterate_retained_skeleton(vertices, PacketForest(disks=[]), i0, i1)
            retained_ok = iteration[-1].status == "COVER_COMPLETE" if iteration else False
        if t052.status == "PROVED_LOCALLY_ORDERED_FOREST":
            status = "PROVED_LOCALLY_BOUNDED_GATE"
            msgs.append("T052 cluster signature satisfied")
    return T053BCertificate(
        status=status,
        t057=t057,
        t052=t052,
        retained_complete=retained_ok,
        messages=msgs,
    )


def audit_t050r(
    *,
    gate_count: int,
    jordan_hull: bool,
    outerplanar: bool,
    unbounded_sequence: bool,
    positive_scale: bool,
) -> T050RAudit:
    """T050R replaces overstrong T050 with five explicit branches."""
    if unbounded_sequence:
        return T050RAudit(
            status="CONJECTURAL_STRUCTURAL_TARGET",
            branch="UNBOUNDED_GATE_SEQUENCE",
            messages=["Gate count unbounded along sequence"],
        )
    if not jordan_hull:
        return T050RAudit(
            status="CONJECTURAL_STRUCTURAL_TARGET",
            branch="NON_JORDAN_HULL",
            messages=["Saturation hull obstruction"],
        )
    if positive_scale:
        return T050RAudit(
            status="CONJECTURAL_STRUCTURAL_TARGET",
            branch="POSITIVE_SCALE",
            messages=["Positive geometric scale"],
        )
    if gate_count <= 2:
        return T050RAudit(
            status="PROVED_LOCALLY_FINITE",
            branch="TWO_GATE",
            messages=["Two-gate cluster"],
        )
    if outerplanar and gate_count >= 4:
        return T050RAudit(
            status="CONJECTURAL_STRUCTURAL_TARGET",
            branch="OUTERPLANAR_MULTI_GATE",
            messages=["Finite outerplanar multi-gate cluster"],
        )
    return T050RAudit(
        status="CONJECTURAL_STRUCTURAL_TARGET",
        branch="TWO_GATE",
        messages=["Fallback classification"],
    )
