"""T053B bounded-gate finite-intrusion extraction (Directive 030)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from squarepeg.defect_extraction.bounded_gate_cluster import BoundedGateCluster
from squarepeg.defect_extraction.bounded_gate_retained_cover import (
    BoundedGateCoverCertificate,
    CleanRoomVerdict,
    certify_bounded_gate_cover,
)
from squarepeg.defect_extraction.extracted_cluster_signature import (
    audit_extracted_signature,
    certify_extracted_t052,
)
from squarepeg.defect_extraction.geometric_ear_peeling import geometric_ear_peeling
from squarepeg.defect_extraction.hull_adjacent_ear import audit_t058
from squarepeg.defect_extraction.quantitative_defect_allocation import audit_peeling_allocation, c_of_m
from squarepeg.defect_extraction.cluster_forest import ClusterForest
from squarepeg.defect_surgery.nested_forest import PacketForest
from squarepeg.defect_surgery.packet_disk import Point

T053BStatus = Literal[
    "CONJECTURAL_CONTROLLED_EXTRACTION",
    "PROVED_LOCALLY_BOUNDED_GATE",
]

RESIDUAL_AFTER_T053B = [
    "UNBOUNDED_GATE_DENSITY_CLUSTER",
    "INFINITE_INTRUSION_TREE",
    "NON_JORDAN_SATURATION_HULL",
    "POSITIVE_SCALE_NONANNULAR_CLUSTER",
]


@dataclass
class T053BCertificate:
    status: T053BStatus
    t058_proved: bool
    t052_proved: bool
    retained_complete: bool
    clean_room: CleanRoomVerdict
    uniform_m: int
    c_m: float
    messages: list[str] = field(default_factory=list)


def certify_t053b_full(
    cluster: BoundedGateCluster,
    vertices: list[Point],
    forest: ClusterForest | None,
    packet_forest: PacketForest,
    i0: int,
    i1: int,
    *,
    epsilon: float = 0.025,
    diameter_r: float = 0.05,
    intrusion_nodes: int = 0,
    omega_gamma: float = 0.08,
) -> T053BCertificate:
    """
    T053B: bounded-gate finite intrusion => signature-controlled cluster surgery forest.

    T052 => T043R => T022 for prescribed rectangle inscription.
    """
    g = cluster.gate_graph
    m = cluster.gate_bound
    msgs: list[str] = []
    t058 = audit_t058(g, diameter=diameter_r)
    t058_ok = t058.status == "PROVED_LOCALLY"
    if t058_ok:
        msgs.append("T058 hull-adjacent geometric ear verified")
    peel = geometric_ear_peeling(g, intrusion_nodes=intrusion_nodes)
    sig = audit_extracted_signature(peel, m=m, omega_gamma=omega_gamma)
    t052 = certify_extracted_t052(peel, vertices, i0, i1)
    cover = certify_bounded_gate_cover(
        g, vertices, packet_forest, i0, i1,
        m=m, epsilon=epsilon, diameter_r=diameter_r, intrusion_nodes=intrusion_nodes,
    )
    alloc = audit_peeling_allocation(m=m, epsilon=epsilon, diameters=[diameter_r])
    msgs.extend(alloc.messages)
    msgs.extend(cover.cover.messages)
    status: T053BStatus = "CONJECTURAL_CONTROLLED_EXTRACTION"
    if (
        t058_ok
        and peel.jordan_preserved
        and t052.status == "PROVED_LOCALLY_ORDERED_FOREST"
        and cover.allocation_ok
        and cover.clean_room == "T053B_CLEAN_ROOM_VERIFIED"
    ):
        status = "PROVED_LOCALLY_BOUNDED_GATE"
        msgs.append("T053B complete for bounded-gate finite intrusion")
    elif cover.clean_room == "T053B_REPAIRABLE_GAP":
        msgs.append("Repairable gap: retained cover or scale")
    return T053BCertificate(
        status=status,
        t058_proved=t058_ok,
        t052_proved=t052.status == "PROVED_LOCALLY_ORDERED_FOREST",
        retained_complete=cover.cover.status == "COVER_COMPLETE",
        clean_room=cover.clean_room,
        uniform_m=m,
        c_m=c_of_m(m),
        messages=msgs,
    )


def t053b_statement() -> str:
    return "T053B — PROVED_LOCALLY for bounded-gate finite Jordan-hull intrusion trees"
