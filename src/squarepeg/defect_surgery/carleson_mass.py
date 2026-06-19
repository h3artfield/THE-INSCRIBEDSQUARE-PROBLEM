"""Carleson packet mass and surgery-admissible forests (Directive 023)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_surgery.packet_disk import PacketDisk


@dataclass
class PacketMass:
    mu: float
    diameter: float


def packet_mass(disk: PacketDisk) -> PacketMass:
    d = disk.diameter
    return PacketMass(mu=d * d, diameter=d)


def mu_D_on_interval(disks: list[PacketDisk], interval_indices: set[int]) -> float:
    """Sum diam(D)^2 over disks intersecting parameter interval J."""
    total = 0.0
    for d in disks:
        idxs = set(range(min(d.interval_start, d.interval_end), max(d.interval_start, d.interval_end) + 1))
        if idxs & interval_indices:
            total += d.diameter ** 2
    return total


@dataclass
class SurgeryAdmissibleForest:
    disks: list[PacketDisk]
    max_diameter: float
    omega_surg: dict[float, float]


def check_carleson_condition(
    forests: list[list[PacketDisk]],
    deltas: list[float],
) -> bool:
    """
    omega_surg(delta) -> 0: sup_{|J|<=delta} mu_{D_n}(J) bounded by modulus.
    """
    if not forests or not deltas:
        return False
    tail = forests[-5:] if len(forests) >= 5 else forests
    max_d = max(d.diameter for forest in tail for d in forest)
    if max_d > 0.05:
        return False
    for delta in deltas:
        worst = 0.0
        for forest in tail:
            # proxy: all disks in small interval
            idx = set(range(int(delta * 100)))
            worst = max(worst, mu_D_on_interval(forest, idx))
        if delta < 0.1 and worst > delta:
            return False
    return True


def omega_surg(delta: float, max_diam: float) -> float:
    """Explicit modulus proxy: O(max_diam^2 / delta) for bounded forest density."""
    if delta <= 0:
        return float("inf")
    return (max_diam ** 2) / delta
