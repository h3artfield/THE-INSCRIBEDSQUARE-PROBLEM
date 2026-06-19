"""Summable ray signature (Directive 040)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.defect_extraction.intrusion_ray_geometry import IntrusionRay, extract_ray
from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree


@dataclass
class RayScaleMass:
    S_ray: float
    S_area: float
    S_gate: float
    summable_ray: bool
    summable_area: bool
    summable_gate: bool


@dataclass
class AttachmentChain:
    truncation_N: int
    intrinsic_tail_area: float
    cross_join_area: float
    crosscut_area: float
    skeleton_correction: float


@dataclass
class SummableRaySignatureAudit:
    scale_mass: RayScaleMass
    satisfies_summable: bool
    tail_vanishes: bool
    chains: list[AttachmentChain]
    messages: list[str]


def ray_scale_mass(ray: IntrusionRay) -> RayScaleMass:
    radii = [d.diameter for d in ray.data]
    gates = [d.gate_count for d in ray.data]
    s_ray = sum(radii)
    s_area = sum(r * r for r in radii)
    s_gate = sum(g * g * r * r for g, r in zip(gates, radii))
    return RayScaleMass(
        S_ray=s_ray,
        S_area=s_area,
        S_gate=s_gate,
        summable_ray=s_ray < 3.0,
        summable_area=s_area < 2.0,
        summable_gate=s_gate < 5.0,
    )


def build_attachment_chains(ray: IntrusionRay, *, heads: list[int] | None = None) -> list[AttachmentChain]:
    """Finite truncations Z_N and attachment chain estimates."""
    heads = heads or [2, 4, 8, min(16, len(ray.data))]
    chains: list[AttachmentChain] = []
    total_defect = sum(d.defect for d in ray.data) or 1.0
    for N in heads:
        if N >= len(ray.data):
            continue
        tail = ray.data[N:]
        tail_area = sum(d.defect for d in tail)
        join = 0.5 * sum(ray.data[i].defect * ray.data[j].defect for i in range(N) for j in range(N, len(ray.data)))
        crosscut = ray.data[N - 1].diameter * 0.5 if N > 0 else 0.0
        chains.append(
            AttachmentChain(
                truncation_N=N,
                intrinsic_tail_area=tail_area,
                cross_join_area=join,
                crosscut_area=crosscut,
                skeleton_correction=0.05 * tail_area,
            )
        )
    return chains


def audit_summable_ray_signature(tree: CanonicalIntrusionTree) -> SummableRaySignatureAudit | None:
    """SUMMABLE_RAY_SIGNATURE: lim sup |A_{Z_inf - Z_N}| = 0."""
    ray = extract_ray(tree)
    if not ray:
        return None
    mass = ray_scale_mass(ray)
    chains = build_attachment_chains(ray)
    satisfies = mass.summable_gate or (mass.summable_area and mass.summable_ray)
    tail_vanishes = True
    if chains:
        tail_vanishes = chains[-1].intrinsic_tail_area < 0.15 * sum(d.defect for d in ray.data)
    return SummableRaySignatureAudit(
        scale_mass=mass,
        satisfies_summable=satisfies,
        tail_vanishes=tail_vanishes,
        chains=chains,
        messages=[f"S_gate={mass.S_gate:.4f}, summable={satisfies}"],
    )
