"""Independent outward-rounded interval backend for T025 replay."""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass
class IVal:
    lo: float
    hi: float

    def __post_init__(self) -> None:
        if self.lo > self.hi:
            self.lo, self.hi = self.hi, self.lo

    def mid(self) -> float:
        return 0.5 * (self.lo + self.hi)

    def width(self) -> float:
        return self.hi - self.lo

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


def i_cos(x: IVal) -> IVal:
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


def contains_zero(iv: IVal) -> bool:
    return iv.lo <= 0.0 <= iv.hi


def excludes_zero(iv: IVal) -> bool:
    return iv.lo > 0.0 or iv.hi < 0.0


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


def boxes_from_fractions(boxes: tuple[tuple[float, float], ...]) -> tuple[IVal, IVal, IVal, IVal]:
    return tuple(IVal(lo, hi) for lo, hi in boxes)  # type: ignore[return-value]


def min_radius_lower_bound(thetas: tuple[IVal, ...]) -> float:
    return min(i_r_outer(t).lo for t in thetas)


def side_length_lower_bound(thetas: tuple[IVal, ...]) -> float:
    p0, p1 = gamma_plus_interval(thetas[0]), gamma_plus_interval(thetas[1])
    dx = i_sub(p0[0], p1[0])
    dy = i_sub(p0[1], p1[1])
    ds = i_add(i_mul(dx, dx), i_mul(dy, dy))
    return ds.lo ** 0.5 if ds.lo > 0 else 0.0


def pairwise_separation_lower_bounds(thetas: tuple[IVal, ...]) -> list[float]:
    pts = [gamma_plus_interval(t) for t in thetas]
    out: list[float] = []
    for i in range(4):
        for j in range(i + 1, 4):
            ds = dist_sq_interval(pts[i], pts[j])
            out.append(ds.lo ** 0.5 if ds.lo > 0 else 0.0)
    return out


def det4(m: list[list[float]]) -> float:
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


def jacobian_float(center: list[float], eps: float = 1e-7) -> list[list[float]]:
    def F_float(th: list[float]) -> list[float]:
        def gp(t: float) -> tuple[float, float]:
            r = (1.0 + t) ** (-0.5)
            return r * math.cos(t), r * math.sin(t)

        pts = [gp(t) for t in th]

        def sq(a: tuple[float, float], b: tuple[float, float]) -> float:
            return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2

        return [
            sq(pts[0], pts[1]) - sq(pts[1], pts[2]),
            sq(pts[1], pts[2]) - sq(pts[2], pts[3]),
            sq(pts[2], pts[3]) - sq(pts[3], pts[0]),
            sq(pts[0], pts[2]) - sq(pts[1], pts[3]),
        ]

    f0 = F_float(center)
    jac = [[0.0] * 4 for _ in range(4)]
    for j in range(4):
        t = list(center)
        t[j] += eps
        fj = F_float(t)
        for i in range(4):
            jac[i][j] = (fj[i] - f0[i]) / eps
    return jac


def jacobian_at_point(thetas: list[float]) -> list[list[float]]:
    return jacobian_float(thetas)


def det_interval_on_box(boxes: tuple[tuple[float, float], ...]) -> IVal:
    """Evaluate det J at all 2^4 corners of theta box — valid for small boxes."""
    corners: list[list[float]] = []
    for b0 in (boxes[0][0], boxes[0][1]):
        for b1 in (boxes[1][0], boxes[1][1]):
            for b2 in (boxes[2][0], boxes[2][1]):
                for b3 in (boxes[3][0], boxes[3][1]):
                    corners.append([b0, b1, b2, b3])
    dets = [det4(jacobian_at_point(c)) for c in corners]
    return IVal(min(dets), max(dets))
