"""Analytic routing for infinite-dimensional transition branches (Directive 053)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.canonical_intrusion_tree import CanonicalIntrusionTree
from squarepeg.defect_extraction.measure_valued_transition import audit_measure_valued_transition

InfiniteBranch = Literal[
    "COUNTABLY_MANY_CHILDREN",
    "MEASURE_VALUED_CHILDREN",
    "UNBOUNDED_GATE_COMPLEXITY",
    "INFINITE_CENTER_LIMIT",
]

AnalyticRoute = Literal["T081I", "T073I", "T077A", "INFINITE_CENTER_RESIDUAL", "NOT_TRIGGERED"]


@dataclass
class InfiniteBranchRecord:
    branch: InfiniteBranch
    triggered: bool
    route: AnalyticRoute
    theorem: str


@dataclass
class InfiniteDimensionalRouteAudit:
    records: list[InfiniteBranchRecord]
    all_routed_analytically: bool
    infinite_branch_remains: bool
    messages: list[str]


def audit_infinite_dimensional_transition_routes(tree: CanonicalIntrusionTree) -> InfiniteDimensionalRouteAudit:
    measure = audit_measure_valued_transition(tree)
    records = [
        InfiniteBranchRecord(
            "COUNTABLY_MANY_CHILDREN",
            not measure.finite_replacement_sufficient,
            "T081I" if not measure.finite_replacement_sufficient else "NOT_TRIGGERED",
            "T081I countable branching surgery",
        ),
        InfiniteBranchRecord(
            "MEASURE_VALUED_CHILDREN",
            not measure.finite_replacement_sufficient,
            "T073I" if not measure.finite_replacement_sufficient else "NOT_TRIGGERED",
            "T073I measure-valued child transition",
        ),
        InfiniteBranchRecord(
            "UNBOUNDED_GATE_COMPLEXITY",
            False,
            "NOT_TRIGGERED",
            "T068I/T077-A gate complexity",
        ),
        InfiniteBranchRecord(
            "INFINITE_CENTER_LIMIT",
            False,
            "NOT_TRIGGERED",
            "infinite-center residual",
        ),
    ]
    triggered = [r for r in records if r.triggered]
    routed = all(r.route != "NOT_TRIGGERED" for r in triggered) if triggered else True
    # Analytic closure of infinite-dimensional branches is not proved in D053.
    remains = True
    return InfiniteDimensionalRouteAudit(
        records=records,
        all_routed_analytically=routed and not remains,
        infinite_branch_remains=remains,
        messages=[f"triggered={len(triggered)}, remains={remains}"],
    )
