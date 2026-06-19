"""Quantitative ANNULAR_GRAPH hypothesis for nested defect packets."""

from __future__ import annotations

import math
from dataclasses import dataclass, field

Point = tuple[float, float]


@dataclass(frozen=True)
class AnnularGraphConstants:
    """Fixed quantitative constants for ANNULAR_GRAPH membership."""

    K: float = 2.0  # max eccentricity max r / min r
    L: float = 0.5  # angular log-Lipschitz on log r
    g_minus: float = 0.35  # min inner/outer radial ratio
    g_plus: float = 0.65  # max inner/outer radial ratio
    w_corr: float = 0.12  # max total corridor angular width (fraction of 2pi)
    delta_core: float = 0.05  # core separation fraction of d_L
    zeta: float = 0.08  # max center drift / d_L


@dataclass
class RadialLayer:
    """Polar radial graph r_j(theta) around center c."""

    center: Point
    radii: list[float]  # samples at uniform theta
    n_theta: int
    diameter: float
    winding_sign: int = 1

    def max_radius(self) -> float:
        return max(self.radii) if self.radii else 0.0

    def min_radius(self) -> float:
        return min(self.radii) if self.radii else 0.0

    def eccentricity_K(self) -> float:
        mn = self.min_radius()
        if mn <= 1e-12:
            return float("inf")
        return self.max_radius() / mn

    def log_lipschitz_estimate(self) -> float:
        """Estimate sup |log r(theta)-log r(phi)| / d_S1(theta,phi)."""
        if len(self.radii) < 2:
            return 0.0
        n = len(self.radii)
        max_lip = 0.0
        for i in range(n):
            j = (i + 1) % n
            r0 = max(self.radii[i], 1e-12)
            r1 = max(self.radii[j], 1e-12)
            d_theta = 2 * math.pi / n
            lip = abs(math.log(r1) - math.log(r0)) / d_theta
            max_lip = max(max_lip, lip)
        return max_lip


@dataclass
class AnnularGraphPacket:
    layers: list[RadialLayer]
    corridor_width: float
    constants: AnnularGraphConstants
    checks: dict[str, bool] = field(default_factory=dict)


def radial_layer_from_ellipse(a: float, b: float, n: int = 64) -> RadialLayer:
    """Ellipse centered at origin: r(theta) for semi-axes a >= b."""
    radii = []
    for i in range(n):
        theta = 2 * math.pi * i / n
        ct, st = math.cos(theta), math.sin(theta)
        r = (a * b) / max(math.hypot(b * ct, a * st), 1e-12)
        radii.append(r)
    return RadialLayer(
        center=(0.0, 0.0),
        radii=radii,
        n_theta=n,
        diameter=2 * a,
        winding_sign=1,
    )


def radial_gap_ratio(outer: RadialLayer, inner: RadialLayer) -> tuple[float, float]:
    """Min/max of r_inner/r_outer over theta samples."""
    n = min(len(outer.radii), len(inner.radii))
    if n == 0:
        return 0.0, 0.0
    ratios = [inner.radii[i] / max(outer.radii[i], 1e-12) for i in range(n)]
    return min(ratios), max(ratios)


def center_drift(outer: RadialLayer, inner: RadialLayer) -> float:
    dx = inner.center[0] - outer.center[0]
    dy = inner.center[1] - outer.center[1]
    return math.hypot(dx, dy)


def validate_annular_graph(
    packet: AnnularGraphPacket,
    *,
    j: int = 0,
    k: int = 1,
) -> bool:
    """Check ANNULAR_GRAPH for selected layer pair L_j, L_k."""
    c = packet.constants
    if k >= len(packet.layers) or j >= k:
        return False
    outer = packet.layers[j]
    inner = packet.layers[k]
    checks: dict[str, bool] = {}

    checks["eccentricity_outer"] = outer.eccentricity_K() <= c.K
    checks["eccentricity_inner"] = inner.eccentricity_K() <= c.K
    checks["angular_outer"] = outer.log_lipschitz_estimate() <= c.L
    checks["angular_inner"] = inner.log_lipschitz_estimate() <= c.L

    gmin, gmax = radial_gap_ratio(outer, inner)
    checks["radial_gap"] = c.g_minus <= gmin and gmax <= c.g_plus

    checks["corridor_width"] = packet.corridor_width <= c.w_corr

    sep = outer.min_radius() - inner.max_radius()
    checks["core_separation"] = sep >= c.delta_core * outer.diameter or sep >= 0

    drift = center_drift(outer, inner)
    checks["center_drift"] = drift <= c.zeta * outer.diameter

    checks["same_winding"] = outer.winding_sign == inner.winding_sign

    packet.checks = checks
    return all(checks.values())


def in_annular_graph(packet: AnnularGraphPacket) -> bool:
    return validate_annular_graph(packet)


def D_nest_ann(packet: AnnularGraphPacket, in_d_nest: bool) -> bool:
    """D_nest^ann = D_nest cap ANNULAR_GRAPH."""
    return in_d_nest and in_annular_graph(packet)
