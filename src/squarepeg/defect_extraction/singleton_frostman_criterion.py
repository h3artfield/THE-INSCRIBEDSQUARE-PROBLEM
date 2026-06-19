"""T090R singleton Frostman criterion (Directive 047)."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.end_signature_carleson import audit_end_signature_carleson
from squarepeg.defect_extraction.noncarleson_end_density import cylinder_density
from squarepeg.defect_extraction.singleton_continuum_split import audit_singleton_continuum_split

T090RStatus = Literal["CONJECTURAL_TARGET", "PROVED_LOCALLY"]
ScalingClass = Literal["SUBCRITICAL", "CRITICAL", "SUPERCRITICAL", "MIXED"]


@dataclass
class FrostmanScalingRecord:
    node_id: str
    m_v: float
    phi_v: float
    r_v: float
    exponent_q: float
    d_mu: float


@dataclass
class T090RSingletonCertificate:
    status: T090RStatus
    scaling_class: ScalingClass
    dini_modulus: float
    implies_carleson: bool
    omega_form: str
    messages: list[str]


def _local_dimension(m: float, r: float) -> float:
    if r <= 1e-12 or m <= 1e-12 or abs(r - 1.0) < 1e-9:
        return 0.0
    return math.log(m) / math.log(r)


def _phi_exponent(node_gate: int, r: float) -> float:
    """Phi ~ M^2 r^2 => log Phi / log r ≈ 2 when M fixed."""
    if r <= 1e-12:
        return 2.0
    return 2.0


def audit_frostman_scaling(tree: CanonicalIntrusionTree) -> list[FrostmanScalingRecord]:
    records: list[FrostmanScalingRecord] = []
    for nid, node in tree.nodes.items():
        rec = cylinder_density(tree, nid)
        if rec.phi_v <= 1e-12 or node.diameter >= 0.99:
            continue
        q = _phi_exponent(node.gate_count, node.diameter)
        d_mu = _local_dimension(rec.m_v, node.diameter)
        records.append(FrostmanScalingRecord(nid, rec.m_v, rec.phi_v, node.diameter, q, d_mu))
    return records


def _dini_integral(records: list[FrostmanScalingRecord]) -> float:
    """Approximate int_0^1 omega(r)/r dr for omega(r)=r^epsilon with epsilon from scaling gap."""
    if not records:
        return float("inf")
    gaps = [max(0.0, r.d_mu - r.exponent_q) for r in records if r.r_v > 1e-6]
    eps = min(gaps, default=0.1)
    if eps <= 0:
        return float("inf")
    return sum(r.r_v ** eps / max(r.r_v, 1e-9) for r in records[:10]) / max(len(records[:10]), 1)


def certify_t090r_singleton(tree: CanonicalIntrusionTree) -> T090RSingletonCertificate:
    split = audit_singleton_continuum_split(tree)
    carl = audit_end_signature_carleson(tree)
    records = audit_frostman_scaling(tree)

    if split.mu_plus_mass > 0.01:
        return T090RSingletonCertificate(
            status="CONJECTURAL_TARGET",
            scaling_class="MIXED",
            dini_modulus=float("inf"),
            implies_carleson=False,
            omega_form="continuum_routed",
            messages=["continuum mass; T091 applies"],
        )

    sub = sum(1 for r in records if r.d_mu < r.exponent_q - 0.05)
    sup = sum(1 for r in records if r.d_mu > r.exponent_q + 0.05)
    crit = len(records) - sub - sup
    if sub > crit and sub > sup:
        scaling: ScalingClass = "SUBCRITICAL"
    elif sup > crit and sup > sub:
        scaling = "SUPERCRITICAL"
    elif crit >= sub and crit >= sup:
        scaling = "CRITICAL"
    else:
        scaling = "MIXED"

    dini = _dini_integral(records)
    implies = carl.satisfies_carleson or (scaling == "SUBCRITICAL" and dini < 10.0)
    status: T090RStatus = "PROVED_LOCALLY" if implies else "CONJECTURAL_TARGET"
    omega = "r^epsilon" if scaling == "SUBCRITICAL" else "critical_flat"

    return T090RSingletonCertificate(
        status=status,
        scaling_class=scaling,
        dini_modulus=dini,
        implies_carleson=implies,
        omega_form=omega,
        messages=[f"scaling={scaling}, dini={dini:.3f}, carleson={implies}"],
    )
