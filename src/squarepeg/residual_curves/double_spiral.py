"""Double-spiral residual curve (Directive 010)."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Callable

Point = tuple[float, float]


def r_outer(theta: float) -> float:
    return (1.0 + theta) ** (-0.5)


def d_separation(theta: float, eps: float = 0.05) -> float:
    return eps * (1.0 + theta) ** (-2.0)


def gamma_plus(theta: float) -> Point:
    r = r_outer(theta)
    return (r * math.cos(theta), r * math.sin(theta))


def gamma_minus(theta: float, eps: float = 0.05) -> Point:
    r = r_outer(theta) - d_separation(theta, eps)
    return (r * math.cos(theta), r * math.sin(theta))


def polar_arc_length_integrand(theta: float) -> float:
    """Integrand sqrt(r^2 + (dr/dtheta)^2) for outer arm."""
    r = r_outer(theta)
    dr = -0.5 * (1.0 + theta) ** (-1.5)
    return math.hypot(r, dr)


def arm_arc_length(theta0: float, theta1: float, n: int = 5000) -> float:
    if theta1 <= theta0:
        return 0.0
    total = 0.0
    for i in range(n):
        t0 = theta0 + (theta1 - theta0) * i / n
        t1 = theta0 + (theta1 - theta0) * (i + 1) / n
        total += polar_arc_length_integrand(0.5 * (t0 + t1)) * (t1 - t0)
    return total


def opposite_increment_bound(theta: float) -> float:
    """|gamma+(theta+pi) - gamma+(theta)| >= c * r(theta) for large theta."""
    p0 = gamma_plus(theta)
    p1 = gamma_plus(theta + math.pi)
    return math.hypot(p1[0] - p0[0], p1[1] - p0[1])


def two_var_partition_sum(turns: int, eps: float = 0.05) -> float:
    """Sum of squared increments using opposite points on successive half-turns."""
    theta0 = 2.0 * math.pi
    total = 0.0
    for k in range(turns):
        th = theta0 + k * math.pi
        p0 = gamma_plus(th)
        p1 = gamma_plus(th + math.pi)
        dx = p1[0] - p0[0]
        dy = p1[1] - p0[1]
        total += dx * dx + dy * dy
    return total


def one_arm_action(theta0: float, theta1: float, n: int = 2000) -> float:
    """(1/2) int r(theta)^2 dtheta — symmetrized area form."""
    total = 0.0
    for i in range(n):
        t0 = theta0 + (theta1 - theta0) * i / n
        t1 = theta0 + (theta1 - theta0) * (i + 1) / n
        tm = 0.5 * (t0 + t1)
        total += 0.5 * r_outer(tm) ** 2 * (t1 - t0)
    return total


def annulus_area_between_arms(theta: float, eps: float = 0.05) -> float:
    """Local (1/2) int (r+^2 - r_-^2) dtheta over [theta, theta+dtheta] approx."""
    rp = r_outer(theta)
    rm = r_outer(theta) - d_separation(theta, eps)
    return 0.5 * (rp * rp - rm * rm)


@dataclass
class TruncatedDoubleSpiral:
    """Polygonal truncation with N half-turns per arm."""

    turns: int
    eps: float = 0.05
    theta0: float = 2.0 * math.pi

    def outer_vertices(self) -> list[Point]:
        pts: list[Point] = []
        for k in range(self.turns * 2 + 1):
            pts.append(gamma_plus(self.theta0 + k * math.pi / 2))
        return pts

    def inner_vertices(self) -> list[Point]:
        pts: list[Point] = []
        for k in range(self.turns * 2, -1, -1):
            pts.append(gamma_minus(self.theta0 + k * math.pi / 2, self.eps))
        return pts

    def closed_polygon(self) -> list[Point]:
        """Outer arm in, connector at origin, inner arm out (exploratory PL)."""
        outer = self.outer_vertices()
        inner = self.inner_vertices()
        return outer + [(0.0, 0.0)] + inner
