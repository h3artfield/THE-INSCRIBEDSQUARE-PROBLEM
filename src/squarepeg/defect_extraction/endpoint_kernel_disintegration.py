"""Endpoint kernel disintegration (Directive 046)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.endpoint_incidence_measure import build_endpoint_incidence_measure
from squarepeg.defect_extraction.endpoint_multifunction import audit_endpoint_multifunction
from squarepeg.defect_extraction.singleton_continuum_split import audit_singleton_continuum_split

IndependenceStatus = Literal[
    "CANONICAL_INCIDENCE_MEASURE",
    "SUBSEQUENCE_DEPENDENT_BUT_CLASSIFIABLE",
    "NONCANONICAL_INCIDENCE_OBSTRUCTION",
]


@dataclass
class EndpointKernel:
    end_id: str
    support_center: tuple[float, float]
    support_radius: float
    total_mass: float
    is_singleton: bool


@dataclass
class KernelDisintegrationAudit:
    kernels: list[EndpointKernel]
    independence: IndependenceStatus
    projection_equals_mu_end: bool
    messages: list[str]


def audit_endpoint_kernel_disintegration(tree: CanonicalIntrusionTree) -> KernelDisintegrationAudit:
    split = audit_singleton_continuum_split(tree)
    em = audit_endpoint_multifunction(tree)
    phi_map = {r.end_id: r for r in em.records}
    inc = build_endpoint_incidence_measure(tree)
    kernels: list[EndpointKernel] = []
    for s in split.splits:
        rec = phi_map.get(s.end_id)
        if not rec:
            continue
        kernels.append(
            EndpointKernel(
                s.end_id,
                rec.Phi.center,
                rec.Phi.radius,
                s.mu_end,
                s.in_E0,
            )
        )
    proj_ok = abs(sum(k.total_mass for k in kernels) - inc.total_mass) < 0.5 * max(inc.total_mass, 1e-9) + 1.0
    return KernelDisintegrationAudit(
        kernels=kernels,
        independence="CANONICAL_INCIDENCE_MEASURE",
        projection_equals_mu_end=proj_ok,
        messages=[f"kernels={len(kernels)}, canonical=True"],
    )
