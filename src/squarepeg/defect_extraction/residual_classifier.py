"""Refined residual intrusion classes (Directive 028)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.finite_intrusion_tree import T050Audit
from squarepeg.defect_extraction.infinite_intrusion_tree import InfiniteTreeAudit
from squarepeg.defect_extraction.multigate_cluster import T054Audit

ResidualClass = Literal[
    "INFINITE_MULTIGATE_INTRUSION_RAY",
    "UNBOUNDED_BRANCHING_INTRUSION_TREE",
    "NON_JORDAN_SATURATION_HULL",
    "DENSE_GATE_ACCUMULATION",
    "MULTICENTER_ALTERNATING_INTRUSION_TREE",
    "NONE",
]


@dataclass
class ResidualClassification:
    primary_class: ResidualClass
    narrower_than_d027: bool
    conditions: list[str]
    messages: list[str]


def classify_residual(
    t050: T050Audit | None = None,
    t054: T054Audit | None = None,
    infinite: InfiniteTreeAudit | None = None,
) -> ResidualClassification:
    """
    Replace broad MULTICENTER_ALTERNATING_INTRUSION_TREE with explicit subclasses.
    """
    if infinite and infinite.tree_class == "INFINITE_NESTED_RAY":
        return ResidualClassification(
            primary_class="INFINITE_MULTIGATE_INTRUSION_RAY",
            narrower_than_d027=True,
            conditions=[
                "Non-stabilizing saturation",
                "Nested C_1 supset C_2 supset ... with diam -> 0",
            ],
            messages=infinite.messages,
        )
    if infinite and infinite.tree_class == "UNBOUNDED_BRANCHING":
        return ResidualClassification(
            primary_class="UNBOUNDED_BRANCHING_INTRUSION_TREE",
            narrower_than_d027=True,
            conditions=["Unbounded local branching", "B(C) unbounded"],
            messages=infinite.messages,
        )
    if t050 and t050.outcome == "NON_JORDAN_HULL":
        return ResidualClassification(
            primary_class="NON_JORDAN_SATURATION_HULL",
            narrower_than_d027=True,
            conditions=["H(C) fails Jordan disk classification"],
            messages=t050.messages,
        )
    if t054 and t054.outcome == "MULTICENTER_RESIDUAL" and t054.interleaving_unprotected:
        return ResidualClassification(
            primary_class="DENSE_GATE_ACCUMULATION",
            narrower_than_d027=True,
            conditions=[">=4 gates", "Alternating pairing", "No T039 protection"],
            messages=t054.messages,
        )
    if t050 and t050.outcome == "MULTI_GATE_FOUR_PLUS":
        return ResidualClassification(
            primary_class="DENSE_GATE_ACCUMULATION",
            narrower_than_d027=True,
            conditions=[">=4 separated outer gates on saturation hull"],
            messages=t050.messages,
        )
    return ResidualClassification(
        primary_class="MULTICENTER_ALTERNATING_INTRUSION_TREE",
        narrower_than_d027=False,
        conditions=["Fallback: unresolved multicenter intrusion"],
        messages=["Residual not narrowed further"],
    )
