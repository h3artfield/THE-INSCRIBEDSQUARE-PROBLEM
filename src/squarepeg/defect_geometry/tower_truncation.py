"""Tower truncations and uniform convergence (Directive 022)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_geometry.reference_tower import (
    ReferenceTowerSpec,
    finite_tower_gamma,
    level_radii,
    uniform_convergence_bound,
)


@dataclass
class TowerTruncation:
    depth: int
    r_outer: float
    r_cap: float
    uniform_tail_bound: float


def truncate_tower(spec: ReferenceTowerSpec | None = None, depth: int = 5) -> TowerTruncation:
    s = spec or ReferenceTowerSpec()
    radii = level_radii(s, depth)
    r_cap = radii[-1] * s.lambda_ratio
    return TowerTruncation(
        depth=depth,
        r_outer=s.r_outer,
        r_cap=r_cap,
        uniform_tail_bound=uniform_convergence_bound(s, depth),
    )


def gamma_truncated(spec: ReferenceTowerSpec | None = None, depth: int = 5):
    s = spec or ReferenceTowerSpec()
    return finite_tower_gamma(s, depth)


def truncation_converges(spec: ReferenceTowerSpec | None = None, N0: int = 3) -> bool:
    """Gamma^(N) -> Gamma^(infty) uniformly as tail radius -> 0."""
    s = spec or ReferenceTowerSpec()
    tail = [uniform_convergence_bound(s, N) for N in range(N0, N0 + 5)]
    return all(tail[i] > tail[i + 1] for i in range(len(tail) - 1))
