"""Dual certificates for positive midpoint lower bounds (when found)."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction


@dataclass
class DualCertificate:
    kappa: Fraction
    lower_bound: Fraction
    description: str
    multipliers: dict[str, Fraction] | None = None


def no_positive_bound_certificate(kappa: Fraction) -> DualCertificate:
    """Placeholder when infimum is 0 — continuum countermodel supersedes dual bound."""
    return DualCertificate(
        kappa=kappa,
        lower_bound=Fraction(0),
        description="Level-F infimum is 0; see continuum countermodel in functional_countermodels.md",
    )
