"""Velocity-matched cubic Bézier corner smoothing (T018, Directive 007R)."""

from __future__ import annotations

import math
from dataclasses import dataclass

from squarepeg.variation.p_variation import Point, euclidean, path_difference, p_variation, total_variation


def _sub(a: Point, b: Point) -> Point:
    return (a[0] - b[0], a[1] - b[1])


def _add(a: Point, b: Point) -> Point:
    return (a[0] + b[0], a[1] + b[1])


def _scale(a: Point, s: float) -> Point:
    return (a[0] * s, a[1] * s)


def _dot(a: Point, b: Point) -> float:
    return a[0] * b[0] + a[1] * b[1]


def _norm(a: Point) -> float:
    return math.hypot(a[0], a[1])


def _lerp(a: Point, b: Point, t: float) -> Point:
    return (a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1]))


def cross2(a: Point, b: Point) -> float:
    return a[0] * b[1] - a[1] * b[0]


def signed_area(vertices: list[Point]) -> float:
    n = len(vertices)
    if n < 3:
        return 0.0
    a = 0.0
    for i in range(n):
        x0, y0 = vertices[i]
        x1, y1 = vertices[(i + 1) % n]
        a += x0 * y1 - x1 * y0
    return 0.5 * a


def remove_collinear_vertices(vertices: list[Point], tol: float = 1e-12) -> list[Point]:
    """Drop redundant collinear vertices (including antiparallel backtrack)."""
    if len(vertices) < 4:
        return list(vertices)
    out: list[Point] = []
    n = len(vertices)
    for i in range(n):
        prev_v = vertices[(i - 1) % n]
        v = vertices[i]
        nxt = vertices[(i + 1) % n]
        u, w = _sub(v, prev_v), _sub(nxt, v)
        la, lb = _norm(u), _norm(w)
        if la <= tol or lb <= tol:
            continue
        if abs(cross2(u, w)) <= tol * max(la, lb, 1.0):
            continue
        if _dot(u, w) < -la * lb + tol * max(la, lb, 1.0):
            continue
        out.append(v)
    return out if len(out) >= 3 else list(vertices)


def cubic_control_points(a: Point, v: Point, c: Point, delta: float) -> tuple[Point, Point, Point, Point]:
    """
    Q0=A, Q1=A+(2/3)(v-A), Q2=C-(2/3)(C-v), Q3=C with L=2δ.
    Endpoint velocities: dS/dt = (v-A)/δ at A-side, (C-v)/δ at C-side.
    """
    q0 = a
    q1 = _add(a, _scale(_sub(v, a), 2.0 / 3.0))
    q2 = _add(c, _scale(_sub(v, c), 2.0 / 3.0))
    q3 = c
    return q0, q1, q2, q3


def cubic_bezier_eval(q0: Point, q1: Point, q2: Point, q3: Point, s: float) -> Point:
    o = 1.0 - s
    return (
        o**3 * q0[0] + 3 * o**2 * s * q1[0] + 3 * o * s**2 * q2[0] + s**3 * q3[0],
        o**3 * q0[1] + 3 * o**2 * s * q1[1] + 3 * o * s**2 * q2[1] + s**3 * q3[1],
    )


def cubic_bezier_derivative_ds(q0: Point, q1: Point, q2: Point, q3: Point, s: float) -> Point:
    o = 1.0 - s
    return (
        3 * o**2 * (q1[0] - q0[0]) + 6 * o * s * (q2[0] - q1[0]) + 3 * s**2 * (q3[0] - q2[0]),
        3 * o**2 * (q1[1] - q0[1]) + 6 * o * s * (q2[1] - q1[1]) + 3 * s**2 * (q3[1] - q2[1]),
    )


def cubic_endpoint_velocity_a(a: Point, v: Point, delta: float) -> Point:
    """dS/dt at τ-δ equals u_- = (v-A)/δ."""
    return _scale(_sub(v, a), 1.0 / delta)


def cubic_endpoint_velocity_c(v: Point, c: Point, delta: float) -> Point:
    """dS/dt at τ+δ equals u_+ = (C-v)/δ."""
    return _scale(_sub(c, v), 1.0 / delta)


def cubic_derivative_dt(q0: Point, q1: Point, q2: Point, q3: Point, s: float, L: float) -> Point:
    d_ds = cubic_bezier_derivative_ds(q0, q1, q2, q3, s)
    return _scale(d_ds, 1.0 / L)


def projection_witness(a: Point, v: Point, c: Point) -> Point:
    """w = a/|a| + b/|b| with a=v-A, b=C-v; w·S'>0 on cubic."""
    aa = _sub(v, a)
    bb = _sub(c, v)
    na, nb = _norm(aa), _norm(bb)
    if na <= 1e-18 or nb <= 1e-18:
        return aa if na >= nb else bb
    return _add(_scale(aa, 1.0 / na), _scale(bb, 1.0 / nb))


def w_dot_derivative_positive(q0: Point, q1: Point, q2: Point, q3: Point, w: Point, L: float) -> bool:
    """Sample-check w · dS/dt > 0 on [0,1]."""
    for i in range(101):
        s = i / 100.0
        ddt = cubic_derivative_dt(q0, q1, q2, q3, s, L)
        if _dot(w, ddt) <= 1e-10:
            return False
    return True


def polygon_corner_sample(
    a: Point,
    v: Point,
    c: Point,
    delta: float,
    n: int,
) -> tuple[list[Point], list[Point]]:
    """
    Common partition on [τ-δ, τ+δ]: first half A→v, second half v→C.
    Returns (polygon_samples, smoothed_samples) of equal length n+1.
    """
    L = 2.0 * delta
    q0, q1, q2, q3 = cubic_control_points(a, v, c, delta)
    poly: list[Point] = []
    smooth: list[Point] = []
    for i in range(n + 1):
        s = i / n
        t_local = s * L
        if t_local <= delta:
            poly.append(_lerp(a, v, t_local / delta))
        else:
            poly.append(_lerp(v, c, (t_local - delta) / delta))
        smooth.append(cubic_bezier_eval(q0, q1, q2, q3, s))
    return poly, smooth


@dataclass
class SmoothedPolygon:
    polygon: list[Point]
    smoothed: list[Point]
    corner_deltas: list[float]

    @property
    def max_sup_distance(self) -> float:
        return max(euclidean(p, s) for p, s in zip(self.polygon, self.smoothed))

    @property
    def tv_difference(self) -> float:
        return total_variation(path_difference(self.polygon, self.smoothed))


def _edge_points(a: Point, b: Point, n: int) -> list[Point]:
    return [_lerp(a, b, i / n) for i in range(n + 1)]


def round_corners_c1_cubic(
    vertices: list[Point],
    epsilon: float,
    samples_per_corner: int = 12,
    basepoint_edge: int = 0,
) -> SmoothedPolygon:
    """
    Velocity-matched cubic corner smoothing on common parametrization.
    Basepoint placed on interior of edge `basepoint_edge` (unchanged segment).
    """
    verts = remove_collinear_vertices(vertices)
    if verts and euclidean(verts[0], verts[-1]) < 1e-12:
        verts = verts[:-1]
    n = len(verts)
    if n < 3:
        raise ValueError("need at least 3 vertices")

    ccw = signed_area(verts + [verts[0]]) > 0
    ns = max(samples_per_corner, 4)

    max_delta: list[float] = []
    for i in range(n):
        prev_v, v, nxt = verts[(i - 1) % n], verts[i], verts[(i + 1) % n]
        max_delta.append(0.49 * min(euclidean(prev_v, v), euclidean(v, nxt)))

    budget = epsilon / 4.0 if epsilon > 0 else 0.0
    ssum = sum(max_delta)
    deltas = [min(m, budget * m / ssum if ssum > 0 else 0.0) for m in max_delta]

    a_pts: list[Point] = []
    c_pts: list[Point] = []
    for i in range(n):
        if deltas[i] <= 1e-15:
            a_pts.append(verts[i])
            c_pts.append(verts[i])
        else:
            prev_v, v, nxt = verts[(i - 1) % n], verts[i], verts[(i + 1) % n]
            d = deltas[i]
            a_pts.append(_lerp(v, prev_v, d / euclidean(prev_v, v)))
            c_pts.append(_lerp(v, nxt, d / euclidean(v, nxt)))

    poly_pts: list[Point] = []
    smooth_pts: list[Point] = []

    for i in range(n):
        v = verts[i]
        a, c = a_pts[i], c_pts[i]
        a_next = a_pts[(i + 1) % n]
        d = deltas[i]

        bridge = _edge_points(c, a_next, ns)
        poly_pts.extend(bridge[:-1])
        smooth_pts.extend(bridge[:-1])

        if d <= 1e-15:
            leg = _edge_points(a, c, ns)
            poly_pts.extend(leg[:-1])
            smooth_pts.extend(leg[:-1])
        else:
            corner_p, corner_s = polygon_corner_sample(a, v, c, d, ns)
            poly_pts.extend(corner_p[:-1])
            smooth_pts.extend(corner_s[:-1])

    poly_pts.append(poly_pts[0])
    smooth_pts.append(smooth_pts[0])

    if not ccw:
        poly_pts = list(reversed(poly_pts))
        smooth_pts = list(reversed(smooth_pts))

    assert len(poly_pts) == len(smooth_pts)
    return SmoothedPolygon(polygon=poly_pts, smoothed=smooth_pts, corner_deltas=deltas)


def _resample_polyline(points: list[Point], n: int) -> list[Point]:
    """Resample open polyline to exactly n+1 points (arc-length uniform)."""
    if len(points) < 2:
        return list(points)
    lengths = [0.0]
    for i in range(len(points) - 1):
        lengths.append(lengths[-1] + euclidean(points[i], points[i + 1]))
    total = lengths[-1]
    if total <= 1e-18:
        return [points[0]] * (n + 1)
    out: list[Point] = []
    j = 0
    for i in range(n + 1):
        tgt = total * i / n
        while j + 1 < len(lengths) - 1 and lengths[j + 1] < tgt - 1e-15:
            j += 1
        seg_len = lengths[j + 1] - lengths[j]
        t = 0.0 if seg_len <= 1e-18 else (tgt - lengths[j]) / seg_len
        out.append(_lerp(points[j], points[j + 1], t))
    return out


def q_variation_monotonicity_holds(h_points: list[Point], q: float) -> bool:
    """Check |h|_{q-var} <= |h|_{1-var} on sampled path."""
    if q < 1.0:
        return True
    return p_variation(h_points, q) <= total_variation(h_points) + 1e-9


def quadratic_bezier(a: Point, control: Point, b: Point, n: int = 16) -> list[Point]:
    """Legacy quadratic — superseded by cubic T018."""
    pts: list[Point] = []
    for i in range(n + 1):
        t = i / n
        omt = 1.0 - t
        pts.append(
            (
                omt * omt * a[0] + 2 * omt * t * control[0] + t * t * b[0],
                omt * omt * a[1] + 2 * omt * t * control[1] + t * t * b[1],
            )
        )
    return pts
