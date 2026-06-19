"""Incidence concentration without point endpoints (Directive 046)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.endpoint_incidence_measure import build_endpoint_incidence_measure

IncidenceConcentrationClass = Literal[
    "CONCENTRATED",
    "FINITE_CENTER",
    "DIFFUSE",
    "CONTINUUM_SUPPORTED",
    "INFINITE_CENTER",
]


@dataclass
class IncidenceConcentrationAudit:
    C_eta: list[tuple[float, float]]
    concentration_class: IncidenceConcentrationClass
    routes_t064: bool
    routes_t062: bool
    messages: list[str]


def concentration_function_eta(
    tree: CanonicalIntrusionTree,
    *,
    radii: list[float] | None = None,
) -> list[tuple[float, float]]:
    m = build_endpoint_incidence_measure(tree)
    total = m.total_mass or 1.0
    pts = [(a.x, a.y, a.mass / total) for a in m.atoms]
    radii = radii or [0.05, 0.1, 0.15, 0.2]
    out: list[tuple[float, float]] = []
    for rho in radii:
        best = 0.0
        for px, py in {(p[0], p[1]) for p in pts}:
            mass = sum(w for x, y, w in pts if (x - px) ** 2 + (y - py) ** 2 <= rho * rho)
            best = max(best, mass)
        out.append((rho, best))
    return out


def audit_incidence_concentration(tree: CanonicalIntrusionTree) -> IncidenceConcentrationAudit:
    C = concentration_function_eta(tree)
    centers = len({(round(a.x, 1), round(a.y, 1)) for a in build_endpoint_incidence_measure(tree).atoms})
    cc: IncidenceConcentrationClass = "DIFFUSE"
    if C and C[-1][1] >= 0.55:
        cc = "CONCENTRATED"
    elif centers <= 4:
        cc = "FINITE_CENTER"
    elif centers > 10:
        cc = "INFINITE_CENTER"
    return IncidenceConcentrationAudit(
        C_eta=C,
        concentration_class=cc,
        routes_t064=cc == "CONCENTRATED",
        routes_t062=cc == "FINITE_CENTER",
        messages=[f"class={cc}, centers={centers}"],
    )
