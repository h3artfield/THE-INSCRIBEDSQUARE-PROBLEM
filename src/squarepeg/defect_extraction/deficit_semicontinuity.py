"""Ledger deficit semicontinuity audit (Directive 050)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from squarepeg.defect_extraction.equality_ledger import LedgerID, get_ledger

Semicontinuity = Literal[
    "CONTINUOUS_UNDER_CORE_CONVERGENCE",
    "LOWER_SEMICONTINUOUS",
    "UPPER_SEMICONTINUOUS",
    "NOT_CLOSED",
]


@dataclass
class DeficitSemicontinuityRecord:
    ledger_id: LedgerID
    direction: Semicontinuity
    repair: str


@dataclass
class DeficitSemicontinuityAudit:
    records: list[DeficitSemicontinuityRecord]
    all_closed_for_equality: bool
    messages: list[str]


_DEFAULT: dict[LedgerID, Semicontinuity] = {
    "WEDGE_PRODUCT": "LOWER_SEMICONTINUOUS",
    "TRIANGLE_NORM": "LOWER_SEMICONTINUOUS",
    "CAUCHY_SCHWARZ": "CONTINUOUS_UNDER_CORE_CONVERGENCE",
    "CHILD_INCREMENT": "UPPER_SEMICONTINUOUS",
    "HULL_DIAMETER": "CONTINUOUS_UNDER_CORE_CONVERGENCE",
    "CROSSCUT_AREA": "LOWER_SEMICONTINUOUS",
    "RETAINED_SKELETON": "NOT_CLOSED",
    "CENTER_PACKING": "UPPER_SEMICONTINUOUS",
    "FINITE_CENTER_GROUP": "UPPER_SEMICONTINUOUS",
    "SIGN_GROUPING": "NOT_CLOSED",
    "CORONA_TRUNCATION": "LOWER_SEMICONTINUOUS",
    "MULTIGEN_PACKING": "LOWER_SEMICONTINUOUS",
}


def audit_deficit_semicontinuity() -> DeficitSemicontinuityAudit:
    records: list[DeficitSemicontinuityRecord] = []
    closed = True
    for entry in get_ledger():
        d = _DEFAULT[entry.id]
        repair = "none" if d != "NOT_CLOSED" else "carry auxiliary wedge vectors"
        if d == "NOT_CLOSED":
            closed = False
        records.append(DeficitSemicontinuityRecord(entry.id, d, repair))
    return DeficitSemicontinuityAudit(
        records=records,
        all_closed_for_equality=closed,
        messages=[f"closed={closed}, not_closed={sum(1 for r in records if r.direction=='NOT_CLOSED')}"],
    )
