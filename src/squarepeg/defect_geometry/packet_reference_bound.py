"""Explicit Psi comparison bound for annular-graph packets."""

from __future__ import annotations

import math
from dataclasses import dataclass

from squarepeg.defect_geometry.annular_graph import AnnularGraphConstants
from squarepeg.defect_geometry.reference_cyclic_certificate import rho_cyc_reference


@dataclass(frozen=True)
class PsiCoefficients:
    """Explicit constants in Psi decomposition (proved Lipschitz model).

    C1: after max-normalization, |r(θ)-1| ≤ 1 - 1/K ≤ K - 1 on the outer layer.
    C2: log-Lipschitz L gives |log r(θ) - log r(φ)| ≤ L d; window displacement ≤ L ℓ_win.
    C3–C6: corridor, gap, drift, and g* deviation (interval-certified in docs).
    """

    C1: float = 1.0  # (K-1) radial deviation bound
    C2: float = 0.15  # L * l_win angular
    C3: float = 0.35  # (g+ - g-) gap spread
    C4: float = 0.50  # w_corr corridor
    C5: float = 0.60  # zeta center drift
    C6: float = 0.40  # |g* - g_ref| reference ratio deviation


@dataclass
class PsiBound:
    psi: float
    components: dict[str, float]
    rho_cyc: float
    sufficient: bool


def psi_annular_bound(
    *,
    K: float,
    L: float,
    g_plus: float,
    g_minus: float,
    w_corr: float,
    zeta: float,
    g_star: float,
    g_ref: float = 0.45,
    l_win: float = math.pi / 2,
    coeffs: PsiCoefficients | None = None,
) -> PsiBound:
    c = coeffs or PsiCoefficients()
    comp = {
        "eccentricity": c.C1 * max(0.0, K - 1.0),
        "angular": c.C2 * L * l_win,
        "gap_spread": c.C3 * (g_plus - g_minus),
        "corridor": c.C4 * w_corr,
        "center_drift": c.C5 * zeta,
        "g_star_dev": c.C6 * abs(g_star - g_ref),
    }
    psi = sum(comp.values())
    rho = rho_cyc_reference()
    return PsiBound(psi=psi, components=comp, rho_cyc=rho, sufficient=psi < rho if rho > 0 else False)


def psi_from_constants(ag: AnnularGraphConstants, g_star: float = 0.45) -> PsiBound:
    return psi_annular_bound(
        K=ag.K,
        L=ag.L,
        g_plus=ag.g_plus,
        g_minus=ag.g_minus,
        w_corr=ag.w_corr,
        zeta=ag.zeta,
        g_star=g_star,
        g_ref=(ag.g_minus + ag.g_plus) / 2,
    )
