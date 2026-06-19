"""Diffuse dense gate limits (Directive 031)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.normalized_gate_measure import GateMeasure, GateMeasureLimit, extract_measure_limit

LimitFormalism = Literal[
    "RECTIFIABLE_CURRENT",
    "SIGNED_MEASURE",
    "YOUNG_MEASURE",
    "PLANAR_1_CURRENT",
    "NONCROSSING_LAMINATION",
]


@dataclass
class DiffuseGateLimit:
    formalism: LimitFormalism
    measure_limit: GateMeasureLimit
    attachment_signature: float
    vanishing_limit: bool
    protected_component: bool
    messages: list[str]


def classify_diffuse_limit(
    measure_sequence: list[GateMeasure],
    attachment_normalized: float,
) -> DiffuseGateLimit:
    """D3: continuum gate limit with limiting second-level signature."""
    ml = extract_measure_limit(measure_sequence)
    formalism: LimitFormalism = "SIGNED_MEASURE"
    if ml.measure_type == "DIFFUSE":
        formalism = "NONCROSSING_LAMINATION"
    vanish = abs(attachment_normalized) < 0.01
    protected = False
    msgs = [f"Measure limit: {ml.measure_type}"]
    if vanish:
        msgs.append("Limiting signature vanishes — noncrossing order")
    return DiffuseGateLimit(
        formalism=formalism,
        measure_limit=ml,
        attachment_signature=attachment_normalized,
        vanishing_limit=vanish,
        protected_component=protected,
        messages=msgs,
    )
