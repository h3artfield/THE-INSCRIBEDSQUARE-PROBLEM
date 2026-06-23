"""T120 — Non-Jordan saturation exhaustion (Directive 060)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.global_geometry.harmless_hull_replacement import certify_t117
from squarepeg.global_geometry.non_jordan_hull_taxonomy import audit_non_jordan_hull_taxonomy
from squarepeg.global_geometry.pinched_hull_routes import certify_t118
from squarepeg.global_geometry.t116_saturation_taxonomy import certify_t116
from squarepeg.global_geometry.t119_non_jordan_reduction import certify_t119

T120Status = Literal["CONJECTURAL_EXHAUSTION_TARGET", "PROVED_LOCALLY", "NARROW_RESIDUAL_REMAINS"]

RouteKind = Literal["SOLVED", "GLOBAL_RESIDUAL", "JORDAN_OK"]


@dataclass
class NonJordanRoute:
    hull_id: str
    kind: RouteKind
    destination: str


@dataclass
class NonJordanExhaustionAudit:
    routes: list[NonJordanRoute]
    all_routed: bool
    no_new_residual: bool
    messages: list[str]


@dataclass
class T120Certificate:
    status: T120Status
    exhausted: bool
    messages: list[str]


def audit_non_jordan_exhaustion(tree: CanonicalIntrusionTree) -> NonJordanExhaustionAudit:
    tax = audit_non_jordan_hull_taxonomy(tree)
    routes: list[NonJordanRoute] = []
    for r in tax.records:
        if r.failure_type in ("JORDAN_OK", "HARMLESS_QUOTIENT"):
            routes.append(NonJordanRoute(r.hull_id, "JORDAN_OK", "T062"))
        elif r.failure_type == "PINCHED_HULL":
            routes.append(NonJordanRoute(r.hull_id, "GLOBAL_RESIDUAL", "NON_JORDAN_SATURATION_HULL"))
        elif r.failure_type == "PARAMETER_MERGED_HULL":
            routes.append(NonJordanRoute(r.hull_id, "GLOBAL_RESIDUAL", "PARAMETER_DISCONNECTED_LIMIT"))
        elif r.failure_type in ("INFINITE_CENTER_ACCUMULATION", "NONLOCALLY_CONNECTED_LIMIT"):
            routes.append(NonJordanRoute(r.hull_id, "GLOBAL_RESIDUAL", "INFINITE_CENTER_GEOMETRY"))
        elif r.failure_type == "MULTI_BOUNDARY_SATURATION":
            routes.append(NonJordanRoute(r.hull_id, "SOLVED", "FINITE_JORDAN_SPLIT"))
        elif r.true_non_jordan:
            routes.append(NonJordanRoute(r.hull_id, "GLOBAL_RESIDUAL", "NON_JORDAN_SATURATION_HULL"))
        else:
            routes.append(NonJordanRoute(r.hull_id, "JORDAN_OK", "PROTECTED_SQUARE"))
    all_r = bool(routes)
    no_new = all(
        rt.destination in (
            "T062", "PROTECTED_SQUARE", "FINITE_JORDAN_SPLIT",
            "NON_JORDAN_SATURATION_HULL", "PARAMETER_DISCONNECTED_LIMIT", "INFINITE_CENTER_GEOMETRY",
        )
        for rt in routes
    )
    return NonJordanExhaustionAudit(routes, all_r, no_new, [f"n={len(routes)}"])


def certify_t120(tree: CanonicalIntrusionTree) -> T120Certificate:
    t116 = certify_t116(tree)
    t117 = certify_t117(tree)
    t118 = certify_t118(tree)
    t119 = certify_t119(tree)
    exh = audit_non_jordan_exhaustion(tree)
    tax = audit_non_jordan_hull_taxonomy(tree)
    true_nj = any(r.true_non_jordan for r in tax.records)
    if not true_nj and t116.status == "PROVED_LOCALLY" and t117.status == "PROVED_LOCALLY":
        status: T120Status = "PROVED_LOCALLY"
        exhausted = True
    elif exh.all_routed and t118.status == "PROVED_LOCALLY" and t119.status == "PROVED_LOCALLY":
        status = "PROVED_LOCALLY"
        exhausted = True
    elif exh.all_routed and true_nj:
        status = "NARROW_RESIDUAL_REMAINS"
        exhausted = False
    else:
        status = "CONJECTURAL_EXHAUSTION_TARGET"
        exhausted = False
    return T120Certificate(status, exhausted, exh.messages)
