"""Exact affine solution sets for square edge-quadruple linear systems."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from fractions import Fraction
from typing import Literal, Sequence

from squarepeg.curves.polygon import Point, PolygonCurve

Rotation = Literal["ccw", "cw"]
FeasibilityKind = Literal["empty", "point", "closed_interval", "open_interval", "union"]

# Sentinel fractions for unbounded interval endpoints in parameter t
NEG_INF = Fraction(-10**18, 1)
POS_INF = Fraction(10**18, 1)

VAR_NAMES = ("u1", "u2", "u3", "u4", "vx", "vy")


@dataclass(frozen=True)
class TInterval:
    """Parameter interval [lo, hi] with endpoint openness."""

    lo: Fraction
    hi: Fraction
    lo_closed: bool = True
    hi_closed: bool = True

    def is_empty(self) -> bool:
        if self.lo > self.hi:
            return True
        if self.lo == self.hi and (not self.lo_closed or not self.hi_closed):
            return True
        return False

    def contains(self, t: Fraction) -> bool:
        if self.is_empty():
            return False
        if self.lo_closed:
            if t < self.lo:
                return False
        elif t <= self.lo:
            return False
        if self.hi_closed:
            if t > self.hi:
                return False
        elif t >= self.hi:
            return False
        return True


@dataclass(frozen=True)
class AffineSolveResult:
    rank: int
    inconsistent: bool
    particular: tuple[Fraction, ...] | None = None
    nullspace: tuple[tuple[Fraction, ...], ...] = ()
    matrix: tuple[tuple[Fraction, ...], ...] = ()
    rhs: tuple[Fraction, ...] = ()


def _mat_vec(
    m: Sequence[Sequence[Fraction]], v: Sequence[Fraction]
) -> list[Fraction]:
    return [sum(row[i] * v[i] for i in range(len(v))) for row in m]


def solve_affine_system(
    matrix: list[list[Fraction]], rhs: list[Fraction]
) -> AffineSolveResult:
    """Exact RREF; returns particular solution and nullspace basis."""
    m_rows = len(matrix)
    n_cols = len(matrix[0]) if matrix else 0
    aug = [row[:] + [rhs[i]] for i, row in enumerate(matrix)]

    pivot_cols: list[int] = []
    pivot_row = 0
    for col in range(n_cols):
        sel = None
        for r in range(pivot_row, m_rows):
            if aug[r][col] != 0:
                sel = r
                break
        if sel is None:
            continue
        aug[pivot_row], aug[sel] = aug[sel], aug[pivot_row]
        pv = aug[pivot_row][col]
        aug[pivot_row] = [val / pv for val in aug[pivot_row]]
        for r in range(m_rows):
            if r == pivot_row or aug[r][col] == 0:
                continue
            factor = aug[r][col]
            aug[r] = [aug[r][c] - factor * aug[pivot_row][c] for c in range(n_cols + 1)]
        pivot_cols.append(col)
        pivot_row += 1
        if pivot_row == m_rows:
            break

    rank = len(pivot_cols)
    for r in range(pivot_row, m_rows):
        if all(aug[r][c] == 0 for c in range(n_cols)) and aug[r][n_cols] != 0:
            frozen = tuple(tuple(row) for row in matrix)
            return AffineSolveResult(
                rank=rank,
                inconsistent=True,
                matrix=frozen,
                rhs=tuple(rhs),
            )

    particular = [Fraction(0)] * n_cols
    for i, pcol in enumerate(pivot_cols):
        particular[pcol] = aug[i][n_cols]

    free_cols = [c for c in range(n_cols) if c not in pivot_cols]
    nullspace: list[tuple[Fraction, ...]] = []
    for fcol in free_cols:
        direction = [Fraction(0)] * n_cols
        direction[fcol] = Fraction(1)
        for i, pcol in enumerate(pivot_cols):
            direction[pcol] = -aug[i][fcol]
        nullspace.append(tuple(direction))

    frozen = tuple(tuple(row) for row in matrix)
    return AffineSolveResult(
        rank=rank,
        inconsistent=False,
        particular=tuple(particular),
        nullspace=tuple(nullspace),
        matrix=frozen,
        rhs=tuple(rhs),
    )


def x_at_t(
    particular: Sequence[Fraction],
    direction: Sequence[Fraction],
    t: Fraction,
) -> tuple[Fraction, ...]:
    return tuple(particular[i] + t * direction[i] for i in range(len(particular)))


def residual_at(
    matrix: Sequence[Sequence[Fraction]],
    rhs: Sequence[Fraction],
    x: Sequence[Fraction],
) -> list[Fraction]:
    return [sum(matrix[r][c] * x[c] for c in range(len(x))) - rhs[r] for r in range(len(matrix))]


def _interval_from_bounds(lo: Fraction, hi: Fraction) -> TInterval | None:
    if lo > hi:
        return None
    return TInterval(lo, hi, True, True)


def _u_interval(x0: Fraction, d: Fraction) -> list[TInterval]:
    if d == 0:
        if Fraction(0) <= x0 <= 1:
            return [TInterval(NEG_INF, POS_INF, False, False)]
        return []
    lo = (Fraction(0) - x0) / d
    hi = (Fraction(1) - x0) / d
    if lo > hi:
        lo, hi = hi, lo
    iv = _interval_from_bounds(lo, hi)
    return [iv] if iv else []


def _strict_inequality_interval(
    lhs0: Fraction, lhsd: Fraction, rhs0: Fraction, rhsd: Fraction
) -> list[TInterval]:
    """Interval where lhs0 + t*lhsd > rhs0 + t*rhsd."""
    dc = lhsd - rhsd
    rhs = rhs0 - lhs0
    if dc == 0:
        if rhs < 0:
            return [TInterval(NEG_INF, POS_INF, False, False)]
        return []
    t_bound = rhs / dc
    if dc > 0:
        return [TInterval(t_bound, POS_INF, False, False)]
    return [TInterval(NEG_INF, t_bound, False, False)]


def _side_positive_excluded(
    x0: Sequence[Fraction], d: Sequence[Fraction]
) -> list[Fraction]:
    """Parameter values where vx^2 + vy^2 = 0."""
    vx0, vy0, vxd, vyd = x0[4], x0[5], d[4], d[5]
    a = vxd * vxd + vyd * vyd
    b = 2 * (vx0 * vxd + vy0 * vyd)
    c = vx0 * vx0 + vy0 * vy0
    if a == 0:
        return [] if c != 0 else [Fraction(0)]
    disc = b * b - 4 * a * c
    if disc < 0:
        return []
    from math import isqrt

    def sqrt_frac(x: Fraction) -> Fraction:
        if x < 0:
            raise ValueError
        num, den = x.numerator, x.denominator
        sn = isqrt(num)
        sd = isqrt(den)
        if sn * sn * den != num * sd * sd:
            import math
            return Fraction(math.sqrt(float(x))).limit_denominator(10**12)
        return Fraction(sn, sd)

    if disc == 0:
        return [-b / (2 * a)]
    s = sqrt_frac(disc)
    t1 = (-b - s) / (2 * a)
    t2 = (-b + s) / (2 * a)
    return [t1] if t1 == t2 else sorted(set([t1, t2]))


def intersect_interval_lists(
    a: list[TInterval], b: list[TInterval]
) -> list[TInterval]:
    if not a or not b:
        return []
    out: list[TInterval] = []
    for ia in a:
        for ib in b:
            lo = max(ia.lo, ib.lo)
            hi = min(ia.hi, ib.hi)
            lo_closed = ia.lo_closed if ia.lo >= ib.lo else ib.lo_closed
            hi_closed = ia.hi_closed if ia.hi <= ib.hi else ib.hi_closed
            if lo < hi or (lo == hi and lo_closed and hi_closed):
                out.append(TInterval(lo, hi, lo_closed, hi_closed))
    return out


def union_interval_list(intervals: list[TInterval]) -> list[TInterval]:
    if not intervals:
        return []
    normalized = sorted(intervals, key=lambda iv: (iv.lo, not iv.lo_closed))
    merged: list[TInterval] = [normalized[0]]
    for iv in normalized[1:]:
        last = merged[-1]
        if iv.lo <= last.hi:
            new_hi = max(last.hi, iv.hi)
            hi_closed = last.hi_closed if last.hi > iv.hi else iv.hi_closed
            if last.hi == iv.hi:
                hi_closed = last.hi_closed and iv.hi_closed
            merged[-1] = TInterval(last.lo, new_hi, last.lo_closed, hi_closed)
        else:
            merged.append(iv)
    return merged


def subtract_points(
    intervals: list[TInterval], excluded: Sequence[Fraction]
) -> list[TInterval]:
    """Remove isolated parameter values (zero side length)."""
    result: list[TInterval] = []
    for iv in intervals:
        pts = sorted(set(excluded))
        current_lo = iv.lo
        current_lo_closed = iv.lo_closed
        for pt in pts:
            if not iv.contains(pt):
                continue
            if current_lo < pt or (current_lo == pt and not current_lo_closed):
                left_hi_closed = False
                left = TInterval(current_lo, pt, current_lo_closed, left_hi_closed)
                if not left.is_empty():
                    result.append(left)
            current_lo = pt
            current_lo_closed = False
        if current_lo < iv.hi or (current_lo == iv.hi and current_lo_closed and iv.hi_closed):
            right = TInterval(current_lo, iv.hi, current_lo_closed, iv.hi_closed)
            if not right.is_empty():
                result.append(right)
    return result if result else intervals


def boundary_order_constraints(
    polygon: PolygonCurve,
    edges: tuple[int, int, int, int],
    x0: Sequence[Fraction],
    d: Sequence[Fraction],
) -> list[TInterval]:
    tagged = list(zip(edges, range(4)))
    if len(set(edges)) == 4 and not polygon.cyclic_order(*edges):
        return []
    constraints = [TInterval(NEG_INF, POS_INF, False, False)]
    prev_e, prev_i = tagged[0]
    prev_u0, prev_ud = x0[prev_i], d[prev_i]
    n = polygon.num_edges
    for e, idx in tagged[1:]:
        u0, ud = x0[idx], d[idx]
        de = (e - prev_e) % n
        if de == 0:
            part = _strict_inequality_interval(u0, ud, prev_u0, prev_ud)
            constraints = intersect_interval_lists(constraints, part)
        prev_e, prev_i = e, idx
        prev_u0, prev_ud = u0, ud
    return constraints


def compute_feasible_t(
    polygon: PolygonCurve,
    edges: tuple[int, int, int, int],
    x0: Sequence[Fraction],
    d: Sequence[Fraction],
) -> tuple[FeasibilityKind, list[TInterval], list[Fraction]]:
    intervals = [TInterval(NEG_INF, POS_INF, False, False)]
    for i in range(4):
        intervals = intersect_interval_lists(intervals, _u_interval(x0[i], d[i]))
    intervals = intersect_interval_lists(
        intervals, boundary_order_constraints(polygon, edges, x0, d)
    )
    excluded = _side_positive_excluded(x0, d)
    intervals = subtract_points(intervals, excluded)
    intervals = [iv for iv in intervals if not iv.is_empty()]
    intervals = union_interval_list(intervals)

    if not intervals:
        return "empty", [], excluded

    if len(intervals) == 1:
        iv = intervals[0]
        if iv.lo == iv.hi and iv.lo_closed and iv.hi_closed:
            return "point", intervals, excluded
        if iv.lo_closed and iv.hi_closed:
            return "closed_interval", intervals, excluded
        return "union", intervals, excluded

    return "union", intervals, excluded


def endpoint_values(
    intervals: list[TInterval],
) -> list[Fraction]:
    bound = Fraction(10**12)
    pts: list[Fraction] = []
    for iv in intervals:
        if iv.lo_closed and abs(iv.lo) <= bound:
            pts.append(iv.lo)
        if iv.hi_closed and iv.hi != iv.lo and abs(iv.hi) <= bound:
            pts.append(iv.hi)
    return sorted(set(pts))


@dataclass
class AffineSquareFamily1D:
    polygon_hash: str
    edge_indices: tuple[int, int, int, int]
    orientation: Rotation
    base_point: tuple[str, ...]
    direction: tuple[str, ...]
    feasible_intervals: list[dict]
    excluded_degenerate_t: list[str]
    endpoint_isolated_t: list[str]
    feasibility_kind: FeasibilityKind
    matrix: list[list[str]]
    rhs: list[str]
    proof_residuals: dict[str, str]
    family_id: str
    rank: int = 5

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self, indent: int | None = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, sort_keys=True)

    @classmethod
    def build(
        cls,
        polygon: PolygonCurve,
        edges: tuple[int, int, int, int],
        rotation: Rotation,
        solved: AffineSolveResult,
    ) -> AffineSquareFamily1D:
        assert solved.particular is not None and len(solved.nullspace) == 1
        x0 = solved.particular
        d = solved.nullspace[0]
        kind, intervals, excluded = compute_feasible_t(polygon, edges, x0, d)
        endpoints = endpoint_values(intervals)
        res0 = residual_at(solved.matrix, solved.rhs, x0)
        resd = _mat_vec(solved.matrix, d)
        proof = {
            "particular_residual": str(res0),
            "direction_in_nullspace": str(resd),
        }
        payload = {
            "edges": edges,
            "rotation": rotation,
            "x0": [str(v) for v in x0],
            "d": [str(v) for v in d],
        }
        family_id = hashlib.sha256(
            json.dumps(payload, sort_keys=True).encode()
        ).hexdigest()[:16]
        return cls(
            polygon_hash=polygon.polygon_hash(),
            edge_indices=edges,
            orientation=rotation,
            base_point=tuple(str(v) for v in x0),
            direction=tuple(str(v) for v in d),
            feasible_intervals=[
                {
                    "lo": str(iv.lo),
                    "hi": str(iv.hi),
                    "lo_closed": iv.lo_closed,
                    "hi_closed": iv.hi_closed,
                }
                for iv in intervals
            ],
            excluded_degenerate_t=[str(t) for t in excluded],
            endpoint_isolated_t=[str(t) for t in endpoints],
            feasibility_kind=kind,
            matrix=[[str(c) for c in row] for row in solved.matrix],
            rhs=[str(b) for b in solved.rhs],
            proof_residuals=proof,
            family_id=family_id,
            rank=solved.rank,
        )

    def evaluate(self, t: Fraction) -> tuple[Fraction, ...]:
        x0 = tuple(Fraction(v) for v in self.base_point)
        d = tuple(Fraction(v) for v in self.direction)
        return x_at_t(x0, d, t)


@dataclass
class AffineSquareFamilyND:
    polygon_hash: str
    edge_indices: tuple[int, int, int, int]
    orientation: Rotation
    base_point: tuple[str, ...]
    nullspace_basis: list[tuple[str, ...]]
    dimension: int
    matrix: list[list[str]]
    rhs: list[str]
    feasibility_status: Literal["unsupported_exact", "underdetermined"]
    family_id: str
    rank: int

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self, indent: int | None = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, sort_keys=True)

    @classmethod
    def build(
        cls,
        polygon: PolygonCurve,
        edges: tuple[int, int, int, int],
        rotation: Rotation,
        solved: AffineSolveResult,
    ) -> AffineSquareFamilyND:
        dim = len(solved.nullspace)
        payload = {
            "edges": edges,
            "rotation": rotation,
            "rank": solved.rank,
            "dim": dim,
        }
        family_id = hashlib.sha256(
            json.dumps(payload, sort_keys=True).encode()
        ).hexdigest()[:16]
        return cls(
            polygon_hash=polygon.polygon_hash(),
            edge_indices=edges,
            orientation=rotation,
            base_point=tuple(str(v) for v in (solved.particular or (Fraction(0),) * 6)),
            nullspace_basis=[tuple(str(v) for v in ns) for ns in solved.nullspace],
            dimension=dim,
            matrix=[[str(c) for c in row] for row in solved.matrix],
            rhs=[str(b) for b in solved.rhs],
            feasibility_status="unsupported_exact",
            family_id=family_id,
            rank=solved.rank,
        )


@dataclass
class UnsupportedHigherDimensionalFamily:
    """Rank <= 4 positive-dimensional family; exact polytope intersection not implemented."""

    polygon_hash: str
    edge_indices: tuple[int, int, int, int]
    orientation: Rotation
    rank: int
    nullspace_dimension: int
    message: str
    nd_family: AffineSquareFamilyND

    def to_dict(self) -> dict:
        return {
            "polygon_hash": self.polygon_hash,
            "edge_indices": list(self.edge_indices),
            "orientation": self.orientation,
            "rank": self.rank,
            "nullspace_dimension": self.nullspace_dimension,
            "message": self.message,
            "nd_family": self.nd_family.to_dict(),
        }

    def to_json(self, indent: int | None = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, sort_keys=True)

    @classmethod
    def build(
        cls,
        polygon: PolygonCurve,
        edges: tuple[int, int, int, int],
        rotation: Rotation,
        solved: AffineSolveResult,
    ) -> UnsupportedHigherDimensionalFamily:
        nd = AffineSquareFamilyND.build(polygon, edges, rotation, solved)
        return cls(
            polygon_hash=polygon.polygon_hash(),
            edge_indices=edges,
            orientation=rotation,
            rank=solved.rank,
            nullspace_dimension=len(solved.nullspace),
            message=(
                "Exact feasibility for nullspace dimension >= 2 is not implemented. "
                "System recorded without sampling."
            ),
            nd_family=nd,
        )
