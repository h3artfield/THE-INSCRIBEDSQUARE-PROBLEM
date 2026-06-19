"""T082 infinite intrusion-tree structural reduction (Directive 040)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.branching_tree_surgery import certify_t081
from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.defect_tree_pruning import audit_defect_pruning
from squarepeg.defect_extraction.infinite_ray_surgery import certify_t080
from squarepeg.defect_extraction.intrusion_ray_geometry import audit_ray_geometry, extract_ray
from squarepeg.defect_extraction.intrusion_tree_ends import audit_end_decomposition
from squarepeg.defect_extraction.ray_branching_dichotomy import certify_t078

T082Status = Literal["CONJECTURAL_STRUCTURAL_TARGET", "PROVED_LOCALLY_PARTIAL"]
T082Route = Literal[
    "SUMMABLE_SHRINKING_RAY_SURGERY",
    "SUMMABLE_BRANCHING_TREE_SURGERY",
    "CONCENTRATED_DESCENT",
    "FINITE_CENTER_DECOMPOSITION",
    "POSITIVE_SCALE_NONANNULAR",
    "NON_JORDAN_HULL",
    "INFINITE_CENTER_BRANCHING",
    "DIFFUSE_NONSUMMABLE_END",
]


@dataclass
class T082Certificate:
    status: T082Status
    route: T082Route
    t078_branch: str
    t080_status: str
    t081_status: str
    messages: list[str]


def certify_t082(tree: CanonicalIntrusionTree) -> T082Certificate:
    """T082: defect-carrying infinite tree structural reduction."""
    t078 = certify_t078(tree)
    t080 = certify_t080(tree)
    t081 = certify_t081(tree)
    prune = audit_defect_pruning(tree)
    ray_geom = audit_ray_geometry(tree)
    ends = audit_end_decomposition(tree)
    route: T082Route = "DIFFUSE_NONSUMMABLE_END"
    status: T082Status = "CONJECTURAL_STRUCTURAL_TARGET"
    if t080.status == "PROVED_LOCALLY":
        route = "SUMMABLE_SHRINKING_RAY_SURGERY"
        status = "PROVED_LOCALLY_PARTIAL"
    elif t081.status == "PROVED_LOCALLY":
        route = "SUMMABLE_BRANCHING_TREE_SURGERY"
        status = "PROVED_LOCALLY_PARTIAL"
    elif ray_geom and ray_geom.ray.scale_class == "POSITIVE_SCALE_RAY":
        route = "POSITIVE_SCALE_NONANNULAR"
    elif ends.end_measure.measure_class == "FINITE_CENTERS":
        route = "FINITE_CENTER_DECOMPOSITION"
        status = "PROVED_LOCALLY_PARTIAL"
    elif ends.diffuse_residual:
        route = "DIFFUSE_NONSUMMABLE_END"
    elif prune.outcome == "INFINITE_DEFECT_RAY" and t080.status == "CONJECTURAL_TARGET":
        route = "DIFFUSE_NONSUMMABLE_END"
    elif t078.branch == "INFINITE_LOCAL_BRANCHING":
        route = "INFINITE_CENTER_BRANCHING"
    return T082Certificate(
        status=status,
        route=route,
        t078_branch=t078.branch,
        t080_status=t080.status,
        t081_status=t081.status,
        messages=[f"route={route}, t080={t080.status}, t081={t081.status}"],
    )
