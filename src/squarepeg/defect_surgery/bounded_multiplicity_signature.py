"""BOUNDED_MULTIPLICITY_SIGNATURE (Directive 025)."""

from __future__ import annotations

from dataclasses import dataclass

from squarepeg.area_variation.inequality_certificate import SHARP_CANDIDATE
from squarepeg.defect_surgery.attachment_chain import mu1_on_interval, mu2_on_interval
from squarepeg.defect_surgery.exact_component_decomposition import PathComponent, master_area_identity
from squarepeg.defect_surgery.packet_disk import PacketDisk


@dataclass
class BoundedMultiplicityAudit:
    multiplicity: int
    mu1_bound: float
    mu2_bound: float
    sigma_bound: float
    beta_bound: float
    implies_signature: bool


def count_packets_on_interval(disks: list[PacketDisk], interval: set[int]) -> int:
    return sum(1 for d in disks if _hits(d, interval))


def _hits(d: PacketDisk, interval: set[int]) -> bool:
    lo = min(d.interval_start, d.interval_end)
    hi = max(d.interval_start, d.interval_end)
    return bool(set(range(lo, hi + 1)) & interval)


def bounded_multiplicity_bounds(
    *,
    multiplicity: int,
    max_diam: float,
) -> tuple[float, float, float]:
    """
    At most M packets on |J|<=delta with diam <= r:
    mu1 <= M r, mu2 <= M r^2, |A_Z| <= M (pi/4) r^2 (one chord per packet).
    """
    mu1 = multiplicity * max_diam
    mu2 = multiplicity * max_diam ** 2
    sigma = multiplicity * SHARP_CANDIDATE * max_diam ** 2
    return mu1, mu2, sigma


def audit_bounded_multiplicity_signature(
    disks: list[PacketDisk],
    components: list[PathComponent],
    interval: set[int],
    *,
    max_multiplicity: int = 3,
    max_diam: float = 0.01,
) -> BoundedMultiplicityAudit:
    m = count_packets_on_interval(disks, interval)
    mu1, mu2, sigma_b = bounded_multiplicity_bounds(
        multiplicity=min(m, max_multiplicity), max_diam=max_diam
    )
    beta = sum(abs(c.intrinsic_area) for c in components if c.kind == "retained")
    ident = master_area_identity(components)
    sigma_actual = abs(ident.attachment_chain_area)
    ok = m <= max_multiplicity and sigma_actual <= sigma_b + beta + 1e-6
    return BoundedMultiplicityAudit(
        multiplicity=m,
        mu1_bound=mu1,
        mu2_bound=mu2,
        sigma_bound=sigma_b,
        beta_bound=beta,
        implies_signature=ok and max_diam < 0.02,
    )
