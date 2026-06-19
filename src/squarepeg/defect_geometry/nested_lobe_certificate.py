"""Nested lobe certificate and T036-N1 status."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from squarepeg.defect_geometry.annular_windows import extract_windows, windows_disjoint
from squarepeg.defect_geometry.lobe_tree import LobeTree
from squarepeg.defect_geometry.nested_chain import NestedClassParams, in_D_nest
from squarepeg.defect_geometry.packet_reference_distance import compare_packet_to_reference, t036_n1_conditional_theorem
from squarepeg.defect_geometry.reference_cyclic_certificate import certify_reference_annular

T036N1Status = Literal[
    "PROVED_CONDITIONAL",
    "CONJECTURAL_GEOMETRIC_TARGET",
    "COUNTEREXAMPLE_FOUND",
]


@dataclass
class NestedLobeCertificate:
    in_D_nest: bool
    windows_extracted: bool
    reference_t039: bool
    comparison_sufficient: bool
    t036_n1_status: T036N1Status
    side_scale_lower_bound: float
    messages: list[str] = field(default_factory=list)


def certify_nested_packet(tree: LobeTree, params: NestedClassParams | None = None) -> NestedLobeCertificate:
    p = params or NestedClassParams()
    ref = certify_reference_annular()
    in_nest = in_D_nest(tree, p)
    wins = extract_windows(tree) if in_nest else None
    cmp = compare_packet_to_reference(tree, p)
    c_sq = 0.1
    d_outer = tree.root.diameter if in_nest else 0.0
    status: T036N1Status
    if ref.t039_applies and cmp.closeness_sufficient:
        status = "PROVED_CONDITIONAL"
    else:
        status = "CONJECTURAL_GEOMETRIC_TARGET"
    return NestedLobeCertificate(
        in_D_nest=in_nest,
        windows_extracted=wins is not None and windows_disjoint(wins),
        reference_t039=ref.t039_applies,
        comparison_sufficient=cmp.closeness_sufficient,
        t036_n1_status=status,
        side_scale_lower_bound=c_sq * d_outer,
        messages=[
            t036_n1_conditional_theorem(),
            cmp.missing_hypothesis or "Comparison bound satisfied",
        ],
    )
