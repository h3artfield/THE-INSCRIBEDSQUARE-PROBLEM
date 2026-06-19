"""Self-similar curves: Koch snowflake boundary (nonrectifiable, finite p-variation for p>log4/log3)."""

from __future__ import annotations

from fractions import Fraction

from squarepeg.variation.p_variation import FracPoint, p_variation_frac, total_variation

Point = FracPoint

# Koch curve: each segment replaced by 4 segments of length 1/3.
# Hausdorff dimension log(4)/log(3); finite p-variation iff p > log(4)/log(3) ≈ 1.2619.


def koch_points(iterations: int) -> list[Point]:
    """Generate Koch curve from (0,0) to (1,0) as rational approximants."""
    pts: list[Point] = [(Fraction(0), Fraction(0)), (Fraction(1), Fraction(0))]

    def subdivide(a: Point, b: Point) -> list[Point]:
        from math import cos, sin, pi

        ax, ay = float(a[0]), float(a[1])
        bx, by = float(b[0]), float(b[1])
        dx, dy = bx - ax, by - ay
        p1 = (ax + dx / 3, ay + dy / 3)
        p3 = (ax + 2 * dx / 3, ay + 2 * dy / 3)
        ang = pi / 3
        cx = p1[0] + (p3[0] - p1[0]) * cos(ang) - (p3[1] - p1[1]) * sin(ang)
        cy = p1[1] + (p3[0] - p1[0]) * sin(ang) + (p3[1] - p1[1]) * cos(ang)
        # simpler: rotate p2-p1 by 60° and add to p1
        import math

        vx, vy = p3[0] - p1[0], p3[1] - p1[1]
        la = math.radians(60)
        rx = vx * math.cos(la) - vy * math.sin(la)
        ry = vx * math.sin(la) + vy * math.cos(la)
        peak = (p1[0] + rx, p1[1] + ry)
        return [
            a,
            (Fraction(p1[0]).limit_denominator(10**6), Fraction(p1[1]).limit_denominator(10**6)),
            (Fraction(peak[0]).limit_denominator(10**6), Fraction(peak[1]).limit_denominator(10**6)),
            (Fraction(p3[0]).limit_denominator(10**6), Fraction(p3[1]).limit_denominator(10**6)),
            b,
        ]

    for _ in range(iterations):
        new_pts: list[Point] = []
        for i in range(len(pts) - 1):
            seg = subdivide(pts[i], pts[i + 1])
            new_pts.extend(seg[:-1])
        new_pts.append(pts[-1])
        pts = new_pts
    return pts


def koch_variation_exponent() -> float:
    import math

    return math.log(4) / math.log(3)


def koch_is_nonrectifiable(iterations: int) -> bool:
    """Length grows by factor 4/3 each iteration -> infinite as iterations -> inf."""
    pts = koch_points(iterations)
    return iterations >= 2 and p_variation_frac(pts, 1.0) > 1.5


def koch_p_variation(iterations: int, p: float) -> float:
    return p_variation_frac(koch_points(iterations), p)
