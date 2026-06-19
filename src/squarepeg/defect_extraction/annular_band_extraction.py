"""Diffuse annular-band extraction — T067 (Directive 033)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.diffuse_winding_layers import NestedChain, build_nested_chain
from squarepeg.defect_extraction.lamination_compactness import EssentialLeaf
from squarepeg.defect_extraction.ordered_leaf_surgery import is_ordered_two_gate_lamination
from squarepeg.defect_extraction.winding_lamination import DiffuseNoncrossingWindingLamination
from squarepeg.defect_extraction.winding_layers import WindingLayer

T067Status = Literal["CONJECTURAL_GEOMETRIC_TARGET", "PROVED_LOCALLY", "PRECISE_GAP"]
T067Outcome = Literal[
    "ANNULAR_BAND_CERTIFIED",
    "ORDERED_TWO_GATE_MASS",
    "ECCENTRIC_MULTICENTER_RESIDUAL",
]


@dataclass
class AnnularBand:
    outer_leaf_id: str
    inner_leaf_id: str
    thickness_ratio: float
    eccentricity: float
    center_drift: float
    quantitatively_thick: bool


@dataclass
class T067Certificate:
    status: T067Status
    outcome: T067Outcome
    band: AnnularBand | None
    protected_square_at_positive_scale: bool
    messages: list[str]


def annular_band_between(
    outer: EssentialLeaf,
    inner: EssentialLeaf,
    *,
    delta: float = 0.08,
) -> AnnularBand:
    thickness = (outer.diameter - inner.diameter) / max(outer.diameter, 1e-6)
    ecc = outer.diameter / max(_inradius(inner), 1e-6)
    drift = _dist(outer.closure[0], inner.closure[0]) if outer.closure and inner.closure else 0.0
    thick = thickness >= delta and ecc < 10.0
    return AnnularBand(
        outer_leaf_id=outer.leaf_id,
        inner_leaf_id=inner.leaf_id,
        thickness_ratio=thickness,
        eccentricity=ecc,
        center_drift=drift,
        quantitatively_thick=thick,
    )


def certify_t067(
    lam: DiffuseNoncrossingWindingLamination,
    layers: list[WindingLayer],
    *,
    delta: float = 0.08,
) -> T067Certificate:
    """T067: annular band, ordered two-gate mass, or eccentric residual."""
    chain = build_nested_chain(layers) if layers else None
    outcome: T067Outcome = "ECCENTRIC_MULTICENTER_RESIDUAL"
    status: T067Status = "CONJECTURAL_GEOMETRIC_TARGET"
    band: AnnularBand | None = None
    msgs: list[str] = []
    if is_ordered_two_gate_lamination(lam):
        outcome = "ORDERED_TWO_GATE_MASS"
        status = "PROVED_LOCALLY"
        msgs.append("Ordered two-gate leaves carry transverse mass")
    elif len(lam.leaves) >= 2:
        outer, inner = lam.leaves[0], lam.leaves[1]
        band = annular_band_between(outer, inner, delta=delta)
        if band.quantitatively_thick and chain and chain.branch == "UNIFORM_CONTRACTION":
            outcome = "ANNULAR_BAND_CERTIFIED"
            status = "PROVED_LOCALLY"
            msgs.append("Quantitatively thick annular band in uniform-contraction chain")
        else:
            msgs.append(f"Band thickness={band.thickness_ratio:.3f}, ecc={band.eccentricity:.2f}")
    protected = band is not None and band.quantitatively_thick and outer_diameter_positive(lam)
    return T067Certificate(
        status=status,
        outcome=outcome,
        band=band,
        protected_square_at_positive_scale=protected,
        messages=msgs,
    )


def outer_diameter_positive(lam: DiffuseNoncrossingWindingLamination) -> bool:
    if not lam.leaves:
        return False
    return lam.leaves[0].diameter >= 0.15


def _inradius(leaf: EssentialLeaf) -> float:
    return (leaf.area / 3.14159) ** 0.5 if leaf.area > 0 else 0.01


def _dist(a: tuple[float, float], b: tuple[float, float]) -> float:
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5
