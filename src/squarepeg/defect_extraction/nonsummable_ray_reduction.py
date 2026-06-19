"""T085 — Nonsummable ray reduction (Directive 043)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.child_signature_concentration import audit_child_signature_concentration
from squarepeg.defect_extraction.intrusion_ray_geometry import audit_ray_geometry
from squarepeg.defect_extraction.nonsummable_ray_measure import audit_nonsummable_ray_measure
from squarepeg.defect_extraction.summable_ray_signature import audit_summable_ray_signature

T085Status = Literal["CONJECTURAL_STRUCTURAL_TARGET", "PROVED_LOCALLY_CLASSIFIER"]

T085Route = Literal[
    "CONCENTRATED_DESCENT",
    "FINITE_CENTER_DECOMPOSITION",
    "INFINITE_CENTER_GEOMETRY",
    "ANNULAR_BAND_GEOMETRY",
    "NON_JORDAN_DEGENERATION",
    "DIFFUSE_RAY_RESIDUAL",
    "SUMMABLE_RAY",
]


@dataclass
class T085Certificate:
    status: T085Status
    route: T085Route
    nonsummable: bool
    messages: list[str]


def _ray_center_concentrated(tree: CanonicalIntrusionTree, ray) -> bool:
    centers = [tree.nodes[nid].center for nid in ray.node_ids if nid in tree.nodes]
    if not centers:
        return False
    cx = sum(c[0] for c in centers) / len(centers)
    cy = sum(c[1] for c in centers) / len(centers)
    ball_mass = sum(
        1 for c in centers if (c[0] - cx) ** 2 + (c[1] - cy) ** 2 <= 0.04
    ) / len(centers)
    return ball_mass >= 0.85


def certify_t085(tree: CanonicalIntrusionTree) -> T085Certificate:
    """Every nonsummable shrinking intrusion ray reduces structurally."""
    sig = audit_summable_ray_signature(tree)
    ray_audit = audit_nonsummable_ray_measure(tree)
    geom = audit_ray_geometry(tree)
    centers = audit_child_signature_concentration(tree)

    # Non-Jordan terminal hull overrides summable signature
    if ray_audit.measure and any(not tree.nodes[nid].jordan_hull for nid in ray_audit.measure.ray.node_ids):
        return T085Certificate(
            status="PROVED_LOCALLY_CLASSIFIER",
            route="NON_JORDAN_DEGENERATION",
            nonsummable=True,
            messages=["non-Jordan hull on ray node"],
        )

    if geom and geom.ray.scale_class == "PLATEAU_JUMP_RAY":
        return T085Certificate(
            status="PROVED_LOCALLY_CLASSIFIER",
            route="ANNULAR_BAND_GEOMETRY",
            nonsummable=True,
            messages=["plateau jump ray"],
        )

    if ray_audit.measure and _ray_center_concentrated(tree, ray_audit.measure.ray):
        return T085Certificate(
            status="PROVED_LOCALLY_CLASSIFIER",
            route="CONCENTRATED_DESCENT",
            nonsummable=not ray_audit.measure.summable,
            messages=["ray center concentration"],
        )

    if sig is not None and sig.satisfies_summable and (ray_audit.measure is None or ray_audit.measure.summable):
        return T085Certificate(
            status="PROVED_LOCALLY_CLASSIFIER",
            route="SUMMABLE_RAY",
            nonsummable=False,
            messages=["summable ray signature"],
        )

    nonsummable = ray_audit.measure is not None and not ray_audit.measure.summable
    route: T085Route = "DIFFUSE_RAY_RESIDUAL"
    status: T085Status = "CONJECTURAL_STRUCTURAL_TARGET"

    if not nonsummable:
        return T085Certificate(
            status="PROVED_LOCALLY_CLASSIFIER",
            route="SUMMABLE_RAY",
            nonsummable=False,
            messages=["no nonsummable ray detected"],
        )

    if centers.routes_t064:
        route = "CONCENTRATED_DESCENT"
        status = "PROVED_LOCALLY_CLASSIFIER"
    elif centers.routes_t062:
        route = "FINITE_CENTER_DECOMPOSITION"
        status = "PROVED_LOCALLY_CLASSIFIER"
    elif geom and geom.ray.scale_class == "PLATEAU_JUMP_RAY":
        route = "ANNULAR_BAND_GEOMETRY"
        status = "PROVED_LOCALLY_CLASSIFIER"
    elif geom and geom.ray.positive_subclass == "POSITIVE_SCALE_NONANNULAR_RAY":
        route = "ANNULAR_BAND_GEOMETRY"
    elif centers.hull_degenerate:
        route = "NON_JORDAN_DEGENERATION"
        status = "PROVED_LOCALLY_CLASSIFIER"
    elif centers.diffuse_child_center or (
        ray_audit.measure and ray_audit.measure.plateau_run
    ):
        route = "INFINITE_CENTER_GEOMETRY"
    elif ray_audit.measure and ray_audit.measure.intrinsic_tail > 0.08:
        route = "DIFFUSE_RAY_RESIDUAL"

    return T085Certificate(
        status=status,
        route=route,
        nonsummable=nonsummable,
        messages=[f"route={route}, nonsummable={nonsummable}"],
    )
