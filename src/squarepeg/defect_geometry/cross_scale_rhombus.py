"""Cross-scale rhombus / square support pattern search (Directive 022)."""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Literal

from squarepeg.defect_geometry.reference_tower import ReferenceTowerSpec, build_reference_tower, level_radii

Point = tuple[float, float]
SupportPattern = Literal[
    "OUTER_INNER_LEVELS",
    "NONADJACENT_LEVELS",
    "OUTER_CORRIDOR_INNER",
    "FIXED_OUTER_WINDOWS",
    "NONE_CERTIFIED",
]


@dataclass
class CrossScaleCandidate:
    pattern: SupportPattern
    outer_level: int
    inner_level: int
    vertices: tuple[Point, Point, Point, Point]
    side_estimate: float
    separation_estimate: float
    collision_free: bool
    cyclic_order_ok: bool


@dataclass
class CrossScaleSearchResult:
    candidates: list[CrossScaleCandidate]
    geometric_fixed_scale: bool
    certified_cyclic_odd: bool
    best_side_vs_r1: float
    notes: list[str] = field(default_factory=list)


def _polar(r: float, theta: float) -> Point:
    return r * math.cos(theta), r * math.sin(theta)


def search_cross_scale_support(
    spec: ReferenceTowerSpec | None = None,
    max_inner_level: int = 5,
) -> CrossScaleSearchResult:
    """
    Reconnaissance: rhombus vertices from outer gen 0 + inner gen k.
    Fixed outer windows at theta = 0, pi/2, pi, 3pi/2 on r_1.
    """
    s = spec or ReferenceTowerSpec()
    radii = level_radii(s)
    r1 = radii[0]
    candidates: list[CrossScaleCandidate] = []
    thetas = (0.0, math.pi / 2, math.pi, 3 * math.pi / 2)

    for k in range(1, min(max_inner_level, len(radii))):
        rk = radii[k]
        # Pattern: outer at 0 and 3pi/2, inner at pi/2 and pi (cyclic)
        verts = (
            _polar(r1, thetas[0]),
            _polar(rk, thetas[1]),
            _polar(rk, thetas[2]),
            _polar(r1, thetas[3]),
        )
        sides = [
            math.hypot(verts[i][0] - verts[(i + 1) % 4][0], verts[i][1] - verts[(i + 1) % 4][1])
            for i in range(4)
        ]
        side_min = min(sides)
        sep = min(
            math.hypot(verts[0][0] - verts[1][0], verts[0][1] - verts[1][1]),
            math.hypot(verts[2][0] - verts[3][0], verts[2][1] - verts[3][1]),
        )
        # Collision: inner vertices must not coincide; need side ~ O(r1)
        collision_free = side_min > 0.05 * r1 and sep > 0.02 * r1
        candidates.append(
            CrossScaleCandidate(
                pattern="OUTER_INNER_LEVELS",
                outer_level=0,
                inner_level=k,
                vertices=verts,
                side_estimate=side_min,
                separation_estimate=sep,
                collision_free=collision_free,
                cyclic_order_ok=True,
            )
        )

    best = max((c.side_estimate for c in candidates), default=0.0)
    geometric = any(c.collision_free and c.side_estimate >= 0.12 * r1 for c in candidates)
    # T039 cyclic-odd certificate applies to single-level star-annular packets only (Directive 021).
    certified = False
    return CrossScaleSearchResult(
        candidates=candidates,
        geometric_fixed_scale=geometric,
        certified_cyclic_odd=certified,
        best_side_vs_r1=best / r1 if r1 > 0 else 0.0,
        notes=[
            "Inner-generation vertices at level k have characteristic scale r_k = lambda^k r_1",
            "k=1 geometric quadrilateral may have side ~ O(r_1); k>=2 collapses below 0.12 r_1",
            "No cross-scale w_1-certified rhombus family on full tower curve",
        ],
    )
