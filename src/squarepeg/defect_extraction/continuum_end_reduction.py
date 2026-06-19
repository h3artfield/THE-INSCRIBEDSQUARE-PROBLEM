"""T091 — Continuum-end positive-scale reduction (Directive 046)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.endpoint_multifunction import audit_endpoint_multifunction
from squarepeg.defect_extraction.intrusion_ray_geometry import audit_ray_geometry
from squarepeg.defect_extraction.singleton_continuum_split import audit_singleton_continuum_split

T091Status = Literal["CONJECTURAL_TARGET", "PROVED_LOCALLY_CLASSIFIER"]

T091Route = Literal[
    "POSITIVE_SCALE_END_RAY",
    "PLATEAU_END_RAY",
    "POSITIVE_SCALE_NONANNULAR_CLUSTER",
    "NON_JORDAN_END_DEGENERATION",
    "INCOMPATIBLE_NESTED_HULLS",
    "NO_CONTINUUM_MASS",
]


@dataclass
class T091Certificate:
    status: T091Status
    route: T091Route
    mu_plus_positive: bool
    messages: list[str]


def certify_t091(tree: CanonicalIntrusionTree) -> T091Certificate:
    """Positive-diameter ends cannot be shrinking; route to positive-scale geometry."""
    split = audit_singleton_continuum_split(tree)
    em = audit_endpoint_multifunction(tree)
    geom = audit_ray_geometry(tree)

    if split.mu_plus_mass <= 1e-6 * (split.mu_0_mass + split.mu_plus_mass + 1e-9):
        return T091Certificate(
            status="PROVED_LOCALLY_CLASSIFIER",
            route="NO_CONTINUUM_MASS",
            mu_plus_positive=False,
            messages=["no positive-diameter mass"],
        )

    route: T091Route = "POSITIVE_SCALE_END_RAY"
    status: T091Status = "PROVED_LOCALLY_CLASSIFIER"

    not_nested = sum(1 for r in em.records if r.nesting == "END_HULLS_NOT_NESTED")
    if not_nested > 0.3 * len(em.records):
        route = "INCOMPATIBLE_NESTED_HULLS"
    elif geom and geom.ray.scale_class == "PLATEAU_JUMP_RAY":
        route = "PLATEAU_END_RAY"
    elif geom and geom.ray.positive_subclass == "POSITIVE_SCALE_NONANNULAR_RAY":
        route = "POSITIVE_SCALE_NONANNULAR_CLUSTER"
    elif any(r.diameter_class == "NONCONNECTED_ENDPOINT_SET" for r in em.records):
        route = "NON_JORDAN_END_DEGENERATION"
    elif geom and geom.ray.scale_class == "POSITIVE_SCALE_RAY":
        route = "POSITIVE_SCALE_END_RAY"

    return T091Certificate(
        status=status,
        route=route,
        mu_plus_positive=True,
        messages=[f"route={route}, mu+={split.mu_plus_mass:.3f}"],
    )
