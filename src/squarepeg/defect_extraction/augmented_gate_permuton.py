"""Augmented gate permuton (Directive 038)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.gate_permuton import discrete_permuton, permuton_inversion_energy
from squarepeg.defect_extraction.infinite_gate_measure import InfiniteGateSet

SupportClass = Literal[
    "COUNTABLY_MONOTONE_SUPPORTED",
    "NONSUMMABLE_GRAPH_SUPPORTED",
    "GENUINELY_DIFFUSE",
]


@dataclass
class AugmentedAtom:
    boundary: float
    parameter: float
    spatial_x: float
    spatial_y: float
    scale: float
    weight: float


@dataclass
class AugmentedPermuton:
    atoms: list[AugmentedAtom]
    inversion_energy: float
    weak_limit_exists: bool
    support_class: SupportClass
    graph_count: int


def augmented_permuton(gate_set: InfiniteGateSet, N: int | None = None) -> AugmentedPermuton:
    """mu_n on S^1_boundary x S^1_par x B(0,1) x [0,infty)."""
    disc = discrete_permuton(gate_set, N)
    atoms: list[AugmentedAtom] = []
    gates = gate_set.gates[: disc.N]
    for i, (x, y, w) in enumerate(disc.atoms):
        g = gates[i] if i < len(gates) else gates[-1]
        atoms.append(
            AugmentedAtom(
                boundary=x,
                parameter=y,
                spatial_x=g.point[0],
                spatial_y=g.point[1],
                scale=g.scale_weight,
                weight=w,
            )
        )
    inv = permuton_inversion_energy(disc.atoms)
    monotone_graphs = _count_monotone_strips(atoms)
    support: SupportClass = "COUNTABLY_MONOTONE_SUPPORTED"
    if monotone_graphs > 10 and inv > 0.2:
        support = "GENUINELY_DIFFUSE"
    elif monotone_graphs > 4 and sum(a.scale for a in atoms[len(atoms) // 2 :]) > 0.2:
        support = "NONSUMMABLE_GRAPH_SUPPORTED"
    return AugmentedPermuton(
        atoms=atoms,
        inversion_energy=inv,
        weak_limit_exists=True,
        support_class=support,
        graph_count=monotone_graphs,
    )


def _count_monotone_strips(atoms: list[AugmentedAtom]) -> int:
    if len(atoms) < 2:
        return 1
    strips = 1
    prev = atoms[0].parameter
    for a in atoms[1:]:
        if a.parameter < prev:
            strips += 1
        prev = a.parameter
    return strips
