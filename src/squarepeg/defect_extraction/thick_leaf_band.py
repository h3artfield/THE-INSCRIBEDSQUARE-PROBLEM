"""Thick leaf bands and T067R (Directive 034)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.lamination_compactness import EssentialLeaf
from squarepeg.defect_extraction.thin_leaf_geometry import leaf_width

T067RStatus = Literal["CONJECTURAL_STRUCTURAL_TARGET", "PROVED_LOCALLY_CLASSIFIER"]
T067ROutcome = Literal[
    "T066_ORDERED_TWO_GATE",
    "T068_FINITE_MULTIGATE",
    "T069_THIN_ECCENTRIC",
    "THICK_NESTED_BAND",
    "EXPLICIT_RESIDUAL",
]


@dataclass
class ThickLeafBand:
    outer_id: str
    inner_id: str
    band_modulus: float
    center_drift: float
    quantitatively_thick: bool


@dataclass
class T067RCertificate:
    status: T067RStatus
    outcome: T067ROutcome
    band: ThickLeafBand | None
    multicenter_obstruction: bool
    messages: list[str]


def band_modulus(outer: EssentialLeaf, inner: EssentialLeaf) -> float:
    """dist(dL_out, dL_in) / diam(L_out)."""
    gap = max(outer.diameter - inner.diameter, 0.0)
    return gap / max(outer.diameter, 1e-6)


def is_thick_leaf(leaf: EssentialLeaf, *, c: float = 0.12) -> bool:
    w = leaf_width(leaf)
    return w >= c * leaf.diameter


def audit_thick_band(outer: EssentialLeaf, inner: EssentialLeaf, *, delta: float = 0.08) -> ThickLeafBand:
    bm = band_modulus(outer, inner)
    drift = _center_drift(outer, inner)
    return ThickLeafBand(
        outer_id=outer.leaf_id,
        inner_id=inner.leaf_id,
        band_modulus=bm,
        center_drift=drift,
        quantitatively_thick=bm >= delta and is_thick_leaf(outer) and is_thick_leaf(inner),
    )


def classify_t067r(
    *,
    t066_closed: bool,
    t068_closed: bool,
    t069_closed: bool,
    outer: EssentialLeaf | None,
    inner: EssentialLeaf | None,
    residual: str = "EXPLICIT_RESIDUAL",
) -> T067RCertificate:
    outcome: T067ROutcome = "EXPLICIT_RESIDUAL"
    band = None
    if t066_closed:
        outcome = "T066_ORDERED_TWO_GATE"
    elif t068_closed:
        outcome = "T068_FINITE_MULTIGATE"
    elif t069_closed:
        outcome = "T069_THIN_ECCENTRIC"
    elif outer and inner:
        band = audit_thick_band(outer, inner)
        if band.quantitatively_thick and band.center_drift < 0.2:
            outcome = "THICK_NESTED_BAND"
    multicenter = band is not None and band.center_drift >= 0.2
    return T067RCertificate(
        status="PROVED_LOCALLY_CLASSIFIER",
        outcome=outcome,
        band=band,
        multicenter_obstruction=multicenter,
        messages=[f"T067R outcome={outcome}"],
    )


def _center_drift(a: EssentialLeaf, b: EssentialLeaf) -> float:
    if not a.closure or not b.closure:
        return 0.0
    ca = (sum(p[0] for p in a.closure) / len(a.closure), sum(p[1] for p in a.closure) / len(a.closure))
    cb = (sum(p[0] for p in b.closure) / len(b.closure), sum(p[1] for p in b.closure) / len(b.closure))
    return ((ca[0] - cb[0]) ** 2 + (ca[1] - cb[1]) ** 2) ** 0.5 / max(a.diameter, 1e-6)
