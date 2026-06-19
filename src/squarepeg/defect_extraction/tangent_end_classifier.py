"""Tangent end classifier (Directive 045)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.normalized_end_tangent import NormalizedEndTangent, normalize_bad_cylinder
from squarepeg.defect_extraction.tangent_tree_compactness import build_tangent_sequence

TangentRoute = Literal[
    "SPATIAL_CONCENTRATION",
    "FINITE_CENTER",
    "INFINITE_CENTER",
    "POINT_VALUED_ENDPOINT",
    "END_CONTINUUM",
    "PARAMETER_CONNECTED",
    "PARAMETER_DISCONNECTED",
    "JORDAN_STABLE",
    "NON_JORDAN",
    "ATOMIC_RAY",
]


@dataclass
class TangentClassification:
    routes: list[TangentRoute]
    primary: TangentRoute
    routes_t064: bool
    routes_t062: bool
    routes_t085: bool
    messages: list[str]


def classify_tangent(tangent: NormalizedEndTangent) -> TangentClassification:
    centers = [(n.hull_center[0], n.hull_center[1]) for n in tangent.nodes if n.mu_tilde > 0.01]
    uniq = len({(round(c[0], 1), round(c[1], 1)) for c in centers})
    cx = sum(c[0] for c in centers) / max(len(centers), 1)
    cy = sum(c[1] for c in centers) / max(len(centers), 1)
    ball_mass = sum(
        1 for c in centers if (c[0] - cx) ** 2 + (c[1] - cy) ** 2 <= 0.04
    ) / max(len(centers), 1)
    jordan = all(n.jordan_hull for n in tangent.nodes)
    param_widths = [n.param_interval[1] - n.param_interval[0] for n in tangent.nodes]
    param_conn = max(param_widths, default=1.0) < 0.5
    atomic = any(n.mu_tilde > 0.9 for n in tangent.nodes if n.hull_radius < 0.05)

    routes: list[TangentRoute] = []
    if ball_mass >= 0.6:
        routes.append("SPATIAL_CONCENTRATION")
    if uniq <= 4:
        routes.append("FINITE_CENTER")
    elif uniq > 8:
        routes.append("INFINITE_CENTER")
    if uniq == 1 and ball_mass >= 0.5:
        routes.append("POINT_VALUED_ENDPOINT")
    elif not jordan:
        routes.append("NON_JORDAN")
    else:
        routes.append("JORDAN_STABLE")
    if param_conn:
        routes.append("PARAMETER_CONNECTED")
    else:
        routes.append("PARAMETER_DISCONNECTED")
    if atomic:
        routes.append("ATOMIC_RAY")

    primary = routes[0] if routes else "END_CONTINUUM"
    if "SPATIAL_CONCENTRATION" in routes:
        primary = "SPATIAL_CONCENTRATION"
    elif "FINITE_CENTER" in routes:
        primary = "FINITE_CENTER"
    elif "INFINITE_CENTER" in routes:
        primary = "INFINITE_CENTER"

    return TangentClassification(
        routes=routes,
        primary=primary,
        routes_t064=primary == "SPATIAL_CONCENTRATION",
        routes_t062=primary == "FINITE_CENTER",
        routes_t085=primary == "ATOMIC_RAY" or "ATOMIC_RAY" in routes,
        messages=[f"primary={primary}, routes={routes}"],
    )


def audit_tangent_end_classifier(
    tree: CanonicalIntrusionTree,
    *,
    A: float = 4.0,
) -> TangentClassification:
    seq = build_tangent_sequence(tree, A=A)
    if not seq.tangents:
        return TangentClassification([], "END_CONTINUUM", False, False, False, ["no tangent"])
    return classify_tangent(seq.tangents[0])
