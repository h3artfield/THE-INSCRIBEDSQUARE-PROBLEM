"""Diffuse end measure classifier (Directive 042)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.diffuse_end_measure import audit_diffuse_end_measure, build_end_measure
from squarepeg.defect_extraction.infinite_ray_surgery import certify_t080

EndAtomClass = Literal[
    "FINITE_ATOMIC",
    "COUNTABLY_ATOMIC",
    "NONATOMIC_DIFFUSE",
]

SpatialPushforward = Literal[
    "ATOMIC",
    "FINITE_CENTER",
    "DIFFUSE",
    "CANTOR",
    "NONINJECTIVE",
]


@dataclass
class DiffuseEndClassifierAudit:
    end_atom_class: EndAtomClass
    spatial_class: SpatialPushforward
    summable_atomic: bool
    diffuse_end_tree: bool
    messages: list[str]


def classify_diffuse_ends(tree: CanonicalIntrusionTree) -> DiffuseEndClassifierAudit:
    em = build_end_measure(tree)
    diffuse = audit_diffuse_end_measure(tree)
    t080 = certify_t080(tree)
    eac: EndAtomClass = "FINITE_ATOMIC"
    if em.measure_class == "ATOMIC":
        eac = "FINITE_ATOMIC"
    elif em.measure_class == "COUNTABLY_ATOMIC":
        eac = "COUNTABLY_ATOMIC"
    else:
        eac = "NONATOMIC_DIFFUSE"
    spatial: SpatialPushforward = "ATOMIC"
    if em.measure_class == "FINITE_CENTERS":
        spatial = "FINITE_CENTER"
    elif em.measure_class == "INFINITE_CENTERS":
        spatial = "DIFFUSE"
    elif em.measure_class == "DIFFUSE_CANTOR":
        spatial = "CANTOR"
    summable = eac == "FINITE_ATOMIC" and t080.status == "PROVED_LOCALLY"
    return DiffuseEndClassifierAudit(
        end_atom_class=eac,
        spatial_class=spatial,
        summable_atomic=summable,
        diffuse_end_tree=diffuse.status == "DIFFUSE_END_MEASURE_TREE",
        messages=[f"end={eac}, spatial={spatial}"],
    )
