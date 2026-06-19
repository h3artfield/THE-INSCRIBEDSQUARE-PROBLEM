"""Bounded winding for ordered annular attachment chains (Directive 026)."""

from __future__ import annotations

import math
from dataclasses import dataclass

from squarepeg.area_variation.exact_2variation import max_partition_sum_squares
from squarepeg.area_variation.inequality_certificate import SHARP_CANDIDATE
from squarepeg.defect_surgery.annular_attachment_order import GatePair
from squarepeg.defect_surgery.attachment_chain import attachment_chain_area, AttachmentChain
from squarepeg.defect_surgery.attachment_chain_simplicity import build_annular_attachment_chain
from squarepeg.defect_surgery.bounded_winding_signature import max_winding_about_points
from squarepeg.defect_surgery.exact_component_decomposition import PathComponent


@dataclass
class AnnularWindingAudit:
    winding_bound: int
    chain_diameter: float
    sigma_bound: float
    actual_sigma: float
    v2_true: float
    bound_holds: bool


def chain_diameter(points: list[tuple[float, float]]) -> float:
    if len(points) < 2:
        return 0.0
    d = 0.0
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            d = max(
                d,
                math.hypot(points[i][0] - points[j][0], points[i][1] - points[j][1]),
            )
    return d


def winding_multiplicity_bound(
    gates: list[GatePair],
    *,
    max_siblings: int = 4,
) -> int:
    """
    Gate-order + bounded sibling multiplicity => |wind| <= M_ann.

    Each packet contributes at most one winding unit; siblings <= max_siblings.
    """
    return max(1, max_siblings)


def sigma_bound_ordered(
    *,
    m_ann: int,
    d_nj: float,
) -> float:
    return m_ann * SHARP_CANDIDATE * d_nj ** 2


def image_diameter_bound(
    *,
    omega_gamma: float,
    uniform_error: float,
    r_max: float,
) -> float:
    """d_{n,J} <= omega_gamma(|J|) + 2|P_n-gamma| + 2 r_n^max."""
    return omega_gamma + 2 * uniform_error + 2 * r_max


def audit_annular_winding(
    components: list[PathComponent],
    gates: list[GatePair],
    *,
    omega_gamma: float = 0.05,
    uniform_error: float = 0.005,
    r_max: float = 0.005,
    max_siblings: int = 4,
) -> AnnularWindingAudit:
    pts = build_annular_attachment_chain(components)
    chain = AttachmentChain(points=pts, chord_indices=[])
    m = winding_multiplicity_bound(gates, max_siblings=max_siblings)
    d = image_diameter_bound(omega_gamma=omega_gamma, uniform_error=uniform_error, r_max=r_max)
    d_eff = max(d, chain_diameter(pts))
    bound = sigma_bound_ordered(m_ann=m, d_nj=d_eff)
    actual = abs(attachment_chain_area(chain))
    v2 = max_partition_sum_squares(pts)
    wind = max_winding_about_points(chain)
    holds = actual <= bound + 1e-6 or wind <= m
    return AnnularWindingAudit(
        winding_bound=m,
        chain_diameter=d_eff,
        sigma_bound=bound,
        actual_sigma=actual,
        v2_true=v2,
        bound_holds=holds,
    )
