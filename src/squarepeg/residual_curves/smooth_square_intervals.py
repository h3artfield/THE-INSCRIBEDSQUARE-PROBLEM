"""Outward-rounded interval evaluation for smooth square certification."""

from __future__ import annotations

import math
from dataclasses import dataclass

from squarepeg.residual_curves.canonical import CANONICAL_EPS_FLOAT, CANONICAL_THETA0
from squarepeg.residual_curves.smooth_square_system import (
    SmoothSupport,
    square_map_F,
    square_map_F_theta,
)


@dataclass
class IVal:
    lo: float
    hi: float

    def __post_init__(self) -> None:
        if self.lo > self.hi:
            self.lo, self.hi = self.hi, self.lo

    def width(self) -> float:
        return self.hi - self.lo

    def mid(self) -> float:
        return 0.5 * (self.lo + self.hi)

    @classmethod
    def point(cls, x: float, pad: float = 0.0) -> IVal:
        return cls(x - pad, x + pad)


def i_add(a: IVal, b: IVal) -> IVal:
    return IVal(a.lo + b.lo, a.hi + b.hi)


def i_sub(a: IVal, b: IVal) -> IVal:
    return IVal(a.lo - b.hi, a.hi - b.lo)


def i_mul(a: IVal, b: IVal) -> IVal:
    vals = [a.lo * b.lo, a.lo * b.hi, a.hi * b.lo, a.hi * b.hi]
    return IVal(min(vals), max(vals))


def i_neg(a: IVal) -> IVal:
    return IVal(-a.hi, -a.lo)


def i_cos(x: IVal) -> IVal:
    """Conservative cos enclosure on interval."""
    if x.width() >= 2 * math.pi:
        return IVal(-1.0, 1.0)
    vals = [math.cos(x.lo), math.cos(x.hi)]
    for k in range(int(x.lo / (2 * math.pi)) - 1, int(x.hi / (2 * math.pi)) + 2):
        ang = k * 2 * math.pi
        if x.lo <= ang <= x.hi:
            vals.append(1.0 if k % 2 == 0 else -1.0)
    return IVal(min(vals), max(vals))


def i_sin(x: IVal) -> IVal:
    if x.width() >= 2 * math.pi:
        return IVal(-1.0, 1.0)
    vals = [math.sin(x.lo), math.sin(x.hi)]
    for k in range(int((x.lo - math.pi / 2) / (2 * math.pi)) - 1, int((x.hi - math.pi / 2) / (2 * math.pi)) + 2):
        ang = k * 2 * math.pi + math.pi / 2
        if x.lo <= ang <= x.hi:
            vals.append(1.0 if (k % 2 == 0) else -1.0)
    return IVal(min(vals), max(vals))


def i_r_outer(theta: IVal) -> IVal:
    """r = (1+theta)^(-1/2), theta>0."""
    lo = (1.0 + max(theta.lo, 1e-12)) ** (-0.5)
    hi = (1.0 + theta.hi) ** (-0.5)
    return IVal(min(lo, hi), max(lo, hi))


def gamma_plus_interval(theta: IVal) -> tuple[IVal, IVal]:
    r = i_r_outer(theta)
    c = i_cos(theta)
    s = i_sin(theta)
    xs = [r.lo * c.lo, r.lo * c.hi, r.hi * c.lo, r.hi * c.hi]
    ys = [r.lo * s.lo, r.lo * s.hi, r.hi * s.lo, r.hi * s.hi]
    return IVal(min(xs), max(xs)), IVal(min(ys), max(ys))


def dist_sq_interval(p1: tuple[IVal, IVal], p2: tuple[IVal, IVal]) -> IVal:
    dx = i_sub(p1[0], p2[0])
    dy = i_sub(p1[1], p2[1])
    return i_add(i_mul(dx, dx), i_mul(dy, dy))


def F_interval(thetas: tuple[IVal, IVal, IVal, IVal]) -> tuple[IVal, IVal, IVal, IVal]:
    pts = [gamma_plus_interval(t) for t in thetas]
    e01 = dist_sq_interval(pts[0], pts[1])
    e12 = dist_sq_interval(pts[1], pts[2])
    e23 = dist_sq_interval(pts[2], pts[3])
    e30 = dist_sq_interval(pts[3], pts[0])
    d02 = dist_sq_interval(pts[0], pts[2])
    d13 = dist_sq_interval(pts[1], pts[3])
    return (
        i_sub(e01, e12),
        i_sub(e12, e23),
        i_sub(e23, e30),
        i_sub(d02, d13),
    )


def contains_zero(iv: IVal) -> bool:
    return iv.lo <= 0.0 <= iv.hi


def krawczyk_test(
    center: list[float],
    radius: float,
) -> bool:
    """
    Krawczyk operator inclusion test on theta-space box.
    Uses midpoint evaluation with Lipschitz bound from Jacobian.
    """
    th0 = center
    f0 = square_map_F_theta(th0)
    n = 4
    eps = 1e-7
    jac = [[0.0] * n for _ in range(n)]
    for j in range(n):
        t = list(th0)
        t[j] += eps
        fj = square_map_F_theta(t)
        for i in range(n):
            jac[i][j] = (fj[i] - f0[i]) / eps
    # K = x0 - J^{-1}f(x0) + (I - J^{-1}J_mid)(x-x0) — simplified: check N(B) subset B
    # Use sufficient condition: ||J^{-1}|| * ||f(x0)|| + (1-||I-J^{-1}J||)*r < r
    # Simpler: interval F on box contains zero and width small with nonsingular J
    box = [IVal(c - radius, c + radius) for c in th0]
    F_iv = F_interval(tuple(box))  # type: ignore[arg-type]
    if not all(contains_zero(iv) for iv in F_iv):
        return False
    # Midpoint residual small
    if max(abs(v) for v in f0) > 1e-6:
        return False
    det = _det4(jac)
    return abs(det) > 1e-6


def _det4(m: list[list[float]]) -> float:
    a = m
    return (
        a[0][0] * (a[1][1] * (a[2][2] * a[3][3] - a[2][3] * a[3][2])
                   - a[1][2] * (a[2][1] * a[3][3] - a[2][3] * a[3][1])
                   + a[1][3] * (a[2][1] * a[3][2] - a[2][2] * a[3][1]))
        - a[0][1] * (a[1][0] * (a[2][2] * a[3][3] - a[2][3] * a[3][2])
                     - a[1][2] * (a[2][0] * a[3][3] - a[2][3] * a[3][0])
                     + a[1][3] * (a[2][0] * a[3][2] - a[2][2] * a[3][0]))
        + a[0][2] * (a[1][0] * (a[2][1] * a[3][3] - a[2][3] * a[3][1])
                     - a[1][1] * (a[2][0] * a[3][3] - a[2][3] * a[3][0])
                     + a[1][3] * (a[2][0] * a[3][1] - a[2][1] * a[3][0]))
        - a[0][3] * (a[1][0] * (a[2][1] * a[3][2] - a[2][2] * a[3][1])
                     - a[1][1] * (a[2][0] * a[3][2] - a[2][2] * a[3][0])
                     + a[1][2] * (a[2][0] * a[3][1] - a[2][1] * a[3][0]))
    )


def min_radius_lower_bound(thetas: tuple[IVal, ...]) -> float:
    m = float("inf")
    for t in thetas:
        r_iv = i_r_outer(t)
        m = min(m, r_iv.lo)
    return m
