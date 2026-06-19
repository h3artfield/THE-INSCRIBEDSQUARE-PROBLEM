"""Smooth square equations on canonical double-spiral pieces."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Callable, Literal

from squarepeg.residual_curves.canonical import (
    CANONICAL_EPS_FLOAT,
    CANONICAL_THETA0,
    outer_connector_point,
)
from squarepeg.residual_curves.double_spiral import gamma_minus, gamma_plus

Piece = Literal["outer", "inner", "connector"]
Point = tuple[float, float]


@dataclass(frozen=True)
class SmoothSupport:
    piece: Piece
    theta_lo: float
    theta_hi: float

    def evaluate(self, u: float) -> Point:
        """u in [0,1] linearly parametrizes theta in [theta_lo, theta_hi]."""
        th = self.theta_lo + u * (self.theta_hi - self.theta_lo)
        if self.piece == "outer":
            return gamma_plus(th)
        if self.piece == "inner":
            return gamma_minus(th, CANONICAL_EPS_FLOAT)
        if self.piece == "connector":
            return outer_connector_point(u, CANONICAL_THETA0)
        raise ValueError(self.piece)

    def theta_at(self, u: float) -> float:
        return self.theta_lo + u * (self.theta_hi - self.theta_lo)


def eval_piece(piece: Piece, theta: float) -> Point:
    if piece == "outer":
        return gamma_plus(theta)
    if piece == "inner":
        return gamma_minus(theta, CANONICAL_EPS_FLOAT)
    raise ValueError(piece)


def square_map_F(params: list[float], supports: list[SmoothSupport]) -> list[float]:
    """F=0 with params as u in [0,1] on each support piece."""
    pts = [supports[i].evaluate(params[i]) for i in range(4)]

    def sq(a: Point, b: Point) -> float:
        return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2

    return [
        sq(pts[0], pts[1]) - sq(pts[1], pts[2]),
        sq(pts[1], pts[2]) - sq(pts[2], pts[3]),
        sq(pts[2], pts[3]) - sq(pts[3], pts[0]),
        sq(pts[0], pts[2]) - sq(pts[1], pts[3]),
    ]


def square_map_F_theta(thetas: list[float]) -> list[float]:
    """All four points on gamma_+ at angles thetas."""
    pts = [gamma_plus(t) for t in thetas]

    def sq(a: Point, b: Point) -> float:
        return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2

    return [
        sq(pts[0], pts[1]) - sq(pts[1], pts[2]),
        sq(pts[1], pts[2]) - sq(pts[2], pts[3]),
        sq(pts[2], pts[3]) - sq(pts[3], pts[0]),
        sq(pts[0], pts[2]) - sq(pts[1], pts[3]),
    ]


def midpoint_rotation_residuals(params: list[float], supports: list[SmoothSupport]) -> list[float]:
    """Independent validator: p1+p3=p2+p4 and 90deg rotation."""
    pts = [supports[i].evaluate(params[i]) for i in range(4)]
    p1, p2, p3, p4 = pts
    mid1 = (p1[0] + p3[0] - p2[0] - p4[0], p1[1] + p3[1] - p2[1] - p4[1])
    dx, dy = p2[0] - p4[0], p2[1] - p4[1]
    rot_x = p3[0] - p1[0] + dy
    rot_y = p3[1] - p1[1] - dx
    return [mid1[0], mid1[1], rot_x, rot_y]


def side_length(params: list[float], supports: list[SmoothSupport]) -> float:
    p0 = supports[0].evaluate(params[0])
    p1 = supports[1].evaluate(params[1])
    return math.hypot(p0[0] - p1[0], p0[1] - p1[1])


def jacobian_theta(thetas: list[float], eps: float = 1e-8) -> list[list[float]]:
    f0 = square_map_F_theta(thetas)
    jac: list[list[float]] = []
    for i in range(4):
        row = []
        for j in range(4):
            t = list(thetas)
            t[j] += eps
            row.append((square_map_F_theta(t)[i] - f0[i]) / eps)
        jac.append(row)
    return jac


# Reconnaissance root (Directive 012) — all on gamma_+.
DISCOVERED_SMOOTH_THETA = (
    5.904664570522921,
    10.768443130208531,
    15.133643385520857,
    7.207559275277679,
)

# Compact outer parameter windows (theta intervals, disjoint where required).
OUTER_THETA_WINDOWS: tuple[tuple[float, float], ...] = (
    (5.75, 6.05),   # J1 — first arm turn
    (10.55, 11.0),  # J2
    (14.95, 15.35), # J3
    (7.05, 7.45),   # J4 — second point on first-turn arm
)


def supports_from_theta_windows() -> list[SmoothSupport]:
    return [SmoothSupport("outer", lo, hi) for lo, hi in OUTER_THETA_WINDOWS]


def theta_to_u(theta: float, support: SmoothSupport) -> float:
    return (theta - support.theta_lo) / (support.theta_hi - support.theta_lo)


def discovered_params() -> list[float]:
    sup = supports_from_theta_windows()
    return [theta_to_u(t, sup[i]) for i, t in enumerate(DISCOVERED_SMOOTH_THETA)]
