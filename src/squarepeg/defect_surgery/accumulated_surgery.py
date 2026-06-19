"""Accumulated surgery decomposition (Directive 024)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_surgery.attachment_chain import (
    AttachmentChain,
    attachment_chain_area,
    chain_controls,
    mu1_on_interval,
    mu2_on_interval,
)
from squarepeg.defect_surgery.concatenation_area import finite_concatenation_identity
from squarepeg.defect_surgery.local_surgery import apply_local_surgery
from squarepeg.defect_surgery.nested_forest import PacketForest, apply_disjoint_surgeries, maximal_disks
from squarepeg.defect_surgery.packet_disk import PacketDisk, Point


@dataclass
class SurgeredDecomposition:
    retained_areas: list[float]
    attachment_area: float
    wedge_corrections: float
    total_area: float
    alpha_bound: float


@dataclass
class AccumulatedEstimate:
    beta: float
    a_att: float
    mu1: float
    mu2: float
    omega_gamma: float
    alpha_upper: float


def beta_retained_skeleton(
    retained_paths: list[list[Point]],
) -> float:
    """Sup sum of |A(R_i)| over retained components in interval."""
    from squarepeg.defect_surgery.concatenation_area import relative_area_path

    return sum(abs(relative_area_path(p)) for p in retained_paths)


def decompose_surgered_subarc(
    retained_paths: list[list[Point]],
    chord_paths: list[list[Point]],
) -> SurgeredDecomposition:
    """Q_n|_J = R_0 * C_1 * R_1 * ... using concatenation identity."""
    all_paths = []
    for i, r in enumerate(retained_paths):
        all_paths.append(r)
        if i < len(chord_paths):
            all_paths.append(chord_paths[i])
    dec = finite_concatenation_identity(all_paths)
    ret_sum = sum(abs(a) for a in dec.component_areas[: len(retained_paths)])
    return SurgeredDecomposition(
        retained_areas=dec.component_areas,
        attachment_area=sum(dec.component_areas[len(retained_paths) :]),
        wedge_corrections=sum(dec.wedge_terms),
        total_area=dec.reconstructed,
        alpha_bound=abs(dec.reconstructed),
    )


def accumulated_area_estimate(
    *,
    beta: float,
    a_att: float,
    mu1: float,
    mu2: float,
    omega_gamma: float,
    C: float = 1.0,
) -> AccumulatedEstimate:
    """
    alpha_{Q_n}(delta) <= beta + |A_att| + C omega mu1 + C mu2 + o_n(1).
    """
    alpha_upper = beta + abs(a_att) + C * omega_gamma * mu1 + C * mu2
    return AccumulatedEstimate(
        beta=beta,
        a_att=a_att,
        mu1=mu1,
        mu2=mu2,
        omega_gamma=omega_gamma,
        alpha_upper=alpha_upper,
    )


def simultaneous_surgery_jordan(
    vertices: list[Point],
    forest: PacketForest,
) -> tuple[list[Point], bool]:
    """Apply maximal disjoint surgeries; return (Q vertices, is Jordan)."""
    maximal = PacketForest(disks=maximal_disks(forest))
    out, results = apply_disjoint_surgeries(vertices, maximal)
    return out, all(r.is_jordan for r in results)
