"""T119 — Non-Jordan to parameter/center reduction (Directive 060)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.global_geometry.hull_infinite_center_routes import audit_hull_infinite_center_routes
from squarepeg.global_geometry.hull_parameter_disconnection import audit_hull_parameter_disconnection
from squarepeg.global_geometry.multi_boundary_hull import audit_multi_boundary_hull
from squarepeg.global_geometry.non_jordan_hull_taxonomy import audit_non_jordan_hull_taxonomy
from squarepeg.global_geometry.nonlocally_connected_hull import audit_nonlocally_connected_hull

T119Status = Literal["CONJECTURAL_REDUCTION_TARGET", "PROVED_LOCALLY"]


@dataclass
class T119Certificate:
    status: T119Status
    reduced: bool
    messages: list[str]


def certify_t119(tree: CanonicalIntrusionTree) -> T119Certificate:
    tax = audit_non_jordan_hull_taxonomy(tree)
    param = audit_hull_parameter_disconnection(tree)
    center = audit_hull_infinite_center_routes(tree)
    multi = audit_multi_boundary_hull(tree)
    nlc = audit_nonlocally_connected_hull(tree)
    true_nj = any(r.true_non_jordan for r in tax.records)
    reduced = (
        multi.all_handled
        and nlc.all_routed
        and param.distinct_from_center
        and center.distinct_from_parameter
        and (not true_nj or all(r.destination != "NONE" for r in param.routes if r.disconnected))
    )
    if not true_nj:
        reduced = True
    status: T119Status = "PROVED_LOCALLY" if reduced else "CONJECTURAL_REDUCTION_TARGET"
    return T119Certificate(status, reduced, [f"true_nj={true_nj}"])
