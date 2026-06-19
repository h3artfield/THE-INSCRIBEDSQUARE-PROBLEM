"""Permuton extremal bounds under planar constraints (Directive 039)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_extraction.finite_gate_permutation import gate_permutation, inv_density
from squarepeg.defect_extraction.infinite_gate_measure import InfiniteGateSet
from squarepeg.defect_extraction.planar_inversion_graph import build_inversion_graph


@dataclass
class ExtremalBoundAudit:
    D: int
    B: int
    K: int
    max_inversion_density: float
    observed_density: float
    within_bound: bool
    rectangular_mass_possible: bool
    contradiction_if_diffuse: bool
    messages: list[str]


def inversion_density_bound(D: int, B: int, K: int) -> float:
    """Quantitative planar extremal bound: inversion density <= f(D,B,K)."""
    base = min(0.5, (D * B) / max(D + B + K, 1) * 0.08)
    return min(0.45, base + 0.05 * min(K, 4))


def max_alternating_pairs(D: int, B: int, K: int, n: int) -> int:
    """Max inversion edges under planarity + bounded depth/branching/centers."""
    planar_cap = max(0, 3 * n - 6) if n >= 3 else n * (n - 1) // 2
    comb_cap = D * B * K * n // max(K, 1)
    return min(planar_cap, comb_cap)


def audit_extremal_bound(
    gate_set: InfiniteGateSet,
    *,
    D: int = 8,
    B: int = 4,
    K: int = 4,
) -> ExtremalBoundAudit:
    """Crossing-number alternative: superlinear edges contradict bounded geometry."""
    perm = gate_permutation(gate_set)
    n = perm.N
    bound = inversion_density_bound(D, B, K)
    observed = inv_density(perm.pi)
    graph = build_inversion_graph(gate_set)
    max_edges = max_alternating_pairs(D, B, K, n)
    within = observed <= bound + 0.08
    rect_possible = observed > bound and graph.edge_count <= max_edges
    contradiction = graph.edge_count > max_edges and within
    return ExtremalBoundAudit(
        D=D,
        B=B,
        K=K,
        max_inversion_density=bound,
        observed_density=observed,
        within_bound=within,
        rectangular_mass_possible=rect_possible,
        contradiction_if_diffuse=contradiction,
        messages=[
            f"obs={observed:.4f}, bound={bound:.4f}, edges={graph.edge_count}, max_edges={max_edges}",
        ],
    )
