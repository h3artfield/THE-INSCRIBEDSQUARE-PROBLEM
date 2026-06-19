"""Infinite-center end geometry (Directive 044)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.end_signature_measure import build_end_signature_measure_v2
from squarepeg.defect_extraction.tree_end_cylinders import build_cylinder


@dataclass
class CenterCoverRecord:
    node_id: str
    N_c: int
    eta: float
    radius: float


@dataclass
class InfiniteCenterEndAudit:
    records: list[CenterCoverRecord]
    infinite_center: bool
    diffuse_end_measure: bool
    positive_scale: bool
    parameter_disconnected: bool
    messages: list[str]


def center_cover_number(
    tree: CanonicalIntrusionTree,
    node_id: str,
    *,
    eta: float = 0.15,
) -> int:
    """Minimum eta r(v)-scale regions covering cylinder signature mass."""
    node = tree.nodes[node_id]
    r = node.diameter * eta
    cyl = build_cylinder(tree, node_id)
    centers: set[tuple[int, int]] = set()
    for eid in cyl.end_ids:
        if eid not in tree.nodes:
            continue
        c = tree.nodes[eid].center
        centers.add((round(c[0] / r), round(c[1] / r)))
    return max(len(centers), 1)


def audit_infinite_center_end_geometry(
    tree: CanonicalIntrusionTree,
    *,
    eta: float = 0.15,
    threshold: int = 6,
) -> InfiniteCenterEndAudit:
    em = build_end_signature_measure_v2(tree)
    records: list[CenterCoverRecord] = []
    for cyl in em.cylinders:
        if not tree.nodes[cyl.node_id].child_ids:
            continue
        nc = center_cover_number(tree, cyl.node_id, eta=eta)
        records.append(
            CenterCoverRecord(cyl.node_id, nc, eta, tree.nodes[cyl.node_id].diameter * eta)
        )

    infinite = any(r.N_c >= threshold for r in records)
    diffuse = em.continuous_mass > 0.1 * em.total_unsigned
    pos_scale = any(tree.nodes[n].diameter > 0.25 for n in tree.nodes)
    param_disc = len({round(n.param_interval[0], 1) for n in tree.nodes.values()}) > 12

    return InfiniteCenterEndAudit(
        records=records,
        infinite_center=infinite,
        diffuse_end_measure=diffuse and infinite,
        positive_scale=pos_scale,
        parameter_disconnected=param_disc,
        messages=[f"infinite_center={infinite}, max_N_c={max((r.N_c for r in records), default=0)}"],
    )
