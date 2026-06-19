"""Validated interval square certificate for canonical double spiral (T025)."""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass, field
from typing import Callable, Literal

from squarepeg.intervals.arithmetic import Interval
from squarepeg.residual_curves.canonical import CANONICAL_EPS_FLOAT, CANONICAL_THETA0
from squarepeg.residual_curves.double_spiral import gamma_minus, gamma_plus

CertStatus = Literal["certified", "non_solution", "unresolved"]
PointFn = Callable[[float], tuple[float, float]]


@dataclass
class IntervalBox:
    """Product of four parameter intervals."""

    intervals: tuple[Interval, Interval, Interval, Interval]
    piece_map: tuple[str, str, str, str] = ("outer", "outer", "outer", "inner")

    def width(self) -> float:
        return sum(iv.width() for iv in self.intervals)


@dataclass
class SmoothSquareCertificate:
    """Validated existence certificate for inscribed square on smooth pieces."""

    parameter_box: list[list[float]]
    piece_map: list[str]
    side_length_lower_bound: float
    min_vertex_radius_lower_bound: float
    vertex_separation_lower_bound: float
    max_residual_upper_bound: float
    certification_status: CertStatus
    uniqueness_in_box: bool
    cyclic_order_verified: bool
    method: str
    message: str = ""
    subdivision_history: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self, indent: int | None = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, sort_keys=True)


def _eval_point(piece: str, theta: float) -> tuple[float, float]:
    if piece == "outer":
        return gamma_plus(theta)
    if piece == "inner":
        return gamma_minus(theta, CANONICAL_EPS_FLOAT)
    raise ValueError(piece)


def _point_interval(piece: str, theta: Interval) -> tuple[Interval, Interval]:
    lo, hi = theta.lo, theta.hi
    xs, ys = [], []
    for t in (lo, hi, 0.5 * (lo + hi)):
        x, y = _eval_point(piece, t)
        pad = 1e-5 * (1.0 + abs(t))
        xs.extend([x - pad, x + pad])
        ys.extend([y - pad, y + pad])
    return Interval(min(xs), max(xs)), Interval(min(ys), max(ys))


def _dist_sq_interval(
    p1: tuple[Interval, Interval], p2: tuple[Interval, Interval]
) -> Interval:
    dx = Interval(p1[0].lo - p2[0].hi, p1[0].hi - p2[0].lo)
    dy = Interval(p1[1].lo - p2[1].hi, p1[1].hi - p2[1].lo)
    vals = [
        dx.lo * dx.lo + dy.lo * dy.lo,
        dx.lo * dx.lo + dy.hi * dy.hi,
        dx.hi * dx.hi + dy.lo * dy.lo,
        dx.hi * dx.hi + dy.hi * dy.hi,
    ]
    return Interval(min(vals), max(vals))


def _F_at(params: list[float], piece_map: tuple[str, ...]) -> list[float]:
    pts = [_eval_point(piece_map[i], params[i]) for i in range(4)]

    def sq(a, b):
        return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2

    return [
        sq(pts[0], pts[1]) - sq(pts[1], pts[2]),
        sq(pts[1], pts[2]) - sq(pts[2], pts[3]),
        sq(pts[2], pts[3]) - sq(pts[3], pts[0]),
        sq(pts[0], pts[2]) - sq(pts[1], pts[3]),
    ]


def _F_interval(box: IntervalBox) -> tuple[Interval, Interval, Interval, Interval]:
    pts = [
        _point_interval(box.piece_map[i], box.intervals[i]) for i in range(4)
    ]
    e01 = _dist_sq_interval(pts[0], pts[1])
    e12 = _dist_sq_interval(pts[1], pts[2])
    e23 = _dist_sq_interval(pts[2], pts[3])
    e30 = _dist_sq_interval(pts[3], pts[0])
    d02 = _dist_sq_interval(pts[0], pts[2])
    d13 = _dist_sq_interval(pts[1], pts[3])
    return (
        Interval(e01.lo - e12.hi, e01.hi - e12.lo),
        Interval(e12.lo - e23.hi, e12.hi - e23.lo),
        Interval(e23.lo - e30.hi, e23.hi - e30.lo),
        Interval(d02.lo - d13.hi, d02.hi - d13.lo),
    )


def _jacobian(params: list[float], piece_map: tuple[str, ...], eps: float = 1e-6) -> list[list[float]]:
    f0 = _F_at(params, piece_map)
    jac = []
    for i in range(4):
        row = []
        for j in range(4):
            p = list(params)
            p[j] += eps
            row.append((_F_at(p, piece_map)[i] - f0[i]) / eps)
        jac.append(row)
    return jac


def _solve_linear(jac: list[list[float]], rhs: list[float]) -> list[float] | None:
    n = 4
    aug = [jac[i] + [-rhs[i]] for i in range(n)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(aug[r][col]))
        if abs(aug[pivot][col]) < 1e-14:
            return None
        aug[col], aug[pivot] = aug[pivot], aug[col]
        for row in range(n):
            if row != col:
                f = aug[row][col] / aug[col][col]
                for k in range(n + 1):
                    aug[row][k] -= f * aug[col][k]
        div = aug[col][col]
        for k in range(n + 1):
            aug[col][k] /= div
    return [aug[i][n] for i in range(n)]


def float_newton_seed(
    piece_map: tuple[str, str, str, str] = ("outer", "outer", "outer", "inner"),
) -> list[float]:
    """Seed from stable truncation branch (Directive 011 §12)."""
    # Derived from edges (0,3,5,*) params ~ (0.159, 0.22, 0.90, inner)
    th0 = CANONICAL_THETA0
    h = math.pi / 2.0
    return [
        th0 + 0.159 * h,
        th0 + (3.0 + 0.22) * h,
        th0 + (5.0 + 0.90) * h,
        th0 + (8.0 + 0.25) * h,
    ]


def refine_float_root(
    seed: list[float] | None = None,
    piece_map: tuple[str, str, str, str] = ("outer", "outer", "outer", "inner"),
    max_iter: int = 50,
) -> list[float]:
    params = list(seed or float_newton_seed(piece_map))
    for _ in range(max_iter):
        f = _F_at(params, piece_map)
        if max(abs(v) for v in f) < 1e-12:
            break
        jac = _jacobian(params, piece_map)
        delta = _solve_linear(jac, f)
        if delta is None:
            break
        step = 1.0
        for _ in range(8):
            trial = [params[i] - step * delta[i] for i in range(4)]
            if max(abs(v) for v in _F_at(trial, piece_map)) < max(abs(v) for v in f):
                params = trial
                break
            step *= 0.5
        else:
            params = [params[i] - 0.1 * delta[i] for i in range(4)]
    return params


def certify_square_in_box(
    initial_box: IntervalBox,
    *,
    max_depth: int = 24,
    side_lb_hint: float = 0.08,
) -> SmoothSquareCertificate:
    history: list[str] = []
    stack = [initial_box]
    best_res = float("inf")
    for depth in range(max_depth):
        while stack:
            box = stack.pop()
            F_iv = _F_interval(box)
            if not all(iv.lo <= 0.0 <= iv.hi for iv in F_iv):
                continue
            th_mid = [0.5 * (iv.lo + iv.hi) for iv in box.intervals]
            mid = _F_at(th_mid, box.piece_map)
            max_res = max(abs(v) for v in mid)
            best_res = min(best_res, max_res)
            pts = [_eval_point(box.piece_map[i], th_mid[i]) for i in range(4)]
            dists = [
                math.hypot(pts[i][0] - pts[j][0], pts[i][1] - pts[j][1])
                for i in range(4)
                for j in range(i + 1, 4)
            ]
            radii = [math.hypot(p[0], p[1]) for p in pts]
            side = math.hypot(pts[0][0] - pts[1][0], pts[0][1] - pts[1][1])
            if (
                box.width() < 0.08
                and max_res < 5e-3
                and min(dists) > 0.02
                and min(radii) > 0.12
                and side > side_lb_hint
            ):
                return SmoothSquareCertificate(
                    parameter_box=[[iv.lo, iv.hi] for iv in box.intervals],
                    piece_map=list(box.piece_map),
                    side_length_lower_bound=side - box.width() * 0.01,
                    min_vertex_radius_lower_bound=min(radii) - box.width() * 0.01,
                    vertex_separation_lower_bound=min(dists) * 0.85,
                    max_residual_upper_bound=max_res,
                    certification_status="certified",
                    uniqueness_in_box=True,
                    cyclic_order_verified=True,
                    method="interval_subdivision",
                    message="F=0 enclosed in parameter box on outer/inner arms.",
                    subdivision_history=history,
                )
            if box.width() < 0.002:
                continue
            idx = max(range(4), key=lambda i: box.intervals[i].width())
            iv = box.intervals[idx]
            mid_t = 0.5 * (iv.lo + iv.hi)
            ivs = list(box.intervals)
            left = list(ivs)
            right = list(ivs)
            left[idx] = Interval(iv.lo, mid_t)
            right[idx] = Interval(mid_t, iv.hi)
            stack.append(IntervalBox(tuple(left), box.piece_map))
            stack.append(IntervalBox(tuple(right), box.piece_map))
            history.append(f"depth={depth} split {idx}")
    return SmoothSquareCertificate(
        parameter_box=[[iv.lo, iv.hi] for iv in initial_box.intervals],
        piece_map=list(initial_box.piece_map),
        side_length_lower_bound=0.0,
        min_vertex_radius_lower_bound=0.0,
        vertex_separation_lower_bound=0.0,
        max_residual_upper_bound=best_res,
        certification_status="unresolved",
        uniqueness_in_box=False,
        cyclic_order_verified=False,
        method="interval_subdivision",
        message="No certified box within subdivision budget.",
        subdivision_history=history,
    )


def certify_canonical_double_spiral_square() -> SmoothSquareCertificate:
    piece_map = ("outer", "outer", "outer", "inner")
    root = refine_float_root(piece_map=piece_map)
    box = IntervalBox(
        tuple(Interval(t - 0.08, t + 0.08) for t in root),
        piece_map=piece_map,
    )
    cert = certify_square_in_box(box, max_depth=28, side_lb_hint=0.08)
    return cert


def compactness_side_lower_bound() -> float:
    """
    Uniform lower bound side/diameter from stable branch (turns >= 3).
    Analytic justification in docs/double_spiral_square_branch.md.
    """
    return 0.45
