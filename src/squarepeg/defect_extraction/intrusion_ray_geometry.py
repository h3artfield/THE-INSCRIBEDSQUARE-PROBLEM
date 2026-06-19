"""Intrusion ray geometry and scale classification (Directive 040)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree, IntrusionTreeNode

RayScaleClass = Literal[
    "POSITIVE_SCALE_RAY",
    "SHRINKING_RAY",
    "PLATEAU_JUMP_RAY",
    "GEOMETRIC_DECAY_RAY",
]

PositiveScaleClass = Literal[
    "POSITIVE_SCALE_ANNULAR_RAY",
    "POSITIVE_SCALE_FINITE_CENTER_RAY",
    "POSITIVE_SCALE_NONANNULAR_RAY",
    "POSITIVE_SCALE_NON_JORDAN_RAY",
]


@dataclass
class RayNodeData:
    node_id: str
    diameter: float
    defect: float
    gate_count: int
    center: tuple[float, float]
    sign: int


@dataclass
class IntrusionRay:
    node_ids: list[str]
    data: list[RayNodeData]
    scale_class: RayScaleClass
    positive_subclass: PositiveScaleClass | None


@dataclass
class RayGeometryAudit:
    ray: IntrusionRay
    limsup_r: float
    ratios_stable: bool
    lambda_bounds: tuple[float, float] | None
    messages: list[str]


def extract_ray(tree: CanonicalIntrusionTree) -> IntrusionRay | None:
    """Extract longest path as intrusion ray."""
    path: list[str] = []

    def walk(nid: str) -> None:
        path.append(nid)
        node = tree.nodes[nid]
        if node.child_ids:
            walk(node.child_ids[0])

    if tree.root_id not in tree.nodes:
        return None
    walk(tree.root_id)
    data = [
        RayNodeData(
            nid,
            tree.nodes[nid].diameter,
            tree.nodes[nid].defect,
            tree.nodes[nid].gate_count,
            tree.nodes[nid].center,
            tree.nodes[nid].sign,
        )
        for nid in path
    ]
    scale = _classify_scale(data)
    pos = _positive_subclass(data) if scale == "POSITIVE_SCALE_RAY" else None
    return IntrusionRay(path, data, scale, pos)


def _classify_scale(data: list[RayNodeData]) -> RayScaleClass:
    if not data:
        return "SHRINKING_RAY"
    radii = [d.diameter for d in data]
    if radii[-1] > 0.15 * radii[0]:
        return "POSITIVE_SCALE_RAY"
    if len(radii) < 2:
        return "SHRINKING_RAY"
    ratios = [radii[i + 1] / max(radii[i], 1e-9) for i in range(len(radii) - 1)]
    if all(0.95 <= r <= 1.05 for r in ratios[-3:]) if len(ratios) >= 3 else False:
        return "PLATEAU_JUMP_RAY"
    if all(0.3 <= r <= 0.95 for r in ratios):
        return "GEOMETRIC_DECAY_RAY"
    return "SHRINKING_RAY"


def _positive_subclass(data: list[RayNodeData]) -> PositiveScaleClass:
    if all(d.gate_count == 2 for d in data):
        return "POSITIVE_SCALE_ANNULAR_RAY"
    centers = len({(round(d.center[0], 1), round(d.center[1], 1)) for d in data})
    if centers <= 3:
        return "POSITIVE_SCALE_FINITE_CENTER_RAY"
    if any(not True for d in data):
        return "POSITIVE_SCALE_NON_JORDAN_RAY"
    return "POSITIVE_SCALE_NONANNULAR_RAY"


def audit_ray_geometry(tree: CanonicalIntrusionTree) -> RayGeometryAudit | None:
    ray = extract_ray(tree)
    if not ray:
        return None
    radii = [d.diameter for d in ray.data]
    limsup = max(radii) if radii else 0.0
    ratios = [radii[i + 1] / max(radii[i], 1e-9) for i in range(len(radii) - 1)] if len(radii) > 1 else []
    stable = len(ratios) >= 3 and all(0.5 <= r <= 0.9 for r in ratios[-3:])
    lam = (min(ratios), max(ratios)) if ratios else None
    return RayGeometryAudit(
        ray=ray,
        limsup_r=limsup,
        ratios_stable=stable,
        lambda_bounds=lam,
        messages=[f"scale={ray.scale_class}, limsup_r={limsup:.4f}"],
    )
