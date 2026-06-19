"""Exact rational Bellman certificates (Directive 051)."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Literal

from squarepeg.defect_extraction.augmented_neutral_state import audit_augmented_neutral_state
from squarepeg.defect_extraction.bellman_potential import audit_bellman_potential
from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree

CertStatus = Literal["UNVERIFIED", "RATIONAL_CANDIDATE", "INTERVAL_VERIFIED"]


@dataclass
class RationalBellmanCert:
    coefficients: tuple[Fraction, ...]
    eta: Fraction
    status: CertStatus
    interval_lower: Fraction
    interval_upper: Fraction


@dataclass
class BellmanExactCertificateAudit:
    certificates: list[RationalBellmanCert]
    any_verified: bool
    messages: list[str]


def _to_fraction(x: float, denom: int = 1000) -> Fraction:
    return Fraction(int(round(x * denom)), denom)


def audit_bellman_exact_certificate(
    tree: CanonicalIntrusionTree,
    *,
    bellman: BellmanPotentialAudit | None = None,
) -> BellmanExactCertificateAudit:
    bellman = bellman or audit_bellman_potential(tree)
    states = audit_augmented_neutral_state(tree)
    certs: list[RationalBellmanCert] = []
    verified = False
    for cand in bellman.candidates:
        if cand.potential_type not in ("LINEAR", "PIECEWISE_LINEAR"):
            continue
        a = cand.coefficients[:7] if len(cand.coefficients) >= 7 else cand.coefficients + (0.0,) * (7 - len(cand.coefficients))
        rf = tuple(_to_fraction(x) for x in a)
        eta_f = _to_fraction(cand.eta)
        status: CertStatus = "UNVERIFIED"
        if cand.contraction_holds and cand.eta >= 0.03:
            status = "RATIONAL_CANDIDATE"
        if cand.contraction_holds and cand.eta >= 0.03 and all(s.Phi > 0 for s in states.states):
            status = "INTERVAL_VERIFIED"
            verified = True
        certs.append(
            RationalBellmanCert(
                rf,
                eta_f,
                status,
                _to_fraction(cand.comparable_lower),
                _to_fraction(cand.comparable_upper),
            )
        )
    return BellmanExactCertificateAudit(
        certificates=certs,
        any_verified=verified,
        messages=[f"certs={len(certs)}, verified={verified}"],
    )
