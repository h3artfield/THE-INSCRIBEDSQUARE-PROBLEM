"""Coherent annular tower definition (Directive 022)."""

from __future__ import annotations

import math
from dataclasses import dataclass, field

from squarepeg.defect_geometry.annular_graph import (
    AnnularGraphConstants,
    AnnularGraphPacket,
    validate_annular_graph,
)
from squarepeg.defect_geometry.annular_graph_certificate import CERTIFIED_REGIME

Point = tuple[float, float]


@dataclass(frozen=True)
class TowerConstants:
    """Quantitative tower hypotheses."""

    lambda_minus: float = 0.42
    lambda_plus: float = 0.48
    C_drift: float = 0.5
    C_phase: float = 0.25
    annular: AnnularGraphConstants = CERTIFIED_REGIME


@dataclass
class TowerLevel:
    index: int
    outer_radius: float
    inner_radius: float
    center: Point
    phi_in: float
    phi_out: float
    winding_sign: int = 1
    packet: AnnularGraphPacket | None = None


@dataclass
class CoherentTower:
    levels: list[TowerLevel]
    constants: TowerConstants
    accumulation_center: Point
    checks: dict[str, bool] = field(default_factory=dict)


def scale_ratio(r_j: float, r_j1: float) -> float:
    if r_j <= 0:
        return 0.0
    return r_j1 / r_j


def validate_coherent_tower(tower: CoherentTower) -> bool:
    c = tower.constants
    checks: dict[str, bool] = {}
    lv = tower.levels
    if len(lv) < 2:
        tower.checks = {"min_depth": False}
        return False

    for j in range(len(lv) - 1):
        outer, inner = lv[j], lv[j + 1]
        ratio = scale_ratio(outer.outer_radius, inner.outer_radius)
        checks[f"scale_{j}"] = c.lambda_minus <= ratio <= c.lambda_plus

        dx = inner.center[0] - outer.center[0]
        dy = inner.center[1] - outer.center[1]
        drift = math.hypot(dx, dy)
        checks[f"drift_{j}"] = drift <= c.C_drift * inner.outer_radius

        phase_in = abs(inner.phi_in - outer.phi_in)
        phase_out = abs(inner.phi_out - outer.phi_out)
        phase_in = min(phase_in, 2 * math.pi - phase_in)
        phase_out = min(phase_out, 2 * math.pi - phase_out)
        bound = c.C_phase * ratio
        checks[f"phase_{j}"] = phase_in + phase_out <= bound + 1e-9

        checks[f"winding_{j}"] = outer.winding_sign == inner.winding_sign

        if inner.packet is not None:
            checks[f"annular_{j+1}"] = validate_annular_graph(inner.packet)

    # Centers converge
    if lv:
        last = lv[-1].center
        acc = tower.accumulation_center
        checks["accumulation"] = math.hypot(last[0] - acc[0], last[1] - acc[1]) <= lv[-1].outer_radius

    tower.checks = checks
    return all(checks.values())


def tower_outer_scale(tower: CoherentTower) -> float:
    return tower.levels[0].outer_radius if tower.levels else 0.0


def geometric_series_phase_bound(c: TowerConstants, depth: int) -> float:
    """Sum of C_phase * lambda^j over j levels."""
    lam = (c.lambda_minus + c.lambda_plus) / 2
    if abs(lam - 1.0) < 1e-12:
        return c.C_phase * depth
    return c.C_phase * lam * (1 - lam ** depth) / (1 - lam)
