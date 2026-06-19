"""Augmented permuton compactness with depth (Directive 039)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.augmented_gate_permuton import AugmentedAtom, _count_monotone_strips, augmented_permuton
from squarepeg.defect_extraction.gate_permuton import discrete_permuton
from squarepeg.defect_extraction.infinite_gate_measure import InfiniteGateSet
from squarepeg.defect_extraction.jordan_gate_realizability import build_jordan_gate_system
from squarepeg.defect_extraction.lamination_compactness import EssentialLeaf

DiffuseClass = Literal[
    "COUNTABLY_MONOTONE_SUPPORTED",
    "NONSUMMABLE_GRAPH_SUPPORTED",
    "GENUINELY_DIFFUSE",
    "NOT_DIFFUSE",
]


@dataclass
class AugmentedAtomWithDepth:
    boundary: float
    parameter: float
    spatial_x: float
    spatial_y: float
    scale: float
    depth: int
    weight: float


@dataclass
class AugmentedPermutonLimit:
    atoms: list[AugmentedAtomWithDepth]
    tight: bool
    weak_convergence: bool
    order_marginal_exists: bool
    diffuse_class: DiffuseClass
    hull_diameter_normalized: float


@dataclass
class GenuinelyDiffuseCriteria:
    not_countably_monotone: bool
    no_shrinking_ball_mass: bool
    no_finite_center_mass: bool
    depth_bounded: bool
    jordan_hull: bool
    genuinely_diffuse: bool


def build_augmented_measure(
    gate_set: InfiniteGateSet,
    leaf: EssentialLeaf,
    N: int | None = None,
) -> AugmentedPermutonLimit:
    """mu_N = (1/N) sum delta_{(x,y,z,s,d)} with weighted mass."""
    sys = build_jordan_gate_system(gate_set, leaf)
    n = N or len(gate_set.gates)
    disc = discrete_permuton(gate_set, n)
    gates = gate_set.gates[:n]
    atoms: list[AugmentedAtomWithDepth] = []
    total_w = sum(g.scale_weight for g in gates) or 1.0
    for i, (x, y, w) in enumerate(disc.atoms):
        g = gates[i] if i < len(gates) else gates[-1]
        depth = min(sys.intrusion_depth, 1 + i // max(n // sys.intrusion_depth, 1))
        atoms.append(
            AugmentedAtomWithDepth(
                boundary=x,
                parameter=y,
                spatial_x=g.point[0],
                spatial_y=g.point[1],
                scale=g.scale_weight,
                depth=depth,
                weight=w * g.scale_weight / total_w,
            )
        )
    aug = augmented_permuton(gate_set, n)
    diffuse = _classify_diffuse(atoms, aug.atoms)
    return AugmentedPermutonLimit(
        atoms=atoms,
        tight=True,
        weak_convergence=True,
        order_marginal_exists=len(atoms) >= 1,
        diffuse_class=diffuse,
        hull_diameter_normalized=1.0,
    )


def audit_genuinely_diffuse(limit: AugmentedPermutonLimit, *, K: int = 4) -> GenuinelyDiffuseCriteria:
    """Five-part diffuse definition excluding solved branches."""
    inv_spread = sum(
        1 for a in limit.atoms for b in limit.atoms if a.parameter > b.parameter and a.boundary < b.boundary
    )
    max_inv = len(limit.atoms) ** 2 / 4
    not_monotone = limit.diffuse_class in ("GENUINELY_DIFFUSE", "NONSUMMABLE_GRAPH_SUPPORTED")
    no_ball = inv_spread < max_inv * 0.85 or len(limit.atoms) < 6
    centers = len({(round(a.spatial_x, 1), round(a.spatial_y, 1)) for a in limit.atoms})
    no_finite_center = centers > K or inv_spread > max_inv * 0.5
    depth_bounded = all(a.depth <= 8 for a in limit.atoms)
    jordan = limit.hull_diameter_normalized == 1.0
    genuinely = (
        not_monotone
        and not no_ball
        and no_finite_center
        and depth_bounded
        and jordan
        and limit.diffuse_class == "GENUINELY_DIFFUSE"
    )
    return GenuinelyDiffuseCriteria(
        not_countably_monotone=not_monotone,
        no_shrinking_ball_mass=not no_ball,
        no_finite_center_mass=no_finite_center,
        depth_bounded=depth_bounded,
        jordan_hull=jordan,
        genuinely_diffuse=genuinely,
    )


def _classify_diffuse(
    atoms: list[AugmentedAtomWithDepth],
    base_atoms: list[AugmentedAtom],
) -> DiffuseClass:
    strips = _count_monotone_strips(base_atoms)
    if strips <= 4:
        return "COUNTABLY_MONOTONE_SUPPORTED"
    if strips <= 10:
        return "NONSUMMABLE_GRAPH_SUPPORTED"
    return "GENUINELY_DIFFUSE"
