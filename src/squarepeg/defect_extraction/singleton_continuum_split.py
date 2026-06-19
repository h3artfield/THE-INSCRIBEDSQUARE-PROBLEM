"""Singleton/continuum end decomposition (Directive 046)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.endpoint_multifunction import audit_endpoint_multifunction
from squarepeg.defect_extraction.end_signature_measure import build_end_signature_measure_v2


@dataclass
class EndMassSplit:
    end_id: str
    mu_end: float
    d_phi: float
    in_E0: bool
    in_E_plus: bool
    phi_point: tuple[float, float] | None


@dataclass
class SingletonContinuumSplitAudit:
    splits: list[EndMassSplit]
    mu_0_mass: float
    mu_plus_mass: float
    phi_measurable: bool
    E0_fraction: float
    E_plus_fraction: float
    messages: list[str]


def audit_singleton_continuum_split(tree: CanonicalIntrusionTree) -> SingletonContinuumSplitAudit:
    em = audit_endpoint_multifunction(tree)
    esm = build_end_signature_measure_v2(tree)
    leaf_mass = {s.node_id: s.s_local for s in esm.cylinders if not tree.nodes[s.node_id].child_ids}
    splits: list[EndMassSplit] = []
    mu0 = 0.0
    mup = 0.0
    for rec in em.records:
        m = leaf_mass.get(rec.end_id, rec.Phi.radius)
        in_e0 = rec.d_phi <= 0.02
        in_ep = rec.d_phi > 0.02
        if in_e0:
            mu0 += m
        if in_ep:
            mup += m
        splits.append(EndMassSplit(rec.end_id, m, rec.d_phi, in_e0, in_ep, rec.singleton_point))
    total = mu0 + mup or 1.0
    return SingletonContinuumSplitAudit(
        splits=splits,
        mu_0_mass=mu0,
        mu_plus_mass=mup,
        phi_measurable=all(s.phi_point is not None or s.in_E_plus for s in splits),
        E0_fraction=mu0 / total,
        E_plus_fraction=mup / total,
        messages=[f"mu0={mu0:.3f}, mu+={mup:.3f}"],
    )
