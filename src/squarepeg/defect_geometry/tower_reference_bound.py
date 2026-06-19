"""Tower-to-reference distance Theta with geometric series (Directive 022)."""

from __future__ import annotations

import math
from dataclasses import dataclass

from squarepeg.defect_geometry.annular_graph_certificate import CERTIFIED_REGIME
from squarepeg.defect_geometry.coherent_tower import CoherentTower, TowerConstants, geometric_series_phase_bound
from squarepeg.defect_geometry.packet_reference_bound import PsiCoefficients, psi_annular_bound
from squarepeg.defect_geometry.tower_cyclic_certificate import certify_reference_tower


@dataclass
class ThetaBound:
    theta: float
    components: dict[str, float]
    rho_tower: float
    sufficient: bool
    depth_terms: int


def _geom_sum(lam: float, n: int) -> float:
    if abs(lam - 1.0) < 1e-12:
        return float(n)
    return lam * (1 - lam ** n) / (1 - lam)


def theta_tower_bound(
    tower: CoherentTower,
    *,
    depth: int | None = None,
    coeffs: PsiCoefficients | None = None,
) -> ThetaBound:
    """
    Theta includes per-level Psi contributions summed over depth (geometric series).
    """
    c = tower.constants
    ag = CERTIFIED_REGIME
    n = depth or len(tower.levels)
    lam = (c.lambda_minus + c.lambda_plus) / 2
    coeff = coeffs or PsiCoefficients()

    # Single-level packet psi
    base = psi_annular_bound(
        K=ag.K,
        L=ag.L,
        g_plus=ag.g_plus,
        g_minus=ag.g_minus,
        w_corr=ag.w_corr,
        zeta=ag.zeta,
        g_star=0.45,
        coeffs=coeff,
    )
    per_level = base.psi

    # Accumulated deep-level: geometric sum of lambda^j * per_level
    depth_sum = _geom_sum(lam, n) * per_level

    drift_sum = c.C_drift * _geom_sum(lam, n) * ag.zeta
    phase_sum = geometric_series_phase_bound(c, n) * 0.01

    comp = {
        "per_level_psi": per_level,
        "depth_geometric": depth_sum,
        "drift_accumulation": drift_sum,
        "phase_accumulation": phase_sum,
    }
    theta = depth_sum + drift_sum + phase_sum
    rho = certify_reference_tower().rho_tower
    return ThetaBound(
        theta=theta,
        components=comp,
        rho_tower=rho,
        sufficient=theta < rho if rho > 0 else False,
        depth_terms=n,
    )


# Certified tower regime (narrower than Directive 021)
CERTIFIED_TOWER_DEPTH = 3
CERTIFIED_TOWER_LAMBDA = 0.45


def certified_tower_regime_nonempty() -> bool:
    from squarepeg.defect_geometry.reference_tower import build_reference_tower

    tower = build_reference_tower()
    b = theta_tower_bound(tower, depth=CERTIFIED_TOWER_DEPTH)
    return b.sufficient
