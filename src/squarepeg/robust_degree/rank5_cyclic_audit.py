"""Rank-5 polygon family cyclic-odd classification."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from squarepeg.curves.polygon import PolygonCurve
from squarepeg.exact_squares.solver import solve_polygon_full
from squarepeg.robust_degree.family_certificate import classify_rank5_family

FamilyCyclicStatus = Literal[
    "CYCLIC_ODD_CERTIFIED",
    "EULER_OBSTRUCTION_CERTIFIED",
    "UNPROTECTED",
    "ASSIGNMENT_ARTIFACT",
    "UNRESOLVED",
]


@dataclass
class Rank5CyclicAudit:
    family_id: str
    kind: str
    status: FamilyCyclicStatus
    messages: list[str] = field(default_factory=list)


@dataclass
class Rank5CyclicAuditReport:
    audits: list[Rank5CyclicAudit]
    summary: dict[str, int]


def audit_rank5_family(fam) -> Rank5CyclicAudit:
    kind = classify_rank5_family(fam)
    fid = getattr(fam, "family_id", "unknown")
    if kind != "genuine_1d_family":
        return Rank5CyclicAudit(
            family_id=fid,
            kind=kind,
            status="ASSIGNMENT_ARTIFACT",
            messages=["Not a genuine compact 1D family"],
        )
    return Rank5CyclicAudit(
        family_id=fid,
        kind=kind,
        status="UNPROTECTED",
        messages=[
            "Rank-5 nullity does not imply cyclic-odd certificate",
            "Requires separate rhombus continuation + w_1 pairing computation",
        ],
    )


def audit_polygon_rank5(polygon: PolygonCurve) -> Rank5CyclicAuditReport:
    result = solve_polygon_full(polygon)
    audits = [audit_rank5_family(f) for f in result.families_1d]
    summary: dict[str, int] = {}
    for a in audits:
        summary[a.status] = summary.get(a.status, 0) + 1
    return Rank5CyclicAuditReport(audits=audits, summary=summary)
