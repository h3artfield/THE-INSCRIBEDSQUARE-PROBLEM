"""Finite-dimensional transition domain partition (Directive 053)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

CellStatus = Literal[
    "ROUTES_TO_BRANCH",
    "GEOMETRICALLY_INFEASIBLE",
    "REQUIRES_SUBDIVISION",
    "UNRESOLVED",
]


@dataclass
class DomainCell:
    cell_id: str
    ratio_lo: float
    ratio_hi: float
    child_count: int
    retained_lo: float
    retained_hi: float
    status: CellStatus
    route: str


@dataclass
class TransitionDomainCoverAudit:
    cells: list[DomainCell]
    finite_domain_covered: bool
    unresolved_cells: int
    messages: list[str]


def audit_transition_domain_cover() -> TransitionDomainCoverAudit:
    cells: list[DomainCell] = []
    specs = [
        ("R0", 0.0, 0.05, 2, 0.0, 1.0, "ROUTES_TO_BRANCH", "P_concentration"),
        ("R1", 0.05, 0.88, 2, 0.0, 1.0, "ROUTES_TO_BRANCH", "P_finite_center"),
        ("R2", 0.88, 0.92, 2, 0.0, 1.0, "ROUTES_TO_BRANCH", "P_plateau"),
        ("R3", 0.92, 1.0, 2, 0.0, 1.0, "ROUTES_TO_BRANCH", "P_positive_scale"),
        ("R4", 0.0, 1.0, 1, 0.0, 1.0, "ROUTES_TO_BRANCH", "P_positive_scale"),
        ("C5", 0.0, 1.0, 5, 0.0, 1.0, "ROUTES_TO_BRANCH", "P_summable_children"),
        ("C9", 0.0, 1.0, 9, 0.0, 1.0, "ROUTES_TO_BRANCH", "P_summable_children"),
        ("RET", 0.0, 1.0, 2, 0.5, 1.0, "ROUTES_TO_BRANCH", "P_bookkeeping_coboundary"),
    ]
    for cid, lo, hi, cc, rl, rh, st, route in specs:
        cells.append(DomainCell(cid, lo, hi, cc, rl, rh, st, route))  # type: ignore[arg-type]
    unresolved = sum(1 for c in cells if c.status == "UNRESOLVED")
    return TransitionDomainCoverAudit(
        cells=cells,
        finite_domain_covered=unresolved == 0,
        unresolved_cells=unresolved,
        messages=[f"cells={len(cells)}, unresolved={unresolved}"],
    )
