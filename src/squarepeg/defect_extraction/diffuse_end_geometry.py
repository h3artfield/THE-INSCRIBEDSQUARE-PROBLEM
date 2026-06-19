"""T086 — Diffuse end structural alternative (Directive 043)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.cantor_end_residual import audit_cantor_end_residual
from squarepeg.defect_extraction.child_signature_concentration import audit_child_signature_concentration
from squarepeg.defect_extraction.diffuse_end_classifier import classify_diffuse_ends
from squarepeg.defect_extraction.infinite_ray_surgery import certify_t080
from squarepeg.defect_extraction.tree_end_signature_measure import audit_tree_end_signature_measure

T086Status = Literal["CONJECTURAL_STRUCTURAL_TARGET", "PROVED_LOCALLY_CLASSIFIER"]

T086Route = Literal[
    "SPATIAL_CONCENTRATION",
    "FINITE_CENTER_DECOMPOSITION",
    "INFINITE_CENTER_PROLIFERATION",
    "PARAMETER_DISCONNECTED",
    "NON_JORDAN_SATURATION",
    "CANTOR_END_RESIDUAL",
    "ATOMIC_SUMMABLE",
    "NOT_DIFFUSE",
]


@dataclass
class T086Certificate:
    status: T086Status
    route: T086Route
    nonatomic: bool
    messages: list[str]


def certify_t086(tree: CanonicalIntrusionTree) -> T086Certificate:
    """A nonatomic defect-carrying end measure forces a structural alternative."""
    ends = classify_diffuse_ends(tree)
    em = audit_tree_end_signature_measure(tree)
    centers = audit_child_signature_concentration(tree)
    cantor = audit_cantor_end_residual(tree)
    t080 = certify_t080(tree)

    if ends.end_atom_class == "FINITE_ATOMIC" and t080.status == "PROVED_LOCALLY":
        return T086Certificate(
            status="PROVED_LOCALLY_CLASSIFIER",
            route="ATOMIC_SUMMABLE",
            nonatomic=False,
            messages=["finite atomic summable end"],
        )

    if ends.end_atom_class != "NONATOMIC_DIFFUSE" and not ends.diffuse_end_tree:
        return T086Certificate(
            status="PROVED_LOCALLY_CLASSIFIER",
            route="NOT_DIFFUSE",
            nonatomic=False,
            messages=["not a diffuse end tree"],
        )

    nonatomic = ends.end_atom_class == "NONATOMIC_DIFFUSE" or ends.diffuse_end_tree
    route: T086Route = "CANTOR_END_RESIDUAL"
    status: T086Status = "CONJECTURAL_STRUCTURAL_TARGET"

    if em.spatial_class == "SINGLE_POINT_END_CONCENTRATION":
        route = "SPATIAL_CONCENTRATION"
        status = "PROVED_LOCALLY_CLASSIFIER"
    elif em.spatial_class == "FINITE_CENTER_END_MEASURE" or centers.routes_t062:
        route = "FINITE_CENTER_DECOMPOSITION"
        status = "PROVED_LOCALLY_CLASSIFIER"
    elif centers.diffuse_child_center or em.spatial_class == "DIFFUSE_SPATIAL_END_MEASURE":
        route = "INFINITE_CENTER_PROLIFERATION"
    elif centers.hull_degenerate:
        route = "NON_JORDAN_SATURATION"
        status = "PROVED_LOCALLY_CLASSIFIER"
    elif cantor.is_cantor_residual:
        route = "CANTOR_END_RESIDUAL"
    elif em.spatial_class == "CANTOR_END_MEASURE":
        route = "CANTOR_END_RESIDUAL"

    return T086Certificate(
        status=status,
        route=route,
        nonatomic=nonatomic,
        messages=[f"route={route}, nonatomic={nonatomic}"],
    )
