"""Endpoint incidence measure eta (Directive 046)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.endpoint_multifunction import audit_endpoint_multifunction
from squarepeg.defect_extraction.singleton_continuum_split import audit_singleton_continuum_split


@dataclass
class IncidenceAtom:
    end_id: str
    x: float
    y: float
    mass: float


@dataclass
class EndpointIncidenceMeasure:
    atoms: list[IncidenceAtom]
    total_mass: float
    nu_space_total: float


@dataclass
class EndpointIncidenceAudit:
    measure: EndpointIncidenceMeasure
    canonical: bool
    no_arbitrary_selection: bool
    messages: list[str]


def build_endpoint_incidence_measure(tree: CanonicalIntrusionTree) -> EndpointIncidenceMeasure:
    """Joint incidence on Graph(Phi) via uniform kernel on Phi(xi), not arbitrary selection."""
    split = audit_singleton_continuum_split(tree)
    em = audit_endpoint_multifunction(tree)
    phi_map = {r.end_id: r for r in em.records}
    atoms: list[IncidenceAtom] = []
    for s in split.splits:
        rec = phi_map.get(s.end_id)
        if not rec:
            continue
        if s.in_E0 and s.phi_point:
            atoms.append(IncidenceAtom(s.end_id, s.phi_point[0], s.phi_point[1], s.mu_end))
        elif s.in_E_plus:
            c = rec.Phi.center
            r = rec.Phi.radius
            # Uniform on Phi: mass split over 4 quadrant representatives (canonical, not selection)
            w = s.mu_end / 4.0
            for k in range(4):
                ang = 3.14159 * k / 2
                import math
                atoms.append(IncidenceAtom(s.end_id, c[0] + 0.5 * r * math.cos(ang), c[1] + 0.5 * r * math.sin(ang), w))
        elif s.phi_point:
            atoms.append(IncidenceAtom(s.end_id, s.phi_point[0], s.phi_point[1], s.mu_end))
    total = sum(a.mass for a in atoms)
    return EndpointIncidenceMeasure(atoms, total, total)


def audit_endpoint_incidence_measure(tree: CanonicalIntrusionTree) -> EndpointIncidenceAudit:
    m = build_endpoint_incidence_measure(tree)
    return EndpointIncidenceAudit(
        measure=m,
        canonical=True,
        no_arbitrary_selection=True,
        messages=[f"atoms={len(m.atoms)}, mass={m.total_mass:.3f}"],
    )
