"""Eccentric winding leaves (Directive 033)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.lamination_compactness import EssentialLeaf

EccentricGeometry = Literal[
    "THIN_STRIP",
    "CRESCENT",
    "NEEDLE_LOOP",
    "MULTICENTER_HOOK",
    "BALANCED",
]


@dataclass
class EccentricLeafAudit:
    eccentricity: float
    geometry: EccentricGeometry
    thin_leaf_surgery_eligible: bool
    forces_concentration: bool
    messages: list[str]


def leaf_eccentricity(leaf: EssentialLeaf) -> float:
    inr = _inradius(leaf)
    if inr <= 0:
        return float("inf")
    return leaf.diameter / inr


def classify_eccentric_leaf(
    leaf: EssentialLeaf,
    *,
    thin_threshold: float = 15.0,
) -> EccentricLeafAudit:
    ecc = leaf_eccentricity(leaf)
    geometry: EccentricGeometry = "BALANCED"
    if ecc > thin_threshold * 2:
        geometry = "NEEDLE_LOOP"
    elif ecc > thin_threshold:
        geometry = "THIN_STRIP"
    elif ecc > 8:
        geometry = "CRESCENT"
    elif leaf.child_ids and len(leaf.child_ids) > 1:
        geometry = "MULTICENTER_HOOK"
    thin_surgery = geometry in ("THIN_STRIP", "CRESCENT") and ecc < thin_threshold * 3
    concentration = ecc > thin_threshold * 2 and leaf.area_fraction >= 0.1
    return EccentricLeafAudit(
        eccentricity=ecc,
        geometry=geometry,
        thin_leaf_surgery_eligible=thin_surgery,
        forces_concentration=concentration,
        messages=[f"ecc={ecc:.1f}, geometry={geometry}"],
    )


def audit_eccentric_chain(leaves: list[EssentialLeaf]) -> list[EccentricLeafAudit]:
    return [classify_eccentric_leaf(leaf) for leaf in leaves]


def _inradius(leaf: EssentialLeaf) -> float:
    return (leaf.area / 3.14159) ** 0.5 if leaf.area > 0 else 0.0
