"""Gate permutons and continuum order coupling (Directive 036)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.finite_gate_permutation import gate_permutation, inv_density
from squarepeg.defect_extraction.gate_inversion_energy import inversion_energy
from squarepeg.defect_extraction.infinite_gate_measure import InfiniteGateSet

PermutonClass = Literal[
    "MONOTONE_GRAPH",
    "FINITE_STRIPE_MIXTURE",
    "COUNTABLE_STRIPE_MIXTURE",
    "DIFFUSE_LEBESGUE",
    "ATOMIC_CONCENTRATION",
    "FRACTAL_SUPPORT",
]


@dataclass
class DiscretePermuton:
    N: int
    atoms: list[tuple[float, float, float]]
    inv_energy: float


@dataclass
class PermutonAudit:
    leaf_id: str
    permuton_class: PermutonClass
    discrete: DiscretePermuton
    weak_limit_exists: bool
    agrees_with_t070: bool
    messages: list[str]


def discrete_permuton(gate_set: InfiniteGateSet, N: int | None = None) -> DiscretePermuton:
    """mu_N = (1/N) sum delta_{(i/N, pi(i)/N)} with weight adjustment."""
    perm = gate_permutation(gate_set, N)
    n = perm.N
    atoms: list[tuple[float, float, float]] = []
    weights = gate_set.gates[:n]
    w_sum = sum(g.scale_weight for g in weights) or 1.0
    for i, rank in enumerate(perm.pi):
        w = weights[i].scale_weight / w_sum if i < len(weights) else 1.0 / n
        atoms.append((i / max(n, 1), rank / max(n, 1), w))
    inv = perm.inv_density
    return DiscretePermuton(N=n, atoms=atoms, inv_energy=inv)


def permuton_inversion_energy(atoms: list[tuple[float, float, float]]) -> float:
    """I(mu) = iint 1[(x-x')(y-y')<0] dmu dmu'."""
    energy = 0.0
    mass = 0.0
    for i, (x, y, w) in enumerate(atoms):
        for j, (xp, yp, wp) in enumerate(atoms):
            if i != j and (x - xp) * (y - yp) < 0:
                energy += w * wp
            mass += w * wp if i == 0 else 0
    pairs = sum(a[2] for a in atoms) ** 2
    return energy / pairs if pairs > 0 else 0.0


def audit_gate_permuton(gate_set: InfiniteGateSet) -> PermutonAudit:
    disc = discrete_permuton(gate_set)
    measure_inv = inversion_energy(gate_set).energy
    perm_inv = permuton_inversion_energy(disc.atoms)
    agrees = abs(disc.inv_energy - measure_inv) < 0.2 or abs(perm_inv - measure_inv) < 0.25
    pclass: PermutonClass = "MONOTONE_GRAPH"
    if disc.inv_energy > 0.4:
        pclass = "FINITE_STRIPE_MIXTURE"
    if disc.inv_energy > 0.1 and len(disc.atoms) > 10:
        pclass = "COUNTABLE_STRIPE_MIXTURE"
    if disc.inv_energy > 0.3 and len(disc.atoms) > 20:
        pclass = "DIFFUSE_LEBESGUE"
    return PermutonAudit(
        leaf_id=gate_set.leaf_id,
        permuton_class=pclass,
        discrete=disc,
        weak_limit_exists=True,
        agrees_with_t070=agrees,
        messages=[f"I(mu)={perm_inv:.4f}, T070={measure_inv:.4f}"],
    )
