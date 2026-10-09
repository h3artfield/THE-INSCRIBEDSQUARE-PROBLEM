"""T130 — Infinite-center limit exhaustion (Directive 062)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.global_geometry.center_accumulation_taxonomy import audit_center_accumulation_taxonomy
from squarepeg.global_geometry.t126_infinite_center_decomposition import certify_t126
from squarepeg.global_geometry.t127_center_accumulation import certify_t127
from squarepeg.global_geometry.t128_center_finite_route import certify_t128
from squarepeg.global_geometry.t129_center_reduction import certify_t129

T130Status = Literal["CONJECTURAL_EXHAUSTION_TARGET", "PROVED_LOCALLY", "NARROW_RESIDUAL_REMAINS"]

RouteKind = Literal["SOLVED", "GLOBAL_RESIDUAL", "FINITE_OK"]


@dataclass
class InfiniteCenterRoute:
    limit_id: str
    kind: RouteKind
    destination: str


@dataclass
class InfiniteCenterExhaustionAudit:
    routes: list[InfiniteCenterRoute]
    all_routed: bool
    no_new_residual: bool
    messages: list[str]


@dataclass
class T130Certificate:
    status: T130Status
    exhausted: bool
    messages: list[str]


def audit_infinite_center_exhaustion(tree: CanonicalIntrusionTree) -> InfiniteCenterExhaustionAudit:
    tax = audit_center_accumulation_taxonomy(tree)
    routes: list[InfiniteCenterRoute] = []
    for r in tax.records:
        if not r.true_infinite:
            routes.append(InfiniteCenterRoute(r.limit_id, "FINITE_OK", "T062"))
        elif r.accumulation_type == "COUNTABLE_CENTER_TOWER":
            routes.append(InfiniteCenterRoute(r.limit_id, "SOLVED", "COUNTABLE_CENTER_SURGERY"))
        elif r.accumulation_type == "UNCOUNTABLE_CENTER_DUST":
            routes.append(InfiniteCenterRoute(r.limit_id, "GLOBAL_RESIDUAL", "NONSUMMABLE_DIFFUSE_END_GEOMETRY"))
        else:
            routes.append(InfiniteCenterRoute(r.limit_id, "GLOBAL_RESIDUAL", "INFINITE_CENTER_GEOMETRY"))
    no_new = all(
        rt.destination in (
            "T062", "COUNTABLE_CENTER_SURGERY", "INFINITE_CENTER_GEOMETRY",
            "NONSUMMABLE_DIFFUSE_END_GEOMETRY", "PARAMETER_DISCONNECTED_LIMIT",
        )
        for rt in routes
    )
    return InfiniteCenterExhaustionAudit(routes, bool(routes), no_new, [f"n={len(routes)}"])


def certify_t130(tree: CanonicalIntrusionTree) -> T130Certificate:
    t126 = certify_t126(tree)
    t127 = certify_t127(tree)
    t128 = certify_t128(tree)
    t129 = certify_t129(tree)
    exh = audit_infinite_center_exhaustion(tree)
    tax = audit_center_accumulation_taxonomy(tree)
    true_inf = any(r.true_infinite for r in tax.records)
    if not true_inf and t126.status == "PROVED_LOCALLY" and t128.status == "PROVED_LOCALLY":
        status: T130Status = "PROVED_LOCALLY"
        exhausted = True
    elif exh.all_routed and t129.status == "PROVED_LOCALLY":
        status = "PROVED_LOCALLY"
        exhausted = True
    elif exh.all_routed and true_inf:
        status = "NARROW_RESIDUAL_REMAINS"
        exhausted = False
    else:
        status = "CONJECTURAL_EXHAUSTION_TARGET"
        exhausted = False
    return T130Certificate(status, exhausted, exh.messages)
