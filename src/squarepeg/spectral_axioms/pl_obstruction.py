"""Finite-PL obstruction lemma and slope analysis."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction


@dataclass(frozen=True)
class PLSegment:
    x0: Fraction
    x1: Fraction
    y0: Fraction
    slope: Fraction

    def contains(self, x: Fraction) -> bool:
        return self.x0 <= x <= self.x1

    def value_at(self, x: Fraction) -> Fraction:
        return self.y0 + self.slope * (x - self.x0)


@dataclass
class StrictPLFunction:
    """Strictly increasing PL function with rational breakpoints."""

    breakpoints: list[tuple[Fraction, Fraction]]

    def __post_init__(self) -> None:
        bps = self.breakpoints
        if bps[0][0] != 0 or bps[-1][0] != 1:
            raise ValueError("breakpoints must span [0,1]")
        for i in range(len(bps) - 1):
            x0, y0 = bps[i]
            x1, y1 = bps[i + 1]
            if x1 <= x0:
                raise ValueError("breakpoints must be strictly increasing in x")
            if y1 <= y0:
                raise ValueError("strict increase required")

    @property
    def segments(self) -> list[PLSegment]:
        out: list[PLSegment] = []
        for i in range(len(self.breakpoints) - 1):
            x0, y0 = self.breakpoints[i]
            x1, y1 = self.breakpoints[i + 1]
            slope = (y1 - y0) / (x1 - x0)
            out.append(PLSegment(x0, x1, y0, slope))
        return out

    def slope_at_half(self) -> tuple[str, Fraction]:
        """Return ('interior'|'breakpoint', positive slope or average)."""
        half = Fraction(1, 2)
        segs = self.segments
        for seg in segs:
            if seg.x0 < half < seg.x1:
                return "interior", seg.slope
        for i, (x, _) in enumerate(self.breakpoints):
            if x == half:
                s_left = segs[i - 1].slope if i > 0 else segs[0].slope
                s_right = segs[i].slope if i < len(segs) else segs[-1].slope
                return "breakpoint", (s_left + s_right) / 2
        raise ValueError("1/2 not in domain")

    def D_h(self, h: Fraction) -> Fraction:
        half = Fraction(1, 2)
        lo, hi = half - h, half + h
        return (self.value_at(hi) - self.value_at(lo)) / (2 * h)

    def value_at(self, x: Fraction) -> Fraction:
        if x <= self.breakpoints[0][0]:
            return self.breakpoints[0][1]
        if x >= self.breakpoints[-1][0]:
            return self.breakpoints[-1][1]
        for seg in self.segments:
            if seg.x0 <= x <= seg.x1:
                return seg.value_at(x)
        return self.breakpoints[-1][1]

    def D_plus_lower_bound(self) -> Fraction:
        """Positive lower bound on D^+(g, 1/2) from obstruction lemma."""
        _, slope = self.slope_at_half()
        return slope

    def is_strictly_increasing(self) -> bool:
        return all(seg.slope > 0 for seg in self.segments)

    def flat_intervals(self) -> list[tuple[Fraction, Fraction]]:
        return [
            (seg.x0, seg.x1)
            for seg in self.segments
            if seg.slope == 0
        ]


def finite_pl_obstruction_holds(g: StrictPLFunction) -> bool:
    """Obstruction lemma: strict finite PL => D^+(g,1/2) > 0."""
    return g.D_plus_lower_bound() > 0


def weak_pl_from_grid(values: list[Fraction], N: int) -> list[tuple[Fraction, Fraction]]:
    """Breakpoints at every grid point (allows zero-slope segments)."""
    return [(Fraction(i, N), values[i]) for i in range(N + 1)]


def strict_pl_from_grid(values: list[Fraction], N: int, delta: Fraction) -> StrictPLFunction | None:
    """Build strict PL only if all consecutive grid gaps >= delta."""
    for i in range(N):
        if values[i + 1] - values[i] < delta:
            return None
    return StrictPLFunction(weak_pl_from_grid(values, N))
