"""Global residual ledger (Directive 058)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

ResidualClass = Literal[
    "SOLVED",
    "LOCALLY_SOLVED",
    "FIXTURE_LOCAL",
    "BRIDGE_NEEDED",
    "GENUINELY_OPEN",
    "INVALIDLY_CLAIMED",
    "REMOVED_AS_INDEPENDENT",
]

GLOBAL_RESIDUALS: tuple[str, ...] = (
    "POSITIVE_SCALE_NONANNULAR_CLUSTER",
    "NON_JORDAN_SATURATION_HULL",
    "PARAMETER_DISCONNECTED_LIMIT",
    "INFINITE_CENTER_GEOMETRY",
    "NONSUMMABLE_DIFFUSE_END_GEOMETRY",
    "T045R_UNIVERSAL_EXTRACTION_BRIDGE",
)

REMOVED_RESIDUALS: tuple[str, ...] = (
    "NONCARLESON_SINGLETON_CANTOR_END_TANGENT",
)


@dataclass
class ResidualRecord:
    name: str
    classification: ResidualClass
    blocking_theorem: str
    route_source: str
    risk_level: str


@dataclass
class ResidualLedger:
    records: list[ResidualRecord]
    complete: bool
    messages: list[str]


_RESIDUAL_META: dict[str, tuple[ResidualClass, str, str, str]] = {
    "NONCARLESON_SINGLETON_CANTOR_END_TANGENT": (
        "REMOVED_AS_INDEPENDENT",
        "T089E",
        "T103/T089E",
        "LOW",
    ),
    "POSITIVE_SCALE_NONANNULAR_CLUSTER": (
        "FIXTURE_LOCAL",
        "T091",
        "R_POSITIVE_SCALE",
        "MEDIUM",
    ),
    "NON_JORDAN_SATURATION_HULL": (
        "GENUINELY_OPEN",
        "T064D",
        "R_COLLISION_DEGENERATION",
        "HIGH",
    ),
    "PARAMETER_DISCONNECTED_LIMIT": (
        "GENUINELY_OPEN",
        "T072C",
        "R_PARAMETER_DISCONNECTED",
        "HIGH",
    ),
    "INFINITE_CENTER_GEOMETRY": (
        "GENUINELY_OPEN",
        "T085",
        "R_INFINITE_CENTER",
        "MEDIUM",
    ),
    "NONSUMMABLE_DIFFUSE_END_GEOMETRY": (
        "BRIDGE_NEEDED",
        "T077-A",
        "diffuse_order",
        "HIGH",
    ),
    "T045R_UNIVERSAL_EXTRACTION_BRIDGE": (
        "BRIDGE_NEEDED",
        "T045R",
        "universal_extraction",
        "CRITICAL",
    ),
}


def build_residual_ledger() -> ResidualLedger:
    records: list[ResidualRecord] = []
    for name in REMOVED_RESIDUALS + GLOBAL_RESIDUALS:
        cls, block, route, risk = _RESIDUAL_META[name]
        records.append(ResidualRecord(name, cls, block, route, risk))
    return ResidualLedger(records=records, complete=True, messages=[f"n={len(records)}"])
