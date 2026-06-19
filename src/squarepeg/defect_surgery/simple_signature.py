"""SIMPLE_SIGNATURE => SIGNATURE_CARLESON (Directive 025)."""

from __future__ import annotations

import math
from dataclasses import dataclass

from squarepeg.area_variation.inequality_certificate import SHARP_CANDIDATE
from squarepeg.defect_surgery.attachment_2var_audit import simple_chain_t021_bound, v2_variation_squared
from squarepeg.defect_surgery.attachment_chain import AttachmentChain
from squarepeg.defect_surgery.exact_component_decomposition import PathComponent, master_area_identity


@dataclass
class SimpleSignatureAudit:
    chain_is_simple: bool
    v2_vanishes: bool
    sigma_vanishes: bool
    implies_signature_sigma: bool


def is_simple_polygonal_chain(points: list[tuple[float, float]]) -> bool:
    """No self-intersection except possibly shared endpoints (T021 regime)."""
    n = len(points)
    if n < 3:
        return True
    for i in range(n - 1):
        for j in range(i + 2, n - 1):
            if _segments_proper_intersect(points[i], points[i + 1], points[j], points[j + 1]):
                return False
    return True


def _segments_proper_intersect(p1, p2, p3, p4) -> bool:
    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    d1 = cross(p3, p4, p1)
    d2 = cross(p3, p4, p2)
    d3 = cross(p1, p2, p3)
    d4 = cross(p1, p2, p4)
    return (
        ((d1 > 1e-12 and d2 < -1e-12) or (d1 < -1e-12 and d2 > 1e-12))
        and ((d3 > 1e-12 and d4 < -1e-12) or (d3 < -1e-12 and d4 > 1e-12))
    )


def sigma_bound_simple_chain(chain: AttachmentChain) -> float:
    """T021: |A_Z| <= (pi/4) V_2^2 for simple chains."""
    v2 = v2_variation_squared(chain)
    return SHARP_CANDIDATE * v2


def simple_signature_implies_sigma(
    chain: AttachmentChain,
    *,
    v2_threshold: float = 0.01,
) -> SimpleSignatureAudit:
    simple = is_simple_polygonal_chain(chain.points)
    v2 = v2_variation_squared(chain.points)
    v2_ok = v2 < v2_threshold
    if simple and v2_ok:
        from squarepeg.defect_surgery.attachment_chain import attachment_chain_area

        sigma_ok = abs(attachment_chain_area(chain)) <= SHARP_CANDIDATE * v2 + 1e-8
    else:
        sigma_ok = False
    return SimpleSignatureAudit(
        chain_is_simple=simple,
        v2_vanishes=v2_ok,
        sigma_vanishes=sigma_ok,
        implies_signature_sigma=simple and v2_ok and sigma_ok,
    )


def simple_signature_implies_carleson_sigma(
    components: list[PathComponent],
    *,
    v2_threshold: float = 0.01,
) -> bool:
    """SIMPLE_SIGNATURE (simple chain + V_2 -> 0) => sigma_n -> 0."""
    from squarepeg.defect_surgery.exact_component_decomposition import (
        attachment_chain_area_from_deltas,
        attachment_chain_vertices,
    )

    if not components:
        return True
    deltas = [c.delta for c in components]
    origin = components[0].path[0]
    pts = attachment_chain_vertices(origin, deltas)
    chain = AttachmentChain(points=pts, chord_indices=[])
    audit = simple_signature_implies_sigma(chain, v2_threshold=v2_threshold)
    return audit.implies_signature_sigma
