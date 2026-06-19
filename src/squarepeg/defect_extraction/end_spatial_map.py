"""Spatial and parameter endpoint maps (Directive 044)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.intrusion_tree_boundary import TreeEndClass, build_tree_boundary

SpatialEndClass = Literal[
    "END_POINT_SINGLETON",
    "END_CONTINUUM",
    "END_HULLS_NOT_NESTED",
    "END_HULL_NONCOMPACT",
    "NON_JORDAN_END_DEGENERATION",
]

ParameterEndClass = Literal[
    "PARAMETER_POINT",
    "PARAMETER_INTERVAL",
    "PARAMETER_CANTOR",
    "PARAMETER_DISCONNECTED",
    "PARAMETER_INCOMPATIBLE",
]


@dataclass
class EndSpatialMapRecord:
    end_id: str
    spatial_class: SpatialEndClass
    point: tuple[float, float] | None
    hull_diameters: list[float]


@dataclass
class EndSpatialMapAudit:
    records: list[EndSpatialMapRecord]
    point_valued_ae: bool
    noninjective: bool
    messages: list[str]


@dataclass
class EndParameterMapRecord:
    end_id: str
    param_class: ParameterEndClass
    param_support: tuple[float, float] | None


@dataclass
class EndParameterMapAudit:
    records: list[EndParameterMapRecord]
    disconnected: bool
    messages: list[str]


def _spatial_point_from_ray(tree: CanonicalIntrusionTree, end: TreeEndClass) -> tuple[float, float] | None:
    if not end.ray_prefix:
        return end.spatial_center
    centers = [tree.nodes[n].center for n in end.ray_prefix if n in tree.nodes]
    if not centers:
        return end.spatial_center
    cx = sum(c[0] for c in centers) / len(centers)
    cy = sum(c[1] for c in centers) / len(centers)
    spread = max((c[0] - cx) ** 2 + (c[1] - cy) ** 2 for c in centers) ** 0.5
    if spread < 0.08:
        return (cx, cy)
    return None


def audit_end_spatial_map(tree: CanonicalIntrusionTree) -> EndSpatialMapAudit:
    ends = build_tree_boundary(tree)
    records: list[EndSpatialMapRecord] = []
    for end in ends:
        diameters = [tree.nodes[n].diameter for n in end.ray_prefix if n in tree.nodes]
        jordan_ok = all(tree.nodes[n].jordan_hull for n in end.ray_prefix if n in tree.nodes)
        pt = _spatial_point_from_ray(tree, end)
        sc: SpatialEndClass = "END_POINT_SINGLETON"
        if not jordan_ok:
            sc = "NON_JORDAN_END_DEGENERATION"
        elif pt is None:
            sc = "END_CONTINUUM" if len(set(diameters)) > 2 else "END_HULLS_NOT_NESTED"
        elif diameters and diameters[-1] > 0.2 * diameters[0]:
            sc = "END_HULL_NONCOMPACT"
        records.append(EndSpatialMapRecord(end.end_id, sc, pt, diameters))

    singletons = sum(1 for r in records if r.spatial_class == "END_POINT_SINGLETON")
    point_ae = singletons >= 0.85 * len(records) if records else True
    pts = [r.point for r in records if r.point]
    noninj = len(pts) != len({(round(p[0], 2), round(p[1], 2)) for p in pts}) if pts else False

    return EndSpatialMapAudit(
        records=records,
        point_valued_ae=point_ae,
        noninjective=noninj,
        messages=[f"point_ae={point_ae}, records={len(records)}"],
    )


def audit_end_parameter_map(tree: CanonicalIntrusionTree) -> EndParameterMapAudit:
    ends = build_tree_boundary(tree)
    records: list[EndParameterMapRecord] = []
    for end in ends:
        intervals = [tree.nodes[n].param_interval for n in end.ray_prefix if n in tree.nodes]
        if not intervals:
            records.append(EndParameterMapRecord(end.end_id, "PARAMETER_INCOMPATIBLE", None))
            continue
        lo = min(i[0] for i in intervals)
        hi = max(i[1] for i in intervals)
        width = hi - lo
        pc: ParameterEndClass = "PARAMETER_POINT" if width < 0.05 else (
            "PARAMETER_INTERVAL" if width < 0.3 else "PARAMETER_CANTOR"
        )
        records.append(EndParameterMapRecord(end.end_id, pc, (lo, hi)))

    disconnected = any(r.param_class == "PARAMETER_DISCONNECTED" for r in records)
    return EndParameterMapAudit(
        records=records,
        disconnected=disconnected,
        messages=[f"records={len(records)}"],
    )
