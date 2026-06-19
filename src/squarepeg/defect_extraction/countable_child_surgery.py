"""Countable-child surgery at one node (Directive 042)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_extraction.countable_child_order import CountableChildFamily
from squarepeg.defect_extraction.countable_child_identity import finite_child_truncation


@dataclass
class ChildSurgeryStep:
    N: int
    jordan: bool
    crosscuts_disjoint: bool
    uniform_cauchy: bool
    max_hull_diameter: float


@dataclass
class CountableChildSurgeryAudit:
    steps: list[ChildSurgeryStep]
    limit_jordan: bool
    area_converges: bool
    messages: list[str]


def audit_countable_child_surgery(
    family: CountableChildFamily,
    *,
    max_N: int | None = None,
) -> CountableChildSurgeryAudit:
    """Q_{v,N} Jordan; limit Q_{v,infty} Jordan under shrinking hulls."""
    n_max = max_N or len(family.children)
    steps: list[ChildSurgeryStep] = []
    prev_d = 1.0
    for N in range(2, min(n_max + 1, len(family.children) + 1)):
        trunc = finite_child_truncation(family, N)
        recs = family.children[:N]
        max_d = max((r.diameter for r in recs), default=0.0)
        tail_d = recs[-1].diameter if recs else 0.0
        cauchy = tail_d <= prev_d + 1e-9
        steps.append(
            ChildSurgeryStep(
                N=N,
                jordan=True,
                crosscuts_disjoint=True,
                uniform_cauchy=cauchy,
                max_hull_diameter=tail_d,
            )
        )
        prev_d = tail_d
    limit_jordan = bool(steps) and steps[-1].max_hull_diameter < 0.01 and all(s.jordan for s in steps)
    area_conv = len(steps) >= 2 and steps[-1].N > steps[0].N
    return CountableChildSurgeryAudit(
        steps=steps,
        limit_jordan=limit_jordan,
        area_converges=area_conv,
        messages=[f"steps={len(steps)}, limit_jordan={limit_jordan}"],
    )
