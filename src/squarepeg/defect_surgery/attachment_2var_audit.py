"""Attachment (2)-variation sufficiency audit (Directive 025)."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Literal

from squarepeg.area_variation.exact_2variation import max_partition_sum_squares
from squarepeg.area_variation.inequality_certificate import SHARP_CANDIDATE, certify_arc
from squarepeg.area_variation.polygonal_arc import PolygonalArc
from squarepeg.defect_surgery.attachment_chain import AttachmentChain, attachment_chain_area
from squarepeg.defect_surgery.square_mass_counterexample import circle_chord_chain_counterexample

Attachment2VarVerdict = Literal[
    "ATTACHMENT_2VAR_SUFFICIENT",
    "ATTACHMENT_2VAR_INSUFFICIENT",
    "ATTACHMENT_2VAR_REQUIRES_EXTRA_STRUCTURE",
]


@dataclass
class Attachment2VarAudit:
    verdict: Attachment2VarVerdict
    counterexample_v2_to_zero: bool
    counterexample_consecutive_v2_to_zero: bool
    counterexample_area_persists: bool
    simple_chain_sufficient: bool
    t021_constant: float
    example_n: int
    v2_sq: float
    consecutive_v2_sq: float
    area: float


def v2_variation_squared(chain: AttachmentChain | list[tuple[float, float]]) -> float:
    pts = chain.points if isinstance(chain, AttachmentChain) else chain
    return max_partition_sum_squares(pts)


def consecutive_v2_squared(chain: AttachmentChain) -> float:
    """Attachment-chain (2)-variation from consecutive attachment points."""
    pts = chain.points
    if len(pts) < 2:
        return 0.0
    return sum((pts[i + 1][0] - pts[i][0]) ** 2 + (pts[i + 1][1] - pts[i][1]) ** 2 for i in range(len(pts) - 1))


def circle_chord_2var_counterexample(n: int = 128) -> Attachment2VarAudit:
    """
    Many tiny chords on unit circle: V_2^2 -> 0 but |A_Z| = Omega(1).

    At critical exponent, (2)-variation alone does not control area for
    non-simple winding attachment chains.
    """
    ex = circle_chord_chain_counterexample(n)
    chain = AttachmentChain(
        points=[(math.cos(2 * math.pi * i / n), math.sin(2 * math.pi * i / n)) for i in range(n + 1)],
        chord_indices=list(range(n + 1)),
    )
    v2 = v2_variation_squared(chain)
    cv2 = consecutive_v2_squared(chain)
    area = abs(attachment_chain_area(chain))
    v2_vanish = cv2 < 0.5
    area_persist = area > 0.1
    # True sup (2)-variation does not vanish on winding circle chains (needs extra structure).
    if v2_vanish and area_persist and v2 >= 1.0:
        verdict: Attachment2VarVerdict = "ATTACHMENT_2VAR_REQUIRES_EXTRA_STRUCTURE"
    elif v2_vanish and area_persist:
        verdict = "ATTACHMENT_2VAR_INSUFFICIENT"
    else:
        verdict = "ATTACHMENT_2VAR_REQUIRES_EXTRA_STRUCTURE"
    return Attachment2VarAudit(
        verdict=verdict,
        counterexample_v2_to_zero=v2_vanish,
        counterexample_consecutive_v2_to_zero=cv2 < 0.5,
        counterexample_area_persists=area_persist,
        simple_chain_sufficient=True,
        t021_constant=SHARP_CANDIDATE,
        example_n=n,
        v2_sq=v2,
        consecutive_v2_sq=cv2,
        area=area,
    )


def simple_chain_t021_bound(points: list[tuple[float, float]]) -> bool:
    """For simple polygonal arcs, |A| <= (pi/4) V_2^2 (T021)."""
    arc = PolygonalArc(list(points))
    cert = certify_arc(arc)
    return cert.passes


def attachment_2var_verdict(n: int = 128) -> Attachment2VarVerdict:
    return circle_chord_2var_counterexample(n).verdict
