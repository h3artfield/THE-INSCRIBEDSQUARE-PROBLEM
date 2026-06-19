"""Planar permuton rigidity — T077 (Directive 038)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.augmented_gate_permuton import AugmentedPermuton, SupportClass, augmented_permuton
from squarepeg.defect_extraction.infinite_gate_measure import InfiniteGateSet
from squarepeg.defect_extraction.summable_block_geometry import audit_summable_block_geometry
from squarepeg.defect_extraction.measurable_countable_blocks import extend_decomposition_to_countable

T077Status = Literal["CONJECTURAL_RIGIDITY_TARGET", "PROVED_LOCALLY_PARTIAL"]
T077Outcome = Literal[
    "ROUTED_TO_T073I",
    "INFINITE_INTRUSION_DEPTH",
    "NON_JORDAN_DEGENERATION",
    "INFINITE_CENTER_PROLIFERATION",
    "POSITIVE_SCALE_NONANNULAR",
    "GENUINELY_DIFFUSE_RESIDUAL",
]


@dataclass
class GenuinelyDiffusePermuton:
    """Not supported on countable union of locally finite monotone graphs."""
    inversion_energy: float
    graph_support_count: int
    locally_finite_decomposition: bool
    geometric_scale_data: bool


@dataclass
class T077Certificate:
    status: T077Status
    outcome: T077Outcome
    genuinely_diffuse: bool
    support_class: SupportClass
    messages: list[str]


def is_genuinely_diffuse(aug: AugmentedPermuton) -> GenuinelyDiffusePermuton:
    return GenuinelyDiffusePermuton(
        inversion_energy=aug.inversion_energy,
        graph_support_count=aug.graph_count,
        locally_finite_decomposition=aug.support_class != "GENUINELY_DIFFUSE",
        geometric_scale_data=True,
    )


def certify_t077(gate_set: InfiniteGateSet) -> T077Certificate:
    """T077: genuinely diffuse permuton forces intrusion/non-Jordan/infinite-center."""
    aug = augmented_permuton(gate_set)
    decomp = extend_decomposition_to_countable(gate_set, target_blocks=12)
    geom = audit_summable_block_geometry(decomp.blocks, gate_set)
    outcome: T077Outcome = "GENUINELY_DIFFUSE_RESIDUAL"
    status: T077Status = "CONJECTURAL_RIGIDITY_TARGET"
    if geom.summable and aug.support_class == "COUNTABLY_MONOTONE_SUPPORTED":
        outcome = "ROUTED_TO_T073I"
        status = "PROVED_LOCALLY_PARTIAL"
    elif aug.support_class == "GENUINELY_DIFFUSE":
        if aug.inversion_energy > 0.4:
            outcome = "INFINITE_INTRUSION_DEPTH"
        elif aug.graph_count > 8:
            outcome = "INFINITE_CENTER_PROLIFERATION"
        else:
            outcome = "GENUINELY_DIFFUSE_RESIDUAL"
    elif aug.support_class == "NONSUMMABLE_GRAPH_SUPPORTED":
        outcome = "NON_JORDAN_DEGENERATION"
    return T077Certificate(
        status=status,
        outcome=outcome,
        genuinely_diffuse=aug.support_class == "GENUINELY_DIFFUSE",
        support_class=aug.support_class,
        messages=[f"support={aug.support_class}, outcome={outcome}"],
    )
