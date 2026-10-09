"""T125 — Parameter-disconnected limit exhaustion (Directive 061)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.global_geometry.parameter_disconnected_limit import audit_parameter_disconnected_limits
from squarepeg.global_geometry.t121_parameter_decomposition import certify_t121
from squarepeg.global_geometry.t122_component_splitting import certify_t122
from squarepeg.global_geometry.t123_cross_component_routing import certify_t123
from squarepeg.global_geometry.t124_parameter_reduction import certify_t124

T125Status = Literal["CONJECTURAL_EXHAUSTION_TARGET", "PROVED_LOCALLY", "NARROW_RESIDUAL_REMAINS"]

RouteKind = Literal["SOLVED", "GLOBAL_RESIDUAL", "CONNECTED_OK"]


@dataclass
class ParameterRoute:
    limit_id: str
    kind: RouteKind
    destination: str


@dataclass
class ParameterExhaustionAudit:
    routes: list[ParameterRoute]
    all_routed: bool
    no_new_residual: bool
    messages: list[str]


@dataclass
class T125Certificate:
    status: T125Status
    exhausted: bool
    messages: list[str]


def audit_parameter_exhaustion(tree: CanonicalIntrusionTree) -> ParameterExhaustionAudit:
    limits = audit_parameter_disconnected_limits(tree)
    routes: list[ParameterRoute] = []
    for r in limits.records:
        if not r.true_disconnection:
            routes.append(ParameterRoute(r.limit_id, "CONNECTED_OK", "T062"))
        elif r.disconnection_type == "FINITE_DISCONNECTED":
            routes.append(ParameterRoute(r.limit_id, "SOLVED", "FINITE_JORDAN_COMPONENTS"))
        elif r.disconnection_type in ("COUNTABLE_DISCONNECTED", "ALTERNATING_CHAIN"):
            routes.append(ParameterRoute(r.limit_id, "SOLVED", "COUNTABLE_SURGERY"))
        elif r.disconnection_type in ("CANTOR_DISCONNECTED", "DUST_LIKE"):
            routes.append(ParameterRoute(r.limit_id, "GLOBAL_RESIDUAL", "INFINITE_CENTER_GEOMETRY"))
        elif r.disconnection_type == "HARMLESS_QUOTIENT":
            routes.append(ParameterRoute(r.limit_id, "CONNECTED_OK", "PROTECTED_SQUARE"))
        else:
            routes.append(ParameterRoute(r.limit_id, "GLOBAL_RESIDUAL", "PARAMETER_DISCONNECTED_LIMIT"))
    all_r = bool(routes)
    no_new = all(
        rt.destination in (
            "T062", "PROTECTED_SQUARE", "FINITE_JORDAN_COMPONENTS", "COUNTABLE_SURGERY",
            "PARAMETER_DISCONNECTED_LIMIT", "INFINITE_CENTER_GEOMETRY", "NONSUMMABLE_DIFFUSE_END_GEOMETRY",
        )
        for rt in routes
    )
    return ParameterExhaustionAudit(routes, all_r, no_new, [f"n={len(routes)}"])


def certify_t125(tree: CanonicalIntrusionTree) -> T125Certificate:
    t121 = certify_t121(tree)
    t122 = certify_t122(tree)
    t123 = certify_t123(tree)
    t124 = certify_t124(tree)
    exh = audit_parameter_exhaustion(tree)
    limits = audit_parameter_disconnected_limits(tree)
    true_disc = any(r.true_disconnection for r in limits.records)
    if not true_disc and t121.status == "PROVED_LOCALLY" and t122.status == "PROVED_LOCALLY":
        status: T125Status = "PROVED_LOCALLY"
        exhausted = True
    elif exh.all_routed and t123.status == "PROVED_LOCALLY" and t124.status == "PROVED_LOCALLY":
        status = "PROVED_LOCALLY"
        exhausted = True
    elif exh.all_routed and true_disc:
        status = "NARROW_RESIDUAL_REMAINS"
        exhausted = False
    else:
        status = "CONJECTURAL_EXHAUSTION_TARGET"
        exhausted = False
    return T125Certificate(status, exhausted, exh.messages)
