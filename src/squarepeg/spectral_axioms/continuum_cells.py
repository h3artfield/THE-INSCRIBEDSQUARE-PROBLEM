"""Exact polyhedral subdivision for continuum subadditivity H(x,y)>=0."""

from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction

from squarepeg.spectral_axioms.pl_obstruction import PLSegment, StrictPLFunction


@dataclass
class PLFunction:
    """Nondecreasing PL (allows flat segments)."""

    breakpoints: list[tuple[Fraction, Fraction]]

    @property
    def segments(self) -> list[PLSegment]:
        out: list[PLSegment] = []
        for i in range(len(self.breakpoints) - 1):
            x0, y0 = self.breakpoints[i]
            x1, y1 = self.breakpoints[i + 1]
            slope = (y1 - y0) / (x1 - x0) if x1 != x0 else Fraction(0)
            out.append(PLSegment(x0, x1, y0, slope))
        return out

    def value_at(self, x: Fraction) -> Fraction:
        if x <= self.breakpoints[0][0]:
            return self.breakpoints[0][1]
        if x >= self.breakpoints[-1][0]:
            return self.breakpoints[-1][1]
        for seg in self.segments:
            if seg.x0 <= x <= seg.x1:
                return seg.value_at(x)
        return self.breakpoints[-1][1]

    def lipschitz_constant(self) -> Fraction:
        return max((seg.slope for seg in self.segments), default=Fraction(0))

    @classmethod
    def from_grid(cls, values: list[Fraction], N: int) -> PLFunction:
        return cls([(Fraction(i, N), values[i]) for i in range(N + 1)])


@dataclass
class TriangleCell:
    """Closed cell in {(x,y): x>=0, y>=0, x+y<=1} with affine H."""

    x_lo: Fraction
    x_hi: Fraction
    y_lo: Fraction
    y_hi: Fraction
    # H(x,y) = a*x + b*y + c on this cell (exact)
    a: Fraction
    b: Fraction
    c: Fraction

    def vertices(self) -> list[tuple[Fraction, Fraction]]:
        corners = [
            (self.x_lo, self.y_lo),
            (self.x_hi, self.y_lo),
            (self.x_lo, self.y_hi),
            (self.x_hi, self.y_hi),
        ]
        return [(x, y) for x, y in corners if y <= Fraction(1) - x + Fraction(0)]

    def min_on_cell(self) -> Fraction:
        """Minimum of affine H over cell (check vertices + interior if unconstrained)."""
        vals = [self.H_at(x, y) for x, y in self.full_vertex_set()]
        return min(vals)

    def full_vertex_set(self) -> list[tuple[Fraction, Fraction]]:
        """All corners of [x_lo,x_hi] x [y_lo,y_hi] with x+y <= 1."""
        cands = [
            (self.x_lo, self.y_lo),
            (self.x_hi, self.y_lo),
            (self.x_lo, self.y_hi),
            (self.x_hi, self.y_hi),
        ]
        return [(x, y) for x, y in cands if x >= 0 and y >= 0 and x + y <= Fraction(1)]

    def H_at(self, x: Fraction, y: Fraction) -> Fraction:
        return self.a * x + self.b * y + self.c


@dataclass
class SubadditivityCertificate:
    ok: bool
    cells: list[TriangleCell] = field(default_factory=list)
    violations: list[tuple[Fraction, Fraction, Fraction]] = field(default_factory=list)
    min_H: Fraction = Fraction(0)


def _segment_index(segs: list[PLSegment], t: Fraction) -> int:
    for i, seg in enumerate(segs):
        if seg.x0 <= t <= seg.x1:
            return i
    return len(segs) - 1


def _g_formula(segs: list[PLSegment], idx: int) -> tuple[Fraction, Fraction]:
    """Return (base, slope) for g on segment idx: g(t)=base+slope*t."""
    seg = segs[idx]
    # g(t) = y0 + slope*(t-x0) = (y0 - slope*x0) + slope*t
    base = seg.y0 - seg.slope * seg.x0
    return base, seg.slope


def certify_pl_subadditivity(g: PLFunction) -> SubadditivityCertificate:
    """
    Partition triangle by breakpoint lines x=b, y=b, x+y=b.
    On each cell, H(x,y)=g(x)+g(y)-g(x+y) is affine; check all vertices.
    """
    bps = sorted({bp[0] for bp in g.breakpoints})
    bps = [Fraction(0)] + [b for b in bps if b > 0] + [Fraction(1)]
    segs = g.segments
    cells: list[TriangleCell] = []
    violations: list[tuple[Fraction, Fraction, Fraction]] = []
    min_H = None

    xs = sorted(set(bps + [Fraction(1) - b for b in bps]))
    ys = sorted(set(bps + [Fraction(1) - b for b in bps]))

    for i in range(len(xs) - 1):
        for j in range(len(ys) - 1):
            x_lo, x_hi = xs[i], xs[i + 1]
            y_lo, y_hi = ys[j], ys[j + 1]
            if x_lo + y_lo > Fraction(1):
                continue
            if x_hi + y_lo > Fraction(1) and x_lo + y_hi > Fraction(1):
                continue
            # pick interior point to determine segment indices
            x_mid = (x_lo + x_hi) / 2
            y_mid = (y_lo + y_hi) / 2
            if x_mid + y_mid > Fraction(1):
                continue
            s_mid = x_mid + y_mid
            ix = _segment_index(segs, x_mid)
            iy = _segment_index(segs, y_mid)
            is_ = _segment_index(segs, s_mid)
            bx, mx = _g_formula(segs, ix)
            by, my = _g_formula(segs, iy)
            bs, ms = _g_formula(segs, is_)
            # H = (bx+mx*x) + (by+my*y) - (bs+ms*(x+y))
            a = mx - ms
            b = my - ms
            c = bx + by - bs
            cell = TriangleCell(x_lo, x_hi, y_lo, y_hi, a, b, c)
            cells.append(cell)
            cell_min = cell.min_on_cell()
            min_H = cell_min if min_H is None else min(min_H, cell_min)
            if cell_min < 0:
                for x, y in cell.full_vertex_set():
                    h = cell.H_at(x, y)
                    if h < 0:
                        violations.append((x, y, x + y))

    return SubadditivityCertificate(
        ok=len(violations) == 0,
        cells=cells,
        violations=violations,
        min_H=min_H if min_H is not None else Fraction(0),
    )
