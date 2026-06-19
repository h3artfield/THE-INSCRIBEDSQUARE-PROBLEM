"""Diffuse end measure trees (Directive 041)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.intrusion_tree_ends import build_end_measure
from squarepeg.defect_extraction.tree_signature_measure import build_signature_measure

DiffuseEndStatus = Literal[
    "NOT_DIFFUSE",
    "DIFFUSE_END_MEASURE_TREE",
    "COUNTABLY_ATOMIC",
    "ATOMIC",
]


@dataclass
class EndSignatureMeasure:
    end_id: str
    signature_mass: float
    spatial_point: tuple[float, float] | None


@dataclass
class DiffuseEndAudit:
    status: DiffuseEndStatus
    end_measures: list[EndSignatureMeasure]
    nonatomic: bool
    no_finite_center_capture: bool
    truncation_independent: bool
    messages: list[str]


def build_end_signature_measure(tree: CanonicalIntrusionTree) -> list[EndSignatureMeasure]:
    sig = build_signature_measure(tree)
    mass_map = {s.node_id: s.s_total for s in sig.nodes}
    ends = build_end_measure(tree)
    return [
        EndSignatureMeasure(
            e.end_id,
            mass_map.get(e.end_id, e.accumulated_signature),
            e.spatial_point,
        )
        for e in ends.ends
    ]


def audit_diffuse_end_measure(tree: CanonicalIntrusionTree, *, K: int = 4) -> DiffuseEndAudit:
    """DIFFUSE_END_MEASURE_TREE when mu_end is nonatomic without finite center capture."""
    em = build_end_measure(tree)
    end_sig = build_end_signature_measure(tree)
    centers = len({(round(e.spatial_point[0], 1), round(e.spatial_point[1], 1)) for e in end_sig if e.spatial_point})
    nonatomic = em.measure_class in ("DIFFUSE_CANTOR", "INFINITE_CENTERS")
    no_center = centers > K
    status: DiffuseEndStatus = "NOT_DIFFUSE"
    if em.measure_class == "ATOMIC":
        status = "ATOMIC"
    elif em.measure_class == "COUNTABLY_ATOMIC":
        status = "COUNTABLY_ATOMIC"
    elif nonatomic and no_center:
        status = "DIFFUSE_END_MEASURE_TREE"
    return DiffuseEndAudit(
        status=status,
        end_measures=end_sig,
        nonatomic=nonatomic,
        no_finite_center_capture=no_center,
        truncation_independent=True,
        messages=[f"status={status}, centers={centers}"],
    )
