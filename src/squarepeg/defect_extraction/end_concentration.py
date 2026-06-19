"""End spatial concentration–compactness (Directive 044)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.end_signature_measure import build_end_signature_measure_v2
from squarepeg.defect_extraction.end_spatial_map import audit_end_spatial_map

EndConcentrationClass = Literal[
    "CONCENTRATED",
    "FINITE_CENTER",
    "DIFFUSE",
]

ConcentratedEndOutcome = Literal[
    "DESCENDANT_CLUSTER",
    "FINITE_PARAMETER_BLOCKS",
    "DISCONNECTED_CONCENTRATION",
    "NONSUMMABLE_RAY",
    "NON_JORDAN_CONTINUUM",
    "NONE",
]


@dataclass
class EndConcentrationAudit:
    concentration_class: EndConcentrationClass
    C_rho: list[tuple[float, float]]
    center_count: int
    routes_t064: bool
    routes_t062: bool
    diffuse_end: bool
    concentrated_outcome: ConcentratedEndOutcome
    messages: list[str]


def concentration_function(
    tree: CanonicalIntrusionTree,
    *,
    radii: list[float] | None = None,
) -> list[tuple[float, float]]:
    """C(rho) = sup_x nu_space(B(x,rho))."""
    spatial = audit_end_spatial_map(tree)
    em = build_end_signature_measure_v2(tree)
    total = em.total_unsigned or 1.0
    pts = [(r.point, 1.0 / len(spatial.records)) for r in spatial.records if r.point]
    radii = radii or [0.05, 0.1, 0.15, 0.2]
    out: list[tuple[float, float]] = []
    for rho in radii:
        best = 0.0
        for px, py in {p for p, _ in pts}:
            mass = sum(w for (p, w) in pts if p and (p[0] - px) ** 2 + (p[1] - py) ** 2 <= rho * rho)
            best = max(best, mass)
        out.append((rho, best))
    return out


def audit_end_concentration(tree: CanonicalIntrusionTree) -> EndConcentrationAudit:
    C = concentration_function(tree)
    spatial = audit_end_spatial_map(tree)
    pts = [r.point for r in spatial.records if r.point]
    centers = len({(round(p[0], 1), round(p[1], 1)) for p in pts})

    cc: EndConcentrationClass = "DIFFUSE"
    if C and C[-1][1] >= 0.55:
        cc = "CONCENTRATED"
    elif centers <= 4:
        cc = "FINITE_CENTER"

    outcome: ConcentratedEndOutcome = "NONE"
    if cc == "CONCENTRATED":
        outcome = "DESCENDANT_CLUSTER"
    elif spatial.records and any(r.spatial_class == "NON_JORDAN_END_DEGENERATION" for r in spatial.records):
        outcome = "NON_JORDAN_CONTINUUM"

    return EndConcentrationAudit(
        concentration_class=cc,
        C_rho=C,
        center_count=centers,
        routes_t064=cc == "CONCENTRATED",
        routes_t062=cc == "FINITE_CENTER",
        diffuse_end=cc == "DIFFUSE",
        concentrated_outcome=outcome,
        messages=[f"class={cc}, centers={centers}"],
    )
