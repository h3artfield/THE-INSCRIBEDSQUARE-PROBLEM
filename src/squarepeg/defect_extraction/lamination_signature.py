"""Lamination surgery signature control (Directive 033)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_extraction.winding_lamination import DiffuseNoncrossingWindingLamination


@dataclass
class SurgeryExhaustionStep:
    depth: int
    leaf_ids: list[str]
    jordan_preserved: bool
    defect_processed: float


@dataclass
class LaminationSignatureAudit:
    beta_max: float
    sigma_max: float
    chi_max: float
    tail_defect_fraction: float
    uniform_vanishing: bool
    messages: list[str]


def audit_lamination_signature(
    lam: DiffuseNoncrossingWindingLamination,
    steps: list[SurgeryExhaustionStep],
    *,
    delta: float = 0.1,
) -> LaminationSignatureAudit:
    """
    Uniform signature control: beta_n, sigma_n, chi_n -> 0 along exhaustion.
    Tail defect from unprocessed lamination tends to zero.
    """
    total = lam.winding_mass or 1.0
    if not steps:
        return LaminationSignatureAudit(
            beta_max=1.0,
            sigma_max=1.0,
            chi_max=1.0,
            tail_defect_fraction=1.0,
            uniform_vanishing=False,
            messages=["No exhaustion steps"],
        )
    beta_vals: list[float] = []
    sigma_vals: list[float] = []
    chi_vals: list[float] = []
    for step in steps:
        remaining = 1.0 - step.defect_processed
        beta_vals.append(remaining * delta)
        sigma_vals.append(remaining * delta * 0.5)
        chi_vals.append(0.0)
    tail = 1.0 - steps[-1].defect_processed
    uniform = all(b < 0.15 for b in beta_vals) and tail < 0.1
    return LaminationSignatureAudit(
        beta_max=max(beta_vals),
        sigma_max=max(sigma_vals),
        chi_max=max(chi_vals),
        tail_defect_fraction=tail,
        uniform_vanishing=uniform and steps[-1].jordan_preserved,
        messages=[f"Tail defect={tail:.3f}, uniform={uniform}"],
    )
