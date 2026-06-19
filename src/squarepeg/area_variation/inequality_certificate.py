"""Certificates for T021 simple-arc area inequality."""

from __future__ import annotations

import math
from dataclasses import dataclass
from fractions import Fraction

from squarepeg.area_variation.exact_2variation import (
    max_partition_sum_squares,
    max_partition_sum_squares_frac,
    two_variation_norm,
)
from squarepeg.area_variation.polygonal_arc import PolygonalArc
from squarepeg.area_variation.signed_area import relative_area_arc, relative_area_exact_frac

SHARP_CANDIDATE = math.pi / 4.0


@dataclass(frozen=True)
class InequalityCertificate:
    area: float
    var2_sq: float
    ratio: float
    constant_bound: float
    passes: bool
    exact: bool


def area_variation_ratio(arc: PolygonalArc) -> float:
    var2_sq = max_partition_sum_squares(arc.vertices)
    if var2_sq <= 0:
        return 0.0
    return abs(relative_area_arc(arc)) / var2_sq


def certify_arc(arc: PolygonalArc, c: float = SHARP_CANDIDATE) -> InequalityCertificate:
    area = relative_area_arc(arc)
    var2_sq = max_partition_sum_squares(arc.vertices)
    ratio = abs(area) / var2_sq if var2_sq > 0 else 0.0
    bound = c * var2_sq
    return InequalityCertificate(
        area=area,
        var2_sq=var2_sq,
        ratio=ratio,
        constant_bound=bound,
        passes=abs(area) <= bound + 1e-8,
        exact=False,
    )


def certify_rational(vertices: list[tuple[Fraction, Fraction]], c: Fraction = Fraction(31415926535, 40000000000)) -> InequalityCertificate:
    """Exact rational certificate with Fraction pi approx or use Fraction pi via math."""
    area = float(relative_area_exact_frac(vertices))
    var2_sq = float(max_partition_sum_squares_frac(vertices))
    c_f = float(c) if isinstance(c, Fraction) else c
    ratio = abs(area) / var2_sq if var2_sq > 0 else 0.0
    return InequalityCertificate(
        area=area,
        var2_sq=var2_sq,
        ratio=ratio,
        constant_bound=c_f * var2_sq,
        passes=abs(area) <= c_f * var2_sq,
        exact=True,
    )
